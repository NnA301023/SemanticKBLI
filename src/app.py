import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable Cross-Origin Resource Sharing (CORS) for all origins
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = origins,
    allow_headers = origins,
)

@app.post("/predict")
async def classify_text(text: str):
    # In a real-world scenario, perform your text classification here
    # This is a placeholder function that just returns the input text
    return {"text": text}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
