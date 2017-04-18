#!/usr/bin/python

import requests
import urllib2
import os
from BeautifulSoup import BeautifulSoup
import zipfile
import cStringIO 

def ff_url(url):
	#fetch from url
	try:
		request=urllib2.Request(url)
		image=urllib2.urlopen(request).read()
		return image

	except urllib2.HTTPError:
		print "Error fetching image from %s" % url
		return -1	
	except AssertionError:
		print 'assertion error for type str: %s; actually %s' % (url, type(url))
		return -2
def sf_url(url, name):
	#save from url
	data=ff_url(url)
	if data != -1:
		try:
			#save_to(dir,name,data)
			f = open(name, 'wb')
			f.write(dl)
			f.close()
			return 0
		except:
			print 'couldnt save %s to disk!' % url
			return -1

def save_to(dir,name,data):
	if not os.path.exists(dir):
		os.makedirs(dir)
	if not os.path.isfile(dir+"/"+name):
		try:
			f = open(dir+"/"+name, 'wb')
			f.write(data)
			f.close()
			return 0

		except:
			print 'couldnt save %s to disk!' % url
                        return -1

def get_zip(album_url):
	remotezip=urllib2.urlopen(album_url+'/zip')
	buffer=cStringIO.StringIO(remotezip.read())
		

def album_iterator(album_url):
	
	#test for truncation (load more images button)

	#try:
	remotezip=urllib2.urlopen(album_url+'/zip')

	#fh=open('/tmp/test.zip', 'w')
	#fh.write(zipped.read())
	#fh.close()
	#print type(zipped)
	buffer=cStringIO.StringIO(remotezip.read())
	myzip=zipfile.ZipFile(buffer)

	page = urllib2.urlopen(album_url)
	soup=BeautifulSoup(page.read())
	#except:
	#	print 'couldnt download %s' % album_url
	#	return False

	
	
	#finds body
	imgs=BeautifulSoup(str(soup.findAll("div", {"class":"post-image"})))
	img_list=[]
	img_count=0
	for image in imgs.findAll('img'):
		img_list.append('http:' + image['src'])
		img_count+=1

	
	try:
		print 'downloaded %s images from album' % img_count
		return img_list
	except:
		return False


