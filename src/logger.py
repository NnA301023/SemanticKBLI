import firebase_admin
from datetime import datetime
from fastapi import Request, Response
from firebase_admin import credentials, firestore

def connect_firebase(cert_path: str = "secret/firebase-cred.json"):
    credential = credentials.Certificate(cert_path)
    firebase_admin.initialize_app(credential)
    database = firestore.client()
    return database

def send_logger(request: Request, response: Response, database: object, collection: str = "logs"): 
    schema_logs = {
        "datetime" : datetime.now().isoformat(), 
        "method" : request.method, 
        "url" : request.url.path, 
        "headers" : dict(request.headers), 
        "client_ip" : request.client.host, 
        "product_name" : response["body"][0]["nama_produk"],
        "prediction_type_product" : response["body"][0]["prediksi_jenis"],
        "prediction_kbli_product" : response["body"][0]["prediksi_kbli"], 
        "prediction_result" : response["body"][0]["message"], 
        "product_name_nearest" : response['body'][0]["nama_produk_terdekat"]
    }
    document = database.collection(collection).document()
    document.set(schema_logs)