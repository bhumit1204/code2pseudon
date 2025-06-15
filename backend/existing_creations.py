from flask import Blueprint, render_template
from pymilvus import MilvusClient
import dotenv
import os
import datetime

dotenv.load_dotenv()
milvus_uri = os.getenv("MILVUS_URI")
milvus_token = os.getenv("MILVUS_KEY")
COLLECTION_NAME = "code_data"

client = MilvusClient(uri=milvus_uri, token=milvus_token)

existing_creations_api = Blueprint('existing_creations', __name__)

@existing_creations_api.route('/existing-creations')
def existing_creations():
    try:
        results = client.query(
            collection_name=COLLECTION_NAME,
            filter="conversion_direction in [\"code_to_pseudo\", \"pseudo_to_code\", \"description_to_pseudocode\"]",
            output_fields=[
                "code_content",
                "pseudocode_content",
                "description",
                "timestamp",
                "conversion_direction",
                "creator_user_id",
                "code_language",
                "id"
            ]
        )

        creations = []
        for res in results:
            direction = res.get("conversion_direction")
            if not direction:
                continue

            if direction == "code_to_pseudo":
                content = res.get("pseudocode_content")
                type_ = "pseudo"
            elif direction == "pseudo_to_code":
                content = res.get("code_content")
                type_ = "code"
            else:
                content = res.get("pseudocode_content")
                type_ = "pseudo"

            timestamp = res.get("timestamp", 0)
            try:
                date_str = datetime.datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
            except:
                date_str = "Unknown"

            first_line = (content or '').strip().splitlines()[0] if content else ""
            fallback_title = first_line.replace("START", "").strip() or "Untitled"

            creations.append({
                "code": (content or "").strip(),
                "type": type_,
                "user_name": res.get("creator_user_id", "Anonymous"),
                "date": date_str,
                "title": fallback_title,
                "description": res.get("description", "")
            })

        return render_template(
            "existing-creations.html",
            title="Code2Pseudo - Explore Creations",
            creations=creations,
            year=datetime.datetime.now().year
        )

    except Exception as e:
        return f"Error fetching creations: {str(e)}"
