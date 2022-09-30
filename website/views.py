from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
import psycopg2
import requests


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

    if request.method == 'POST':
        note = request.form.get('note')
        recipe = requests.get(
            'https://www.themealdb.com/api/json/v1/1/random.php')
        if len(note) < 1:
            flash('Note is too short!', category= 'error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash ('Note Added', category= 'success')
    return render_template('home.html', user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})

@views.route('/connect', methods=['POST', 'GET'])
def connect_to_db():
    conn = psycopg2.connect(host='localhost', port=8080, dbname='Galaxy_Dev', passwd='Raelyn')
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS note (noteId INTEGER PRIMARY KEY AUTOINCREMENT, noteId  VARCHAR(255) NOT NULL)')
    cur.execute("""
    INSERT INTO note VALUES
    (1, 'hELLO PEOPLE', 1434),
    (2, 'SUP', 2929),
    (3, 'HOW ARE YOU', 29210)
    """)