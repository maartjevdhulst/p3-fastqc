from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/project')
def project():
    return render_template("project_info.html")

@app.route('/tool_page')
def tool_page():
    return render_template("tool_page.html")

@app.route('/fastqc', methods=['GET', 'POST'])
def fastqc():
    if request.method == 'GET':
        return render_template('fastqc_page.html')

    elif request.method == 'POST':
        kwargs = {
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
            'adapter' : request.form.getlist('adapter')
        }
        return render_template('fastqc_page_results.html', **kwargs)

@app.route('/duplicate')
def duplicate():
    return render_template('fastqc_help/8_Duplicate_Sequences.html')

@app.route('/kmer')
def kmer():
    return render_template('fastqc_help/11_Kmer_Content.html')

@app.route('/ncontent')
def ncontent():
    return render_template('fastqc_help/6_Per_Base_N_Content.html')

@app.route('/overrepresented')
def overrepresented():
    return render_template('fastqc_help/9OverrepresentedSequences.html')

@app.route('/quality_base')
def quality_base():
    return render_template('fastqc_help/2_Per_Base_Sequence_Quality.html')

@app.route('/sequence')
def sequence():
    return render_template('fastqc_help/4_Per_Base_Sequence_Content.html')

@app.route('/gc_sequence')
def gc_sequence():
    return render_template('fastqc_help/5PerSequenceGCContent.html')

@app.route('/quality_sequence')
def quality_sequence():
    return render_template('fastqc_help/3_Per_Sequence_Quality_Scores.html')

@app.route('/tile')
def tile():
    return render_template('fastqc_help/12PerTileSequenceQuality.html')

@app.route('/sequence_length')
def sequence_length():
    return render_template('fastqc_help/7SequenceLengthDistribution.html')

@app.route('/adapter')
def adapter():
    return render_template('fastqc_help/10AdapterContent.html')



@app.route('/references')
def references():
    return render_template("references_page.html")


if __name__ == '__main__':
    app.run(debug=True)