from yandex_tracker_client import TrackerClient 
import os
from dto import Client
from dto import Vacancy
from dotenv import load_dotenv

load_dotenv()

class ClientService:
    def __init__(self):
        self.tracker_client = TrackerClient(token=os.getenv("YANDEX_TRACKER_TOKEN"), cloud_org_id=os.getenv("YANDEX_TRACKER_ORG_ID"))

    def findByTelegramId(self, telegram_id):
        issues = self.tracker_client.issues.find(
            filter={'queue': 'PROCESING', 'type' : 'klient', 'telegram_Id' : telegram_id},
            per_page=1
        )
        if issues:
            issue = issues[0]
            client = Client(fullname=issue.summary, telegram_id=telegram_id, meta={'issue' : issue.key, 'queue' : issue.queue.key})
            return client
        return None

    def createVacancyForClient(self, client, vacancy):
        if isinstance(client, Client) and isinstance(vacancy, Vacancy):
            try:
                response = self.tracker_client.issues.create(
                    queue=client.meta.get('queue'),
                    summary='Обработка вакансии: ' + vacancy.link,
                    type={'key': 'vacancy'},
                    ssylka=vacancy.link,
                    parent={'key': client.meta.get('issue')},
                    unique=vacancy.link + '_' + client.meta.get('issue')
                )
                print(response)
            except Exception as e:
                raise RuntimeError("Ошибка при добавлении вакансии в обработку")
        else:
            raise RuntimeError("Ошибка при добавлении вакансии в обработку")
        return True