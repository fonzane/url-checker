import sqlite3
from flask import g

class Database:

  def __init__(self, database_path):
    self.database_path = database_path

  def get_db(self):
    db = getattr(g, '_database', None)
    if db is None:
      db = g._database = sqlite3.connect(self.database_path)
    return db

  def close_db(self, exception):
    db = getattr(g, '_database', None)
    if db is not None:
      db.close()

  def setup_database(self):
    with self.get_db() as db:
      cursor = db.cursor()

      create_table_query = '''
      CREATE TABLE IF NOT EXISTS urls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT NOT NULL
      );
      CREATE TABLE IF NOT EXISTS numbers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        number TEXT NOT NULL
      );
      '''
      cursor.executescript(create_table_query)



  def get_urls(self):
    with self.get_db() as db:
      cursor = db.cursor()
      cursor.execute('SELECT url FROM urls')
      return [row[0] for row in cursor.fetchall()]


  def get_numbers(self):
    with self.get_db() as db:
      cursor = db.cursor()
      cursor.execute('SELECT number FROM numbers')
      return [row[0] for row in cursor.fetchall()]

  def write_url(self, url):
    with self.get_db() as db:
      cursor = db.cursor()
      insert_query = 'INSERT INTO urls (url) VALUES (?)'
      cursor.execute(insert_query, (url,))

  def write_number(self, number):
    with self.get_db() as db:
      cursor = db.cursor()
      insert_query = 'INSERT INTO numbers (number) VALUES (?)'
      cursor.execute(insert_query, (number,))

  def delete_url(self, url_id):
    with self.get_db() as db:
      cursor = db.cursor()
      delete_query = 'DELETE FROM urls WHERE id = ?'
      cursor.execute(delete_query, (url_id,))