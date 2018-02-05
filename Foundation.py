import re
import time
from DB import DB
from datetime import datetime
from urllib import request

from Core import common
from Items import fund as fundItem;
from Items import net as netItem;

class company():
    def __init__(self, item):
        self.col_name = "company"
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
        print('%s(%s): total funds %s' % (self.item.name, self.item.code, str(len(funds))))
        for item in funds:
            _fundCtrl = fund(fundItem(self.item.code, item[0], item[1]))
            _fundCtrl.insert()

class fund():
    def __init__(self, item):
        self.col_name = "fund"
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
        time.sleep(1)
        strDateFrom = date_from.strftime('%Y-%m-%d')
        strDateTo = date_to.strftime('%Y-%m-%d')
        url = "http://jingzhi.funds.hexun.com/database/jzzs.aspx?fundcode=%s&startdate=%s&enddate=%s" % (item["code"], strDateFrom, strDateTo)

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        req = request.Request(url=url, headers=headers)
        response = request.urlopen(req)
        html = response.read();
        content = html.decode('gb2312')
        nets = re.findall(r'<td style="text-align: center;">(.*?)</td>\r\n<td style="text-align: center;">(.*?)</td>\r\n<td style="text-align: center;" class="end">(.*?)</td>', content)

        for cur_net in nets:
            net_date = datetime.strptime(cur_net[0],'%Y-%m-%d')
            net_cur = float(cur_net[1])
            net_total = float(cur_net[2])
            netCtrl = net(netItem(item["code"], net_date, net_cur, net_total))
            netCtrl.insert();

    def insertAllNet(self, date_from, date_to):
        lngIndex = 0
        funds = self.find({})
        for item in funds:
            lngIndex = lngIndex + 1
            print("Check and insert fund net: %s-(%s) %s/%s" % (item["name"], item["code"], str(lngIndex), str(len(funds))))
            self.insertNet(item, date_from, date_to)

    def findNet(self, item, date):
        return;

class net():
    def __init__(self, net):
        self.col_name = "net"
        self.net = net
        self.db = DB(self.col_name)

    def insert(self):
        self.db.insert(common.props(self.net))
