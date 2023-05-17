#!/usr/bin/env python3

from flask import *
import time
import requests
import os

###############################################################################

def send_mattermost(report):
  mmwebhooks=os.getenv("MM_WEBHOOKS_URL", "https://default-url.com")
  headers = {'Content-Type': 'application/json',}
  values = json.dumps({ "text": report})
  response = requests.post(mmwebhooks, headers=headers, data=values)

###############################################################################

app = Flask(__name__)

#ip=os.popen('hostname -I').read().strip()
ip=os.popen('hostname -I').read().strip().split(" ")[0]
cluster=ip.split('.')[2][-1]

critical_words=['PVC']
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

    unhold=False
    for word in critical_words:
      if (word in desc):
        unhold=True

    if (h not in messages or timeinseconds-messages[h]>300*86400 or unhold):
      msg=msg+"* "+desc+"\n"
      messages[h]=timeinseconds
      send=1

  if (send): send_mattermost(msg)

  return("")

###############################################################################

if __name__ == '__main__': 
  app.run(host=ip,port=os.getenv("FLASK_PORT", "5000"))
