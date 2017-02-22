from BeautifulSoup import BeautifulSoup
import urllib2


def scrape(url):
	try:
		page = urllib2.urlopen(url)
		soup=BeautifulSoup(page.read())
		webm=soup.find("source", {"id":"webmSource"})['src']
		return webm
	except:
		return -1
