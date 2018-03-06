import traceback
import re
import datetime
import time
import socket
from urllib import request
from lxml import etree

from Items import company as companyItem
from Items import stock as stockItem
from Foundation import company as companyCtrl
from Foundation import fund as fundCtrl
from Foundation import fundStock as fundStockCtrl
from Foundation import stock as stockCtrl
from Core import common

class Spider():
    def __init__(self):
        self.url = "http://fund.eastmoney.com/company/default.html"

    def start(self):
        self.fetchCompanies()
        self.fetchStocks()
        self.fetchFundsStock()
        self.fetchFundsNets()

    def fetchCompanies(self):
        try:
            response = request.urlopen(self.url)
            html = response.read();
            content = html.decode('utf-8')

            # fetch all companies and funds
            lngIndex = 0
            companies = re.findall(r'<td.*?class=.*?><a href="/Company/(.*?).html">(.*?)</a></td>', content)
            for item in companies:
                lngIndex = lngIndex + 1
                print("%s Check and insert fund company and funds: %s-(%s) %s/%s" % (
                common.getCurrentDateTimeString(), item[1], item[0], str(lngIndex), str(len(companies))))
                _companyCtrl = companyCtrl(companyItem(item[0], item[1]))
                _companyCtrl.insert()
        except:
            traceback.print_exc()
            pass

    def fetchFundsStock(self):
        _fundStockCtrl = fundStockCtrl()
        _fundCtrl = fundCtrl({})
        funds = _fundCtrl.find({})

        lngIndex = 0

        for item in funds:
            try:
                lngIndex = lngIndex + 1
                print("%s Check and insert fund stock: %s-(%s) %s/%s" % (common.getCurrentDateTimeString(), item["name"], item["code"], str(lngIndex), str(funds.count())))
                _fundStockCtrl.fetchByFundCode(item["code"])
            except:
                traceback.print_exc()
                print("Catch exception, and will try again after 5 seconds")
                time.sleep(5)
                _fundStockCtrl.fetchByFundCode(item["code"])
        funds.close()

    def fetchFundsNets(self):
        _fundCtrl = fundCtrl({})
        funds = _fundCtrl.find({})

        lngIndex = 0
        date_from = datetime.date(2017, 1, 1)
        date_to = datetime.date(2017, 12, 31)

        for item in funds:
            try:
                lngIndex = lngIndex + 1
                print("%s Check and insert fund net: %s-(%s) %s/%s" % (common.getCurrentDateTimeString(), item["name"], item["code"], str(lngIndex), str(funds.count())))
                _fundCtrl.insertNet(item, date_from, date_to)
            except:
                traceback.print_exc()
                print("Catch exception, and will try again after 5 seconds")
                time.sleep(5)
                _fundCtrl.insertNet(item, date_from, date_to)
        funds.close()

    def fetchStocks(self):
        try:
            response = request.urlopen("http://quote.eastmoney.com/stocklist.html")
            html = response.read();

            # fetch all stock
            lngIndex = 0
            stockBody = etree.HTML(html).xpath("//div[@class='quotebody']")
            stocks = etree.HTML(etree.tostring(stockBody[0]).decode('utf-8')).xpath("//ul/li/a/text()")

            for stock in stocks:
                lngIndex = lngIndex + 1
                print("Find stock : %s %s/%s" % (stock, lngIndex, len(stocks)))
                name = stock[:stock.index("(")]
                code = stock[stock.index("(")+1:len(stock)-1]
                _stockCtrl = stockCtrl(stockItem(code, name))
                _stockCtrl.insert();
        except:
            traceback.print_exc()
            pass


socket.setdefaulttimeout(30)
spider = Spider();
spider.start();