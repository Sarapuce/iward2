import uuid
import utils
import random
import hashlib
import database

class user:
  def __init__(self, email):
    
    self.db = database.database()

    self.email = email
    self.user_headers = {
          "unique_device_id": hashlib.md5("{}{}".format(uuid.uuid4(), email).encode()).hexdigest()[:16],
          "ad_id":            str(uuid.uuid4()),
          "adjust_id":        hashlib.md5("{}{}".format(uuid.uuid4(), email).encode()).hexdigest(),
          "amplitude_id":     str(uuid.uuid4()) + 'R'
        }
    device = utils.get_random_device()
    self.device_id             = hashlib.md5("{}{}".format(uuid.uuid4(), email).encode()).hexdigest()[:16]
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