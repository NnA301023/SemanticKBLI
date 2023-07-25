import uvicorn
from fastapi import FastAPI, Request
from logger import send_logger, connect_firebase
from fastapi.middleware.cors import CORSMiddleware

# Define global variable
app = FastAPI()
database = connect_firebase()

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
    send_logger(request, response, database)
    return response 

@app.post("/predict")
async def classify_text(text: str):
    response = {"message" : "Success", "status_code" : 200, "body" : []}
    response["body"].append({"nama_produk" : text})
    response["body"].append({"prediksi_jenis" : "Misalnya Serealia"})
    response["body"].append({"prediksi_kbli" : "12345"})
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
