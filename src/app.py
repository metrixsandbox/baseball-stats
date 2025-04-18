from flask import Flask
from src.api.routes import api_bp

app = Flask(__name__)

# Register the API blueprint
app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/')
def home():
    return "Welcome to the Baseball Stats API!"

if __name__ == '__main__':
    app.run(debug=True)