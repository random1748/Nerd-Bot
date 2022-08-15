from flask import Flask, render_template, url_for, send_from_directory
import os
app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'fav.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/info")
def info():
    return render_template("info.html")
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)