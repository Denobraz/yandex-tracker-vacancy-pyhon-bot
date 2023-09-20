class Client:
    def __init__(self, fullname, telegram_id=None, meta=None):
        self.fullname = fullname
        self.telegram_id = telegram_id
        self.meta = meta

class Vacancy:
    def __init__(self, link):
        self.link = link