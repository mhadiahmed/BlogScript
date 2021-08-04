from genericpath import isfile
from django.conf import Settings
from blog_script.settings import BASE_DIR
import os
from posts.utils import random_string_generator

FILE_PATH = f"{BASE_DIR}/core/templates/core/"
TEMPLATE_PATH = "core/"

def create_flat_page_template(file_name):
    if check_file_exists(file_name):
        file_name = f'{file_name}-{random_string_generator(size=4)}'.lower()
        file_creation(f'{FILE_PATH}{file_name}.html','w')
        return f"{file_name}.html"
    else:
        file_creation(f'{FILE_PATH}{file_name.lower()}.html','w')
        return f"{file_name.lower()}.html"
        

def file_creation(file_path,status):
    try:
        with open(file_path, status) as f:
            f.write(file_contet_template())
            f.close()
    except:
        pass


def file_contet_template():
    return """
        {% extends 'base.html' %}


        {% block title %}
        {{pages.title}}
        {% endblock title %}
        {% block content %}
        {{pages.content}}
        {% endblock content %}
    """
    
def delete_flat_page_template(file_name):
    
    try:
        os.remove(f"{FILE_PATH}{file_name}.html")
    except FileNotFoundError as e:
        pass

# check if the file exists
def check_file_exists(file_name):
    return isfile(f"{FILE_PATH}{file_name.lower()}.html")

