import os
import uuid
import time
from datetime import datetime
from flask import Flask, request, jsonify
import logging
from logging.handlers import TimedRotatingFileHandler



logs_directory=r'C:\excellenteam\excercises\excercises-python\final-projects-hodaya12\logs\web_api'
UPLOADS_PATH='C:/Users/user/Desktop/uploads'
OUTPUT_PATH='C:/Users/user/Desktop/outputs'
if os.getenv("UPLOADS") is None:
    os.environ["UPLOADS"] = UPLOADS_PATH
UPLOADS_DIR=os.environ["UPLOADS"]
if os.getenv("OUTPUTS") is None:
    os.environ["OUTPUTS"] = OUTPUT_PATH
OUTPUTS_DIR=os.environ["OUTPUTS"]
if not os.path.exists(UPLOADS_DIR):
    os.mkdir(UPLOADS_DIR)
if not os.path.exists(OUTPUTS_DIR):
    os.mkdir(OUTPUTS_DIR)

app = Flask(__name__)
def set_logger():
    """
        Configure the logger for the Flask application.
    """
    # Configure the default Flask logger
    app.logger.setLevel(logging.INFO)
    # Create log formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # Create file handler and set formatter
    file_handler = TimedRotatingFileHandler(os.path.join(logs_directory, 'web_api.log'), when='midnight', interval=1,
                                            backupCount=5)
    file_handler.setFormatter(formatter)
    # Add file handler to the app's logger
    app.logger.addHandler(file_handler)

set_logger()

def generate_uid():
    """
      Generate a unique identifier (UUID) as a string.

      :return: A unique identifier.
    """
    return str(uuid.uuid4())


def get_file_timestamp():
    """
       Get the current timestamp in a specific format.

       :return: Current timestamp in the format 'YYYYMMDD_HHMMSS'.
       """
    return datetime.now().strftime('%Y%m%d_%H%M%S')


@app.route('/upload', methods=['POST'])
def upload_file():
    """
        Handle file upload requests.

        :return: JSON response with upload status or error message.
    """
    # Get the client's IP address
    client_ip = request.remote_addr
    # Logging example with client's IP address
    app.logger.info(f'Received file upload request from {client_ip}.')
    if not request.files:
        app.logger.info('No file part in the request')
        return jsonify({'error': 'No file part in the request'}), 400
    files = list(request.files.values())
    if len(files)!=1:
        app.logger.info('sent more than 1 file in the request')
        return jsonify({'error': 'Only 1 file is possible'}), 400
    file=files[0]
    # Get the file extension from the filename
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension != '.pptx':
        app.logger.info('sent not a pptx file')
        return jsonify({'error': 'Only pptx file is possible'}), 400
    if file.filename == '':
        app.logger.info('sent an invalid file')
        return jsonify({'error': 'No selected file'}), 400
    uid = generate_uid()
    timestamp = get_file_timestamp()
    # Create the filename
    filename = f"{file.filename}".split('.')[0]+f"_{timestamp}_{uid}.pptx"
    file_path = os.path.join(UPLOADS_DIR, filename)
    # Save the file to the uploads directory
    file.save(file_path)
    app.logger.info(filename+' was saved in the upload directory')
    return jsonify({'uid': uid}), 200


@app.route('/status/<string:uid>', methods=['GET'])
def get_status(uid):
    """
       Retrieve the status of a file processing request.

       :param uid: Unique identifier of the file processing request.
       :return: JSON response with processing status or error message.
    """
    # Get the client's IP address
    client_ip = request.remote_addr
    # Logging example with client's IP address
    app.logger.info(f'Received a status request from {client_ip}. with uid: '+uid)
    # Check if the file exists in the uploads and output directories
    uid_uploads = [filename.split("_")[-1].split(".")[0] for filename in os.listdir(UPLOADS_DIR)]
    uid_outputs = [filename.split("_")[-1].split(".")[0] for filename in os.listdir(OUTPUTS_DIR)]
    if f"{uid}" not in uid_uploads and f"{uid}" not in uid_outputs:
        return jsonify({'status': 'not found'}), 404

    # Check if the file has been processed and exists in the outputs directory
    if f"{uid}" in uid_outputs:
        file=list(filter(lambda filename:filename.split("_")[-1].split(".")[0]==f"{uid}",os.listdir(OUTPUTS_DIR)))[0]
        # File has been processed, read the content from the output file
        output_path = os.path.join(OUTPUTS_DIR, file)
        with open(output_path, 'r') as f:
            output_data = f.read()
        return jsonify({'status': 'done', 'filename': file, 'timestamp': file.split("_")[-2], 'explanation': output_data}), 200
    else:
        # File has not been processed yet
        file = list(filter(lambda filename: filename.split("_")[-1].split(".")[0] == f"{uid}", os.listdir(UPLOADS_DIR)))[0]
        return jsonify({'status': 'pending','filename': file, 'timestamp': file.split("_")[-2]}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
