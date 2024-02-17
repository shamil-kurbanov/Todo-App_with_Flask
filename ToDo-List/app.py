from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Create Flask application instance
app = Flask(__name__)
# Configure SQLAlchemy to use SQLite database located at db.sqlite file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app) # Create SQLAlchemy database instance

# Define Todo model representing the 'todos' table in the database
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)


# Define route for the home page
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':            # If form is submitted
        title = request.form.get('title')   # Get the title of the new todo task from the form
        new_todo = Todo(title=title)        # Create a new Todo object with the provided title
        db.session.add(new_todo)            # Add the new todo task to the database session
        db.session.commit()                 # Commit the changes to the database
        return redirect(url_for('home'))    # Redirect to the home page to refresh the todo list
    else:  # If the request is a GET request
        todo_list = Todo.query.all()    # Query all todo tasks from the database
        # Render the base.html template with the todo_list passed as context
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
        # 
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
