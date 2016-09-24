from flask import Flask
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)


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
# @app.route('/', methods=['POST'])
# def my_form_post():
#     text = request.form['text']
#     processed_text = text.upper()
#     return processed_text

if __name__ == "__main__":
    app.run()
