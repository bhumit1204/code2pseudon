import os
import requests
from flask import Blueprint, request, jsonify, session
from dotenv import load_dotenv
import datetime
import json
import re
from pymilvus import MilvusClient, DataType, FieldSchema, CollectionSchema
import time

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
print(OPENROUTER_API_KEY)
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "meta-llama/llama-3.3-8b-instruct:free"

milvus_uri = os.getenv("MILVUS_URI")
milvus_token = os.getenv("MILVUS_KEY")
COLLECTION_NAME = "code_data"
EMBEDDING_DIM = 768

SYSTEM_PROMPT = """
You are a helpful assistant that converts natural language descriptions of code into structured, language-agnostic pseudocode.

You will receive three user inputs:

title – A short name for the code (e.g., "Bubble Sort Algorithm")

description – A plain English explanation of what the code should do. This helps you understand the logic and expected behavior.

tags – A comma-separated list of relevant programming concepts (like loops, arrays, recursion, search, etc.). Use these to understand which structures or topics to include.

Your task is to:

Analyze the user's description and tags

Generate clean, readable pseudocode that explains the logic step-by-step

Output a JSON object containing:

title: same as the input title

pseudo_content: the generated pseudocode

description: same as the input description

timestamp: current UTC timestamp in ISO format (e.g., "2025-06-15T08:30:00Z")

Guidelines for pseudocode:

Use clear, concise English

Use structured pseudocode (e.g., IF...ELSE, FOR loop, WHILE, FUNCTION definitions)

Do not use any specific programming language syntax

Keep indentation and formatting readable

Example Outputs:

Example 1
Input:
title: Find Maximum Number
description: This code takes an array and finds the largest number in it.
tags: array, loop, comparison

Output:
{
"title": "Find Maximum Number",
"pseudo_content": "START\nSET max TO first element in array\nFOR each number in array\n IF number > max THEN\n SET max TO number\n END IF\nEND FOR\nPRINT max\nEND",
"description": "This code takes an array and finds the largest number in it.",
"timestamp": "2025-06-15T08:30:00Z"
}

Final instruction:
Always return only a single JSON object with the required fields and no extra commentary.
"""

generate_pseudo_api = Blueprint('generate_pseudo_api', __name__)

def init_milvus_client():
    """Initialize Milvus client"""
    try:
        client = MilvusClient(
            uri=milvus_uri,
            token=milvus_token
        )
        
        if client.has_collection(collection_name=COLLECTION_NAME):
            if client.get_load_state(collection_name=COLLECTION_NAME).get('state') != 'Loaded':
                client.load_collection(collection_name=COLLECTION_NAME)
        
        return client
    except Exception as e:
        print(f"Milvus client initialization error: {e}")
        return None

def generate_dummy_embedding(text, dim=768):
    import hashlib
    hash_obj = hashlib.md5(text.encode())
    hash_hex = hash_obj.hexdigest()
    
    embedding = []
    for i in range(0, len(hash_hex), 2):
        val = int(hash_hex[i:i+2], 16) / 255.0
        embedding.append(val)
    
    while len(embedding) < dim:
        embedding.extend(embedding[:min(len(embedding), dim - len(embedding))])
    
    return embedding[:dim]

def store_to_milvus(client, title, description, tags, pseudo_content, user_id=None):
    """Store data to Milvus using your schema"""
    try:
        print(f"📝 Storing data:")
        print(f"  Title: {title}")
        print(f"  Description: {description}")
        print(f"  Tags: {tags}")
        print(f"  Pseudo content length: {len(pseudo_content)}")
        
        combined_description = f"{title} | Tags: {tags}"
        
        embedding = generate_dummy_embedding(pseudo_content, EMBEDDING_DIM)
        print(f"  Generated embedding dimension: {len(embedding)}")
        
        current_timestamp = int(time.time())
        
        creator_user_id = user_id or 'anonymous'
        print(f"  User ID: {creator_user_id}")
        
        data = [{
            "embedding": embedding,
            "pseudocode_content": pseudo_content,
            "code_language": "pseudocode",
            "description": combined_description,
            "conversion_direction": "description_to_pseudocode",
            "creator_user_id": creator_user_id,
            "timestamp": current_timestamp,
            "code_content": ""
        }]
        
        print("  Inserting data into Milvus...")
        
        insert_result = client.insert(
            collection_name=COLLECTION_NAME,
            data=data
        )
        
        print(f"✅ Data stored to Milvus successfully!")
        print(f"  Insert result: {insert_result}")
        
        client.flush(COLLECTION_NAME)
        print("  Data flushed to storage")
        
        return True
        
    except Exception as e:
        print(f"❌ Error storing to Milvus: {e}")
        import traceback
        traceback.print_exc()
        return False

@generate_pseudo_api.route('/generate', methods=['POST'])
def generate_pseudocode():
    try:
        milvus_client = init_milvus_client()
        if not milvus_client:
            print("Warning: Milvus client not available")
        
        data = request.json
        
        user_title = data.get("title", "").strip()
        user_description = data.get("description", "").strip()
        user_tags = data.get("tags", "").strip()

        if not user_title or not user_description or not user_tags:
            return jsonify({"error": "Missing required fields: title, description, or tags."}), 400

        user_prompt = f"""
Input:
title: {user_title}
description: {user_description}
tags: {user_tags}

Output:
"""

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        body = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ]
        }

        response = requests.post(OPENROUTER_API_URL, headers=headers, json=body)
        response.raise_for_status()
        ai_response = response.json()

        reply_content = ai_response['choices'][0]['message']['content']

        reply_content = re.sub(r'^```(json)?\n?', '', reply_content.strip(), flags=re.IGNORECASE | re.MULTILINE)
        reply_content = re.sub(r'\n?```$', '', reply_content.strip(), flags=re.MULTILINE)

        try:
            ai_result = json.loads(reply_content)
            generated_pseudo_content = ai_result["pseudo_content"]
        except json.JSONDecodeError:
            reply_content_cleaned = reply_content.encode('utf-8', 'ignore').decode('utf-8')
            generated_pseudo_content = reply_content_cleaned

        if milvus_client:
            print("Attempting to store data to Milvus...")
            store_success = store_to_milvus(
                client=milvus_client,
                title=user_title,
                description=user_description,
                tags=user_tags,
                pseudo_content=generated_pseudo_content,
                user_id=session.get('user_id') 
            )
            
            if store_success:
                print("✅ Data successfully stored to Milvus")
            else:
                print("❌ Warning: Failed to store data to Milvus")
        else:
            print("❌ Milvus client not available")

        return jsonify({ "pseudo_content": generated_pseudo_content })

    except requests.exceptions.RequestException as e:
        print("OpenRouter request failed:", e)
        return jsonify({"error": "Failed to connect to OpenRouter API."}), 500

    except Exception as e:
        print("Unexpected backend error:", e)
        return jsonify({"error": "Internal server error."}), 500

@generate_pseudo_api.route('/history', methods=['GET'])
def get_user_history():
    """Get user's pseudocode history from Milvus"""
    try:
        milvus_client = init_milvus_client()
        if not milvus_client:
            return jsonify({"error": "Milvus client not available"}), 500
        
        user_id = session.get('user_id', 'anonymous')
        
        results = milvus_client.query(
            collection_name=COLLECTION_NAME,
            filter=f"creator_user_id == '{user_id}'",
            output_fields=["id", "pseudocode_content", "description", "timestamp"],
            limit=50
        )
        
        formatted_results = []
        for result in results:
            formatted_results.append({
                "id": result.get("id"),
                "pseudocode_content": result.get("pseudocode_content"),
                "description": result.get("description"),
                "timestamp": result.get("timestamp")
            })
        
        return jsonify({"history": formatted_results})
        
    except Exception as e:
        print(f"Error retrieving history: {e}")
        return jsonify({"error": "Failed to retrieve history"}), 500

@generate_pseudo_api.route('/test-milvus', methods=['GET'])
def test_milvus():
    """Test Milvus connection and collection status"""
    try:
        milvus_client = init_milvus_client()
        if not milvus_client:
            return jsonify({"status": "error", "message": "Failed to initialize Milvus client"}), 500
        
        has_collection = milvus_client.has_collection(collection_name=COLLECTION_NAME)
        load_state = milvus_client.get_load_state(collection_name=COLLECTION_NAME) if has_collection else None
        
        stats = milvus_client.get_collection_stats(collection_name=COLLECTION_NAME) if has_collection else None
        
        return jsonify({
            "status": "success",
            "collection_exists": has_collection,
            "collection_name": COLLECTION_NAME,
            "load_state": load_state,
            "stats": stats,
            "milvus_uri": milvus_uri[:50] + "..." if len(milvus_uri) > 50 else milvus_uri
        })
        
    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": str(e),
            "collection_name": COLLECTION_NAME
        }), 500
def search_similar():
    """Search for similar pseudocode based on description"""
    try:
        milvus_client = init_milvus_client()
        if not milvus_client:
            return jsonify({"error": "Milvus client not available"}), 500
        
        data = request.json
        search_text = data.get("search_text", "").strip()
        
        if not search_text:
            return jsonify({"error": "Search text is required"}), 400
        
        search_embedding = generate_dummy_embedding(search_text, EMBEDDING_DIM)
        
        search_results = milvus_client.search(
            collection_name=COLLECTION_NAME,
            data=[search_embedding],
            output_fields=["pseudocode_content", "description", "timestamp"],
            limit=10
        )
        
        formatted_results = []
        for hits in search_results:
            for hit in hits:
                formatted_results.append({
                    "pseudocode_content": hit.get("entity", {}).get("pseudocode_content"),
                    "description": hit.get("entity", {}).get("description"),
                    "timestamp": hit.get("entity", {}).get("timestamp"),
                    "score": hit.get("distance")
                })
        
        return jsonify({"results": formatted_results})
        
    except Exception as e:
        print(f"Error searching: {e}")
        return jsonify({"error": "Failed to search"}), 500
