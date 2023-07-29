import json
import faiss 
from typing import List
from sentence_transformers import SentenceTransformer


def load_corpus():
    """
    Load pretrained model and corpus, while take a bit longer in first running.
    """
    model = SentenceTransformer("msmarco-MiniLM-L-6-v3")
    data_maps_self_declare = json.load(open('corpus/self-declare.json', 'r'))
    index_self_declare = faiss.read_index("corpus/self-declare.index")
    data_maps_reguler = json.load(open('corpus/reguler.json', 'r'))
    index_reguler = faiss.read_index("corpus/reguler.index")
    return (
        model, data_maps_self_declare, index_self_declare,
        data_maps_reguler, index_reguler
    ) 


# Create function to indexing results
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