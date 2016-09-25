from flask import Flask
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from werkzeug.utils import secure_filename

#import tesserocr
#from PIL import Image
#from tesserocr import PyTessBaseAPI

ALLOWED_IMAGE_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
ALLOWED_PDF_EXTENSIONS = set(['pdf'])

PDF_UPLOAD_DICTIONARY = 'uploads/'


import requests
import os
import uuid

app = Flask(__name__)
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = PDF_UPLOAD_DICTIONARY

@app.route('/')
def rendering_main_page():
    return render_template("index.html")


@app.route('/link')
def input_link_form():
    return render_template("input_link.html")


@app.route('/text')
def input_text_form():
    return render_template("input_text.html")


@app.route('/pdf')
def input_pdf_form():
    return render_template("input_pdf.html")


@app.route('/img')
def input_img_form():
    return render_template("input_img.html")


@app.route('/rawtext', methods=['POST'])
def rawtext():
    agreement = request.form['text']

    check_result = check_agreement(agreement.split("\n"))

    return check_result

@app.route('/agreementurl', methods=['POST'])
def agreementurl():

    url = "http://boilerpipe-web.appspot.com/extract?url=" + request.form['agreement_url'] + "&extractor=ArticleExtractor&output=text&extractImages=&token="

    print(url)
    r = requests.get(url)

    if r.status_code == 200:
        agreement = r.text
        check_result = check_agreement(agreement.split("\n"))
        print(agreement.split("\n")[:10])
        return check_result
    else:
        return "Check your url"

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'photo' not in request.files:
        print('No file part')
        return redirect(request.url)
    file = request.files['photo']
    if file.filename == '':
        print('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename, ALLOWED_IMAGE_EXTENSIONS):
#        with PyTessBaseAPI(lang='pol') as api:
#            image = Image.open(file)
#            api.SetImage(image)
#            check_result = check_agreement(str(api.GetUTF8Text().replace("\n", " ").split(".")) )
            return "OK"  # check_result

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'pdf' not in request.files:
        print('No file part')
        return redirect(request.url)
    file = request.files['pdf']
    if file.filename == '':
        print('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename, ALLOWED_PDF_EXTENSIONS):
        filename = str(uuid.uuid4()) + ".pdf"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        os.system("pdftotext uploads/" + filename + " uploads/" + filename + ".txt -nopgbrk")
        with open("uploads/" + filename + ".txt") as file:
            check_result = check_agreement(str("".join(file.readlines()).replace("\n", " ").split(".")))
            return check_result

@app.route('/result')
def result_page():
    return render_template("result_page.html")


def allowed_file(filename, extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in extensions

def check_agreement(agreement):
    return "OK!"

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run()
