import os
from flask import Flask, request, jsonify
from googletrans import Translator

# import our OCR function
from ocr import ocr_core

# define a folder to store and later serve the images
UPLOAD_FOLDER = '/static/uploads/'

# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)

# function to check the file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def translate_text(text, dest='en'):
    translator = Translator()
    return translator.translate(text, dest=dest)

# route and function to handle the upload page
@app.route('/check', methods=['POST'])
def check():
    # check if there is a file in the request
    if 'file' not in request.files:
        return jsonify(message='No file selected'), 418
    file = request.files['file']
    # if no file is selected
    if file.filename == '':
        return jsonify(message='No file selected'), 418

    if file and allowed_file(file.filename):

        # call the OCR function on it
        extracted_text = ocr_core(file)

        translate_to = request.form['dest']

        translated_text = translate_text(extracted_text, dest=translate_to)

        # extract the text and display it
        return jsonify(extracted_text=extracted_text, translated_text=translated_text.text)
    else:
        return jsonify(message='Enter a valid image'), 418

if __name__ == '__main__':
    app.run(debug=True)