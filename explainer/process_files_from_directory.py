import os
import pathlib
import subprocess
import time
import create_logger

logger=create_logger.create_logger(r'C:\excellenteam\excercises\excercises-python\final-projects-hodaya12\logs\explainer')
UPLOADS_PATH = 'C:/Users/user/Desktop/uploads'
OUTPUT_PATH = 'C:/Users/user/Desktop/outputs'
if os.getenv("UPLOADS") is None:
    os.environ["UPLOADS"] = UPLOADS_PATH
UPLOADS_DIR = os.environ["UPLOADS"]
if os.getenv("OUTPUTS") is None:
    os.environ["OUTPUTS"] = OUTPUT_PATH
OUTPUTS_DIR = os.environ["OUTPUTS"]
if not os.path.exists(UPLOADS_DIR):
    os.mkdir(UPLOADS_DIR)
if not os.path.exists(OUTPUTS_DIR):
    os.mkdir(OUTPUTS_DIR)
uploads_directory = pathlib.Path(os.getenv("UPLOADS"))
archive_directory = uploads_directory / 'archive'
archive_directory.mkdir(mode=0o777, exist_ok=True)

def process_file(pptx_file):
    """
    Process a PowerPoint file by sending it to the program for processing with ChatGPT.

    :param pptx_file: The file path of the PowerPoint file to be processed.
    """
    print("Start processing " + pptx_file.name)
    logger.info('Start processing %s', pptx_file.name)
    # Construct the command to run the main script
    command = ["python", "main.py", str(pptx_file)]
    # Run the main script as a subprocess
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        print(result.stdout)
        print("Finish processing " +pptx_file.name )
        logger.info(result.stdout)
        logger.info('Finish processing %s', pptx_file.name)

        pptx_file.rename(archive_directory / pptx_file.name)
    else:
        print("Error for processing "+pptx_file.name)
        print(result.stderr)
        logger.info('Error for processing %s', pptx_file.name)
        logger.info(result.stderr)

def process_all_new_files():
    """
       Continuously processes new PowerPoint files from the uploads directory.
    """
    while True:
        pptx_files = list(uploads_directory.glob("*.pptx"))
        [process_file(pptx_file) for pptx_file in pptx_files]
        time.sleep(10)

if __name__ == "__main__":
    process_all_new_files()
