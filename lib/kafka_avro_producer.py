import json
import uuid

import avro
import requests
from confluent_kafka.avro import AvroProducer
from confluent_kafka.cimpl import KafkaError, Message

producer_config = {
    "bootstrap.servers": None,
    "schema.registry.url": None,
    'auto.offset.reset': 'latest',
    'security.protocol': 'sasl_ssl',
    'sasl.mechanism': 'GSSAPI',
    'sasl.kerberos.service.name': 'kafka_{ENV}_clt1',
    'sasl.kerberos.principal': 'kaf_ca_pdt_{ENV}@pytaf.com',
    'enable.auto.commit': 'true'
}


def send_message(args: dict):
    """
    Send Kafka message in avro format
    :param args: commandline arguments
    :return: None
    """
    setup_kafka_config(args)
    schema_key = get_avro_schema_from_registry(args['schema_registry'], args['schema_key'])
    schema_value = get_avro_schema_from_registry(args['schema_registry'], args['schema_value'])

    # create AvroProducer object
    producer = AvroProducer(producer_config, default_key_schema=schema_key, default_value_schema=schema_value)

    key = json.loads(args['message_key']) if args['message_key'] else str(uuid.uuid4())
    value = json.loads(args['message_value'])

    # send message
    try:
        producer.produce(topic=args['topic'], key=key, value=value, on_delivery=delivery_report)
    except Exception as e:
        print(f"Exception while producing message \nvalue - {value} to topic - {args['topic']} \nERROR: {e}")
    else:
        print(f"Successfully producing message \nvalue - {value} to topic - {args['topic']}")

    producer.flush()


def setup_kafka_config(args):
    """
    setup kafka config
    :param args: commandline arguments
    :return: None
    """
    producer_config["bootstrap.servers"] = args['bootstrap_servers']
    producer_config["schema.registry.url"] = args['schema_registry']
    producer_config['sasl.kerberos.service.name'] = producer_config['sasl.kerberos.service.name'].format(
        ENV=args.get('environment'))
    producer_config['sasl.kerberos.principal'] = producer_config['sasl.kerberos.principal'].format(
        ENV=args.get('environment'))


def get_avro_schema_from_registry(schema_registry, key):
    """
    Get avro schema key and schema value from avro schema registry
    :param schema_registry: schema registry url
    :param key: key stored n schema registry
    :return: schema json string
    """
    schema_key_url = f"{schema_registry}/subjects/{key}/versions/latest/schema"
    return avro.schema.parse(requests.get(url=schema_key_url).text)


def delivery_report(err: KafkaError, msg: Message):
    """
    Reports the failure or success of a message delivery.

    Args:
        err (KafkaError): The error that occurred on None on success.

        msg (Message): The message that was produced or failed.

    Note:
        In the delivery report callback the Message.key() and Message.value()
        will be the binary format as encoded by any configured Serializers and
        not the same object that was passed to produce().
        If you wish to pass the original object(s) for key and value to delivery
        report callback we recommend a bound callback or lambda where you pass
        the objects along.

    """
    if err:
        print(f"\nDelivery failed for message {msg.key()}: {err}")
        return
    print(f"\nUser message {msg.key()} successfully produced to topic:{msg.topic()}, partition:[{msg.partition()}] "
          f"at offset {msg.offset()}")
