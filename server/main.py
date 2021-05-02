from processor import Response
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


@app.route("/newmessage", methods=['POST'])
def newmessage():
  messageto = request.json.get('from')
  message = request.json.get('message')
  response = Response(message, messageto).get_response()
  response['to'] = request.json.get('from')
  return jsonify(response)


if __name__ == "__main__":
  app.run(debug=True)