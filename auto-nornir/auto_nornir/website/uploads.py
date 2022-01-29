from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = {'txt', 'csv'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


