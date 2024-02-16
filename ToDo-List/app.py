from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        title = request.form.get('title')
        new_todo = Todo(title=title)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        todo_list = Todo.query.all()
        return render_template('base.html', todo_list=todo_list)


@app.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    todo_to_edit = Todo.query.get(id)
    new_title = request.form.get('new_title')
    todo_to_edit.title = new_title
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete(id):
    if request.method == 'POST':
        todo_to_delete = Todo.query.get(id)
        db.session.delete(todo_to_delete)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        # Handle other HTTP methods gracefully
        return redirect(url_for('home'))

@app.route('/toggle_complete/<int:id>', methods=['POST'])
def toggle_complete(id):
    todo_to_toggle = Todo.query.get(id)
    todo_to_toggle.completed = not todo_to_toggle.completed
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
