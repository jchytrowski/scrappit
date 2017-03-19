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
import argparse
import sys

def special_characters(word):
	invalidChars = set(str.punctuation.replace("_", ""))
	if any(char in invalidChars for char in word):
		return True

	else:
		return False

def unsave_post(post_id):
	try:
		parameters = {'id':post_id}
		ugh = requests.post("https://oauth.reddit.com/api/unsave", headers=headers, params=parameters)
		return 0
	except:
		return -1


def download_img(current_url,subreddit,nsfw,home=os.environ['HOME']):
	try:
		file_name=os.path.basename(current_url.split('?')[0])+'.jpg'
		img=imgur.ff_url(current_url)
		if img != -1:
			imgur.save_to(home+'/'+nsfw+'/'+subreddit, file_name, img)
			print 'downloading %s/%s/%s' % (nsfw,subreddit,file_name)
			return True
		else:
			return False
	except Exception, e:
		print e
		print 'failed to retrieve from %s' % current_url
		return False

def special_download_img(current_url,subreddit,nsfw,home=os.environ['HOME']):
	#it's *special* because redditmedia and reddituploads serves jpegs
	#with peculiar filenames; source urls need to have '&amp;' stripped.	

	current_url=str(current_url.replace('amp;',''))
	base_name=os.path.basename(current_url.split('?')[0])+'.jpg'
	img=imgur.ff_url(current_url)
	if img != -1:
		imgur.save_to(home+'/'+nsfw+'/'+subreddit, base_name, img)
		print 'downloading %s/%s/%s' % (nsfw,subreddit,base_name)
		return True
	else:
		return False


def triage(post,dl_over_18=False):
	success=False
	subreddit=post['data']['subreddit']
	post_id=str(post['data']['name'])
	l_url=""

	if post['data']['over_18']:
		if dl_over_18:
			nsfw='nsfw'
		else:
			return -403
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
			print 'album detected @ %s:' % l_url
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
		time.sleep(1)
		return 0
	else:
		return -1


def main():
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

        parser = argparse.ArgumentParser(description="Template script tool")
        parser.add_argument('--Download', action='store_true', help='Download Saved images and gifs')
	parser.add_argument('--Archive', action='store_true', help='Build list of saved links')
	parser.add_argument('--Over18', action='store_true', help='Download adult content, default false')
	parser.add_argument('--Users', help='Download user stats for ARG')
        parser.add_argument('--Both', action='store_true', help='Archive And Download')
        args=parser.parse_args()


	if args.Both or args.Archive:
		#load first page of saved contents, and link to next node.
		front_saved = json.loads(response.content)['data']
		next_page = json.loads(response.content)['data']['after']


		i = 0
		aggregate=[]
		aggregate.append(json.loads(response.content)['data']['children'])

		while next_page:
			i+=1
			#API rules restrict number of posts per second by bots (supposed to be >=5sec/post)
			time.sleep(1)
			response = requests.get("https://oauth.reddit.com/user/"+reddit_user+"/saved/?after="+next_page, headers=headers)
			next_page = json.loads(response.content)['data']['after']

			#push content into list
			aggregate.append(json.loads(response.content)['data']['children'])

			sys.stdout.write( 'Pulling page %s\r' % i)
			sys.stdout.flush()

		with open(home+'/reddit_saved.dict', 'w') as handle:
        		pickle.dump(aggregate, handle)


	if args.Both or args.Download:
		#case --Download

		pp=pprint.PrettyPrinter(indent=1)

		content={}
		with open(home+'/reddit_saved.dict', 'r') as file:
			book=pickle.load(file)


		#enumerate
		pcount=0
		for page in book:
                        for post in page:
				pcount+=1	

		dcount=0
		for page in book:
			for post in page:
				dcount+=1
				sys.stdout.write( '%s/%s \r' % (dcount,pcount))
                        	sys.stdout.flush()
				current_url=''
				current_id=str(post['data']['name'])
				subreddit=post['data']['subreddit']
				triage(post,args.Over18)	


if __name__ == "__main__":
	main()
