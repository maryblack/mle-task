from flask import Flask, request, jsonify, make_response
from task_2.classification import MultiClassificator
app = Flask(__name__)


@app.route('/api/goods/classify',  methods=['POST'])
def predict():
    values = request.get_json()
    answer = MultiClassificator().predict(values["text"])
    print(answer)
    result = {'class': answer}
    resp = make_response(jsonify(result))
    return resp


# after we have patched app with controllers, we can return it's 'final form'
def get_app() -> Flask:
    return app


if __name__ == '__main__':
    app.run()
