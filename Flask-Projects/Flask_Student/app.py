from flask import Flask
import config
from extension import register_extension, db

app = Flask(__name__)
app.config.from_object(config)
register_extension(app)


@app.route('/')
def index():
    return 'hello world!'


if __name__ == "__main__":
    app.run(debug=True)
