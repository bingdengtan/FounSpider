import re
import time
import socket
import traceback

from DB import DB
from datetime import datetime
from urllib import request
from lxml import etree

from Core import common
from Items import fund as fundItem;
from Items import netItem as netItem;
from Items import fund_stock as stockItem;

class company():
    def __init__(self, item):
        self.col_name = "fund_company"
        self.item = item
        self.db = DB(self.col_name)

    def insert(self):
        if self.exist({"code": self.item.code}) == False :
            self.item.creation_date = datetime.now()
            self.item.last_updated_date = datetime.now()
            self.db.insert(common.props(self.item))
        self.insertFounds()


    def exist(self,dic):
        items = self.db.find(dic)
        return items.count() > 0

    def insertFounds(self):
        time.sleep(1)
        url = "http://fund.eastmoney.com/Company/%s.html" % (self.item.code)
        response = request.urlopen(url)
        html = response.read();
        content = html.decode('utf-8')
        funds = re.findall(r'<a href="http://fund.eastmoney.com/(.*?).html" class="name" title="(.*?)">', content)
        print('%s %s(%s): total funds %s' % (common.getCurrentDateTimeString(), self.item.name, self.item.code, str(len(funds))))
        for item in funds:
            _fundCtrl = fund(fundItem(self.item.code, item[0], item[1]))
            _fundCtrl.insert()

class stock():
    def __init__(self):
        self.col_name = "fund_stock"
        self.db = DB(self.col_name)

    def fetchByFundCodeAndYear(self, fund_code, year):
        time.sleep(1)
        url = "http://fund.eastmoney.com/f10/FundArchivesDatas.aspx?type=jjcc&code=%s&topline=50&year=%s&month=" % (fund_code, str(year))
        try:
            response = request.urlopen(url)
            html = response.read();
            content = html.decode('utf-8')
            content = re.findall(r'content:"(.*?)"', content)

            if content[0] == "":
                return

            quarters = etree.HTML(content[0]).xpath("//div[@class='box']")
            print("%s Fetch and insert fund stock, Fund code: %s, Year: %s" % (common.getCurrentDateTimeString(), fund_code, str(year)))
            for quarter in quarters:
                tree = etree.HTML(etree.tostring(quarter).decode('utf-8'))
                dates = tree.xpath("//font[@class='px12']/text()")
                stock_codes = tree.xpath("//table/tbody/tr/td[2]/a/text()")
                stock_names = tree.xpath("//table/tbody/tr/td[3]/a/text()")
                stock_weights = tree.xpath("//table/tbody/tr/td[last()-2]/text()")
                stock_numbers = tree.xpath("//table/tbody/tr/td[last()-1]/text()")
                stock_totals = tree.xpath("//table/tbody/tr/td[last()]/text()")

                month = int(str(dates[0]).split("-")[1])
                for index , item in enumerate(stock_codes):
                    try:
                        weight = float(str(stock_weights[index]).replace("%",""))
                    except:
                        weight = stock_weights[index]

                    try:
                        number = float(str(stock_numbers[index]).replace(",",""))
                    except:
                        number = stock_numbers[index]

                    try:
                        total = float(str(stock_totals[index]).replace(",",""))
                    except:
                        total = stock_totals[index]

                    _stockItem = stockItem(fund_code, stock_codes[index], stock_names[index], year, month, weight, number, total)
                    self.insertStock(_stockItem)
        except:
            traceback.print_exc()
            print("FetchByFundCodeAndYear catch exception, fund code: %s" % (fund_code))
            pass

    def insertStock(self, dict):
        if self.exist(dict) == False:
            dict.creation_date = datetime.now()
            dict.last_updated_date = datetime.now()
            self.db.insert(common.props(dict))

    def exist(self,dict):
        items = self.db.find({"fund_code":dict.fund_code, "stock_code": dict.stock_code, "year": dict.year, "month": dict.month})
        return items.count() > 0

    def fetchByFundCode(self, fund_code):
        years = self.fetchStockYearsByFundCode(fund_code)

        if len(years) > 0:
            for year in years:
                self.fetchByFundCodeAndYear(fund_code, int(year))

    def fetchStockYearsByFundCode(self, fund_code):
        nextYear = datetime.now().year + 1
        url = "http://fund.eastmoney.com/f10/FundArchivesDatas.aspx?type=jjcc&code=%s&topline=10&year=%s&month=" % (fund_code, str(nextYear))
        try:
            response = request.urlopen(url)
            html = response.read();
            content = html.decode('utf-8')
            years = re.findall(r'arryear:\[(.*?)\]', content)
            if years[0] == "":
                return []
            else:
                return str(years[0]).split(",")
        except:
            traceback.print_exc()
            print("FetchStockYearsByFundCode catch exception, fund code: %s" % (fund_code))
            pass

class fund():
    def __init__(self, item):
        self.col_name = "fund_fund"
        self.item = item
        self.db = DB(self.col_name)

    def insert(self):
        if self.exist({"code": self.item.code}) == False:
            self.item.creation_date = datetime.now()
            self.item.last_updated_date = datetime.now()
            self.db.insert(common.props(self.item))

    def exist(self,dic):
        items = self.db.find(dic)
        return items.count() > 0

    def find(self, dic):
        return self.db.find(dic).sort([("code",1)])

    def insertNet(self, item, date_from, date_to):
        strDateFrom = date_from.strftime('%Y-%m-%d')
        strDateTo = date_to.strftime('%Y-%m-%d')
        url = "http://jingzhi.funds.hexun.com/database/jzzs.aspx?fundcode=%s&startdate=%s&enddate=%s" % (item["code"], strDateFrom, strDateTo)

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        req = request.Request(url=url, headers=headers)

        try:
            response = request.urlopen(req)
            html = response.read();
            content = html.decode('gb2312', 'ignore')
            nets = re.findall(
                r'<td style="text-align: center;">(.*?)</td>\r\n<td style="text-align: center;">(.*?)</td>\r\n<td style="text-align: center;" class="end">(.*?)</td>',
                content)

            for cur_net in nets:
                net_date = datetime.strptime(cur_net[0], '%Y-%m-%d')
                net_cur = float(cur_net[1])
                net_total = float(cur_net[2])
                netCtrl = net(netItem(item["code"], net_date, net_cur, net_total))
                netCtrl.insert();
        except socket.timeout:
            print("Catch timeout, and will try again after 5 seconds")
            time.sleep(5)
            self.insertNet(item, date_from, date_to)
        except:
            print(url)
            traceback.print_exc()
            pass

class net():
    def __init__(self, net):
        self.col_name = "fund_net"
        self.net = net
        self.db = DB(self.col_name)

    def insert(self):
        if self.exist() == False:
            self.db.insert(common.props(self.net))

    def exist(self):
        return self.db.find({'fund_code': self.net.fund_code, "date": self.net.date}).count() > 0