from flask import Flask, request, jsonify, render_template

from langchain.llms import OpenAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
import os
import re
import logging
logging.basicConfig(level=logging.INFO)

TEMPLATE = """You know SQL and have access to an SQLite3 database of AFL statistics.
Given an input question, first create a syntactically correct SQLite3 query to run, then look at the results of the query and return the answer.

Only use the following tables:

player_stats and game.

Few shot examples:
Question: "How many goals did Zak Butters kick in 2023?"
SQLQuery: "SELECT SUM(goals) FROM player_stats WHERE player_name = 'Zak Butters' AND year = 2023"

Question: "How many goals did Max Gawn kick last year?"
SQLQuery = "SELECT SUM(goals) FROM player_stats WHERE player_name = 'Max Gawn' AND year = strftime('%Y', date('now', '-1 year'))"

Whenever you are asked a question, please return additional information that might be implied by the question, such as what year or round a statistic is from.

If you get no result, or an empty table, from the query then return "No result" and suggest a new query to run.

Question: {user_question}"""

load_dotenv()  # This loads the .env variables into the environment
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

application = Flask(__name__)

# Setup LangChain and SQLite
db = SQLDatabase.from_uri("sqlite:///afl.db")
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)

'''Capture Print'''
import io
import sys
from contextlib import redirect_stdout

def capture_print(func):
    def wrapper(*args, **kwargs):
        temp_out = io.StringIO()
        with redirect_stdout(temp_out):
            result = func(*args, **kwargs)
        captured_output = temp_out.getvalue()
        
        # Extract SQL query using regular expression
        sql_query_match = re.search(r"sql_db_query` with `([^`]*)", captured_output)
        if sql_query_match:
            sql_query = sql_query_match.group(1)  # Extracted SQL query
        else:
            sql_query = "No query found"

        return result, sql_query
    return wrapper

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/query', methods=['POST'])
def query():
    try:
        logger = logging.getLogger("query_route")
        data = request.json
        logger.info(f"Data received: {data}")

        question = data['question']
        logger.info(f"Question asked: {question}")

        @capture_print
        def query_internal():
            return agent_executor.invoke(question)

        result, captured_output = query_internal()
        logger.info("Captured output from db_chain.run: %s", captured_output)
        logger.info(f"Result: {result}")

        return jsonify({"answer": result['output'], "sql_query": captured_output})

    except Exception as e:
        return jsonify("Sorry, I couldn't quite figure that one out. Try rephrasing your question, or come back later.")

if __name__ == '__main__':
    application.run(debug=True)
