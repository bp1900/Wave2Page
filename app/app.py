#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import subprocess
from flask import Flask, render_template, redirect, request, send_from_directory

DEVELOPMENT_ENV = True

app = Flask(__name__)

app_data = {
    "name": "Wave2Page",
    "description": "A simple song to music sheet conversor",
    "author": "Carvaca, Gerard and Rodriguez, Armando and Parellada, Benjami",
    "html_title": "Wave2Page",
    "project_name": "Wave2Page",
    "keywords": "wave, page, music",
}

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

PNG_FOLDER = '../static/'
app.config['PNG_FOLDER'] = PNG_FOLDER

@app.route("/")
def index():
    return render_template("index.html", app_data=app_data)

@app.route("/about")
def about():
    return render_template("about.html", app_data=app_data)

@app.route("/service")
def service():
    return render_template("service.html", app_data=app_data)

@app.route("/contact")
def contact():
    return render_template("contact.html", app_data=app_data)

# @app.route('/images/<filename>')
# def serve_image(filename):
#     return send_from_directory(app.config['PNG_FOLDER']+filename.split(".")[0], filename)

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if a file was submitted in the request
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    filename = file.filename

    # Check if the file has a valid extension (.wav in this case)
    if file and filename.endswith('.wav'):
        # Save the uploaded file to the upload folder
        path_to_audio = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path_to_audio)
        subprocess.call(['python', "src/main.py", path_to_audio, "--separate", "--wav2midi", "--midi2sheet"])
        
        # Create folder correctly
        
        path = app.config['PNG_FOLDER']
        png_files = [path+f for f in os.listdir(path) if f.endswith('.png')]
        # print(app.config['PNG_FOLDER']+filename.split(".")[0])
        # print(os.listdir(app.config['PNG_FOLDER']+filename.split(".")[0]))
        print(png_files)
        return render_template("index.html", filename=filename, app_data=app_data, png_files=png_files)
    else:
        return 'Invalid file format. Please upload a .wav file.'

if __name__ == "__main__":
    app.run(debug=DEVELOPMENT_ENV)
