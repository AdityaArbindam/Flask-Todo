from datetime import datetime
from pickle import TRUE
from turtle import title
from flask import Flask, redirect , render_template, request
from datetime import datetime               # this has been used inside the one of the columns in DB
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc    # importing SQLAlchemy to config with DB , it helps in communicating with DB using Python. 
import tkinter
app = Flask(__name__)                      

# Confi with the database  and giving name as Todo

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///Todo.db'      
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

# Storing the app in DB 
db=SQLAlchemy(app)


# making a class to define our table
class Todo(db.Model):
    Sno =db.Column(db.Integer, primary_key= True)
    title =db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    date_created =db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:                # returning this object to be printed into Todo list
        return f"{self.Sno}-{self.title}"     # creating f string
   

#Router point 1 

@app.route('/', methods=['GET','POST'])   
def hello_world():
    if request.method=="POST":
        title=request.form['title']
        desc=request.form['desc']
        todo = Todo( title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo=Todo.query.all()
    return render_template('index.html',allTodo=allTodo)


# end point to upadate entries

@app.route('/update/<int:Sno>',methods=['GET','POST']) # first we are taking SNo inside the update end point as integer, 
def update(Sno):                # then Applying filter Query on that Sno and then giving to update.html using render_template funtion 
    if request.method=="POST":
        title=request.form['title']
        desc=request.form['desc']
        todo = Todo.query.filter_by(Sno=Sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo=Todo.query.filter_by(Sno=Sno).first()
    return render_template('update.html',todo=todo)   

# end point to delete entries 

@app.route('/delete/<int:Sno>')   # the delete router will take int and its name is Sno
def delete(Sno):                  # now passing that serial no to delete function 
    todo=Todo.query.filter_by(Sno=Sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

# Router point 2

if __name__ =="__main__":
    app.run(debug=TRUE)    # Running app and in debug =true will show error if any 