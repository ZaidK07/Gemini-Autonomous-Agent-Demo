import os
from google.genai import types, Client
import requests
from simplegmail import Gmail
import feedparser
import urllib.parse
from googlenewsdecoder import gnewsdecoder
from newspaper import Article

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
GEMINI_MAIN_MODEL = os.environ.get('GEMINI_MAIN_MODEL')
GEMINI_QUICK_MODEL = os.environ.get('GEMINI_QUICK_MODEL')
SEARCH_API_KEY = os.environ.get('SEARCH_API_KEY')
SEARCH_ENGINE_ID = os.environ.get('SEARCH_ENGINE_ID')
PRIMARY_USER_MAIL = os.environ.get('PRIMARY_USER_MAIL')

GEMINI_CLIENT = Client(api_key=GEMINI_API_KEY)

gmail_client = Gmail(
    client_secret_file = "./gmail_credentials/client_secret.json",
    creds_file="./gmail_credentials/gmail_token.json"
)


def get_default_chat_history_list():
    return [{
        'role': 'system',
        'content': 'Keep response length same as a natural conversation. Do not exceed the natural human response length. Be concise and to the point.'
    }]


def web_search_tool(query):
    print("Search Query ----->",query)
    base_url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        'key': SEARCH_API_KEY,
        'cx': SEARCH_ENGINE_ID,
        'q': query,
        'num': 10
    }
    try:
        data = requests.get(base_url, params=params).json()
        # print("DATA:::::",data)

        search_items_list = []
        for item in data.get('items', []):
            search_items_list.append({
                'title': item['title'],
                'link': item['link'],
                'snippet': item['snippet']
            })
        return search_items_list

    except Exception as e:
        return f"Error during web search: {e}"


def email_read_tool():

    messages = gmail_client.get_unread_inbox()

    messages_list = []
    for message in messages:
        message.mark_as_read()

        messages_list.append({
            'sender': message.sender,
            'subject_line': message.subject,
            'body': message.plain
        })
    if len(messages_list) == 0:
        return "No unread emails found."
    return messages_list


def email_send_tool(to,subject,body):
    params = {
        "to": to,
        "sender": PRIMARY_USER_MAIL,
        "subject": subject if subject else "No Subject",
        "msg_plain": body
    }
    gmail_client.send_message(**params)
    return {'message': 'Email sent successfully'}


def get_news_tool(query):
    print(f"Model news search query: {query}")

    query = urllib.parse.quote(query)
    rss_url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(rss_url)

    results = []
    for entry in feed.entries[:5]:
        try:
            decoded = gnewsdecoder(entry.link) # this will decode the encoded url

            if decoded.get("status"):
                real_url = decoded["decoded_url"]
            else:
                continue # skipping if decoding url failed

            article = Article(real_url)
            article.download()
            article.parse()

            results.append({
                "title": entry.title,
                "link": real_url,
                "content": article.text[:1500]
            })

        except Exception as e:
            print(f"Skipping: {e}")
            continue

    return results


def call_selected_tool(func_call_variable):
    function_name = func_call_variable.name

    if function_name == "web_search_tool":
        function_data = web_search_tool(func_call_variable.args['query'])
        # print(function_data)

    elif function_name == "email_read_tool":
        function_data = email_read_tool()
        # print(function_data)

    elif function_name == "email_send_tool":
        try:
            email_send_tool(func_call_variable.args['to'], func_call_variable.args['subject'], func_call_variable.args['body'])
            function_data = "{'message': 'Email has been sent successfully!'}"
        except Exception as e:
            function_data = {'message': f'Error sending email: {str(e)}'}

    elif function_name == "get_news_tool":
        function_data = get_news_tool(func_call_variable.args['query'])
        # print(function_data)

    else:
        function_data = {'message': f'Unknown function: {function_name}'}

    return function_data