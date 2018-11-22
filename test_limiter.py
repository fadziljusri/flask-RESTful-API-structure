from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["2/minute", "1/second"],
)

@app.route("/slow")
@limiter.limit("1/day")
def slow():
    return "24"

@app.route("/fast")
def fast():
    return "42"

@app.route("/ping")
@limiter.exempt
def ping():
    return 'PONG'

app.run(debug=True)