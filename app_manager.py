"""
Starting point for managing/running the app
"""

__author__ = 'Ritaja'

import os

from distutils.util import strtobool
from dotenv import load_dotenv
from kgai_py_commons.logging.log import TRLogger

from kgai_basic_nlp.controller.nlp_controller import NLPController


class AppManager(object):
    def __init__(self):
        self.logger = TRLogger.instance().get_logger(__name__)
        self._kafka_config()
        self.nlp_controller = NLPController(kafka_broker=self.kafka_broker,
                                            kafka_schema=self.kafka_schema, avro_namespace=self.avro_namespace,
                                            group_id=os.getenv("KAFKA_CONSUMER_ID"))

    def _kafka_config(self):
        """
        configuration helper
        Returns:

        """
        # check if all configs are set properly
        if not any([os.getenv("KAFKA_BROKER"), os.getenv("KAFKA_SCHEMA"),
                    os.getenv("AVRO_NAMESPACE")]):
            self.logger.error("Kafka configs not set properly, no defaults set")
            raise EnvironmentError

        if not os.getenv("KAFKA_LISTEN_TOPIC"):
            self.logger.error("Listener kafka topic name not found, no defaults set")
            raise EnvironmentError

        if not os.getenv("KAFKA_PUBLISH_TOPC"):
            self.logger.error("Publisher kafka topic name not found, no defaults set")
            raise EnvironmentError

        self.kafka_broker = os.getenv("KAFKA_BROKER")
        self.kafka_schema = os.getenv("KAFKA_SCHEMA")
        self.avro_namespace = os.getenv("AVRO_NAMESPACE")
        self.kafka_topic = os.getenv("KAFKA_NEWS_RAW_TOPIC")
        self.logger.info(
            "kafka client configured with KAFKA_BROKER: {}, KAFKA_SCHEMA: {}, AVRO_NAMESPACE: {}, "
            "KAFKA_NEWS_RAW_TOPIC: {}".format(
                self.kafka_broker, self.kafka_schema, self.avro_namespace, self.kafka_topic))

    def nlp_tag(self, listen_topic: str, publish_topic: str, kafka_publish: bool = True):
        self.nlp_controller.nlp_tag(listen_topic=listen_topic, publish_topic=publish_topic, kafka_publish=kafka_publish)


if __name__ == '__main__':
    load_dotenv()
    app_manager = AppManager()
    publish_topic = os.getenv("KAFKA_PUBLISH_TOPC")
    listen_topic = os.getenv("KAFKA_LISTEN_TOPIC")
    publish_kafka = strtobool(os.getenv("PUBLISH_NLP_KAFKA"))
    app_manager.nlp_tag(listen_topic=listen_topic, publish_topic=publish_topic, kafka_publish=publish_kafka)
