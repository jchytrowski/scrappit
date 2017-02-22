#!/usr/bin/python
import requests
import requests.auth
import pprint
import json
import time
import getpass
import pickle
import os

pp=pprint.PrettyPrinter(indent=1)
password=getpass.getpass()

#set in ~/.bashrc
api_id=os.environ['REDDIT_API_ID']
api_pass=os.environ['REDDIT_API_PASS']
reddit_user=os.environ['REDDIT_USERNAME']
home=os.environ['HOME']

#create a session
client_auth = requests.auth.HTTPBasicAuth(api_id, api_pass )
post_data = {"grant_type": "password", "username": reddit_user, "password": password }
headers = {"User-Agent": "saved_comment_scrapper"}
response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
my_token=str(json.loads(response.content)['access_token'])
headers = {"Authorization": "bearer "+ my_token, "User-Agent": "saved_comment_scrapper"}
response = requests.get("https://oauth.reddit.com/user/"+reddit_user+"/saved", headers=headers)


#load first page of saved contents, and link to next node.
front_saved = json.loads(response.content)['data']
next_page = json.loads(response.content)['data']['after']


i = 0
aggregate=[]
aggregate.append(json.loads(response.content)['data']['children'])

while next_page: 
	i+=1

	#API rules restrict number of posts per second by bots (supposed to be >=5sec/post)
	time.sleep(5)

	response = requests.get("https://oauth.reddit.com/user/"+reddit_user+"/saved/?after="+next_page, headers=headers)
	next_page = json.loads(response.content)['data']['after']

	#push content into list
	aggregate.append(json.loads(response.content)['data']['children'])
	print '\r  Pulling page %s' % i


with open(home+'/reddit_saved.dict', 'w') as handle:
	pickle.dump(aggregate, handle)

