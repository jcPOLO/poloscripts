import json
import os
from bcrypt import re
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, current_app
from flask_login import login_required, current_user
from . import db
from .models import Note
from werkzeug.utils import secure_filename
from core.models.bootstrap import Bootstrap
from core.models.device import Device


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

@views.route('/upload', methods=['POST', 'GET'])
@login_required
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part', category='error')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash("You haven't selected any file", category='warning')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            flash('File uploaded', category='success')
            return redirect(url_for('views.auto_nornir'))
        else:
            flash('File type must be csv or txt', category='error')
    return redirect(url_for('views.home'))

@views.route('/auto-nornir', methods=['POST', 'GET'])
@login_required
def auto_nornir():
    if request.method == 'GET':
        bootstrap = Bootstrap()
        bootstrap.load_inventory()
        devices = Device.get_devices()
        keys = Device.get_devices_data_keys()
        return render_template("filter.html", devices=devices, keys=keys)
