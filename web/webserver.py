from flask import Flask
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def input_form():
    return render_template("index.html")

# @app.route('/', methods=['POST'])
# def my_form_post():
#     text = request.form['text']
#     processed_text = text.upper()
#     return processed_text

if __name__ == "__main__":
    app.run()
