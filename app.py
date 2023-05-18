from flask import Flask, render_template, request, redirect, flash, url_for
import datetime
from werkzeug.utils import secure_filename
import os
from difflib import SequenceMatcher


app = Flask(__name__)
app.secret_key = "secret key"

ALLOWED_EXTENSIONS = {'pdf', 'cpp'}
list_data_read = []


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method != 'POST':
        return render_template("index.html")

    listoffiles = []
    filenames = []
    match = 0

    files = request.files.getlist('files')
    if len(files) > 2 or len(files) < 2:
        flash("Please Provide 2 file")
        return redirect('/')

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(filename)
            filenames.append(filename)
            file.save(os.path.join("media/files", filename))
            listoffiles.append(os.path.join("media/files", filename))
        else:
            print("got Some Error")
            flash("Allow Cpp files Only")
            return redirect('/')

    flash("File Recived ")

    with open(os.path.join(os.getcwd(), listoffiles[0])) as f1, open(os.path.join(os.getcwd(), listoffiles[1])) as f2:
        file_one_data = f1.read()
        file_two_data = f2.read()
        list_data_read.append(str(file_one_data))
        list_data_read.append(str(file_two_data))

        match = SequenceMatcher(None, file_one_data, file_two_data)
        # convert above output into ratio
        # and multiplying it with 100
        result = match.ratio() * 100

        # Display the final result
        match = int(result)
        print(int(result), "%")

    return redirect(url_for('checker', match=match, file_one=filenames[0], file_two=filenames[1]))


@app.route("/checker/<match>/<file_one>/<file_two>")
def checker(match, file_one, file_two):
    for i in range(len(list_data_read)):
        print(list_data_read[i])

    return render_template("checker.html", match=match, file_one=file_one, file_two=file_two, file_one_data=list_data_read[0], file_two_data=list_data_read[1], hadder="File Checking")


if __name__ == "__main__":
    app.debug = True
