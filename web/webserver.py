from flask import Flask
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from werkzeug.utils import secure_filename
from libshorttext.classifier import *
from gensim import corpora, models, similarities
from collections import defaultdict

#import tesserocr
#from PIL import Image
#from tesserocr import PyTessBaseAPI

ALLOWED_IMAGE_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
ALLOWED_PDF_EXTENSIONS = set(['pdf'])

PDF_UPLOAD_DICTIONARY = 'uploads/'


import requests
import os
import uuid
import re
import csv

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

    return render_template("result_page.html", result=check_result)

@app.route('/agreementurl', methods=['POST'])
def agreementurl():

    url = "http://boilerpipe-web.appspot.com/extract?url=" + request.form['agreement_url'] + "&extractor=ArticleExtractor&output=text&extractImages=&token="

    r = requests.get(url)

    if r.status_code == 200:
        agreement = r.text
        check_result = check_agreement(agreement.split("\n"))
        return render_template("result_page.html", result=check_result)
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
        with PyTessBaseAPI(lang='pol') as api:
            image = Image.open(file)
            api.SetImage(image)
            check_result = check_agreement(str(api.GetUTF8Text().replace("\n", " ").split(".")) )
            return render_template("result_page.html", result=check_result)

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
            return render_template("result_page.html", result=check_result)

@app.route('/result')
def result_page():
    return render_template("result_page.html")


def allowed_file(filename, extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in extensions

def check_agreement(agreement):
    regex_clauses = set()
    similar_clauses = []
    zuza_clauses = []
    knf = []

    main_predictor = Predictor("train_set.txt.model")
    zuza_predictor = Predictor("zuza_train_set.txt.model")
    for line in agreement:
        print(line + ":  "+str(len(line.rstrip())))
        if len(line.rstrip()) > 10:
            knf_result = knf_match(line)
            if knf_result != None:
                knf.append( (line, knf_result[0], knf_result[1]) )

            regex_result = regex_match(line)
            if regex_result != None:
                regex_clauses.add( (line, regex_result[0], regex_result[1]) )

            label = main_predictor.predict(line)
            if label == 'incorrect':
                similar_clauses.append( (line, sentences_similarities.find_similar(line)) )

            zuza_label = zuza_predictor.predict(line)
            print("zuza_label" + zuza_label)
            if zuza_label != 'correct':
                zuza_clauses.append( (line, zuza_label) )

    result = Result(regex_clauses, similar_clauses, zuza_clauses, knf)

    return result

def regex_match(textline):
    with open('data/new_100.csv') as csvfile:
        regexdata = csv.reader(csvfile, strict=True)
        for i in regexdata:
            if re.match(".*"+i[3][1:-1]+".*", textline) is not None:
                return (i[0], i[2])
        return None

def knf_match(textline):
    with open('data/daneknf.csv') as csvfile:
        knf_data = csv.reader(csvfile, strict=True)
        for data in knf_data:
            name = data[0]
            id_number = data[1] 
            if name.rstrip() in textline or (len(id_number.rstrip()) > 0 and id_number.rstrip() in textline):
                return (name, id_number)
        return None

class Result:
    def __init__(self, regex_clauses, similar_clauses, zuza_clauses, knf_data):
        self.regex_clauses = regex_clauses
        self.similar_clauses = similar_clauses
        self.zuza_clauses = zuza_clauses
        self.knf_data = knf_data

    def status(self):
        if len(self.regex_clauses) == 0 and len(self.similar_clauses) == 0 and len(self.zuza_clauses) == 0 and len(self.knf_data) == 0:
            return "OK"
        else:
            return "FORBIDDEN"

    def __str__(self):
        return self.status()

class Predictor(object):
    def __init__(self, model_name):
        self.model_name = model_name
        self.text_model = TextModel()
        self.text_model.load(self.model_name)

    def predict(self, text):
        return predict_single_text(text, self.text_model).predicted_y

class Similarities(object):

    def __init__(self):
        with open("data/documents.txt") as klauzule:
            with open("data/stopwords.txt") as stopwords:
                self.documents = list(filter(lambda line: len(line) > 0,set(map(lambda line: line.rstrip(), klauzule.readlines()))))

                stoplist = set(map(lambda line: line.rstrip(), stopwords.readlines()))
                texts = [[word for word in document.lower().split() if word not in stoplist] for document in self.documents]

                frequency = defaultdict(int)
                for text in texts:
                    for token in text:
                        frequency[token] += 1

                texts = [[token for token in text if frequency[token] > 1] for text in texts]

                self.dictionary = corpora.Dictionary(texts)

                corpus = [self.dictionary.doc2bow(text) for text in texts]

                self.lsi = models.LsiModel(corpus, id2word=self.dictionary)
                self.index = similarities.MatrixSimilarity(self.lsi[corpus])

    def find_similar(self, text):
        vec_bow = self.dictionary.doc2bow(text.lower().split())
        vec_lsi = self.lsi[vec_bow]

        sims = self.index[vec_lsi]

#        print(text.lower().split())
#        print(vec_bow)
#        print(sorted(enumerate(sims), key=lambda item: -item[1])[:5])
        sims = list(map(lambda pair: self.documents[pair[0]] , sorted(enumerate(sims), key=lambda item: -item[1]) ))

        return sims[:5]


sentences_similarities = Similarities()

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run()
