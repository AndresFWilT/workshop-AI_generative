## config
import os
import openai
from config import DevelopmentConfig
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

# server config
app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# global
UPLOAD_FOLDER = '/static/images'
ALLOWED_EXTENSIONS = {'png'}

## ------------------------- view endpoints ----------------------------------------------

## endpoint for the app view
@app.route('/')
def init():
    return index("")

## endpoint to render index.html
@app.route('/index')
def index(message):
    return render_template('index.html', message = message)

## endpoint to render indexNLP_GPT3.html
@app.route('/gpt3')
def view_gpt3():
    return render_template('indexNLP_GPT3.html')

## endpoint to render indexImages_dalle2.html
@app.route('/dall-e2')
def view_dall_e2():
    return render_template('indexImages_dalle2.html')

## ------------------------- API endpoints -----------------------------------------------

## to use all Open AI models using direct prompt
@app.route("/gpt3_generate_response_direct_prompt", methods=("GET", "POST"))
def get_gpt3_response_direct_prompt():
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
        return render_template('indexNLP_GPT3.html', complete_result = complete_result, prompt = prompt)
    message = "No se recibieron datos prompt"
    return render_template("index.html", message=message)

##Generate response by prompt by example
@app.route("/gpt3_generate_response_prompt_by_example", methods=("GET", "POST"))
def get_gpt3_response_by_prompt_example():
    if request.method == "POST":
        prompt2 = request.form["prompt"]
        prompt= generate_prompt_by_example(prompt2)
        ## results from openAI API methods
        complete_example_result = {
            "result_ada": generate_response_ada(prompt),
            "result_babbage": generate_response_babbage(prompt),
            "result_curie": generate_response_curie(prompt),
            "result_davinci": generate_response_davinci(prompt)
        }
        ## rendering page
        return render_template('indexNLP_GPT3.html', complete_example_result = complete_example_result, prompt2 = prompt2)
    message = "No se recibieron datos prompt"
    return render_template("index.html", message=message)


## to create an image
@app.route("/dall_e2_create_image",methods=("GET","POST"))
def get_dall_e2_image():
    if request.method == "POST":
        prompt = request.form["prompt"]
        ## results from openAI API methods
        create_result = dalle2_create_image(prompt)
        ## Rendering page
        return render_template('indexImages_dalle2.html',create_result=create_result, prompt=prompt)
    message = "No se recibieron datos prompt"
    return render_template("index.html", message=message)

## to edit an image
@app.route("/dall_e2_edit_image", methods=['POST'])
def get_dall_e2_edit_image():
    # if post
    if request.method == 'POST':
        # request files from post
        file = request.files['img']
        # if allowed file validation and file exists
        if file and allowed_file(file.filename):
            # save name of file
            filename = secure_filename(file.filename)
            # save file in folder
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            # get prompt
            prompt = request.form["prompt"]
            # path image
            image = "static/images/"+filename
            # API openAI edit image
            edit_result = dalle2_edit_image(prompt, image)
            ## Rendering page
            return render_template('indexImages_dalle2.html',edit_result = edit_result, prompt = prompt)
        else:
            message = "Tipo de archivo no permitido"
            return index(message)  
    message = "No se recibieron datos prompt"
    return render_template("index.html", message=message)

## to variate an image
@app.route("/dall_e2_variate_image", methods=["POST"])
def get_dall_e2_variated_image():
    #if post
    if request.method == 'POST':
        # request files from post
        file = request.files['img']
        # if allowed file validation and file exists
        if file and allowed_file(file.filename):
            # save name of file
            filename = secure_filename(file.filename)
            # save file in folder
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
             # path image
            image = "static/images/"+filename
            # API openAI variate image
            variate_result = dalle2_variate_image(image)
            ## Rendering page
            return render_template('indexImages_dalle2.html',variate_result = variate_result)
        else:
            message = "Tipo de archivo no permitido"
            return index(message)  
    message = "Algo sucedio"
    return render_template("index.html", message=message)
    
## ------------------------- openAI API text--------------------------------------------------
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

## generate prompt by example
def generate_prompt_by_example(direct_prompt):
    return """pregunta: ¿Cual es la capital de Colombia?
        respuesta: Parce, la capital es Bogota DC.
        pregunta:¿Cual es la capital de España?
        respuesta:Tio, la capital es Madrid.
        pregunta:¿Cual es la capital de Venezuela?
        respuesta:  Chamo, la capital es Caracas.
        pregunta:¿Cual es la capital de Argentina?
        respuesta: Pibe, la capital es Buenos aires.
        pregunta: {}
        respuesta:""".format(
                direct_prompt.capitalize()
            )

## ------------------------- openAI API Images-------------------------------------------------

## create image
def dalle2_create_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="256x256"
    )
    return response['data'][0]['url']

## edit image
def dalle2_edit_image(prompt, image):
    response = openai.Image.create_edit(
        image=open(image, "rb"),
        mask=open(image, "rb"),
        prompt=prompt,
        n=1,
        size="256x256"
    )
    return response['data'][0]['url']

## variate image
def dalle2_variate_image(image):
    response = openai.Image.create_variation(
        image=open(image, "rb"),
        n=1,
        size="256x256"
    )
    return response['data'][0]['url']

## -------------------------- services validation -----------------------------------------

## file validation
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS    

## ------------------------- app start ----------------------------------------------------
if __name__ == '__main__':
    app.config.from_object(DevelopmentConfig)
    app.config["SESSION_PERMANENT"]= False
    app.config["SESSION_TYPE"]= "filesystem"
    app.run(debug=True)