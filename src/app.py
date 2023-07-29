import uvicorn
from fastapi import FastAPI, Request
from model import load_corpus, search
from logger import send_logger, connect_firebase
from fastapi.middleware.cors import CORSMiddleware

# Define global variable
app = FastAPI()
database = connect_firebase()
model, mapping_sd, index_sd, mapping_reg, index_reg = load_corpus()

# Enable Cross-Origin Resource Sharing (CORS) for all origins
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = origins,
    allow_headers = origins,
)

@app.middleware("http")
async def logger(request: Request, call_next: object):
    response = await call_next(request)
    return response 

@app.post("/self-declare/predict")
async def classify_text(text: str, request: Request):
    response = {"message" : "Success", "status_code" : 200, "body" : []}
    if text != "":
        response["body"] = search(text, index_sd, model, mapping_sd)
    else: 
        response["message"] = "text blank"
        response["status_code"] = 404
    send_logger(request, response, database)
    return response

@app.post("/reguler/predict")
async def classify_text(text: str, request: Request):
    response = {"message" : "Success", "status_code" : 200, "body" : []}
    if text != "":
        response["body"] = search(text, index_reg, model, mapping_reg)
    else: 
        response["message"] = "text blank"
        response["status_code"] = 404
    send_logger(request, response, database)
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
