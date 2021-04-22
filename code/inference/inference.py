import os
import json
import pickle
from sklearn.preprocessing import StandardScaler

with open(os.path.join(os.path.dirname(__file__), 'StandardScaler.pkl'), 'rb') as outfile:
    scaler = pickle.load(outfile)

def input_handler(data, context):
    """ Pre-process request input before it is sent to TensorFlow Serving REST API
    Args:
        data (obj): the request data, in format of dict or string
        context (Context): an object containing request and configuration details
    Returns:
        (obj): preprocessed input data
    """
    if context.request_content_type == 'application/json':
        d = data.read().decode('utf-8')
        parsed_data = json.loads(d) if len(d) else ''

        parsed_data['instances'] = scaler.transform(parsed_data['instances']).tolist()

        return json.dumps(parsed_data)

    raise ValueError('{{"error": "unsupported content type {}"}}'.format(
        context.request_content_type or "unknown"))


def output_handler(data, context):
    """Post-process TensorFlow Serving output before it is returned to the client.
    Args:
        data (obj): the TensorFlow serving response
        context (Context): an object containing request and configuration details
    Returns:
        (bytes, string): data to return to client, response content type
    """
    if data.status_code != 200:
        raise ValueError(data.content.decode('utf-8'))

    response_content_type = context.accept_header
    prediction = data.content
    return prediction, response_content_type