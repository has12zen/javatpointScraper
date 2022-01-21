import pdfkit
from bs4 import BeautifulSoup
import requests

url = "https://www.javatpoint.com/regex"
name = "regex.pdf"
fo = open("temp.html", "w")


class getPage:
    def __init__(self, urlString):
        super(getPage, self).__init__()
        self.initURL = urlString

    headString = """
	<head>
	<base href="http://www.javatpoint.com/" target="_blank" />
	</head>
	"""
    baseURL = """http://www.javatpoint.com/"""
    fo.write(headString)

    def fetchHTML(self, url):
        try:
            HTML = requests.get(url)
        except:
            print("Error in fetching HTML.Please check URL again.")
        else:
            print("Got HTML of URL : " + url)
            soup = BeautifulSoup(HTML.text, "html.parser")
            return soup

    def cleanDivCity(self, div):
        for i in div.find_all("fieldset"):
            i.decompose()
        for i in div.select(".next"):
            i.decompose()
        for i in div.select(".nexttopicdiv"):
            i.decompose()
        # print("div Tree Cleaned")
        return div

    def getDivCity(self, soup):
        div = soup.find(id="city")
        # print("Div Selected")
        return div

    def fetchUrlList(self, url):
        try:
            HTML = requests.get(url)
        except:
            print("Error in fetching HTML.Please check URL again.")
        else:
            urls = list()
            soup = BeautifulSoup(HTML.text, "html.parser")
            menu = soup.find_all("div", class_="leftmenu")
            for i in menu:
                div = i.find_all("a")
                for j in div:
                    urls.append(j["href"])
            return urls

    def init(self):
        urls = self.fetchUrlList(self.initURL)
        n = len(urls)
        for idx, val in enumerate(urls):
            nextUrl = self.baseURL + val
            soup = self.fetchHTML(nextUrl)
            div = self.getDivCity(soup)
            self.cleanDivCity(div)
            fo.write(str(div))
            print(idx + 1, "out of", n, "Pages written")
        print("All Pages Written")


p = getPage(url)
p.init()
fo.close()
options = {
    "page-size": "Letter",
    "margin-top": "0.75in",
    "margin-right": "0.75in",
    "margin-bottom": "0.75in",
    "margin-left": "0.75in",
    "encoding": "UTF-8",
    "no-outline": None,
}

cssFile = "link.css"
pdfkit.from_file("temp.html", name, options=options, css=cssFile)
print("PDF Successfully Generated.")


# Alternate Selection Conditions
# dict = {
# "style":"float:right",
# "class":"next"
# }
# relativeURL = div.select(".nexttopicdiv > span > a")[0]['href']
