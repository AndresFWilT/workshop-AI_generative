## config
import os
import openai
from config import DevelopmentConfig
from flask import Flask, redirect, render_template, request, url_for

# server config
app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

## ------------------------- view endpoints ----------------------------------------------

## endpoint for the app view
@app.route('/')
def init():
    return index("")

## endpoint to render index.html
@app.route('/index')
def index(message):
    return render_template('index.html', message = message)

@app.route('/nlp')
def view_nlp():
    return render_template('indexNLP.html')

## ------------------------- API endpoints -----------------------------------------------

## to use all Open AI models
@app.route("/generate_all_text", methods=("GET", "POST"))
def get_all_text():
    if request.method == "POST":
        prompt = request.form["prompt"]
        ## results from openAI API methods
        complete_result = {
            "result_ada": generate_response_ada(prompt),
            "result_babbage": generate_response_babbage(prompt),
            "result_curie": generate_response_curie(prompt),
            "result_davinci": generate_response_davinci(prompt)
        }
        ## rendering page
        return render_template('indexNLP.html', complete_result = complete_result, prompt = prompt)
    message = "No se recibieron datos prompt"
    return render_template("index.html", message=message)

## ------------------------- openAI API --------------------------------------------------
## model ada
def generate_response_ada(prompt):
    response = openai.Completion.create(
        model="text-ada-001",
        prompt=prompt,
        temperature=0.1,
        top_p = 1,
        max_tokens = 800
    )
    return response.choices[0].text

## model babbage
def generate_response_babbage(prompt):
    response = openai.Completion.create(
        model="text-babbage-001",
        prompt=prompt,
        temperature=0.1,
        top_p = 1,
        max_tokens = 800
    )
    return response.choices[0].text

## model Curie
def generate_response_curie(prompt):
    response = openai.Completion.create(
        model="text-curie-001",
        prompt=prompt,
        temperature=0.1,
        top_p = 1,
        max_tokens = 800
    )
    return response.choices[0].text

## model davinci
def generate_response_davinci(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.1,
        top_p = 1,
        max_tokens = 800
    )
    return response.choices[0].text

## generate prompt
def generate_prompt(animal):
    return """Who wrote Odysseus?"""

## ------------------------- app start ----------------------------------------------------
if __name__ == '__main__':
    app.config.from_object(DevelopmentConfig)
    app.config["SESSION_PERMANENT"]= False
    app.config["SESSION_TYPE"]= "filesystem"
    app.run(debug=True)
