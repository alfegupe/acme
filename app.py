import os

from acme import create_app
from flask import Flask, request, render_template, redirect, url_for, render_template_string

from controllers.process import ProcessController
from utils import allowed_file

# mongo = PyMongo()
# app = Flask(__name__)
# app.config["MONGO_URI"] = MONGO_URI
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# mongo.init_app(app)
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
    print(process_result_log or "")
    return render_template_string(process_result_log.replace('\n', '<br>'))


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
