import re
from flask import Flask
from flask import request, json
import inference
app = Flask(__name__)

@app.route("/Submit", methods=["GET"])

def Submit():
    if request.method == 'GET':
        data = json.loads(request.data)
        label = inference.pred(data['FileName'])
        return {"label":label}

if __name__ == "__main__":
    app.run(debug=True)