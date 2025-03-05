from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template(template_name_or_list="index.html")

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





@app.route('/references')
def references():
    return render_template("references_page.html")


if __name__ == '__main__':
    app.run(debug=True)