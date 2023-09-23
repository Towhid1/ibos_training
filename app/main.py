from flask import Flask, request
import mlflow
from flask import Flask, request, jsonify
import numpy as np


# # Load model as a PyFuncModel
logged_model = "mlflow-artifacts:/1/342f1114f5bb4618b49c8663bb0011b2/artifacts/LinearReg"

# set tracking uri
mlflow.set_tracking_uri("http://mlflow:5000")
loaded_model = mlflow.pyfunc.load_model(logged_model)

app = Flask(__name__)


@app.route('/api/v1', methods=['POST'])
def pred():
    """
    Make a prediction using the loaded machine learning model based on the JSON data received in the request.

    This function expects the JSON data to contain a 'features' field, which should be a list representing the
    features of the data point to be predicted.

    Returns:
        A JSON response containing the prediction result along with some metadata about the loaded model.

    Raises:
        N/A - This function does not raise any exceptions.
    """
    # Get the JSON data from the request
    request_data = request.json
    # Perform any processing you want with the received data
    if 'features' in request_data:
        features = request_data['features']
        # You can also perform additional logic here based on the received data
        prediction = loaded_model.predict(np.array(features).reshape(1, -1))
        response = {
            'prediction': prediction[0],
            'run_id': loaded_model.metadata.run_id,
            'model_uuid': loaded_model.metadata.model_uuid,
            'utc_time_created': loaded_model.metadata.utc_time_created,
        }
        return jsonify(response), 200
    else:
        return jsonify({'error': 'Invalid data format'}), 400


@app.route('/health', methods=['GET'])
def health():
    """
    Health Check Endpoint.

    This endpoint is used to perform a health check on the server. When a GET request is made to this endpoint,
    the server responds with a JSON object indicating the server's health status.

    Returns:
        dict: A JSON object containing the health status message.

    Example:
        A GET request to '/health' returns:
        {'message': 'healthy'}
    """
    return jsonify({'message': 'healthy'}), 200


if __name__ == '__main__':
    app.run(debug=False, port=6000)
