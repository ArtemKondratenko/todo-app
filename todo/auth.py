from . import repository
from flask import Blueprint, redirect, render_template, request, session

auth = Blueprint('auth', __name__)

@auth.get('/')
def get_auth():
  return render_template('auth.html')

@auth.post("/register")
def register():
  username = request.form["username"]
  password = request.form["password"]
  if not repository.user_exists(username):
     repository.add_user(username, password)
     return 'register successfully'
  return 'user already registered'

@auth.post("/login")
def login():
  username = request.form["username"]
  password = request.form["password"]

  user = repository.get_user(username)
  # print('ВНИМАНИЕ!!!')
  # print(user)
  # print(user.hashed_password)
  # print(repository.hash_password(password))
  if user and user.hashed_password == repository.hash_password(password):
      session['logged_in'] = True
      session['username'] = username
      session['user_id'] = user.id
      return redirect("/")
  return "login failed"
