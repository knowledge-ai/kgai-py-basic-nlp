import json
from typing import Type, Callable, TypeVar

from kgai_py_commons.clients.kafka.consumer.consumer import TRAvroConsumer

T = TypeVar("T")


class KafkaConsumer(TRAvroConsumer):
    def __init__(self, bootstrap_servers: str, group_id: str, data_class: Type[T], schema_registry: str = None,
                 namespace: str = None):
        """
        constructs an AVRO consumer, to use AVRO specify the schema_registry, namespace params
        :param schema_registry:
        :param bootstrap_servers:
        :param namespace:
        :param group_id:
        :param data_class:
        """
        super().__init__(bootstrap_servers=bootstrap_servers, group_id=group_id, data_class=data_class,
                         schema_registry=schema_registry, namespace=namespace)

    def consume_and_callback(self, topic: str, trigger_count: int, callback_function: Callable):
        """
        TODO: move to asyncio
        start consumer
        :param topic:
        :return:
        """
        self._consumer.subscribe([topic])
        dataclass_objs = []
        try:
            while True:
                msg = self._consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                elif msg.error():
                    self._reciept_report(err=True, msg=str(msg.error()))
                    continue
                elif not msg.value():  # empty body not acceptable, log and continue
                    self.logger.error("received empty message in topic: {}, key:{}".format(msg.topic(), msg.key()))
                else:
                    if not self._is_avro:
                        self.logger.error(
                            "Consumer implementation is not tested with non-AVRO consumption, please double check")
                        raise TypeError
                    else:
                        clean_msg = msg.value()
                        self._reciept_report(err=False, msg=clean_msg, topic=topic)
                        dataclass_objs.append(self._from_dict_dataclass(data_dict=clean_msg.__dict__, ctx=None))
                        if len(dataclass_objs) == trigger_count:
                            callback_function(news_articles=dataclass_objs)
                            dataclass_objs = []

        except KeyboardInterrupt:
            self.logger.warn("Interrupted by user/system, existing consumer....")
        finally:
            self._consumer.close()
