
from lxml import html
import requests as request

def scrappingData():

	page = request.get(url)
	tree = html.fromstring(page.content)

	products = tree.xpath('//section//a[@class="g-nombre-prod"]/text()')
	productImages = tree.xpath('//section//a[@class="g-img-prod"]//img')

	print len(productImages)

	count = 0
	for img in productImages:
		f = open( getProductName(count, products) + ".jpg", 'wb')
		f.write( request.get(img.attrib['src']).content)
		count += 1

	print len(products)

def getProductName(index, products):
	print index
	productName = products[index].strip()
	productName = productName.replace(" ","_")
	print productName
	return productName

scrappingData()
