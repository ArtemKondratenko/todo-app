from flask import Flask, redirect, render_template, session

from .auth import auth
from .db import create_tables
from .dictionary import dictionary

create_tables()


app = Flask(__name__)
app.secret_key = b'Jh323G8s!jLKz'
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(dictionary, url_prefix="/dictionary")

@app.get("/")
def main():
  if not session.get('logged_in'):
      return redirect('/auth/')
  return redirect('/dictionary/task')

@app.get("/task/create_task")
def get_task_html():
  return render_template('create_task.html')


app.run(host='0.0.0.0', port=81)