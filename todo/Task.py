from . import repository
from flask import Blueprint, redirect, render_template, request, session

working_task = Blueprint('working_task', __name__)


@working_task.get('/task')
def get_tasks():
  if not session.get('logged_in'):
    return redirect('/auth/')
  tasks = repository.get_all_task(session['user_id'])
  return render_template("task.html", tasks=tasks)

# https://html.form.guide/checkbox/html-checkbox-form-submit-value/


@working_task.post("/task")
def create_task():
  if not session.get('logged_in'):
    return redirect('/auth/')
  task = request.form["task"]
  description = request.form["description"]
  user_id = session['user_id']
  done = bool(request.form.get("completed"))
  repository.add_task(task, description, user_id, done)
  return redirect("/working_task/task")


@working_task.post("/done-task/<int:id>")
def done_task(id: int):
  if not session.get('logged_in'):
    return redirect('/auth/')
  repository.mark_task_done(id)
  return redirect("/working_task/task")


@working_task.post("/delete-task/<int:id>")
def delet_task(id: int):
  if not session.get('logged_in'):
    return redirect('/auth/')
  repository.delet_task(id)
  return redirect("/working_task/task")