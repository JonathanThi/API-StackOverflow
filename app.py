from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import pickle
import joblib

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.run(debug=True, use_reloader=False)

model = joblib.load(open('logit_nlp_model.pkl','rb'))

@app.route('/predict', methods = ['POST'])
@cross_origin()
def predict():
    try:
        data = request.get_json()
        prediction = model.predict_proba([data['features']])
        print(prediction)
        output = {'predictions': prediction.tolist()[0]}
        return jsonify( output )
    except NameError:
        print(NameError)
        return 'something went wrong'

@app.errorhandler(404)

def resource_not_found(e):
    return jsonify(error='The requested URL was not found on the server'), 404

if __name__ == "__main__":
    app.run(host ='0.0.0.0', port = 5000, debug = True)