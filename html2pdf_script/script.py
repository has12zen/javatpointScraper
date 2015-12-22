import pdfkit
from bs4 import BeautifulSoup
import requests
	
url = "http://www.javatpoint.com/java-tutorial"
fo = open("temp.html", "w")
		
class getPage:
	def __init__(self,urlString):
		super(getPage, self).__init__()
		self.initURL = urlString
	headString = """
	<head>
	<base href="http://www.javatpoint.com/" target="_blank" />
	</head>
	"""
	baseURL = """http://www.javatpoint.com/"""
	fo.write(headString)
	def fetchHTML(self,url):
		try:
			HTML = requests.get(url)
		except:
			print ("Error in fetching HTML.Please check URL again.")	
		else:
			print ("Got HTML of URL : " + url)
			soup = BeautifulSoup(HTML.text,'html.parser')
			return soup
	def getDivCity(self,soup):
		div = soup.find(id = 'city')
		print("Div Selected")
		return div
	def nextURL(self,div):
		
		relativeURL = div.find(id="bottomnextup").a['href']
		if relativeURL:
			finalUrl = self.baseURL + relativeURL
			print("Next URL Generated")
			return finalUrl
		else:
			return ""
	def cleanDivCity(self,div):
		for i in div.find_all('fieldset'):
			i.decompose()
		for i in div.select('.next'):
			i.decompose()
		for i in div.select('.nexttopicdiv'):
			i.decompose()
		print("div Tree Cleaned")			
		return div

	def init(self):
		soup = self.fetchHTML(self.initURL)
		div = self.getDivCity(soup)
		nextURL = self.nextURL(div)
		self.cleanDivCity(div)
		# self.finalString+=str(div)
		fo.write(str(div))
		while(nextURL!=""):
			soup = self.fetchHTML(nextURL)
			div = self.getDivCity(soup)
			#Workarounds for inconsistencies found in frontend code of website
			if nextURL == "http://www.javatpoint.com/custom-exception":
				nextURL = "http://www.javatpoint.com/java-inner-class"
			elif nextURL == "http://www.javatpoint.com/java-simpledateformat":
				nextURL = "http://www.javatpoint.com/java-string-to-int"
			elif nextURL == "http://www.javatpoint.com/java-string-to-float":
				nextURL = "http://www.javatpoint.com/collections-in-java"
			elif nextURL == "http://www.javatpoint.com/difference-between-arraylist-and-vector":
				nextURL = "http://www.javatpoint.com/java-jdbc"
			elif nextURL == "http://www.javatpoint.com/jdbc-rowset":
				nextURL = "http://www.javatpoint.com/New-features-in-java"
			elif nextURL == "http://www.javatpoint.com/RMI":
				nextURL = "http://www.javatpoint.com/internationalization-in-java"
			elif nextURL == "http://www.javatpoint.com/internationalizing-currency":
				nextURL = ""				

			else:
				nextURL = self.nextURL(div)
			self.cleanDivCity(div)
			fo.write(str(div))
			# self.finalString+=str(div)
			print("Page written")
	
		
p = getPage(url)
p.init()
fo.close()

cssFile = 'link.css'
pdfkit.from_file('temp.html','javatpointJAVA1.pdf',css=cssFile)
print("PDF Successfully Generated.")


#Alternate Selection Conditions
	# dict = {
	# "style":"float:right",
	# "class":"next"
	# }
	#relativeURL = div.select(".nexttopicdiv > span > a")[0]['href']


