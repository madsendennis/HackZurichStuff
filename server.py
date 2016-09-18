import socket
import sys
import os
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import base64
import json
import time
import ijson.backends.python as ijson
from jsonclient import JsonClient

DISCOVERY_URL = 'https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'  # noqa
APIKEY = 'AIzaSyB_qHC9HNtdGY34qf0V9SjPftKJJzDSL5Q'

HOST = '0.0.0.0'
PORT = 9876
ADDR = (HOST,PORT)
BUFSIZE = 4096


def getData(photo_file):
    """Run a label request on a single image"""

    # [START authenticate]
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('vision', 'v1', credentials=credentials,
                              discoveryServiceUrl=DISCOVERY_URL)
    # [END authenticate]

    # [START construct_request]
    with open(photo_file, 'rb') as image:
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(body={
            'requests': [{
                'image': {
                    'content': image_content.decode('UTF-8')
                },
                'features': [{
                    'type': 'LABEL_DETECTION',
                    'maxResults': 4
                }]
            }]
        })
        # [END construct_request]
        # [START parse_response]
        response = service_request.execute()
        try:
            for r in response['responses'][0]['labelAnnotations']:
                print ' - ' + str(r['description']) + ' : ' + str(r['score'])
            label = response['responses'][0]['labelAnnotations'][0]['description']
            print('Found label: %s for %s' % (label, photo_file))
            with open('result.json', 'w') as outfile:
                json.dump(response['responses'][0]['labelAnnotations'], outfile, sort_keys=True, indent=4)
            # [END parse_response]
        except:
            print response

        try:
            # return response
            return response['responses'][0]['labelAnnotations']
        except:
            return response

if __name__ == '__main__':

    cwd = os.getcwd()
    print os.path.join(cwd, 'hackzurich2016-14caee755056.json')
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(cwd, 'hackzurich2016-c338181229d6.json')

    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    serv.bind(ADDR)
    serv.listen(5)

    print 'listening ...'

    while True:
        conn, addr = serv.accept()
        print 'client connected ... ', addr
        myfile = open('stupid.jpg', 'w')

        while True:
            data = conn.recv(BUFSIZE)
            if not data:
                break
            myfile.write(data)

        print 'finished writing file'
        # conn.close()
        print 'client disconnected'
        myfile.close()


        stuff = getData('stupid.jpg')

       # x = JsonClient()
       # axastuff = x.connect()
        #for item in stuff:
        #    for article in axastuff:
         #       if item in article:




        print "stuff finished"

        ADDRret = (addr[0], 6788)

        stuffSer = json.dumps(stuff).encode('utf-8')
        print "stuff dumped: ", stuffSer
        # stuffSer = ["String1", "String2", "String3", "String4"]

        time.sleep(1)
        ret = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print ADDRret
        while 1:
            try:
                ret.connect(ADDRret)

            # for item in ijson.items(stuffSer):
                ret.sendall(stuffSer)
                break
            except:
                print "no connection open"
                time.sleep(5)

        # ret.send(stuff)
        ret.close()

