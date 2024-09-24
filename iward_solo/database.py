import os
import sqlite3

class database:
  def __init__(self, db_name='db.sqlite3', table='user'):
    self.db_name = db_name
    self.conn = None
    self.cursor = None
    self.connect()
    self.create_table("user", """email varchar(100) NOT NULL,
                          password varchar(100) NOT NULL,
                          token varchar(100),
                          balance integer,
                          today_balance integer,
                          validated_steps integer,
                          banned_cheater varchar(100),
                          id varchar(100),
                          username varchar(100),
                          unique_device_id varchar(100),
                          ad_id varchar(100),
                          adjust_id varchar(100),
                          amplitude_id varchar(100),
                          device_id varchar(100),
                          device_manufacturer varchar(100),
                          device_model varchar(100),
                          device_product varchar(100),
                          device_system_version varchar(100),
                          next_validation varchar(100),
                          validated_today boolean,
                          PRIMARY KEY (email)""")

  def connect(self):
    try:
      self.conn = sqlite3.connect(self.db_name)
      self.cursor = self.conn.cursor()
      print(f"Connected to the database '{self.db_name}' successfully.")
      
    except sqlite3.Error as e:
      print(f"An error occurred while connecting to the database: {e}")
      raise

  def create_table(self, table_name, schema):
    try:
      self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({schema})")
      self.conn.commit()
      print(f"Table '{table_name}' is ready.")
    except sqlite3.Error as e:
      print(f"An error occurred while creating the table: {e}")
      raise