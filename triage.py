#!/usr/bin/python
import pickle
import pprint
import imgur
import os
import gfycat
import requests
import requests.auth
import json
import time
import getpass


def unsave_post(post_id):
	try:
		parameters = {'id':post_id}
		ugh = requests.post("https://oauth.reddit.com/api/unsave", headers=headers, params=parameters)
		return 0
	except:
		return -1


def download_img(current_url,subreddit,nsfw):
	try:
		file_name=os.path.basename(current_url)
		img=imgur.ff_url(current_url)
		if img != -1:
			imgur.save_to(home+'/'+nsfw+'/'+subreddit, file_name, img)
			print 'downloading %s/%s/%s' % (nsfw,subreddit,file_name)
			time.sleep(1)
			return True
		else:
			return False
	except:
		print 'failed to retrieve from %s' % current_url
		return False

def special_download_img(current_url,subreddit,nsfw):
	#it's *special* because redditmedia and reddituploads serves jpegs
	#with peculiar filenames; source urls need to have '&amp;' stripped.

	current_url=str(current_url.replace('amp;',''))
	base_name=os.path.basename(current_url.split('?')[0])+'.jpg'
	print base_name
	img=imgur.ff_url(current_url)
	if img != -1:
		imgur.save_to(home+'/'+nsfw+'/'+subreddit, base_name, img)
		print 'downloading %s/%s/%s' % (nsfw,subreddit,base_name)
		time.sleep(1)
		return True
	else:
		return False


def triage(post):
	success=False
	subreddit=post['data']['subreddit']
	post_id=str(line['data']['name'])
	l_url=""

	if line['data']['over_18']:
		nsfw='nsfw'
	else:
		nsfw='sfw'


	#sometimes the link is in url, othertimes its link_url; not sure why the diff.
	if 'url' in post['data']:
		l_url=post['data']['url']
	elif 'link_url' in post['data']:
		l_url=post['data']['link_url']
		

	if l_url.endswith(('jpeg','jpg','gifv','gif','png','webm','mp4')):
		#trivial case, just download the image
		success=download_img(l_url,subreddit,nsfw)


	elif 'imgur.com' in l_url:
		img_list=imgur.album_iterator(l_url)
		try:
			print 'album detected:'
			for img in img_list:
				download_img(img,subreddit,nsfw)
			success=True
		except:
			sucess=False

	elif 'gfycat.com' in l_url:
		#we need a function to scrape for the url of the embedded media because gfycat has variable formats (gifv, webm, mp4, etc), and variable subdomains (zippy.gfycat.com, fat.gfycat.com, etc)
		l_url=gfycat.scrape(l_url)	
		success=download_img(l_url,subreddit,nsfw)
			
	elif 'reddituploads' in l_url or 'redditmedia' in l_url:
		success=special_download_img(l_url,subreddit,nsfw)	

	if success:
		unsave_post(post_id)
	return 0


#prompt for reddit password
password=getpass.getpass()

#I generally set env vars in ~/.bashrc
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


pp=pprint.PrettyPrinter(indent=1)

content={}
with open(home+'/reddit_saved.dict', 'r') as file:
	book=pickle.load(file)

for page in book:
	for line in page:
		current_url=''
		current_id=str(line['data']['name'])
		subreddit=line['data']['subreddit']
		triage(line)	

