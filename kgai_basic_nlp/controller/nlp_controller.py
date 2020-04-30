from functools import partial
from typing import List

from kgai_py_commons.clients.kafka.producer.producer import TRAvroProducer
from kgai_py_commons.logging.log import TRLogger
from kgai_py_commons.model.googlenews.news_article import NewsArticle

from kgai_basic_nlp.model.NLPArticle import NLPArticle
from kgai_basic_nlp.service.kafka_consumer import KafkaConsumer
from kgai_basic_nlp.service.ner_tagger import NERTagger
from kgai_basic_nlp.utils.common_utils import hash_article

"""
{
  "title": "The Right to Work From Home Could Be Guaranteed By Law in Germany",
  "publishedAt": "2020-04-27T11:34:00Z",
  "url": "https://slashdot.org/story/20/04/27/0516215/the-right-to-work-from-home-could-be-guaranteed-by-law-in-germany",
  "urlToImage": "https://a.fsdn.com/sd/topics/eu_64.png",
  "description": "\"Germany's labor minister wants to enshrine into law the right to work from home if it is feasible 
  to do so, even after the coronavirus pandemic subsides,\" reports the Associated Press:\nLabor Minister Hubertus Heil 
  told Sunday's edition of the Bild am Sonntag…",
  "content": "Labor Minister Hubertus Heil told Sunday's edition of the Bild am Sonntag newspaper that he aims to put 
  forward such legislation this fall. He said initial estimates suggest the proportion of the work force working from 
  home has risen from 12% to 25% during t… [+468 chars]",
  "author": "EditorDavid",
  "articleText": "\"Germany's labor minister wants to enshrine into law the right to work from home if it is feasible 
  to do so, even after the coronavirus pandemic subsides,\" reports the Associated Press:The labor minister had already 
  been calling for a right to work at home back in December, the article notes.",
  "source": {
    "name": "Slashdot.org",
    "id": null,
    "description": null,
    "url": null,
    "category": null,
    "language": null,
    "country": null
  }
}
"""


class NLPController(object):

    def __init__(self, kafka_broker: str, kafka_schema: str, avro_namespace: str, group_id: str):
        self.logger = TRLogger.instance().get_logger(__name__)
        self.ner_tagger = NERTagger()

        self.kafka_producer = TRAvroProducer(bootstrap_servers=kafka_broker,
                                             schema_registry=kafka_schema,
                                             namespace=avro_namespace,
                                             data_class=NLPArticle)

        self.kafka_consumer = KafkaConsumer(bootstrap_servers=kafka_broker,
                                            schema_registry=kafka_schema,
                                            namespace=avro_namespace,
                                            data_class=NewsArticle, group_id=group_id)

    def nlp_tag(self, listen_topic: str, publish_topic: str, kafka_publish: bool):
        # create a partial by applying the kafka topic and setting kafka publish option
        __ner_tag_control = partial(self._ner_tag_control, topic=publish_topic, kafka_publish=kafka_publish)
        # register a kafka calback in the controller
        self.kafka_consumer.consume_and_callback(topic=listen_topic, trigger_count=2,
                                                 callback_function=__ner_tag_control)

    def _ner_tag_control(self, topic: str, news_articles: List[NewsArticle], kafka_publish: bool):
        nlp_articles = self.ner_tagger.tag_sentence(news_articles=news_articles)
        if kafka_publish:
            for article in nlp_articles:
                self.kafka_producer.produce(topic=topic, key=hash_article(article=article), value=article)
