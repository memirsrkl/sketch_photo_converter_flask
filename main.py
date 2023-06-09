from flask import Flask, render_template, request, redirect,send_from_directory
from werkzeug.utils import secure_filename
import os
import uuid
import subprocess
import modules
from adsc import yeni,stop_python_file
from adpc import yenis
from flask_assets import Environment, Bundle

app = Flask(__name__)
assets = Environment(app)

# SCSS dosyasını CSS dosyasına dönüştürme ve Bundle tanımlama
css_bundle = Bundle(
    'scss/main.scss',
    filters='scss',
    output='css/main.css'
)
assets.register('css_bundle', css_bundle)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['CONVERT'] = 'static/converting'
app.config['SKETCH']='static/sketch'
app.config['CONVERT_SKETCH']='static/convertings'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif'}
converted_file=''
reque=''
sketch_file = ''
@app.route('/', methods=['POST'])
def upload_file():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    for file in files:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))
    files = os.listdir(app.config['SKETCH'])
    for file in files:
        os.remove(os.path.join(app.config['SKETCH'], file))
    with open('findpro.txt', 'w') as file:
        file.write('')
    with open('findpros.txt', 'w') as file:
        file.write('')
    file1 = request.files.get('file1')
    file2 = request.files.get('file2')
    global sketch_file
    sketch_file = ''
    global converted_file
    converted_file = ''
    if file2:
        file2 = request.files['file2']
        if file2.filename == '':
            return redirect(request.url)
        if allowed_file(file2.filename):
            filename = str(uuid.uuid1()) + os.path.splitext(file2.filename)[1]

            file2.save(os.path.join(app.config['SKETCH'], filename))
            with open('findpros.txt', 'a') as f:
                f.write(filename + '\n')
            return redirect('/')
    if file1:
        file = request.files['file1']
        if file.filename == '':
            return redirect(request.url)
        if allowed_file(file.filename):
            filename = str(uuid.uuid1()) + os.path.splitext(file.filename)[1]
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            with open('findpro.txt', 'a') as f:
                f.write(filename + '\n')
            return redirect('/')



    else:
        return redirect(request.url)

@app.route('/delete/<filename>')
def delete_file(filename):
    yeni()
    den(filename)
    with open('findpro.txt', 'r') as f:
        lines = f.readlines()
    with open('findpro.txt', 'w') as f:
        for line in lines:
            if line.strip('\n') != filename:
                f.write(line)
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect('/')
@app.route('/deletes/<filename>')
def delete_files(filename):
    yenis()
    dene(filename)
    with open('findpro.txt', 'r') as f:
        lines = f.readlines()
    with open('findpro.txt', 'w') as f:
        for line in lines:
            if line.strip('\n') != filename:
                f.write(line)
    os.remove(os.path.join(app.config['SKETCH'], filename))
    return redirect('/')
def den(filename):
    global converted_file
    global reque
    reque=filename
    converted_file=filename[0:16]+'.jpg'
def dene(filename):
    global sketch_file
    sketch_file=filename[0:16]+'.jpg'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    filenames = os.listdir(app.config['UPLOAD_FOLDER'])
    sketch=os.listdir(app.config['SKETCH'])
    return render_template('index.html', filenames=filenames,sketch=sketch ,converted_file=converted_file,sketch_file=sketch_file,reque=reque)

if __name__ == '__main__':
    from flask_assets import ManageAssets

    manager = ManageAssets(app)
    manager.run()
    app.run(debug=True)
