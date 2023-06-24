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
            self.they_blocked_my_ip()
            self.shit_hit_the_fan = True
            return

        self.shit_hit_the_fan = False
        self.response = self.response_raw.json()
        self.tot_players = int(self.response['total_players'])

    def send_email(self, ping_mode: bool = False, blocked: bool = False):
        if blocked:
            message = 'Subject: {}\n\n{}'.format("BLOCKED BY FPL", "My IP just got blocked")
        elif ping_mode:
            message = 'Subject: {}\n\n{}'.format("PING FPL", "Script is working")
        else:
            message = 'Subject: {}\n\n{}'.format("FPL REGISTRATION IS OPEN", "GO GET THEM")

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
        if self.tot_players < 1_000_000:
            if self.email_sent is None:
                if self.send_email():
                    with open(".env", "a") as f:
                        f.write("EMAIL_SENT=1")

    def ping(self):
        if self.send_email(True):
            pass

    def they_blocked_my_ip(self):
        if self.send_email(True, True):
            pass


if __name__ == '__main__':
    fpl = FPL()

    if not fpl.shit_hit_the_fan:
        if len(sys.argv) == 1:
            fpl.run()

        else:
            fpl.ping()
