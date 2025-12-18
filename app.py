import chromadb
import time
from settings import *
import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sentence_transformers import SentenceTransformer

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

client = chromadb.HttpClient(host="localhost", port=8001)
collection = client.get_or_create_collection(
    name=CHROMADB_COLLECTION
)

model = SentenceTransformer("all-MiniLM-L6-v2")

headers = {
    "Authorization": "Bearer " + LLM_API_KEY,
    "Content-Type": "application/json"
}


def generate(prompt):
    print("----------------- My prompt -----------------")
    print(prompt)

    payload = {
        "model": "meta-llama/Meta-Llama-3-8B-Instruct",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2,
        "max_tokens": 300
    }

    response = requests.post(LLM_URL, headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]



def retrieve_recent_weather(query, now_ts, window_seconds=30):
    q_emb = model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=q_emb,
        n_results=5,
        where={"timestamp": {"$gte": now_ts - window_seconds}}
    )
    return results

def build_prompt(query, context):
    prompt = f"""
    You are a real-time weather advisory system.

    User question:
    {query}

    Recent weather context (last 30 seconds):
    {context}

    Produce a clear summary of the hazard, with instructions.
    """
    return prompt


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/ask")
async def ask(request: Request):
    data = await request.json()
    query = data.get("query")
    if not query:
        return JSONResponse({"error": "No query provided"}, status_code=400)
    
    try:
        results = retrieve_recent_weather(query, int(time.time()))
        context = []
        for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
            context.append(f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(meta['timestamp']))}] {doc}")
        context_text = "\n\n".join(context)
        prompt = build_prompt(query, context_text)
        answer = generate(prompt)
        print("--- Answer ---")
        print(answer)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    
    return {"answer": answer}


# def main():
#     while True:
#         query = input("Enter question: ")
#         results = retrieve_recent_weather(query, int(time.time()))
#         context = []
#         for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
#             context.append(f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(meta['timestamp']))}] {doc}")
#         context_text = "\n\n".join(context)
#         prompt = build_prompt(query, context_text)
#         answer = generate(prompt)
#         print("--- Answer ---")
#         print(answer)

# if __name__ == "__main__":
#     main()