from flask import Flask, render_template, request, redirect
import requests
from time import sleep
from datetime import datetime

urls = []
numbers = []

with open("urls.txt") as urls_file:
    for url in urls_file:
        urls.append(url.strip())
with open("mobiles.txt") as numbers_file:
    for number in numbers_file:
        numbers.append(number.strip())
print(f"read numbers from file: {numbers}")
print(f"read urls from file: {urls}")

app = Flask(__name__)

@app.route("/")
def base():
  return render_template('home.html')

@app.route('/urls', methods=['GET', 'POST'])
def urls_template():
  if request.method == 'POST':
    new_url = request.form.get('new_url')
    if new_url:
       with open('urls.txt', 'a') as file:
          file.write(new_url + '\n')
    return redirect('/')

  return render_template('urls.html', urls=urls)