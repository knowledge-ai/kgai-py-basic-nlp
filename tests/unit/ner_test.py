from dacite import from_dict
from kgai_py_commons.model.googlenews.news_article import NewsArticle

from kgai_basic_nlp.model.NLPArticle import NLPArticle
from kgai_basic_nlp.service.ner_tagger import NERTagger
from kgai_basic_nlp.utils.common_utils import hash_article
from tests.resources.news_article_1 import SAMPLE_1, SAMPLE_1_RESULT


class TestNER(object):
    @classmethod
    def setup_class(cls):
        """
        setup common class functionalities
        """
        cls.ner_svc = NERTagger()
        cls.sample_1_article = from_dict(data_class=NewsArticle, data=SAMPLE_1)
        cls.sample_1_result = from_dict(data_class=NLPArticle, data=SAMPLE_1_RESULT)

    def test_ner(self):
        observed = self.ner_svc.tag_sentence(news_articles=[self.sample_1_article])
        # if the contents are equal the hash would be the same ;)
        assert hash_article(observed.pop(0)) == hash_article(
            self.sample_1_result), "Expected and Observed results of NER different"
