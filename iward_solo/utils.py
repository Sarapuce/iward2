import json
import time
import uuid
import random
import hashlib
import logging
import requests

def decode(cipher):
    clear = ""
    for c in cipher:
        clear += chr(c ^ 0x41)
    return clear

validate_steps_url      = decode(b')5512{nn# "*$/%o13.%o6$6 3%o\'3n 1(n7poqn7 -(% 5$\x1e25$12')
step_progress_url       = decode(b')5512{nn# "*$/%o13.%o6$6 3%o\'3n 1(n7poqn/$6\x1e25$1\x1e13.&3$22')
get_profile_url         = decode(b')5512{nn# "*$/%o13.%o6$6 3%o\'3n 1(n7poqn"425.,$3n&$5\x1e13.\'(-$')
signin_with_email_url   = decode(b')5512{nn# "*$/%o13.%o6$6 3%o\'3n 1(n7poqn"425.,$3n3$04$25\x1e2(&/(/\x1e6(5)\x1e$, (-')
signin_id_token         = decode(b')5512{nn# "*$/%o13.%o6$6 3%o\'3n 1(n7poqn"425.,$3n2(&/(/\x1e6(5)\x1e(%\x1e5.*$/')
referal_url             = decode(b')5512{nn# "*$/%o13.%o6$6 3%o\'3n 1(n7poqn"425.,$3n".,1-$5$\x1e21./2.32)(1\x1e25$1')
base_url                = decode(b')5512{nn666o6$6 3%o 11n2(&/(/\x1e6(5)\x1e$, (-')
host                    = decode(b'# "*$/%o13.%o6$6 3%o\'3')
sender_name             = decode(b'\x16$6 3%')

user_agent = "okhttp/4.11.0"

def generate_headers(user_headers, payload, auth_token=""):
  hex_tags = [
     hex(random.randint(0x10000000, 0xffffffff))[2:],
     hex(random.randint(0x1000000000000000, 0xffffffffffffffff))[2:],
     hex(random.randint(0x1000000000000000, 0xffffffffffffffff))[2:]]
  
  json_payload = json.dumps(payload)

  headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Accept-Encoding": "gzip, deflate",
    "Host": host,
    "User-Agent": user_agent,
    "Ww_message_length": f"{len(json_payload)}",
    "Ww_app_version": "7.9.0",
    "Ww_os": "android",
    "Ww_os_version": "33",
    "Ww_build_version": "242216",
    "Ww_codepush_version": "base",
    "Ww-Unique-Device-Id": user_headers["unique_device_id"],
    "Ww_device_ts": str(int(time.time() * 1000)),
    "Ww_device_timezone": "America/New_York",
    "Ww_device_country": "US",
    "Ww_user_language": "en-US",
    "Ww_user_advertising_id": user_headers["ad_id"],
    "Ww_adjust_id": user_headers["adjust_id"],
    "Push_notification_enabled": "1",
    "Amplitude_device_id": user_headers["amplitude_id"],
    "Ww_track": hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest(),
    "X-Datadog-Origin": "rum",
    "X-Datadog-Sampling-Priority": "0",
    "X-Datadog-Trace-Id": str(random.randint(10000000000000000000, 99999999999999999999)),
    "X-Datadog-Parent-Id": str(random.randint(10000000000000000000, 99999999999999999999)),
    "X-Datadog-Tags": f"dd.p.tid={hex_tags[0]}00000000",
    "Traceparent": f"00-{hex_tags[0]}00000000{hex_tags[1]}-{hex_tags[2]}-00",
    "Tracestate": f"dd=s:0;o:rum;p:{hex_tags[2]}"
  }
  if auth_token:
      headers["Authorization"] = auth_token
  else:
      headers["Authorization"] = None
  return headers

def get_google_token(weward_token):
    payload = {
        "token": weward_token,
        "returnSecureToken": True
    }

    r = requests.post("https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyCustomToken?key=AIzaSyBpVnvwRMvz9lP9A2cVBKIIutli4ZuCmm4", json=payload)
    return r.json()["idToken"]

def get_auth_token(google_token, email, user_headers):
    payload = {
        "id_token" : google_token,
    }

    r = requests.post(signin_id_token, json=payload, headers=user_headers)
    if r.status_code != 200:
        logging.debug("Message from server : {}".format(r.text))
    return r.json()["token"]

def get_random_device():
    with open("./devices.json", "r") as f:
        devices = json.load(f)
    return devices[random.randint(0, len(devices))]

def send_email(email, user_headers):
    payload = {
        "email": email
        }
    headers = generate_headers(user_headers, payload)
    r = requests.post(signin_with_email_url, json=payload, headers=headers)
    print(r.text)
    return r.status_code

def get_code(link):
    code = link.split("custom_token=")[1].split("&new=1")[0]
    payload = {
        "token": code,
        "returnSecureToken": True
    }

    r = requests.post("https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyCustomToken?key=AIzaSyBpVnvwRMvz9lP9A2cVBKIIutli4ZuCmm4", json=payload)
    return r.json()["idToken"]