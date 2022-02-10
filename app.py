from flask import Flask

app = Flask(__name__)

@app.route("/healthz", methods=['GET'])
def health():
    return "200: Service is healthy and running ", 200


if __name__ == '__main__':
    app.run(debug=True)
