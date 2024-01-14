from django.http import JsonResponse
import pyrebase
from django.views.decorators.csrf import csrf_exempt
import os
import uuid
import json
from django.shortcuts import render

import requests
from django.shortcuts import render
from django.http import HttpResponse
from pathlib import Path


config = {
    "apiKey": "AIzaSyBLv1DiRB6egmpaoIKfjODXZF5fYheQKIM",
    "authDomain": "realtimedatabasetest-f226a.firebaseapp.com",
    "databaseURL": "https://realtimedatabasetest-f226a-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "realtimedatabasetest-f226a",
    "storageBucket": "realtimedatabasetest-f226a.appspot.com",
    "messagingSenderId": "348704796176",
    "appId": "1:348704796176:web:b19a37e276fd097a2ce495",
}

# Initialize Firebase
firebase = pyrebase.initialize_app(config)

# Get a reference to the Firebase Realtime Database
db = firebase.database()
storage = firebase.storage()


def get_components_data():
    try:
        # Retrieve data from the "UIcomponentsTable" node
        return db.child("UIcomponentsTable").get().val() or {}

    except Exception as e:
        # Handle exceptions (e.g., network issues, database errors)
        return {'error': str(e)}

def get_hero_data(request):
    components_data = get_components_data()
    return JsonResponse({'hero': components_data.get('hero', [1, 2, 3])})

def get_navbar_data(request):
    components_data = get_components_data()
    return JsonResponse({'navbar': components_data.get('navbar', [1, 2, 3, 4])})

def get_footer_data(request):
    components_data = get_components_data()
    return JsonResponse({'footer': components_data.get('footer', [1, 2, 3, 4])})

def get_features_data(request):
    components_data = get_components_data()
    return JsonResponse({'features': components_data.get('features', [1, 2, 3, 4])})

def get_website_by_uuid(request, website_uuid):
    try:
        # Retrieve the URL from the "websites" table based on the provided UUID
        website_data = db.child("websites").child(website_uuid).get().val()

        
        if website_data:
            website_url = website_data.get('url')
            # Fetch HTML content from the URL
            response = requests.get(website_url)
            response.raise_for_status()  # Raise an exception for bad responses

            # Render the fetched HTML
            return HttpResponse(response.text, content_type='text/html')
        else:
            return JsonResponse({'error': 'Website not found for the given UUID'})

    except Exception as e:
        # Handle exceptions
        return JsonResponse({'error': str(e)})
    
@csrf_exempt
def get_website_url(request):
    try:
        # This is a placeholder function
        # In a real-world scenario, you'd implement logic to generate and return the URL based on the HTML content

        # For demonstration purposes, let's assume the URL is the same as the HTML content
        
        html_content = None
        if 'file' in request.FILES:
            uploaded_file = request.FILES['file']
            html_content = uploaded_file.read().decode('utf-8')
        else:
            html_content = request.body.decode('utf-8')
            html_content = str(json.loads(html_content).get("htmlContent", ''))
        # Generate a random filename with UUID
        filename = str(uuid.uuid4()) + ".html"

        # Create a temporary directory and write the HTML content to a file
        temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp")
        os.makedirs(temp_dir, exist_ok=True)
        file_path = os.path.join(temp_dir, filename)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(html_content)

        # Upload the file to Firebase Storage
        storage.child("websites/" + filename).put(file_path)

        # Get the public URL of the uploaded file
        generated_url = storage.child("websites/" + filename).get_url(None)
        website_uuid = str(uuid.uuid4())
        db.child("websites").child(website_uuid).set({'url': generated_url})

        return JsonResponse({'fetchedUrl': website_uuid})

    except Exception as e:
        # Handle exceptions
        return JsonResponse({'error': str(e)})