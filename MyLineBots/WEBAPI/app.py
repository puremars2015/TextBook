from flask import Flask
from WEBAPI.routes.sample import sample_bp
from WEBAPI.routes.translator import translator_bp

app = Flask(__name__)

@app.route('/')
def home():
    return "", 404

app.register_blueprint(sample_bp)
app.register_blueprint(translator_bp)

if __name__ == '__main__':
    app.run(debug=True)
