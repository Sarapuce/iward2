import os
import sqlite3

class database:
  def __init__(self, db_name='db.sqlite3', table='user'):
    self.db_name = db_name
    self.conn = None
    self.cursor = None
    self.table = table
    self.create_table("user", """db_id integer,
                          email varchar(100),
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
                          PRIMARY KEY (db_id)""")

  def connect(self):
    try:
      self.conn = sqlite3.connect(self.db_name)
      self.cursor = self.conn.cursor()
      print(f"Connected to the database '{self.db_name}' successfully.")
      
    except sqlite3.Error as e:
      print(f"An error occurred while connecting to the database: {e}")
      raise
  
  def close(self):
    try:
      if self.cursor:
        self.cursor.close()
        print("Cursor closed.")
      if self.conn:
        self.conn.close()
        print(f"Connection to the database '{self.db_name}' closed.")
    except sqlite3.Error as e:
      print(f"An error occurred while closing the database: {e}")
    finally:
      self.conn = None
      self.cursor = None

  def create_table(self, table_name, schema):
    try:
      self.connect()
      self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({schema})")
      self.conn.commit()
      print(f"Table '{table_name}' is ready.")

      self.cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE db_id = 0")
      user_count = self.cursor.fetchone()[0]

      if user_count == 0:
        default_user = {
                    "db_id": 0,
                    "email": "default@example.com",
                    "token": None,
                    "balance": 0,
                    "today_balance": 0,
                    "validated_steps": 0,
                    "banned_cheater": None,
                    "id": "default_id",
                    "username": "default_user",
                    "unique_device_id": None,
                    "ad_id": None,
                    "adjust_id": None,
                    "amplitude_id": None,
                    "device_id": None,
                    "device_manufacturer": None,
                    "device_model": None,
                    "device_product": None,
                    "device_system_version": None,
                    "next_validation": None,
                    "validated_today": False
                }
        columns = ', '.join(default_user.keys())
        placeholders = ', '.join(['?'] * len(default_user))
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(insert_query, tuple(default_user.values()))
        self.conn.commit()
        print("Default user created.")
      else:
        print("User already exist")
    except sqlite3.Error as e:
      print(f"An error occurred while creating the table: {e}")
    finally:
      self.close()

  def update(self, update_data):
    try:
      self.connect()
      set_clause = ", ".join([f"{col} = ?" for col in update_data.keys()])
      sql = f"UPDATE {self.table} SET {set_clause} WHERE db_id = 0"
      self.cursor.execute(sql, tuple(update_data.values()))
      self.conn.commit()
      print(f"Updated {self.cursor.rowcount} row(s) successfully.")
    except sqlite3.Error as e:
      print(f"An error occurred while updating the table: {e}")
      self.conn.rollback()
    finally:
      self.close()

  def get_user(self):
    try:
      self.connect()
      self.cursor.execute(f"SELECT * FROM {self.table} WHERE db_id = 0")
      row = self.cursor.fetchone()
      print(row)
      if row:
        column_names = [description[0] for description in self.cursor.description]
        user_data = dict(zip(column_names, row))
        return user_data
      else:
        print("No user found with db_id = 0.")
        return None
    except sqlite3.Error as e:
      print(f"An error occurred while fetching the user: {e}")
      return None
    finally:
      self.close()
