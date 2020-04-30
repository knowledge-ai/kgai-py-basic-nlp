import dataclasses
import json
from typing import List

import spacy
from kgai_py_commons.logging.log import TRLogger
# https://github.com/huggingface/transformers#quick-tour-of-pipelines
from kgai_py_commons.model.googlenews.news_article import NewsArticle
from langdetect import detect
from transformers import pipeline

from kgai_basic_nlp.model.NEREntities import NEREntities
from kgai_basic_nlp.model.NLPArticle import NLPArticle
from kgai_basic_nlp.utils.ner_constants import *


class NERTagger(object):
    def __init__(self):
        self.logger = TRLogger.instance().get_logger(__name__)
        # for spacy based NER
        self.nlp = spacy.load("en_core_web_sm")
        self.transformer_nlp = pipeline("ner")

    def tag_sentence(self, news_articles: List[NewsArticle]) -> List[NLPArticle]:
        return self._ner_wrapper(news_articles=news_articles)

    def _ner_wrapper(self, news_articles: List[NewsArticle]) -> List[NLPArticle]:
        # prepare a list of texts for downstream NLP pipelines
        article_descs = []
        for article in news_articles:
            # map to subclass, so that all actions after this are on attributes of subclass
            article.__class__ = NLPArticle
            # select the article field with the most detailed description
            _lookup = {}
            if article.description:
                _lookup[len(article.description)] = article.description
            if article.content:
                _lookup[len(article.content)] = article.content
            if article.articleText:
                _lookup[len(article.articleText)] = article.articleText

            if not _lookup:
                self.logger.info(
                    "no description/articleText/content found for article, skipping, article: {}".format(article))
                continue
            # overwrite articleText
            article.articleText = _lookup.get(max(_lookup.keys()))
            if detect(article.articleText) != "en":
                self.logger.error(
                    "Only english is supported for now, please add others, detected: {} for text: {}".format(
                        detect(article.articleText), article.articleText))
                continue

            article_descs.append(article.articleText)
            # default the ner list of the class
            article.ner = []
            article = self._transformer_ner(article=article, text=_lookup.get(max(_lookup.keys())))
            article.description = ""
            article.content = ""

        # now append back, the previous step was not a waste of cycle
        # but ml models work better with batches, hence batching
        # for article, entity in zip(news_articles, self._spacy_ner(texts=article_descs)):
        #    article.ner.append(NEREntities(word=entity.text, confidence=None, entity=entity.label_, tool="spacy"))

        # spacy works a lot faster with aggregate or batches, hence the double computation
        news_articles = self._spacy_ner(texts=article_descs, articles=news_articles)

        return news_articles

    def _spacy_ner(self, texts: List[str], articles: List[NLPArticle]) -> List[NLPArticle]:
        """
        creates a efficient spacy pipeline to do NER, using spacy NER
        :param texts:
        :return:
        ref: https://spacy.io/usage/spacy-101#pipelines
        """
        if len(texts) != len(articles):
            self.logger.error(
                "number of articles passed to spacy does not match the number of descriptions, skipping spacy, "
                "YOU SHOULD NEVER SEE THIS ERROR")

        # pass a list of texts to make spacy work faster
        for doc, article in zip(self.nlp.pipe(texts, disable=["tagger", "parser", "textcat"]), articles):
            # Do something with the doc here
            self.logger.debug("document: {}, spacy NER:{}".format(texts, [(ent.text, ent.label_) for ent in doc.ents]))

            article.ner.extend([NEREntities(word=ent.text,
                                            confidence=None,
                                            entity=ent.label_,
                                            tool="spacy") for ent in doc.ents])

        return articles

    def _transformer_ner(self, text: str, article: NLPArticle) -> NLPArticle:
        """
        uses a transformer for NER and appends to the article
        :param text:
        :param article:
        :return:
        ref: https://huggingface.co/transformers/usage.html#named-entity-recognition
        e.g:
        [
            {'word': 'Hu', 'score': 0.9995632767677307, 'entity': 'I-ORG'},
            {'word': '##gging', 'score': 0.9915938973426819, 'entity': 'I-ORG'},
            {'word': 'Face', 'score': 0.9982671737670898, 'entity': 'I-ORG'},
            {'word': 'Inc', 'score': 0.9994403719902039, 'entity': 'I-ORG'},
            {'word': 'New', 'score': 0.9994346499443054, 'entity': 'I-LOC'},
            {'word': 'York', 'score': 0.9993270635604858, 'entity': 'I-LOC'},
            {'word': 'City', 'score': 0.9993864893913269, 'entity': 'I-LOC'},
            {'word': 'D', 'score': 0.9825621843338013, 'entity': 'I-LOC'},
            {'word': '##UM', 'score': 0.936983048915863, 'entity': 'I-LOC'},
            {'word': '##BO', 'score': 0.8987102508544922, 'entity': 'I-LOC'},
            {'word': 'Manhattan', 'score': 0.9758241176605225, 'entity': 'I-LOC'},
            {'word': 'Bridge', 'score': 0.990249514579773, 'entity': 'I-LOC'}
        ]
        """
        results = self.transformer_nlp(text)
        score = []
        word = []
        last_entity = ""
        self.logger.debug("document: {}, transformer NER: {}".format(text, results))
        for res_dict in results:
            if res_dict.get("entity") in [I_ORG, I_LOCATION, I_MISC, I_PERSON] and res_dict.get(
                    "entity") in last_entity or not last_entity:
                last_entity = res_dict.get("entity", "")
                score.append(res_dict.get("score", 0.0))
                word.append(res_dict.get("word", ""))
            # start of a new entity concat the rest and start fresh or if this is the last element in results
            elif res_dict.get("entity") in [BEGIN_ORG, BEGIN_LOCATION, BEGIN_MISC, BEGIN_PERSON] or res_dict.get(
                    "entity") not in last_entity:
                article.ner.append(NEREntities(word="".join(word).replace("#", ""),
                                               confidence=sum(score) / len(score),
                                               entity=IOB_ONTO5[last_entity],
                                               tool="transformer"))
                # clear off and then start
                word = []
                score = []
                last_entity = ""

                # now start
                last_entity = res_dict.get("entity", "")
                score.append(res_dict.get("score", 0.0))
                word.append(res_dict.get("word", ""))

        # for the residual last batch of elements
        article.ner.append(NEREntities(word="".join(word).replace("#", ""),
                                       confidence=sum(score) / len(score) if score else 0.0,
                                       entity=IOB_ONTO5[last_entity] if last_entity else "NA",
                                       tool="transformer"))

        return article
