import firebase_admin
from datetime import datetime
from fastapi import Request, Response
from firebase_admin import credentials, firestore

def connect_firebase(cert_path: str = "secret/firebase-cred.json"):
    credential = credentials.Certificate(cert_path)
    firebase_admin.initialize_app(credential)
    database = firestore.client()
    return database

def send_logger(request: Request, response: Response, database: object, collection: str = "logs", is_bahan: bool = False): 
    schema_logs = {
        "datetime" : datetime.now().isoformat(), 
        "method" : request.method, 
        "url" : request.url.path, 
        "headers" : dict(request.headers), 
        "client_ip" : request.client.host
    }

    if is_bahan:
        schema_logs["step_product"] = response["body"][0]["step_product"]
        schema_logs["ingredient_detected"] = response["body"][0]["ingredient_detected"]
    else:
        schema_logs["product_name"]            = response["body"][0]["nama_produk"]
        schema_logs["prediction_type_product"] = response["body"][0]["prediksi_jenis"]
        schema_logs["prediction_kbli_product"] = response["body"][0]["prediksi_kbli"]
        schema_logs["prediction_result"]       = response["body"][0]["message"]
        schema_logs["product_name_nearest"]    = response['body'][0]["nama_produk_terdekat"]

    document = database.collection(collection).document()
    document.set(schema_logs)