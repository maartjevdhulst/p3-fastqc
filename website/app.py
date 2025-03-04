
from flask import Flask, render_template, request

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

@app.route('/fastqc')
def fastqc():
    return render_template("fastqc_page.html")

@app.route('/references')
def references():
    return render_template("references_page.html")


if __name__ == '__main__':
    app.run(debug=True)