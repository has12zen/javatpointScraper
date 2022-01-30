import pdfkit
from bs4 import BeautifulSoup
import requests

urls = ["https://www.javatpoint.com/iot-internet-of-things","https://www.javatpoint.com/graphql"]


fo = open("temp.html", "w")
class getPage:
    def __init__(self, urlString):
        super(getPage, self).__init__()
        self.initURL = urlString
    baseURL = """http://www.javatpoint.com/"""
    headString = """
        <head>
        <base href="http://www.javatpoint.com/" target="_blank" />
        </head>
        """
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
        try:
            for i in div.find_all("fieldset"):
                i.decompose()
            for i in div.select(".next"):
                i.decompose()
            for i in div.select(".nexttopicdiv"):
                i.decompose()
            return div
        except:
            print("Error in cleaning div Tree")
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
        fo.write(self.headString)
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
for url in urls:
    fo.truncate(0)
    p = getPage(url)
    url_part = url.split("/")[-1]+".pdf"
    p.init()
    pdfkit.from_file("temp.html", url_part, options=options, css=cssFile)
    print("PDF Successfully Generated.")

fo.close()
print("All PDF Successfully Generated.")
