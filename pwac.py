import time
from html.parser import HTMLParser
import http.client as hc
import urllib.parse as up
                                            
# Constants
HEADER = {  "Accept"            : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding"   : "gzip, deflate",
            "Accept-Language"   : "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4",
            "Cache-Control"     : "max-age=0",
            "Connection"        : "keep-alive",
            "Content-Length"    : 116,
            "Content-Type"      : "application/x-www-form-urlencoded",
            "Upgrade-Insecure-Requests" : 1,
            "User-Agent"        : "Mozilla/5.0 (X11; CrOS armv7l 8872.76.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.105 Safari/537.36"
}

class FormParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.form_dict = {}

    def handle_starttag(self, tag, attrs):
        if tag == "input":
            temp_dict = dict(attrs)
            if  "name" in temp_dict and "value" in temp_dict:
                self.form_dict.update({temp_dict["name"]:temp_dict["value"]})
      
    def getForm(self, data):
        self.form_dict = {}
        self.feed(data)
        return self.form_dict

# Constantly check the network
# Handle the redirection
# Get the authentication page
# Parse the page
# Post the authentication
  
class WifiGuard():
    def __init__(self):
        self.conn = None
            
    def run(self):
        while True:
            if self.checkNetwork() == True:
                time.sleep(600)
            else:
                self.reconnect()

    def checkNetwork(self):
        self.conn.request("GET", '')
        resp = self.conn.getresponse()

    def connect(self, url):
        self.conn = hc.HTTPConnection(url)
        conn.request("GET", '')
        return conn.getresponse()
        
    def reconnect(self):
        pass        
         
def main():
    while True:
        conn = hc.HTTPConnection("www.google.com")
        conn.request("GET", "/")
        resp = conn.getresponse()
        code = resp.getcode()
        print("%s code: %d" % (time.asctime(), code))
        if code == 303: # See other
            resp_hdr = dict(resp.getheaders())
            new_url = resp_hdr["Location"]
            print(new_url)
            addr = new_url[new_url.find("http://")+7:new_url.find('/fgtauth')] # ugly
            auth = new_url[new_url.find('/fgtauth'):]
            print("Redirecting to " + new_url)
            print(addr)
            print("auth: " + auth)   
            conn = hc.HTTPConnection(addr)
            conn.request("GET", "/"+auth)
            resp = conn.getresponse()
            if resp.getcode() != 200:
                print("Error!!!")
                return
        else:
            time.sleep(900) 
            continue
        # Read the page
        web_str = str(resp.read())
        print(web_str)
        # Parse the form
        parser = FormParser()
        form_dict = parser.getForm(web_str)
        form_dict["answer"] = 1
        print(form_dict)
        # Post the form
        params = up.urlencode(form_dict)
        conn.request("POST", "", params, HEADER)
        resp = conn.getresponse()
        print(resp.status)
        print(resp.getheaders())
        conn.close()
        time.sleep(900)

if __name__ == "__main__":
	main()
