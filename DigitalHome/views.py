from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv 
from django.http import JsonResponse

import os
from groq import Groq
import sqlparse
import numpy as np
import pandas as pd
import mysql.connector
import json
import re



from rest_framework import generics
from .models import laptops
from .serializers import DeviceSerializer

load_dotenv()
#API used################
#os.environ['GROQ_API_KEY'] = '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'

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
            data = json.loads(request.body)
            prompt = data.get('prompt', '')
            context = {
                'prompt': prompt,
            }


    # Use the Llama3 70b model
    model = "llama3-70b-8192"
    #model = "gemma2-9b-it"

    # Get the Groq API key and create a Groq client
    groq_api_key = os.getenv('GROQ_API_KEY')
    client = Groq(
    api_key=groq_api_key
    )
    # Load the base prompt
    with open('DigitalHome/prompts/base_prompt.txt', 'r') as file:
        base_prompt = file.read()


    user_question = prompt
    if user_question:
        # Generate the full prompt for the AI
        full_prompt = base_prompt.format(user_question=user_question)

        # Get the AI's response as text output
        llm_response = chat_with_groq(client, full_prompt, model,{"type": "json_object"})
        context['llm_response'] = llm_response
        json_part = re.search(r'(\{.*\})', llm_response)
        json_str = json_part.group(0) 
        result_json = json.loads(json_str)
        if 'sql' in result_json:
                sql_query = result_json['sql']
                results_df = execute_mysql_query(sql_query)

                formatted_sql_query = sqlparse.format(sql_query, reindent=True, keyword_case='upper')

                summarization = get_summarization(client,user_question,results_df,model)
                context['summarization'] = summarization
        elif 'error' in result_json:
                context['error'] = result_json['error']

    #template = loader.get_template('suggest.html')    
    #return HttpResponse(template.render(context,request))
    return JsonResponse(context)  



#######################
def chat_with_groq(client, prompt, model,response_format):
    completion = client.chat.completions.create(
        model=model,
        messages=[
              {
                  "role": "user",
                  "content": prompt
              }
          ],
        )
    response_format=response_format
    return completion.choices[0].message.content



def execute_mysql_query(query):
    conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin@123",
            database="device"
        )
    
    try:
        # Execute the query and fetch the results
        cursor = conn.cursor(dictionary=True)  # Use dictionary=True to get results as dicts
        cursor.execute(query)
        query_result = cursor.fetchall()

        # Convert query result to a pandas DataFrame
        results_df = pd.DataFrame(query_result)
    finally:
        # Close the connection
        cursor.close()
        conn.close()

    return results_df



def remove_prefix(text):
        print(text)
        if '{"sql":' in text:
            i=text.index(':')
            text=text[i+1:]
            
        elif '{"error":' in text:
            text=text.replace('{"error":','')
        text=text.replace('}','')
        return text


def get_summarization(client, user_question, df, model):
    """
    This function generates a summarization prompt based on the user's question and the resulting data. 
    It then sends this summarization prompt to the Groq API and retrieves the AI's response.

    Parameters:
    client (Groqcloud): The Groq API client.
    user_question (str): The user's question.
    df (DataFrame): The DataFrame resulting from the SQL query.
    model (str): The AI model to use for the response.

    Returns:
    str: The content of the AI's response to the summarization prompt.
    """
    prompt = '''
      A user asked the following question pertaining to local database tables:
    
      {user_question}
    
      To answer the question, a dataframe was returned:
    
      Dataframe:
      {df}

    In a few sentences, summarize the data in the table as it pertains to the original user question. Avoid qualifiers like "based on the data" and do not comment on the structure or metadata of the table itself
  '''.format(user_question = user_question, df = df)

    # Response format is set to 'None'
    return chat_with_groq(client,prompt,model,None)

class DeviceList(generics.ListCreateAPIView):
    queryset = laptops.objects.all()  # Fetch all rows from the SQL table
    serializer_class = DeviceSerializer  # Specify the serializer class

