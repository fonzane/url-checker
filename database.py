import sqlite3
from flask import g

class Database:

  def __init__(self, database_path, is_flask: bool):
    self.database_path = database_path
    self.is_flask = is_flask

  def get_db(self):
    if(self.is_flask):
      db = getattr(g, '_database', None)
      if db is None:
        db = g._database = sqlite3.connect(self.database_path)
    else:
      db = sqlite3.connect(self.database_path)
    return db

  def close_db(self):
    db = getattr(g, '_database', None)
    if db is not None:
      db.close()

  def setup_database(self):
    with self.get_db() as db:
      cursor = db.cursor()

      # Check if tables exist
      cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='urls';")
      urls_table_exists = cursor.fetchone() is not None

      cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='numbers';")
      numbers_table_exists = cursor.fetchone() is not None

      # If tables don't exist, create them
      if not urls_table_exists:
        cursor.execute('''
          CREATE TABLE urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL
          );
        ''')

      if not numbers_table_exists:
        cursor.execute('''
          CREATE TABLE numbers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number TEXT NOT NULL UNIQUE
          );
        ''')

      db.commit()
      # create_table_query = '''
      # CREATE TABLE IF NOT EXISTS urls (
      #   id INTEGER PRIMARY KEY AUTOINCREMENT,
      #   url TEXT NOT NULL
      # );
      # CREATE TABLE IF NOT EXISTS numbers (
      #   id INTEGER PRIMARY KEY AUTOINCREMENT,
      #   number TEXT NOT NULL UNIQUE
      # );
      # '''
      # cursor.executescript(create_table_query)


  def get_urls(self):
    with self.get_db() as db:
      cursor = db.cursor()
      cursor.execute('SELECT url FROM urls')
      urls = [row[0] for row in cursor.fetchall()]
      print(f"Fetched URLS from Database - {urls}")
      return urls


  def get_numbers(self):
    with self.get_db() as db:
      cursor = db.cursor()
      cursor.execute('SELECT number FROM numbers')
      numbers = [row[0] for row in cursor.fetchall()]
      print(f"Fetched NUMBERS from Database - {numbers}")
      return numbers

  def write_url(self, url):
    with self.get_db() as db:
      cursor = db.cursor()
      print(f"Inserting {url} into the Database.")
      insert_query = 'INSERT INTO urls (url) VALUES (?)'
      cursor.execute(insert_query, (url,))

  def write_number(self, number):
    with self.get_db() as db:
      cursor = db.cursor()
      print(f"Inserting {number} into the Database.")
      insert_query = 'INSERT INTO numbers (number) VALUES (?)'
      cursor.execute(insert_query, (number,))

  def delete_url(self, url):
    with self.get_db() as db:
      cursor = db.cursor()
      print("Deleting " + url + " from Database.")
      delete_query = 'DELETE FROM urls WHERE url = ?'
      cursor.execute(delete_query, (url,))

  def delete_number(self, number):
    with self.get_db() as db:
      cursor = db.cursor()
      print("Deleting " + number + " from Database.")
      delete_query = 'DELETE FROM numbers WHERE number = ?'
      cursor.execute(delete_query, (number,))