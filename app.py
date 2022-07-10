from flask import Flask, redirect, url_for, request, render_template, session
import requests, os, uuid, json
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)


# flash.run


@app.route('/', methods=['GET'])
def index():  # put application's code here
    return render_template('index.html')

"""
Reads the text the user entered and the language they selected on the form
Reads the environmental variables we created earlier from our .env file
Creates the necessary path to call the Translator service, which includes the target language (the source language is automatically detected)
Creates the header information, which includes the key for the Translator service, the location of the service, and an arbitrary ID for the translation
Creates the body of the request, which includes the text we want to translate
Calls post on requests to call the Translator service
Retrieves the JSON response from the server, which includes the translated text
Retrieves the translated text (see the following note)
Calls render_template to display the response page
"""
@app.route('/', methods=['POST'])
def index_post():
    # Read the values from the form
    original_text = request.form['text']
    target_language = request.form['language']

    # Load the values from .env
    key = os.environ['KEY']
    endpoint = os.environ['ENDPOINT']
    location = os.environ['LOCATION']

    # Indicate that we want to translate and the API version (3.0) and the target language
    path = '/translate?api-version=3.0'
    # Add the target language parameter
    target_language_parameter = '&to=' + target_language
    # Create the full URL
    constructed_url = endpoint + path + target_language_parameter

    # Set up the header information, which includes our subscription key
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # Create the body of the request with the text to be translated
    body = [{ 'text': original_text }]

    # Make the call using post
    translator_request = requests.post(constructed_url, headers=headers, json=body)
    # Retrieve the JSON response
    translator_response = translator_request.json()
    # Retrieve the translation
    translated_text = translator_response[0]['translations'][0]['text']

    # Call render template, passing the translated text,
    # original text, and target language to the template
    return render_template(
        'results.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language
    )

if __name__ == '__main__':
    app.run()
