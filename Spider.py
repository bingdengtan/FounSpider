import traceback
import re
import datetime
import socket
from urllib import request

from Items import company as companyItem
from Foundation import company as companyCtrl
from Foundation import fund as fundCtrl
from Core import common

class Spider():
    def __init__(self):
        self.url = "http://fund.eastmoney.com/company/default.html"

    def start(self):
        try:
            response = request.urlopen(self.url)
            html = response.read();
            content = html.decode('utf-8')  #all companies page

            # fetch all companies and funds
            lngIndex = 0
            companies = re.findall(r'<td.*?class=.*?><a href="/Company/(.*?).html">(.*?)</a></td>', content)
            for item in companies:
                lngIndex = lngIndex + 1
                print("%s Check and insert fund company and funds: %s-(%s) %s/%s" % (common.getCurrentDateTimeString(), item[1], item[0], str(lngIndex), str(len(companies))))
                _companyCtrl = companyCtrl(companyItem(item[0], item[1]))
                #_companyCtrl.insert()

            # insert fund net values
            date_from = datetime.date(2017,1,1)
            date_to = datetime.date(2017,12,31)
            fundCtrl({}).insertAllNet(date_from, date_to)


        except:
            traceback.print_exc()

socket.setdefaulttimeout(30)
spider = Spider();
spider.start();