from yandex_tracker_client import TrackerClient 
import os
import csv
from io import StringIO
from io import BytesIO
from dto import Client
from dto import Vacancy
from dto import ReportVacancy
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
            client = Client(
                fullname=issue.summary,
                telegram_id=telegram_id, 
                report_link=issue.report_link,
                meta={'issue' : issue.key, 'queue' : issue.queue.key}
            )
            return client
        return None

    def createVacancyForClient(self, client, vacancy):
        try:
            self.tracker_client.issues.create(
                queue=client.meta.get('queue'),
                summary='Обработка вакансии: ' + vacancy.link,
                type={'key': 'vacancy'},
                ssylka=vacancy.link,
                parent={'key': client.meta.get('issue')},
                unique=vacancy.link + '_' + client.meta.get('issue')
            )
        except Exception as e:
            raise RuntimeError("Ошибка при добавлении вакансии в обработку")
    
    def findReportVacanciesForClient(self, client):
        issues = self.tracker_client.issues.find(
            filter={'queue': 'PROCESING', 'type' : 'vacancy', 'parent' : client.meta.get('issue')},
            per_page=1000
        )

        report_vacancies = []

        for issue in issues:
            title = issue.summary
            link = issue.ssylka
            status = issue.status.name 
            date = issue.start

            report_vacancy = ReportVacancy(title=title, link=link, status=status, date=date)
            report_vacancies.append(report_vacancy)

        return report_vacancies
    
    def generateReportVacanciesForClient(self, client):
        filename = client.meta.get('issue')
        vacancies = self.findReportVacanciesForClient(client=client)
        csv_data = StringIO()
        csv_writer = csv.writer(csv_data)
        csv_writer.writerow(["Вакансия", "Ссылка", "Статус", "Дата обработки"])
        for vacancy in vacancies:
            csv_writer.writerow([vacancy.title, vacancy.link, vacancy.status, vacancy.date])

        csv_data.seek(0)

        buf = BytesIO()
        buf.write(csv_data.getvalue().encode())
        buf.seek(0)
        buf.name = f'report.csv'
        return buf