from flask import Flask, request
import json
app = Flask(__name__)

@app.route('/', methods=['POST'])
def receive():
    data = request.get_json()
    print('ALERT RECEIVED:', json.dumps(data))
    return '', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
