from dataclasses import dataclass, field
from typing import List

from kgai_py_commons.model.googlenews.news_article import NewsArticle

from kgai_basic_nlp.model.NEREntities import NEREntities


@dataclass
class NLPArticle(NewsArticle):
    # although we inherit we will only set certain aspects
    # of news article and throw away the rest
    # complex objects
    ner: List[NEREntities] = field(default_factory=list)
