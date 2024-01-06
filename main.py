from flask import Flask, render_template, request, redirect
from database import Database

urls = []
numbers = []

def read_urls():
  urls.clear()
  for url in db.get_urls():
     urls.append(url)
  print(f"read urls from db: {urls}")

def read_mobiles():
  numbers.clear()
  for number in db.get_numbers():
     numbers.append(number)
  print(f"read numbers from db: {numbers}")

app = Flask(__name__)
db = Database('url_checker.db')

@app.route("/")
def base():
  db.setup_database()
  read_urls()
  read_mobiles()
  return render_template('home.html', data={'urls': urls, 'numbers': numbers})

@app.route('/urls')
@app.route('/urls/new', methods=['POST'])
@app.route('/urls/delete', methods=['POST'])
def urls_template():
  read_urls()

  if 'delete' in request.path:
    delete_url = request.form.get('url')
    print(delete_url)
    return redirect('/urls')

  if request.method == 'POST':
    new_url = request.form.get('new_url')
    if new_url:
       db.write_url(new_url)
    return redirect('/urls')

  return render_template('urls.html', urls=urls)

@app.route('/mobiles')
@app.route('/mobiles/new', methods=['POST'])
@app.route('/mobiles/delete', methods=['POST'])
def mobiles_template():
  read_mobiles()

  if 'delete' in request.path:
    delete_number = request.form.get('url')
    print(delete_number)
    return redirect('/mobiles')

  if request.method == 'POST':
    new_number = request.form.get('new_number')
    if new_number:
        db.write_number(new_number)
    return redirect('/mobiles')

  return render_template('mobiles.html', numbers=numbers)