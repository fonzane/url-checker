from database import Database
import requests
from time import sleep
from datetime import datetime
from os import getenv

class URLChecker:

  def __init__(self):
    self.db = Database(getenv("DB_PATH"), False)
    self.urls = self.db.get_urls()
    self.numbers = self.db.get_numbers()
    print(f"URL Watcher inizialized with urls - {self.urls} and numbers - {self.numbers}.")

  def send_sms(self, number: str, message: str):
    params='{"telephone":"%s","message":"%s"}' %(number, message)
    url=f"http://192.168.0.25:87/sendsms/{params}"
    resp = requests.get(url, timeout=8)
    print(f"SMS sent to {number} - message: {message} - status_code: {resp.status_code}")
    print(f"Response: {resp.text}")

  def check_website_online(self, url: str) -> bool:
    try:
      check_time = datetime.now()
      response = requests.get(url, timeout=8)

      if response.status_code == 200:
          print(f"{url} is online at {check_time}")
          return True
      else:
          print(f"Received status code {response.status_code} for {url}")
          return False
    except requests.exceptions.RequestException as e:
      print(f"[Error] requesting {url} {e}")
      return False

  def reset_numbers(self):
    numbers = self.db.get_numbers()
    self.numbers.clear()
    for number in numbers:
      self.numbers.append(number)
    print(f"URL Checker - reset numbers: {numbers}")

  def reset_urls(self):
    urls = self.db.get_urls()
    self.urls.clear()
    for url in urls:
      self.urls.append(url)
    print(f"URL Checker - reset urls: {urls}")

  def start_wacher(self):
    check_interval = int(getenv('CHECK_INTERVAL'))

    for number in self.numbers:
      self.send_sms(number, f"Webmonitor watcher started at {datetime.now()}...")

    while True:
      for url in self.urls:
        url_online = self.check_website_online(url)

        if not url_online:
          print(f"Couldn't reach url {url} and sending sms to {self.numbers} - {datetime.now()}")
          for number in self.numbers:
            self.send_sms(number, f"Website not reachable: {url} - {datetime.now()}")
      print(f"Checked {self.urls}. Next check in {check_interval/3600} hours...")
      sleep(check_interval)