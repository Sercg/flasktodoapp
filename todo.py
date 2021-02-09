from flask import Flask,render_template,url_for,request, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Projects/05_ToDo/todo.db'
db = SQLAlchemy(app)
app.secret_key='ajsşldkhpgoaunuıjanhfopıdsakljfm'

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)

@app.route("/")
def index ():
    todos=Todo.query.all()
    return render_template("index.html",todos = todos)

@app.route("/add",methods=["POST"])
def addTodo():
    title=request.form.get("title")
    newTodo = Todo(title = title, complete = False)
    db.session.add(newTodo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/complete/<string:id>",methods=["GET","POST"])
def complete(id):
    todo=Todo.query.filter_by(id=id).first()
    if todo.complete:
        Todo.query.filter_by(id=id).update(dict(complete=False))
    else:
        Todo.query.filter_by(id=id).update(dict(complete=True))
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/remove/<string:id>",methods=["GET","POST"])
def remove(id):
    todo=Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)