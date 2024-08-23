import os
import json
from django.conf import settings
base_dir = settings.BASE_DIR


def get_json(blog_id):
    file_path = os.path.join(base_dir, f"blog/blogs/{blog_id}/data.json")
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r", encoding='utf-8') as f:
        con = json.load(f)
    return con

