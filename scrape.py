import pdb
import sys
import csv
import time
import progressbar
from bs4 import BeautifulSoup
from selenium import webdriver
import selenium.common.exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchAttributeException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

def write(dic, filename):
	keys = dic[0].keys()
	with open(str(filename)+'.csv','wb') as fp:
		dict_writer = csv.DictWriter(fp,keys)
		dict_writer.writeheader()
		dict_writer.writerows(dic)


def get_len(source):
	soup = BeautifulSoup(source,'html.parser')
	stream = soup.find('div',class_="stream")
	ol = stream.find('ol')
	items = ol.find_all('li',class_='js-stream-item')
	return len(items)

def get_images(source):
	soup = BeautifulSoup(source,'html.parser')
	stream = soup.find('div',class_="stream")
	ol = stream.find('ol')
	items = ol.find_all('li',class_='js-stream-item')
	result = []
	print "Analysing imges..."
	#pb = progressbar.ProgressBar()
	for item in items:
		tweet_id = item['data-item-id']
		photo_divs = item.find_all('div',class_="AdaptiveMedia-photoContainer")
		for photo_div in photo_divs:
			photo_url = photo_div['data-image-url']
			try:
				
				print({'tweet-id': str(tweet_id),'image-url': str(photo_url)})

				result.append({'tweet-id': str(tweet_id),'image-url': str(photo_url)})
			except Exception:
				continue
	return result

def get_page_source(keyword):

	browser = ''
	action = ''

	try:
		browser = webdriver.Chrome("lib/chromedriver-"+sys.argv[1])
		action  = ActionChains(browser)
		browser.get("http://www.twitter.com/search?q=%23"+keyword)
	except Exception:
	 	print "Error occured. Check internet connectivity and try again"

	print "Expanding Browser...."

	save_length = get_len(browser.page_source)
	print("initial length -"+str(save_length)) 
	while True:
		time.sleep(3)
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight+100);")
		try:
			WebDriverWait(browser,1).until(EC.visibility_of(browser.find_element_by_class_name("back-to-top")))
			print("reached a stop!")
			current_length = get_len(browser.page_source)
			print("save length -"+str(save_length))
			print("current length -"+str(current_length))

			if save_length == current_length:
				print("no change from last time...")
				break
			else:
				print("this is a different 'back to top'")
				save_length = current_length
		except Exception:
			print("didn't reach a stop! current length - "+str(get_len(browser.page_source)))
			continue
	
	result = browser.page_source
	
	#backup
	#with open(keyword+'.html','w') as f:
	#	f.write(result)

	browser.quit()

	return result

keyword = 'TNTQ3SemifinaLs'
src = get_page_source(keyword)
data = get_images(src)
write(data, keyword)
print "Done."
