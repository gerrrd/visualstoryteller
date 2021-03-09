from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import storage
from visualstoryteller.getmorepics import getmorepics
from datetime import datetime

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

    now = datetime.today()
    n = str(now).replace(' ','').replace('-','').replace(':','').replace('.','')

    # get the images
    result = getmorepics(text, saveimage=True, savename=f"output_{n}.jpg")

    # check if the response is empty
    if result['OK'] <= 0:
        return result

    # upload the pictures to google storage
    bucket_name = 'lewagon-bootcamp-305809'
    storage_location = 'project'
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    im_urls = []

    for img in result['saved']:

        path_to_file = img

        blob = bucket.blob(f'{storage_location}/{path_to_file}')
        blob.upload_from_filename(path_to_file)
        blob.make_public()
        im_url = blob.public_url

        im_urls.append(im_url)

    result['im_urls'] = im_urls

    return result
