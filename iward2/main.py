import os
import user
import utils
import logging

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, Cookie, HTTPException, Request
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

app = FastAPI()   
PASSWORD = os.getenv("PASSWORD")

if not PASSWORD:
  logging.error("PASSWORD not set")
  exit()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class cookie_password(BaseModel):
  password: str

class email(BaseModel):
  email: EmailStr

class link(BaseModel):
  link: str

class step_number(BaseModel):
  step_number: int

@app.get("/debug") 
async def debug():
  return {"message": "This is a debug page, there is nothing to see"}

@app.get("/") 
async def main(request: Request, auth: str = Cookie(None)):
  if auth != PASSWORD:
   return templates.TemplateResponse("login.html", {"request": request})
  
  if u.connected():
    u.update_profile()
    return templates.TemplateResponse("profile.html", {"request": request, "user_info": u.get_user_info(), "db_info": u.get_db_info()})
  
  return templates.TemplateResponse("index.html", {"request": request, "user_info": u.get_user_info(), "db_info": u.get_db_info()})

@app.post("/login") 
async def login(item: cookie_password):
  response = RedirectResponse(url="/", status_code=303)
  response.set_cookie(key="auth", value=item.password, httponly=True)
  return response

@app.post("/send_email")
async def send_mail(item: email, request: Request, auth: str = Cookie(None)):
  if auth != PASSWORD:
    return HTTPException(404, detail="Not found")
  
  u.set_mail(item.email)
  u.generate()
  utils.send_email(u.email, u.user_headers)

@app.post("/get_code")
async def get_code(item: link, request: Request, auth: str = Cookie(None)):
  if auth != PASSWORD:
    return HTTPException(404, detail="Not found")
  
  code = utils.get_code(item.link, u.user_headers)
  u.set_token(code)

@app.post("/disconnect")
async def get_code(request: Request, auth: str = Cookie(None)):
  if auth != PASSWORD:
    return HTTPException(404, detail="Not found")
  
  u.disconnect()
  return RedirectResponse(url="/", status_code=303)

@app.post("/validate_steps")
async def get_code(item: step_number, request: Request, auth: str = Cookie(None)):
  if auth != PASSWORD:
    return HTTPException(404, detail="Not found")
  
  u.validate_steps(item.step_number)
  u.update_profile()
  return RedirectResponse(url="/", status_code=303)

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse("./static/icon.ico")

u = user.user()

def reset_new_day():
  logging.info("Reseting timer")
  u.reset_new_day()

def check_validation():
  logging.info("Checking validation")
  u.check_validation()

scheduler = BackgroundScheduler()
scheduler.add_job(reset_new_day, 'cron', hour=0, minute=0)
scheduler.add_job(check_validation, 'interval', minutes=2)
scheduler.start()
