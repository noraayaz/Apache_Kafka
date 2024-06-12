from kafka.admin import *
from kafka import KafkaProducer, KafkaConsumer
import json

admin_client = KafkaAdminClient(bootstrap_servers="localhost:9092", client_id='test')


topic_list = []
new_topic = NewTopic(name="bankbranch", num_partitions= 2, replication_factor=1)
topic_list.append(new_topic)

admin_client.create_topics(new_topics=topic_list)

# Above create topic operation is equivalent to using kafka-topics.sh --topic in Kafka CLI client: 
# "kafka-topics.sh --bootstrap-server localhost:9092 --create --topic bankbranch  --partitions 2 --replication_factor 1"


configs = admin_client.describe_configs(config_resources=[ConfigResource(ConfigResourceType.TOPIC, "bankbranch")])

# Above describe topic operation is equivalent to using kafka-topics.sh --describe in Kafka CLI client:
# kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic bankbranch


producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'))
# Since Kafka produces and consumes messages in raw bytes, we need to encode our JSON messages and serialize them into bytes.


producer.send("bankbranch", {'atmid':1, 'transid':100})
producer.send("bankbranch", {'atmid':2, 'transid':101})
# with the KafkaProducer created, we can use it to produce two ATM transaction messages in JSON format

# The above producing message operation is equivalent to using kafka-console-producer.sh --topic in Kafka CLI client:
# kafka-console-producer.sh --bootstrap-server localhost:9092 --topic bankbranch

consumer = KafkaConsumer('bankbranch')
# Once the consumer is created, it will receive all available messages from the topic bankbranch. Then we can iterate and print them with the following code snippet:
for msg in consumer:
    print(msg.value.decode("utf-8"))

# The above consuming message operation is equivalent to using kafka-console-consumer.sh --topic in Kafka CLI client:
# kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic bankbranch

