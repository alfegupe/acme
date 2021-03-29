import os

from flask import request, render_template, redirect, url_for, render_template_string

from controllers.process import ProcessController
from utils.utils import allowed_file
from acme import create_app

app = create_app()


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['json_file']
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(
                url_for(
                    'process_file',
                    filename=filename
                )
            )

    return redirect('/')


@app.route('/process')
def process_file():
    filename = request.args.get('filename')
    print("Processing: {}".format(filename))

    json_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    process_result_log = ProcessController().read_file_and_process(json_url)
    return render_template_string(process_result_log.replace('\n', '<br>'))


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
