from django.shortcuts import render_to_response
from django.http import HttpResponse
import urllib2
from bs4 import BeautifulSoup


def search(request):
	return render_to_response("search.html")

def search_result(request):
	if 'book' in request.GET:
		book_name = request.GET['book'].encode('utf8')
		message = 'You searched for: %s' % book_name
		url = "http://202.117.255.187:8080/opac/search_rss.php?dept=ALL&title=%s" %book_name
		content = urllib2.urlopen(url).read()
		soup = BeautifulSoup(content,"html.parser")
		tag = soup.channel
		items = tag.find_all("item")
		books = []
		for item in items:
			book = {}
			book['title'] = item.find("title").text
			book['description'] = item.find("description").text
			book['marc_no']= item.find("link").text.split("=")[1]
			books.append(book)
	else:
		message = 'You submitted an empty form.'
	result = True	
	return render_to_response("search.html",locals())

def detail(request,offset):
	url = "http://202.117.255.187:8080/opac/item.php?marc_no=%s"% offset
	content = urllib2.urlopen(url).read()
	soup = BeautifulSoup(content,"html.parser")
	tag = soup.body
	items_parse = tag.find('table')
	items_book = items_parse.find_all('tr')
	book_name = tag(class_="booklist")[0].find('a').text
	books = []
	for x in xrange(1,len(items_book)):
		book = {}
		book['place'] = items_book[x](width = '25%')[0].text.replace("\t", "").replace("\r", "").replace("\n", "").replace(" ", "")
	 	book['status'] = items_book[x](width = '20%')[0].text
	 	books.append(book)
	return render_to_response("details.html",locals())
