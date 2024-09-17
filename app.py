import gradio as gr
import re
import cohere
import numpy as np
import textwrap
import os
import pandas as pd
import requests
import fitz
from tqdm.auto import tqdm
from spacy.lang.en import English
from pinecone import Pinecone, ServerlessSpec

# Retrieve the API keys from environment variables
COHERE_KEY = os.getenv('COHERE_API_KEY')
PINECONE_KEY = os.getenv('PINECONE_API_KEY')

# Initialize global variables
co = cohere.Client(COHERE_KEY)
pc = Pinecone(api_key=PINECONE_KEY)
index_name = 'cohere-pinecone'
nlp = English()
nlp.add_pipe("sentencizer")

def text_formatter(text: str) -> str:
    return text.replace("\n", " ").strip()

def open_and_read_pdf(pdf_path: str, page_offset: int = 0) -> list[dict]:
    doc = fitz.open(pdf_path)
    pages_and_texts = []
    for page_number, page in enumerate(doc):
        text = page.get_text()
        text = text_formatter(text)
        pages_and_texts.append({
            "page_number": page_number - page_offset,
            "page_char_count": len(text),
            "page_word_count": len(text.split(" ")),
            "page_sentence_count_raw": len(text.split(". ")),
            "page_token_count": len(text) / 4,
            "text": text
        })
    return pages_and_texts

def split_list(input_list: list, slice_size: int) -> list[list[str]]:
    return [input_list[i:i + slice_size] for i in range(0, len(input_list), slice_size)]

def process_pdf(pdf_path):
    pages_and_texts = open_and_read_pdf(pdf_path=pdf_path)
    
    for item in pages_and_texts:
        item["sentences"] = [str(sentence) for sentence in nlp(item["text"]).sents]
        item["page_sentence_count_spacy"] = len(item["sentences"])
        item["sentence_chunks"] = split_list(input_list=item["sentences"], slice_size=10)
        item["num_chunks"] = len(item["sentence_chunks"])
    
    pages_and_chunks = []
    for item in pages_and_texts:
        for sentence_chunk in item["sentence_chunks"]:
            chunk_dict = {
                "page_number": item["page_number"],
                "sentence_chunk": "".join(sentence_chunk).replace("  ", " ").strip(),
            }
            chunk_dict["sentence_chunk"] = re.sub(r'\.([A-Z])', r'. \1', chunk_dict["sentence_chunk"])
            chunk_dict["chunk_char_count"] = len(chunk_dict["sentence_chunk"])
            chunk_dict["chunk_word_count"] = len(chunk_dict["sentence_chunk"].split(" "))
            chunk_dict["chunk_token_count"] = len(chunk_dict["sentence_chunk"]) / 4
            pages_and_chunks.append(chunk_dict)
    
    df = pd.DataFrame(pages_and_chunks)
    pages_and_chunks_over_min_token_len = df[df["chunk_token_count"] > 30].to_dict(orient="records")
    
    text_chunks = [item["sentence_chunk"] for item in pages_and_chunks_over_min_token_len]
    
    embeds = co.embed(
        texts=text_chunks,
        model='embed-english-v2.0',
        input_type='search_query',
        truncate='END'
    ).embeddings
    
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=len(embeds[0]),
            metric="cosine",
            spec=ServerlessSpec(cloud='aws', region='us-east-1')
        )
    
    index = pc.Index(index_name)
    
    ids = [str(i) for i in range(len(embeds))]
    meta = [{'text': text} for text in text_chunks]
    to_upsert = list(zip(ids, embeds, meta))
    
    batch_size = 128
    for i in range(0, len(embeds), batch_size):
        i_end = min(i+batch_size, len(embeds))
        index.upsert(vectors=to_upsert[i:i_end])
    
    return "PDF processed and indexed successfully!"

def search_queries(queries: list[str], k: int = 1) -> str:
    query_embeddings = co.embed(
        texts=queries,
        model='embed-english-v2.0',
        input_type='search_query',
        truncate='END'
    ).embeddings
    
    index = pc.Index(index_name)
    all_results = {}
    
    for i, query_embedding in enumerate(query_embeddings):
        res = index.query(vector=query_embedding, top_k=k, include_metadata=True)
        all_results[queries[i]] = res['matches']
    
    result_str = ""
    
    for query, matches in all_results.items():
        result_str += f"Results for Query: {query}\n\n"
        
        for match in matches:
            text = match['metadata']['text']
            result_str += f"{text}\n{'-'*50}\n\n"
        
        result_str += f"\n{'='*100}\n\n"
    
    return result_str

def chatbot(message, history):
    if not message.strip():
        return "Please enter a valid query."
    
    # Split the message into multiple queries
    queries = [q.strip() for q in message.split('||') if q.strip()]
    
    if not queries:
        return "Please enter at least one valid query."
    
    results = []
    for query in queries:
        result = search_queries([query])
        results.append(f"Query: {query}\n\n{result}")
    
    return "\n\n---\n\n".join(results)

def clear_index():
    global pdf_processed
    if not pdf_processed:
        return "Nothing to clear. Please upload and process a PDF first."
    try:
        pc.delete_index(index_name)
        pdf_processed = False
        return "Pinecone index cleared successfully!"
    except Exception as e:
        return f"Error clearing Pinecone index: {str(e)}"

def upload_pdf(file):
    global pdf_processed
    if file is None:
        return "Please upload a PDF file."
    
    file_path = file.name
    result = process_pdf(file_path)
    pdf_processed = True
    return result

demo = gr.Blocks()

with demo:

    gr.Markdown("# PDF Chatbot with Multi-Query Support")

    gr.Markdown("""
    ## How to use:
    1. Upload a PDF and click "Process PDF".
    2. Enter your queries in the chat below.
    3. For multiple queries, separate them with '||'.
    4. Before Uploading a new PDF please clear index.
    
    Example: What are macronutrients? || What is the role of vitamins?
    """)

    with gr.Row():
        with gr.Column(scale=2):
            pdf_upload = gr.File(label="Upload PDF", file_types=[".pdf"])
        with gr.Column(scale=1):
            process_button = gr.Button("Process PDF")
            clear_button_2 = gr.Button("Clear Index")
    
    status_output = gr.Textbox(label="Status")
    
    
    chatbot_interface = gr.ChatInterface(
        fn=chatbot,
        chatbot=gr.Chatbot(height=500),
        textbox=gr.Textbox(placeholder="Enter your query here...", container=False, scale=7),
        submit_btn="Send",
        clear_btn="🗑️ Clear",
        retry_btn="🔄 Retry",
        undo_btn="↩️ Undo",
        theme="soft",
        examples=[
            "What are macronutrients?",
            "What is the role of vitamins? || How do minerals affect health?",
            "Define protein || Define carbohydrates || Define fats"
        ],
    )
    
    clear_button_1 = gr.Button("Clear Index")
    
    process_button.click(upload_pdf, inputs=[pdf_upload], outputs=[status_output])
    clear_button_1.click(clear_index, inputs=None, outputs=[status_output])
    clear_button_2.click(clear_index, inputs=None, outputs=[status_output])

demo.launch()