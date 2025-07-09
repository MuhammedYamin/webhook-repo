from app import create_app
from flask import Flask, render_template
import os

template_dir = os.path.abspath("templates")
app = create_app(template_folder=template_dir)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)