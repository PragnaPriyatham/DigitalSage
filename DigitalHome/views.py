from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv 

import os
import json
import re
import sqlparse
import pandas as pd
import mysql.connector
from groq import Groq
from rest_framework import generics
from .models import laptops
from .serializers import DeviceSerializer

load_dotenv()

# Setup logging
import logging
logger = logging.getLogger(__name__)

def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

def inputprompt(request):
    template = loader.get_template('inputprompt.html')
    return HttpResponse(template.render())
@csrf_exempt
def inputis(request):
    if request.method == 'POST':
        
            # Handle different content types
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            elif request.content_type == 'application/x-www-form-urlencoded':
                data = request.POST  # Django automatically parses form-encoded data
            else:
                return JsonResponse({"error": "Unsupported content type"}, status=400)

            prompt = data.get('prompt', '').strip()  # Use .strip() to remove leading/trailing spaces and line breaks
            if not prompt:
                return JsonResponse({"error": "Prompt not provided"}, status=400)

            # Continue processing...
            # Example: Use the sanitized prompt for your logic here
            context = {'prompt': prompt}

            # Step 1: Retrieve relevant data from the database (retriever step)
            relevant_data = retrieve_device_data(prompt)
            if relevant_data is not None:
                summarization = generate_rag_response(prompt, relevant_data)
                context['summarization'] = summarization
            else:
                context['error'] = "No relevant data found."
            return JsonResponse(context)



# Retriever function - retrieves data from MySQL database based on user input
def retrieve_device_data(user_question):
    # Set up Groq client
    groq_api_key = os.getenv('GROQ_API_KEY')
    client = Groq(api_key=groq_api_key)

    # Define the model to use
    model = "llama3-70b-8192"
    with open('DigitalHome/prompts/base_prompt.txt', 'r') as file:
        base_prompt = file.read()
    if user_question:
        # Generate the full prompt for the AI
        full_prompt = base_prompt.format(user_question=user_question)

    # Get the SQL query or error from Groq
    llm_response = chat_with_groq(client, full_prompt, model,{"type": "json_object"})
    result_json = extract_sql_from_llm_response(llm_response)
    print("$$$$$$$$$$$$"+llm_response)
    if 'sql' in result_json:
        sql_query = result_json['sql']
        sql_query = sqlparse.format(sql_query, reindent=True, keyword_case='upper')
        return execute_mysql_query(sql_query)
    elif 'error' in result_json:
        return None


# Generator function - generates a natural language response based on retrieved data
def generate_rag_response(user_input, data):
    # Load the Groq API key and create a Groq client
    groq_api_key = os.getenv('GROQ_API_KEY')
    client = Groq(api_key=groq_api_key)
    model = "llama3-70b-8192"  # Generative model used

    # Create a prompt for the summarization
    prompt = f'''
        A user asked: "{user_input}"

        Here are some relevant laptops we found:
        {data.to_string(index=False)}

        Can you provide a personalized recommendation based on the data above?
    '''

    # Generate the natural language response
    llm_response = chat_with_groq(client, prompt, model, {"type": "json_object"})
    return llm_response

def chat_with_groq(client, prompt, model, response_format):
    completion = client.chat.completions.create(
        model=model,
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )
    return completion.choices[0].message.content

def execute_mysql_query(query):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin@123",
        database="device"
    )
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        query_result = cursor.fetchall()
        results_df = pd.DataFrame(query_result)
    finally:
        cursor.close()
        conn.close()
    return results_df



def extract_sql_from_llm_response(llm_response):
    # Regular expression to match JSON-like structures
    json_pattern = r'\{[^{}]*\}'  # Match the first JSON-like structure
    match = re.search(json_pattern, llm_response, re.DOTALL)

    if match:
        json_part = match.group(0)  # Extract the matched JSON
        
        # Normalize the SQL string within the JSON
        try:
            # Replace newline characters and extra spaces in the SQL string
            json_part = json_part.replace('\n', ' ').replace('  ', ' ').strip()
            
            # Ensure double quotes for JSON compatibility
            json_part = re.sub(r'(["\'])(.*?)\1', r'"\2"', json_part)  # Normalize quotes
            
            # Load the JSON string
            result_json = json.loads(json_part)
            return result_json
        
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
            return None
    else:
        print("No valid JSON found in the response.")
        return None

class DeviceList(generics.ListCreateAPIView):
    queryset = laptops.objects.all()
    serializer_class = DeviceSerializer
