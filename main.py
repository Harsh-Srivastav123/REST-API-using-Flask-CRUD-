from datetime import datetime

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///employ.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Note(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno}-{self.title}"


with app.app_context():
    db.create_all()


# index of http request
@app.route('/', methods=['GET', 'POST'])
def Home():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        note = Note(title=title, description=description)
        db.session.add(note)
        db.session.commit()
        allNote = Note.query.all()
        return render_template("index.html", allNote=allNote)
    allNote = Note.query.all()
    return render_template("index.html", allNote=allNote)


# querry in a String
@app.route('/qs')
def Get_qs():
    if request.args:
        req = request.args
        return " ".join(f"{k}:{v}" for k, v in req.items())
    return "No querry"


# delete operation
@app.route('/delete/<int:sno>')
def Delete(sno):
    note = Note.query.filter_by(sno=sno).first()
    db.session.delete(note)
    db.session.commit()
    allNote = Note.query.all()
    return render_template("index.html", allNote=allNote)


# update operation
@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def Update(sno):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        note = Note.query.filter_by(sno=sno).first()
        note.title = title
        note.description = description
        db.session.add(note)
        db.session.commit()
        return redirect("/")
    note = Note.query.filter_by(sno=sno).first()
    return render_template("update.html", note=note)


if __name__ == '__main__':
    app.run(debug=True)
