import json

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.conf import settings
import os
import datetime
from blog import get_info
base_dir = settings.BASE_DIR


def index(request):
    blog_list_id = os.listdir(os.path.join(base_dir, 'blog/blogs'))
    blog_info_list = []
    for blog_id in blog_list_id:
        blog_json = get_info.get_json(blog_id)
        blog_name = "NULL"
        if not blog_json is None:
            blog_name = blog_json['name']
        blog_info_list.append([blog_id, blog_name])
    con = {
        "blog_info_list": blog_info_list,
    }
    return render(request, 'blog/blog_list.html', con)


def blog_view(request, blog_id):
    blog_file_path = os.path.join(base_dir, f'blog/blogs/{blog_id}')
    if not os.path.exists(blog_file_path):
        return HttpResponse("404 Not Found.")
    con = {}
    with open(os.path.join(blog_file_path, 'main.md'), 'r', encoding='utf-8') as f:
        con['content'] = f.read()
    blog_json = get_info.get_json(blog_id)
    con['title'] = blog_json['name']
    con['create_time'] = blog_json['create_time']
    con['update_time'] = blog_json['update_time']
    return render(request, 'blog/blog_view.html', con)


def upload_add(request):
    if request.POST:
        blog_name = request.POST['blog_name']
        blog_con = request.POST['blog_con'].replace('\r', '')
        blog_list_id = os.listdir(os.path.join(base_dir, 'blog/blogs'))
        blog_list_id.sort(key=int)
        blog_id = int(blog_list_id[-1]) + 1
        blog_path = os.path.join(base_dir, f"blog/blogs/{blog_id}")
        os.mkdir(blog_path)
        with open(os.path.join(blog_path, "main.md"), "w", encoding='utf-8') as f:
            f.write(blog_con)
        time_now = datetime.datetime.now()
        time_now_str = time_now.strftime('%Y-%m-%d %H:%M:%S')
        blog_json = {
            "name": blog_name,
            "create_time": time_now_str,
            "update_time": time_now_str
        }
        with open(os.path.join(blog_path, "data.json"), "w", encoding='utf-8') as f:
            json.dump(blog_json, f, indent=2)
        return redirect(f"/blog/view/{blog_id}")
    return HttpResponse("404 Not Found.")


def upload_update(request):
    if request.POST:
        blog_name = request.POST['blog_name']
        blog_con = request.POST['blog_con'].replace('\r', '')
        blog_list_id = os.listdir(os.path.join(base_dir, 'blog/blogs'))
        blog_list_id.sort(key=int)
        blog_id = int(blog_list_id[-1])
        blog_path = os.path.join(base_dir, f"blog/blogs/{blog_id}")
        os.mkdir(blog_path)
        with open(os.path.join(blog_path, "main.md"), "w", encoding='utf-8') as f:
            f.write(blog_con)
        time_now = datetime.datetime.now()
        time_now_str = time_now.strftime('%Y-%m-%d %H:%M:%S')
        blog_json = get_info.get_json(blog_id)
        blog_json["name"] = blog_name
        blog_json["update_time"] = time_now_str
        with open(os.path.join(blog_path, "data.json"), "w", encoding='utf-8') as f:
            json.dump(blog_json, f, indent=2)
        return redirect(f"/blog/view/{blog_id}")
    return HttpResponse("404 Not Found.")

