import evaluate
from kafka import KafkaConsumer, KafkaProducer

class Kafka():

    def produceToReceiver(self,dictionary):
        producer = KafkaProducer(bootstrap_servers='localhost:9092')
        for k,v in dictionary.items():
            #print "Inside ProduceToReceiver",k,"v is: ",v
            if len(v)>0:
                msg = k + " { " + str(v) + " } "
            else:
                msg=k
            producer.send('outputTopic',bytes(msg))
            print ("sent topic to outputTopic ",msg)
        producer.close()


    def modelFunction(self,inputMessage):
        dictionary={}
        output=""
        if (len(inputMessage.split()) > 3):
            outputFromModel=evaluate.modelPredict(inputMessage);
            if outputFromModel>=50:
                output="Sarcasm Alert! :P"
            else:
                output="Not a Sarcastic message :)"
        else:
            output="";
        dictionary[inputMessage]=output
        temp1=Kafka()
        temp1.produceToReceiver(dictionary)

    def ConsumeFromUser(self):
        consumer = KafkaConsumer(bootstrap_servers='localhost:9092', auto_offset_reset='latest')
        consumer.subscribe(['inputTopic'])
        #print "Inside ConsumeFromUser"
        for message in consumer:
            print " ---- ",message," ----"
            ''' ConsumerRecord(topic=u'inputTopic', partition=0, offset=149, timestamp=1511587794160, 
            timestamp_type=0, key=None, value='Got input from User', 
            checksum=716050849, serialized_key_size=-1, serialized_value_size=19)
            '''
            inputString = message.value
            temp1=Kafka()
            temp1.modelFunction(inputString)
        consumer.close()

kafka=Kafka()
kafka.ConsumeFromUser()
