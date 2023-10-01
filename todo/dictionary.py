from . import repository
from flask import Blueprint, redirect, render_template, request, session

dictionary = Blueprint('dictionary', __name__)


@dictionary.get('/task')
def get_tasks():
  if not session.get('logged_in'):
    return redirect('/auth/')
  tasks = repository.get_all_task(session['user_id'])
  return render_template("task.html", tasks=tasks)

# https://html.form.guide/checkbox/html-checkbox-form-submit-value/

@dictionary.post("/task")
def create_task():
  if not session.get('logged_in'):
    return redirect('/auth/')
  task = request.form["task"]
  description = request.form["description"]
  user_id = session['user_id']
  done = bool(request.form.get("completed"))
  repository.add_task(task, description, user_id, done)
  return redirect("/dictionary/task")
