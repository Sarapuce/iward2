import uuid
import utils
import random
import hashlib
import database

class user:
  def __init__(self, email="user@example.com"):
    
    self.db = database.database()
    
    user_infos = self.db.get_user()

    if not user_infos:
      self.email = email
      self.generate()
    else:
      print(user_infos)
      self.email = user_infos['email']
      self.user_headers = {
        "unique_device_id": user_infos["unique_device_id"],
        "ad_id":            user_infos["ad_id"],
        "adjust_id":        user_infos["adjust_id"],
        "amplitude_id":     user_infos["amplitude_id"]
      }
      self.device_id             = user_infos["device_id"]
      self.device_manufacturer   = user_infos["device_manufacturer"]
      self.device_model          = user_infos["device_model"]
      self.device_product        = user_infos["device_product"]
      self.device_system_version = user_infos["device_system_version"]
      self.token                 = user_infos["token"]

  def generate(self):
    self.user_headers = {
      "unique_device_id": hashlib.md5("{}{}".format(uuid.uuid4(), self.email).encode()).hexdigest()[:16],
      "ad_id":            str(uuid.uuid4()),
      "adjust_id":        hashlib.md5("{}{}".format(uuid.uuid4(), self.email).encode()).hexdigest(),
      "amplitude_id":     str(uuid.uuid4()) + 'R'
    }
    device = utils.get_random_device()
    self.device_id             = hashlib.md5("{}{}".format(uuid.uuid4(), self.email).encode()).hexdigest()[:16]
    self.device_manufacturer   = device["manufacturer"]
    self.device_model          = device["model"]
    self.device_product        = "{}_{}".format(self.device_manufacturer, self.device_model.replace(" ", "_"))
    self.device_system_version = "{}.0".format(random.randint(10, 14))
    self.db.update({
      "email":                 self.email,
      "unique_device_id":      self.user_headers["unique_device_id"],
      "ad_id":                 self.user_headers["ad_id"],
      "adjust_id":             self.user_headers["adjust_id"],
      "amplitude_id":          self.user_headers["amplitude_id"],
      "device_id":             self.device_id,
      "device_manufacturer":   self.device_manufacturer,
      "device_model":          self.device_model,
      "device_product":        self.device_product,
      "device_system_version": self.device_system_version
    })

  def set_mail(self, email):
    self.email = email
    self.db.update({
      "email": email
    })

  def set_token(self, code):
    self.token = code
    self.db.update({
      "token": code
    })

  def get_db_info(self):
    return self.db.get_user()
  
  def get_user_info(self):
    return {
      "email": self.email,
      "token": self.token,
      "user_headers": self.user_headers,
      "device_id": self.device_id,
      "device_manufacturer" : self.device_manufacturer,
      "device_model": self.device_model,
      "device_product": self.device_product,
      "device_system_version": self.device_system_version
    }