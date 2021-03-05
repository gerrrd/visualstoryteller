from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from visualstoryteller.getmorepics_twonouns import getmorepics_twonouns

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

    result = getmorepics_twonouns(text, saveimage=True)

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