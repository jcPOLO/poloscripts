from bcrypt import re
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, current_app
from flask_login import login_required, current_user
from . import db
from .models import Note
from werkzeug.utils import secure_filename
import json
import os


views = Blueprint('views', __name__)


ALLOWED_EXTENSIONS = {'txt', 'csv'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        note_exists = Note.query.filter_by(data=note, user_id=current_user.id).first() 
        if note_exists:
            flash('Note already exists!', category='error')
        else:
            if len(note) < 1:
                flash('Note does not have enougth text', category='error')
            else:
                new_note = Note(
                    data=note, 
                    user_id=current_user.id
                )
                db.session.add(new_note)
                db.session.commit()
                flash('Note created!', category='success')
                return redirect(url_for('views.home'))

    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    data = json.loads(request.data) # add data in a python dict
    note_id = data['noteId']
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})

@views.route('/upload', methods=['POST'])
@login_required
def upload_file():
    print(os.path.join(current_app.config['UPLOAD_FOLDER']))
    print('si entra12312312')
    if request.method == 'POST':
        print('si entra123123123')
        # check if the post request has the file part
        if 'file' not in request.files:
            print('si entra0')
            flash('No file part', category='warning')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            print('si entra2')
            flash('No selected file', category='info')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print('si entra3')
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            flash('File uploaded', category='success')
            return redirect(url_for('views.home'))
        print('nada')
    return redirect(url_for('views.home'))