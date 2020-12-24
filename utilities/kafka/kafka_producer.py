from lib.kafka_avro_producer import send_message
from lib.utils import trace


@trace(text="Kafka Producer: Send Message")
def producer(command_args: dict):
    send_message(command_args)


"""
'version' in message value stored in mongoDB, to get the latest ClientSubscriptionVersion query to CA mongoDB 
Command -
pytaf>utility_launcher.py kafka_producer kafka_avro_producer.py -t ent-productsubscription-sub-evt-clt-dnr -bs kaf-broker-clt-dev-wdc.pytaf.com:9093 -sr http://kaf-schemaregR-msg-pyx-dev.pytaf.com:8081 -sk ent-productsubscription-sub-evt-clt-dnr-key -sv ent-productsubscription-sub-evt-clt-dnr-value -mk "{\"clientAccountId\": \"00H2A1IUKDOM9LTCEGF8\"}" -mv "{\"version\": 105,\"clientInfo\": {\"enterpriseClientAccountId\": {\"enterpriseClientId\": \"CEID\",\"enterpriseAccountId\": \"00H2A1IUKDOM9LTCEGF8\",\"enterpriseAccountNumber\": \"ACCTNBR\"},\"legalName\": null,\"addressInfo\": null,\"taxIdentificationInfo\": null},\"productSubscriptions\": [{\"productCode\": \"PNG_STRT\",\"serviceAvailability\": {\"startDate\": 18536,\"endDate\": null}}]}"
"""
