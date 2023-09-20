class Client:
    def __init__(self, fullname, telegram_id=None, report_link=None, meta=None):
        self.fullname = fullname
        self.telegram_id = telegram_id
        self.meta = meta
        self.report_link = report_link

class Vacancy:
    def __init__(self, link):
        self.link = link

class ReportVacancy:
    def __init__(self, title=None, link=None, status=None, date=None):
        self.title = title
        self.link = link
        self.status = status
        self.date = date