import requests as rq
from dotenv import load_dotenv, set_key
from pathlib import Path
import newspaper
import os
import smtplib
import sys


class FPL:
    URL = 'https://fantasy.premierleague.com/api/bootstrap-static/'

    def __init__(self):
        self.response_raw = rq.get(FPL.URL)
        load_dotenv()
        self.path = Path('.env')

        self.email_sent = os.getenv('EMAIL_SENT')
        self.app_pw = os.getenv('APP_PW')
        self.email_from = os.getenv('EMAIL_FROM')
        self.email_to = os.getenv('EMAIL_TO')
        self.email_admin = os.getenv('EMAIL_ADMIN')

        if self.response_raw.status_code != 200:
            self.send_email('error', str(self.response_raw.status_code) + ";" + self.response_raw.text)
            self.shit_hit_the_fan = True
            return

        self.shit_hit_the_fan = False
        self.response = self.response_raw.json()
        self.tot_players = int(self.response['total_players'])

    def send_email(self, setting: str = 'normal', error_message: str = ''):
        if setting == 'normal':
            message = 'Subject: {}\n\n{}'.format("FPL REGISTRATION IS OPEN", "GO GET THEM")
            email_from = self.email_from
            email_to = self.email_to
        elif setting == 'ping':
            message = 'Subject: {}\n\n{}'.format("PING FPL", "Script is working")
            email_from = self.email_from
            email_to = self.email_admin
        else:
            message = 'Subject: {}\n\n{}'.format("ERROR FPL", error_message)
            email_from = self.email_from
            email_to = self.email_admin

        recipients = email_to.split(',')

        for recipient in recipients:
            try:
                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.starttls()
                s.login(self.email_from, self.app_pw)
                s.sendmail(email_from, recipient, message)
                s.quit()
            except Exception as e:
                print(e)
                return False
        
        return True

    def run(self):
        self.check_api()
        self.check_news()

    def check_api(self):
        if self.email_sent == 'false':
            if 0 < self.tot_players < 1_000_000:
                if self.send_email():
                    set_key(dotenv_path=self.path, key_to_set='EMAIL_SENT', value_to_set='true')
    
    def check_news(self):
        if self.email_sent == 'false':
            site = newspaper.build('https://www.premierleague.com/news')
            site_urls = site.article_urls()

            for article_url in site_urls:
                article = newspaper.Article(article_url)
                article.download()
                article.parse()
                article_lower = article.text.lower()
                if '2024/25' in article_lower and 'is live' in article_lower:
                    if self.send_email():
                        set_key(dotenv_path=self.path, key_to_set='EMAIL_SENT', value_to_set='true')

    def ping(self):
        if self.send_email('ping'):
            pass

    def reset(self):
        set_key(dotenv_path=self.path, key_to_set='EMAIL_SENT', value_to_set='false')
        print('env variable EMAIL_SENT reset to false')
    


if __name__ == '__main__':
    fpl = FPL()

    if not fpl.shit_hit_the_fan:
        if len(sys.argv) == 1:
            fpl.run()
            sys.exit()

        if sys.argv[1] == '--ping':
            fpl.ping()

        if sys.argv[1] == '--reset':
            fpl.reset()
