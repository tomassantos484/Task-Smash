# Task Smasher - A Simple To-Do List App in Python Flask, HTML/CSS, SASS, and SQLAlchemy

# Imports
from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# My App - CRUD Application (Create, Read, Update, Delete)
app = Flask(__name__)
Scss(app)

# App Configurations
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Data Class - Row of Data
class myTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self) -> str:
        return f'<Task {self.id}>'

# Context Manager
with app.app_context():
        db.create_all()

# Main Page of App, Creating a Route to Webpages
#Home Page
@app.route('/', methods=['POST', 'GET'])
def index():
    # Add a Task
    if request.method == "POST":
        current_task = request.form['content']
        new_task = myTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        
        except Exception as e:
            print("ERROR: {e}")
            return f"ERROR: {e}"

    #See all Current Tasks
    else:
        tasks = myTask.query.order_by(myTask.created).all()
        return render_template('index.html', tasks=tasks)

#Delete Task
@app.route('/delete/<int:id>')
def delete(id):
    delete_task = myTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect('/')
    
    except Exception as e:
        print("ERROR: {e}")
        return f"ERROR: {e}"

# Edit or Update Task
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id: int):
    task = myTask.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        
        except Exception as e:
            print("ERROR: {e}")
            return f"ERROR: {e}"
    else:
        return render_template('edit.html', task=task)


# Run the App
if __name__ == '__main__':
    app.run(debug=True)