from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import storage
from visualstoryteller.getonepic import getonepic

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
def index():
    return {"ok": "True"}


@app.get("/image")
def get_image(text):

    result = getonepic(text, saveimage=True)

    bucket_name = 'lewagon-bootcamp-305809'
    storage_location = 'project'
    path_to_file = 'output.jpg'

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(f'{storage_location}/{path_to_file}')
    blob.upload_from_filename(path_to_file)
    blob.make_public()
    im_url = blob.public_url

    result['im_url'] = im_url
    # image = result['image']
    # content_image = result['content'][0]
    # content_author = result['content'][1]
    # content_profile = result['content'][2]
    # style_image = result['style'][0]
    # style_author = result['style'][1]
    # style_profile = result['style'][2]

    # pipeline = get_model_from_gcp()
    #pipeline = joblib.load('model.joblib')

    return result
