from flask import Flask, request, jsonify, render_template
from langchain.llms import OpenAI
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from dotenv import load_dotenv
import os
load_dotenv()  # This loads the .env variables into the environment
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)

# Setup LangChain and SQLite
db = SQLDatabase.from_uri("sqlite:///afl.db")
llm = OpenAI(temperature=0, verbose=True)
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    question = data['question']
    result = db_chain.run(question)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
