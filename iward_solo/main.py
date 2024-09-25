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

@app.get("/debug") 
async def debug():
  return {"message": "This is a debug page, there is nothing to see"}

@app.get("/") 
async def main(request: Request, auth: str = Cookie(None)):
  if auth != PASSWORD:
   return templates.TemplateResponse("login.html", {"request": request})
  
  return templates.TemplateResponse("index.html", {"request": request})

@app.post("/login") 
async def login(item: cookie_password):
  response = RedirectResponse(url="/", status_code=303)
  response.set_cookie(key="auth", value=item.password, httponly=True)
  return response

@app.post("/send_email")
async def send_mail(item: email, request: Request, auth: str = Cookie(None)):
  if auth != PASSWORD:
    return HTTPException(404, detail="Not found")
  
  u = user.user(item.email)
  utils.send_email(u.email, u.user_headers)
