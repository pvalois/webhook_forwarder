#!/usr/bin/env python3

from flask import *
import time
import requests
import os

###############################################################################

def send_mattermost(report):
  mmwebhooks=""
  headers = {'Content-Type': 'application/json',}
  values = json.dumps({ "text": report})
  response = requests.post(mmwebhooks, headers=headers, data=values)

###############################################################################

app = Flask(__name__)

ip=os.popen('hostname -I').read().strip()
cluster=ip.split('.')[2][-1]

messages={}

@app.route('/forwarder/', methods=['POST'])
def api_gh_message():
  global messages

  send=0
  timeinseconds=int(time.time())
  msg='** Cluster '+str(cluster)+' alert **\n'

  for alert in request.json['alerts']:
    desc=alert['annotations']['description']
    h=hash(desc)
    if (h not in messages or timeinseconds-messages[h]>3600):
      msg=msg+"* "+desc+"\n"
      messages[h]=timeinseconds
      send=1

  if (send): send_mattermost(msg)

  return("")

###############################################################################

if __name__ == '__main__': 
  app.run(host=ip,port="5000")


