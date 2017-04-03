
from lxml import html
import requests as request
import json

class Product:
	def __init__ (self, name, category, brand, price, imgFileName, arrayTags):
		# formatting name
		name = name.strip().replace(" ","_")

		self.productName = name
		self.productCategory = category.lower()
		self.productBrandName = brand
		self.price = price
		self.imageFileName = imgFileName
		self.tags = arrayTags

	def genJsonProduct(self, jsonFileName):

		self.tags.append(self.productBrandName.lower())

		jsonObject = open(jsonFileName, 'w')
		jsonObject.write("{")
		jsonObject.write("\"productName\":\""+self.productName.encode('utf-8').strip()+"\""+","+
		"\"category\":\" "+self.productCategory+"\""+","+
		"\"brandName\":\" "+self.productBrandName+"\""+","+
		"\"price\":\""+self.price+"\""+","+
		"\"imageFileName\":\""+self.imageFileName.encode('utf-8')+"\""+",")

		jsonObject.write("\"tags\":"+ "[" )
		i = 0
		lengthTags = len(self.tags) # 3
		for tag in self.tags:
			if i == lengthTags - 1 :
				jsonObject.write("\""+tag+"\"")
			else :
				jsonObject.write("\""+tag+"\""+",")
			i += 1

		jsonObject.write("]" )
		jsonObject.write("}")
		jsonObject.close()
		return True


def readUrl():

	url = open( './private/urls.json').read()
	#print "url --> "
	print url
	data = json.loads(url)
	return data["url"]

def getProductName(index, productNames):
	# print index
	productName = productNames[index].strip()
	productName = productName.replace(" ","_")
	# print productName
	return productName


def scrappingData():

	url = readUrl()
	page = request.get(url)
	tree = html.fromstring(page.content)

	# /html/body/div[7]/div/section/div/div[1]/ul/li[3]/strong/a
	# /html/body/div[7]/div/section/div/div[1]/ul/li[2]/a
	departmentName = tree.xpath('body/div[6]/div/section/div/div[1]/ul/li[2]//a')
	categoryName = tree.xpath('body/div[6]/div/section/div/div[1]/ul/li[3]//a')
	productNames = tree.xpath('//section//a[@class="g-nombre-prod"]/text()')
	productBrands = tree.xpath('//section//div[@class="g-brand-prod"]//a/text()')
	productImages = tree.xpath('//section//a[@class="g-img-prod"]//img')
	productPrices = tree.xpath('//section//div[@class="g-cnt-brprices"]//div[@class="gi-r g-price"]/div[@class="g-block g-pmejor"]/p/text()')

	# print len(productImages)
	# print productBrands
	print "____"
	# print departmentName[0].get('title')
	# print categoryName[0].get('title')
	# print "____"


	index = 0
	for img in productImages:
		f = open( getProductName(index, productNames) + ".jpg", 'wb')
		f.write( request.get(img.attrib['src']).content)
		arrayTags = []
		arrayTags.append(departmentName[0].get('title').lower())
		arrayTags.append(categoryName[0].get('title').lower())

		product = Product(productNames[index],
							categoryName[0].get('title'),
							productBrands[index].lower(),
							productPrices[index],
							getProductName(index, productNames) + '.jpg',
							arrayTags )
		product.genJsonProduct( 'product_'+ str(index) + '.json')

		index += 1


scrappingData()
