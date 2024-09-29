import uuid
import utils
import random
import hashlib
import datetime
import database

class user:
  def __init__(self, email="user@example.com"):
    
    self.db = database.database()
    
    user_infos = self.db.get_user()

    if not user_infos:
      self.email = email
      self.generate()
    else:
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
      self.next_validation       = user_infos["next_validation"]

  def generate(self):
    print("Generating user")
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
      "device_system_version": self.device_system_version,
      "balance": self.balance,
      "today_balance": self.today_balance,
      "validated_steps": self.validated_steps,
      "banned_cheater": self.banned_cheater,
      "id": self.id,
      "username": self.username,
      "next_validation": self.next_validation
    }
  
  def update_profile(self):
    auth_token        = self.db.get_user()["token"]
    server_data       = utils.get_user_info(self.user_headers, auth_token)
    server_data_steps = utils.get_step_progress(self.user_headers, auth_token)

    if server_data.get("message", "") == "Login required":
      return False
    
    self.balance         = server_data["balance"]
    self.today_balance   = server_data["today_balance"]
    self.validated_steps = server_data_steps["valid_step"]
    self.banned_cheater  = server_data["banned_cheater"]
    self.id              = server_data["id"]
    self.username        = server_data["username"]

    self.db.update({
      "balance": self.balance,
      "today_balance": self.today_balance,
      "validated_steps": self.validated_steps,
      "banned_cheater": self.banned_cheater,
      "id": self.id,
      "username": self.username
    })

  def check_validation(self):
    if self.validated_today:
      return True
    
    now = datetime.now()
    next_validation = [int(i) for i in self.next_validation.split(":")]
    if (next_validation[0] == now.hour and next_validation[1] <= now.minute) or next_validation[0] < now.hour:
      self.validated_today = True
      self.db.update(self.email, {"validated_today": self.validated_today})
      return self.validate_steps()

  def set_timer(self):
    self.validated_today = False
    if random.randint(0, 10) == 5:
      self.validated_today = True
    
    validation_raw       = random.randint(1080, 1380)
    self.next_validation = "{}:{}".format(str(validation_raw // 60).zfill(2), str(validation_raw % 60).zfill(2))
    self.db.update(self.email, {"next_validation": self.next_validation, "validated_today": self.validated_today})
    return True

  def reset_new_day(self):
    self.validate_steps = 0
    self.today_balance  = 0
    self.db.update(self.email, {"validate_steps": self.validate_steps, "today_balance": self.today_balance})
  
  def connected(self):
    return self.token != None and self.token != ""
  
  def disconnect(self):
    # Not very DRY but the user connection is checked by the presence of token value
    self.token           = ""
    self.balance         = 0
    self.today_balance   = 0
    self.validated_steps = 0
    self.banned_cheater  = 0
    self.id              = 0
    self.username        = 0
    self.db.update({
      "token": self.token,
      "balance": self.balance,
      "today_balance": self.balance,
      "validated_steps": self.validated_steps,
      "banned_cheater": self.banned_cheater,
      "id": self.id,
      "username": self.username
    })
