#!/usr/bin/env python3
"""
main script running the flask application
imports limits class to change the user uploaded limits and methods
imports main script with FastQC and ReadingDataTextFile classes to execute the tool and read the
created data to plot those using the plotting classes
use: python .\website\app.py  > click on the link ( http://127.0.0.1:5000/ )
"""

__author__ = "Maartje van der Hulst"
__date__ = 2025.3
__version__ = 1.3

import base64

import os
from datetime import date
from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

from scrips.limits import Limits
from scrips.main import FastQC, ReadingDataTextFile

#GLOBALS
today = date.today().strftime('%a %d %B %Y')

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "./uploads"
app.config["ALLOWED_EXTENSIONS"] = [".fastq", ".SAM"]
app.config["MAX_CONTENT_LENGTH"] = 300 * 1024 * 1024 #300 MB

@app.route('/')
def index():
    """makes home page by rendering base & index files"""
    return render_template('index.html')

@app.route('/project')
def project():
    """makes project page by rendering base & project info files"""
    return render_template("project_info.html")

@app.route('/tool_page')
def tool_page():
    """makes tool page by rendering base & tool files"""
    return render_template("tool_page.html")

@app.route('/references')
def references():
    """makes references page by rendering base & references files"""
    return render_template("references_page.html")

@app.route('/fastqc', methods=['GET', 'POST'])
def fastqc():
    """makes fastqc tool page by rendering base & fastqc files
    if user uses the submit button the post method is used
    which renders the base en results files"""
    if request.method == 'GET':
        return render_template('fastqc_page.html')

    elif request.method == 'POST':

        try:
            # getting file from html form
            file = request.files['myfile2']
            file_name = os.path.splitext(file.filename)[0]
            extention = os.path.splitext(file.filename)[1]
            # checking if file has the correct file extention for the tool
            if extention not in app.config['ALLOWED_EXTENSIONS']:
                return f"file type not allowed, please use a {app.config['ALLOWED_EXTENSIONS']}"
            if file: #checking if file is uploaded and saving it to the upload folder
                file.save(os.path.join(
                    app.config['UPLOAD_FOLDER'],
                    secure_filename(file.filename),
                ))
        # error handling when file exceeds allowed size
        except RequestEntityTooLarge:
            return 'File too large, try smaller file'
        # making dict with which module should be switched on and which corresponding limits
        # should be used
        settings = {
            'duplication' : request.form.getlist('duplication'),
            'kmer' : request.form.getlist('kmer'),
            'n_content' : request.form.getlist('n_content'),
            'overrepresented' : request.form.getlist('overrepresented'),
            'quality_base' : request.form.getlist('quality_base'),
            'sequence' : request.form.getlist('sequence'),
            'gc_sequence' : request.form.getlist('gc_sequence'),
            'quality_sequence' : request.form.getlist('quality_sequence'),
            'tile' : request.form.getlist('tile'),
            'sequence_length' : request.form.getlist('sequence_length'),
            'adapter' : request.form.getlist('adapter'),
            'file': file.filename
        }
        #changing limits.txt file of the tool using user entered settings
        limits = Limits(settings, "Tools/fastqc_v0.12.1/FastQC/Configuration/limits.txt")
        print(limits)
        # executing fastqc tool via FastQC class
        FastQC(file.filename)

        # plotting output by using ReadingDataTextFile and plotting classes
        # output = ReadingDataTextFile("static/fastqc_data_lang.txt")
        output = ReadingDataTextFile(f"{file_name}_fastqc/fastqc_data.txt")
        results = { 'basic_table': output.table,
                    'encoding': output.dataframe.loc[2]['Value'],
                    'today': today,
                    'filename': file.filename,
                    'icons': output.icons,
                    'overrepresented': output.overrepresented,
                    'kmer': output.kmer,
        }
        return render_template('fastqc_page_results.html', **results)

@app.route("/uploads/<path:filename>", methods=['GET'])
def access_file(filename):
    """uploading file?!"""
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)




# giving help pages from fastqc a route so they can be hosted inside the fastqc page using iframes
@app.route('/duplicate')
def duplicate():
    """makes the duplicate help page by rendering the duplicate file"""
    return render_template('fastqc_help/8_Duplicate_Sequences.html')

@app.route('/kmer')
def kmer():
    """makes the kmer help page by rendering the kmer file"""
    return render_template('fastqc_help/11_Kmer_Content.html')

@app.route('/ncontent')
def ncontent():
    """makes the n content help page by rendering the n content file"""
    return render_template('fastqc_help/6_Per_Base_N_Content.html')

@app.route('/overrepresented')
def overrepresented():
    """makes the overrepresented help page by rendering the overrepresented file"""
    return render_template('fastqc_help/9OverrepresentedSequences.html')

@app.route('/quality_base')
def quality_base():
    """makes the base quality help page by rendering the base quality file"""
    return render_template('fastqc_help/2_Per_Base_Sequence_Quality.html')

@app.route('/sequence')
def sequence():
    """makes the sequences help page by rendering the sequence file"""
    return render_template('fastqc_help/4_Per_Base_Sequence_Content.html')

@app.route('/gc_sequence')
def gc_sequence():
    """makes the gc content help page by rendering the gc content file"""
    return render_template('fastqc_help/5PerSequenceGCContent.html')

@app.route('/quality_sequence')
def quality_sequence():
    """makes the sequence quality help page by rendering the sequence quality file"""
    return render_template('fastqc_help/3_Per_Sequence_Quality_Scores.html')

@app.route('/tile')
def tile():
    """makes the tile help page by rendering the tile file"""
    return render_template('fastqc_help/12PerTileSequenceQuality.html')

@app.route('/sequence_length')
def sequence_length():
    """makes the sequence length help page by rendering sequence length file"""
    return render_template('fastqc_help/7SequenceLengthDistribution.html')

@app.route('/adapter')
def adapter():
    """makes the adapter page by rendering adapter file"""
    return render_template('fastqc_help/10AdapterContent.html')


if __name__ == '__main__':
    app.run(debug=True)
