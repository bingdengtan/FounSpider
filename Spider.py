import traceback
import re
from urllib import request

class Spider():
    def __init__(self):
        self.url = "http://fund.eastmoney.com/company/default.html"

    def start(self):
        try:
            response = request.urlopen(self.url)
            html = response.read();
            content = html.decode('utf-8')
            companies = re.findall(r'<td.*?class=.*?><a href="/Company/(.*?).html">(.*?)</a></td>', content)

            for company in companies:
                print(company[1])
        except:
            traceback.print_exc()

spider = Spider();
spider.start();