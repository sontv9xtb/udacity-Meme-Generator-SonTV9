"""Author by SonTV9"""

import random
import os
import requests
from flask import Flask, render_template, request
from MemeEngine.MemeGenerator import MemeGenerator as MemeEngine

from QuoteEngine.Ingestor import Ingestor

app = Flask(__name__)

meme = MemeEngine('./static')


def setup():
    """ Load all resources """

    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']
    # quote_files variable
    quotes = []
    for file in quote_files:
        try:
            quotes.extend(Ingestor.parse(file))
        except ValueError as error:
            print(f'ValueError: {error}')
    images_path = "./_data/photos/dog/"
    imgs = []
    for root, directories, files in os.walk(images_path):
        imgs = [os.path.join(root, file) for file in files]

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """ Generate a random meme """

    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """ User input for meme information """
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """Create a user-defined meme."""
    try:
        # Get the image URL and meme text from the request form
        image_url = request.form['image_url']
        body = request.form['body']
        author = request.form['author']

        # Fetch the image from the URL
        response = requests.get(image_url)
        response.raise_for_status()  # Ensure we raise an error for bad responses

        # Save the image locally
        img_file = f'meme_{os.path.basename(image_url)}.jpeg'
        with open(img_file, 'wb') as file:
            file.write(response.content)

        # Create the meme
        path = meme.make_meme(img_file, body, author)
        print(f"Meme created at: {path}")

        # Remove the temporary image file
        os.remove(img_file)

    except requests.exceptions.RequestException as e:
        # Handle any request-related errors
        print(f"Error fetching image: {e}")
        return render_template('meme_error.html')

    except Exception as e:
        # Handle other possible errors
        print(f"An unexpected error occurred: {e}")
        return render_template('meme_error.html')

    # Render the template with the path to the created meme
    return render_template('meme.html', path=path)


if __name__ == "__main__":
    app.run()
