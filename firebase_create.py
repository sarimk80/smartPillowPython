import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import messaging
import requests
import time


cred = credentials.Certificate("/Users/sarimkhan/Desktop/Home.nosync/smartPillowPython/fypsmartpillow-2a14f-firebase-adminsdk-jxwlt-e0602cdbe5.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


# https://api.thingspeak.com/channels/1868150/feeds.json?api_key=ZYFX22DXKB1RC247

registration_token = 'BK4z0Ka9-hv1d5ThzWALKxIfVOmha7t7kEDua2st1jUYtkBZDcP2pne5JhgotA03kG98WmhJ3qAK8LRdlcotYdU'
topic = 'Testing'



def sendNotification(topic, myData,title,subtitle):
    message = messaging.Message(
        data={
            'field1': myData['field1'],
            'field2': myData['field2'],
            'field3':myData['field3'],
            'title':title,
            'subtitle':subtitle
        },
        topic=topic,
        #token=registration_token,
    )

    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)

while True:
    x = requests.get('https://api.thingspeak.com/channels/1868150/feeds.json?api_key=ZYFX22DXKB1RC247')

    response = x.json()

    feeds = response['feeds']
    data = feeds[-1]

    doc_ref = db.collection("readings").document(str(data['entry_id']))
    doc_ref.set(
        {
            "created_at": data['created_at'],
            "entry_id": data['entry_id'],
            "field1": data['field1'],
            "field2": data['field2'],
            "field3": data['field3']
        }
    )
#{field1=0, field2=20, field3=false}
    if int(data['field1']) > 95:
        sendNotification(topic, data,'High heart rate','Your patient heart rate rose above 95 bpm')
    if int(data['field2']) > 37 :
        sendNotification(topic, data,'High Temperature Alert','Your patient temperature rose above normal body temperature')
    if int(data['field1']) > 50 and not bool(data['field3']) :
        sendNotification(topic, data,'Wake up Alert','Your patient has woke up from bed')

    # See documentation on defining a message payload.
        

    print("Done")
    time.sleep(60)
    




    