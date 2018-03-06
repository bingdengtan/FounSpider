from Core import common

class company():
    def __init__(self, code, name):
        self.code = code
        self.name = name
        self.name_ping_yin = common.getFirstCharAsPingYin(self.name)
        self.creation_date = None
        self.creation_by = ''
        self.last_updated_date = None
        self.last_updated_by = ""

class fund():
    def __init__(self, company_code, code, name):
        self.company_code = company_code
        self.code = code
        self.name = name
        self.name_ping_yin = common.getFirstCharAsPingYin(self.name)
        self.creation_date = None
        self.creation_by = ''
        self.last_updated_date = None
        self.last_updated_by = ""

class stock():
    def __init__(self, code, name):
        self.code = code
        self.name = name
        self.name_ping_yin = common.getFirstCharAsPingYin(self.name)
        self.creation_date = None
        self.creation_by = ''
        self.last_updated_date = None
        self.last_updated_by = ""

class netItem():
    def __init__(self, fund_code, date, current, total):
        self.fund_code = fund_code
        self.date = date
        self.current = current
        self.total = total
        self.creation_date = None
        self.creation_by = ''
        self.last_updated_date = None
        self.last_updated_by = ""

class fund_stock():
    def __init__(self, fund_code, stock_code, stock_name, year, month, weight, number, total):
        self.fund_code = fund_code
        self.stock_code = stock_code
        self.stock_name = stock_name
        self.year = year
        self.month = month
        self.weight = weight
        self.number = number
        self.total = total

        self.creation_date = None
        self.creation_by = ''
        self.last_updated_date = None
        self.last_updated_by = ""