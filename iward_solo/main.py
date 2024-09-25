import os
import user
import utils
import logging

from fastapi import FastAPI, Cookie, HTTPException, Response, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel, EmailStr


app = FastAPI()   
PASSWORD = os.getenv("PASSWORD")

if not PASSWORD:
  logging.debug("PASSWORD not set")
  exit()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class cookie_password(BaseModel):
  password: str

class email(BaseModel):
  email: EmailStr

class link(BaseModel):
  link: str

@app.get("/debug") 
async def debug():
  return {"message": "This is a debug page, there is nothing to see"}

@app.get("/") 
async def main(request: Request, auth: str = Cookie(None)):
  if auth != PASSWORD:
   return templates.TemplateResponse("login.html", {"request": request})
  
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
  
  code = utils.get_code(item.link)
  u.set_token(code)

u = user.user()