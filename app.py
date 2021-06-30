#https://www.digitalocean.com/community/tutorials/processing-incoming-request-data-in-flask

# import main Flask class and request object
from flask import Flask, request
# Import KafkaProducer from Kafka library
from kafka import KafkaProducer
import json
import mysql.connector


# create the Flask app
app = Flask(__name__)

@app.route("/")
def test():
    return "Hello world 1234444555556"


@app.route('/query-example')
def query_example():
    language = request.args.get('language')

    return '''<h1>The language value is: {}</h1>'''.format(language)
#    return 'Query String Example'

@app.route('/form-example')
def form_example():
    return 'Form Data Example'

@app.route('/json-example', methods=['POST'])
def json_example():
    request_data = request.get_json()

    language = request_data['language']
    framework = request_data['framework']

    # two keys are needed because of the nested object
    python_version = request_data['version_info']['python']

    # an index is needed because of the array
    example = request_data['examples'][0]

    boolean_test = request_data['boolean_test']
    #kafkainsert(request_data)
    insertDataDB("CREATE_ORDER",json.dumps(request_data))
    return request_data
    #return '''
    #       The language value is: {}
    #       The framework value is: {}
    #       The Python version is: {}
    #       The item at index 0 in the example list is: {}
    #       The boolean value is: {}'''.format(language, framework, python_version, example, boolean_test)
#    return 'JSON Object Example'

def kafkainsert(jsonStr):
#    bootstrap_servers = ['localhost:9092']
#    server_name = "[" +  + ":9092]"
    #print(server_name)
    bootstrap_servers = ['0.0.0.0:9092']    #--to be used for normal development
    #bootstrap_servers = server_name 
    #bootstrap_servers = ['192.168.49.1:9092']
     
    # Define topic name where the message will publish
    topicName = 'First_Topic'

    # Initialize producer variable
    producer = KafkaProducer(bootstrap_servers = bootstrap_servers)
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                                 value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    producer.send(topicName,jsonStr)
    producer.flush()
    producer.close()
    #str_input = input("enter words to continue")
    #b_input = bytes(str_input,'utf-8')
    #req = bytes(jsonStr, 'utf-8')
    #producer.send(topicName, bytes(jsonStr)
#    data = json.loads(jsonStr.text)
#    sampleStr = json.dumps(data)
#    print(sampleStr)
#    print(data)
    #producer.send(topicName,sampleStr)
#    producer.send(topicName, json.dumps(jsonStr, default=json_util.default).encode('utf-8'))
    #producer.flush()
    #producer.close()

def insertDataDB(jsonType,jsonText):
    #mydb = mysql.connector.connect(host="127.0.0.1",  user="root",  password="root@123",database="itemsdb")    
    mydb = mysql.connector.connect(host="172.17.0.5",  user="root",  password="strongpassword",database="itemsdb")
   # http://192.168.49.2:32346
    mycursor = mydb.cursor()

    sql = "INSERT INTO kafkasample (jsonType,jsonContent,active) VALUES (%s, %s,1)"
    val = (jsonType,jsonText)
    mycursor.execute(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "record inserted.")

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, host="0.0.0.0",port=8000)
