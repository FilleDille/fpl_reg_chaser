import requests as rq
from dotenv import load_dotenv
import os
import smtplib
import sys


class FPL:
    URL = 'https://fantasy.premierleague.com/api/bootstrap-static/'

    def __init__(self):
        self.response_raw = rq.get(FPL.URL)
        load_dotenv()

        self.email_sent = os.getenv('EMAIL_SENT')
        self.app_pw = os.getenv('APP_PW')
        self.email = os.getenv('EMAIL')

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
        elif setting == 'ping':
            message = 'Subject: {}\n\n{}'.format("PING FPL", "Script is working")
        else:
            message = 'Subject: {}\n\n{}'.format("ERROR FPL", error_message)

        try:
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login(self.email, self.app_pw)
            s.sendmail(self.email, self.email, message)
            s.quit()

            return True

        except Exception as e:
            print(e)

            return False

    def run(self):
        if 0 < self.tot_players < 1_000_000:
            if self.email_sent is None:
                if self.send_email():
                    with open(".env", "a") as f:
                        f.write("EMAIL_SENT=1")

    def ping(self):
        if self.send_email('ping'):
            pass


if __name__ == '__main__':
    fpl = FPL()

    if not fpl.shit_hit_the_fan:
        if len(sys.argv) == 1:
            fpl.run()

        else:
            fpl.ping()
