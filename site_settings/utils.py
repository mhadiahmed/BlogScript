from genericpath import isfile
from django.conf import Settings
from blog_script.settings import BASE_DIR
import os

def create_flat_page_template(file_name):
    path = f"{BASE_DIR}/core/templates/core/{file_name.lower()}.html"
    with open(f'{path}', 'w') as f:
        f.write(file_contet_template())
        f.close()
        return f"core/{file_name.lower()}.html"

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
    path = f"{BASE_DIR}/core/templates/core/{file_name.lower()}.html"
    
    try:
        os.remove(path)
    except FileNotFoundError as e:
        pass