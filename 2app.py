from flask import Flask, render_template,request, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
import webbrowser as wb
from threading import Timer

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(15))
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

@app.route('/')
def inicio():
    user_ip = request.remote_addr
    response = make_response(redirect('/holis'))
    response.set_cookie('user_ip', user_ip)
    return response


@app.route('/holis')
def index():
    todo_list = Todo.query.all()
    return render_template('prueba.html', todo_list=todo_list, user_ip=request.remote_addr)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get("title")
    new_todo = Todo(user_id = request.remote_addr, title=title, complete = False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:todo_id>')
def update(todo_id):
    todo = Todo.query.filter_by(user_id = request.remote_addr, id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

def open_browser():
    wb.open('http://127.0.0.1:5000')

if __name__ == '__main__':
    db.create_all()
    Timer(1, open_browser).start()
    app.run(debug=True, host='0.0.0.0')
    

