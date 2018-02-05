class company():
    def __init__(self, code, name):
        self.code = code
        self.name = name
        self.creation_date = None
        self.creation_by = ''
        self.last_updated_date = None
        self.last_updated_by = ""

class fund():
    def __init__(self, company_code, code, name):
        self.company_code = company_code
        self.code = code
        self.name = name
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
