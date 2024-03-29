from flask import Flask, render_template, request, redirect
from database import Database
from url_checker import URLChecker
from threading import Thread
from dotenv import load_dotenv
from os import getenv

load_dotenv()

urls = []
numbers = []
hostadress = getenv("HOSTADRESS")
db_path = getenv("DB_PATH")

def read_urls():
  urls.clear()
  for url in db.get_urls():
     urls.append(url)

def read_mobiles():
  numbers.clear()
  for number in db.get_numbers():
     numbers.append(number)

app = Flask(__name__)
db = Database(db_path, True)
with app.app_context():
  db.setup_database()
url_checker = URLChecker()

@app.route("/")
def base():
  db.setup_database()
  read_urls()
  read_mobiles()
  return render_template('home.html', data={
    'urls': urls,
    'numbers': numbers,
    'interval': int(getenv('CHECK_INTERVAL'))/3600,
    'results': url_checker.results
  })

@app.route('/urls')
@app.route('/urls/new', methods=['POST'])
@app.route('/urls/delete', methods=['POST'])
def urls_template():
  read_urls()

  if 'delete' in request.path:
    delete_url = request.form.get('url')
    db.delete_url(delete_url)
    url_checker.reset_urls()
    return redirect('/urls')

  if request.method == 'POST':
    new_url = request.form.get('new_url')
    if new_url:
       db.write_url(new_url)
       url_checker.reset_urls()
    return redirect('/urls')

  return render_template('urls.html', urls=urls)

@app.route('/mobiles')
@app.route('/mobiles/new', methods=['POST'])
@app.route('/mobiles/delete', methods=['POST'])
def mobiles_template():
  read_mobiles()

  if 'delete' in request.path:
    delete_number = request.form.get('number')
    db.delete_number(delete_number)
    url_checker.reset_numbers()
    return redirect('/mobiles')

  if request.method == 'POST':
    new_number = request.form.get('new_number')
    if new_number:
        db.write_number(new_number)
        url_checker.reset_numbers()
    return redirect('/mobiles')

  return render_template('mobiles.html', numbers=numbers)

if __name__ == '__main__':
  url_checker_process = Thread(target=url_checker.start_wacher)
  url_checker_process.start()
  app.run(host=hostadress, port=5000)