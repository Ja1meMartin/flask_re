import funcs
from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/from/<start>')
def calendar_to_today(start):
    return jsonify(funcs.get_json_from_strings(start, None, 48))
    
@app.route('/from/<start>/to/<end>')
def calendar(start, end):
    return jsonify(funcs.get_json_from_strings(start, end, 48))

if __name__ == '__main__':
    app.run()