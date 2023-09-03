import json
import faiss 
import openai
from typing import List
from sentence_transformers import SentenceTransformer


OPENAI_KEY = json.load(open("./secret/openai-cred.json", "r"))["OPENAI_KEY"]
openai.api_key = OPENAI_KEY

def load_corpus():
    model = SentenceTransformer("msmarco-MiniLM-L-6-v3")
    data_maps_self_declare = json.load(open('corpus/self-declare.json', 'r'))
    index_self_declare = faiss.read_index("corpus/self-declare.index")
    data_maps_reguler = json.load(open('corpus/reguler.json', 'r'))
    index_reguler = faiss.read_index("corpus/reguler.index")
    return (
        model, data_maps_self_declare, index_self_declare,
        data_maps_reguler, index_reguler
    ) 

def fetch_product(idx: int, query: str, df: List):
    result = {}
    result["nama_produk"] = query
    try:
        info = df[idx]
        result["nama_produk_terdekat"] = info['Nama Produk / Rincian']
        result["prediksi_jenis"] = info["Jenis Produk"]
        result["prediksi_kbli"]  = info["Kode KBLI"]
        result["message"]        = "Prediction Success"
    except IndexError:
        result["nama_produk_terdekat"] = ""
        result["prediksi_jenis"] = ""
        result["prediksi_kbli"]  = ""
        result["message"]        = "Prediction Failed "
    return result

def search(query: str, index_vector: object, model_embedding: object, df: List):
    query_vector = model_embedding.encode([query])
    selected_idx = index_vector.search(query_vector, k = 1)
    selected_idx = selected_idx[1].tolist()[0][0]
    result = [fetch_product(selected_idx, query, df)]
    return result

def _set_prompt(description: str):
    custom_prompt = \
    f"""
    Ekstraksi nama bahan dalam deskripsi pemrosesan bahan, dengan contoh cukup menampilkan di bagian result dengan menghapus apabila ada bahan yang duplikat. Tanpa menggunakan embel-embel kata penjelasan.
    
    Dengan contoh deskripsi dan result
    Deskripsi: Produk dibuat dengan cara : 1. Periapan alat dan bahan 2. Pembersihan dan pengupasan bahan (singkong) 3. Penggilingan singkong 4. Pencampuran dengan tepung tapioka, terigu dan garam 5. Pencetakan dan penggorengan 6. Pendinginan, packing dan pemasangan label 
    Result : "singkong", "tepung tapioka", "tepung terigu", "garam"

    Untuk hasil Result, Cukup identifikasi pada deskripsi dibawah ini dan hanya seputar bahan makanan atau minuman.
    Deskripsi: {description}
    Result : 
    """
    return custom_prompt

def _parse_result(result: str):
    return result

def detect_bahan(description: str):
    result = {}
    result["step_product"] = description
    try:
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo", messages = [{"role" : "user", "content" : _set_prompt(description)}], 
            temperature = 0, max_tokens = 256, top_p = 1.0, frequency_penalty = 0.0, presence_penalty = 0.0
        )
        response = _parse_result(response["choices"][0]["message"]["content"])
    except Exception: 
        response = ""
    result["ingredient_detected"] = response
    return result