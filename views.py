from flask import request
from flask_restful import Resource
from utils import *
import os
from tool_declarations import *
import json
from datetime import datetime
import uuid

os.makedirs('./chats', exist_ok=True)
os.makedirs('./gmail_credentials', exist_ok=True)

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
GEMINI_MAIN_MODEL = os.environ.get('GEMINI_MAIN_MODEL')
GEMINI_QUICK_MODEL = os.environ.get('GEMINI_QUICK_MODEL')

GEMINI_CLIENT = Client(api_key=GEMINI_API_KEY)

CHAT_HISTORY_LIST = get_default_chat_history_list()
GLOBAL_CHAT_ID = None

gemini_config = types.GenerateContentConfig(
    tools=[types.Tool(function_declarations=[
        web_search_tool_declaration,
        email_read_tool_declaration,
        email_send_tool_declaration,
        get_news_tool_declaration
    ])]
)

class GeminiChat(Resource):
    def post(self):
        json_data = request.get_json()
        user_prompt = json_data.get('user_prompt',None)

        response = GEMINI_CLIENT.models.generate_content(
            model = GEMINI_MAIN_MODEL,
            contents = f"Previous Chat History:{CHAT_HISTORY_LIST}\nUser:{user_prompt}",
            config = gemini_config
        )

        if response.function_calls:
                func_call = response.function_calls[0]
                print("Model called:", func_call.name)

                function_data = call_selected_tool(func_call_variable = func_call)

                final_response = GEMINI_CLIENT.models.generate_content(
                    model = GEMINI_MAIN_MODEL,
                    contents = f"Previous Chat History:{CHAT_HISTORY_LIST}\nUser:{user_prompt}\nFunction Data: {function_data}"
                )
                CHAT_HISTORY_LIST.append({
                    'role': 'user',
                    'content': user_prompt
                })
                CHAT_HISTORY_LIST.append({
                    'role': 'assistant',
                    'content': final_response.text
                })
                return final_response.text, 200

        CHAT_HISTORY_LIST.append({
            'role': 'user',
            'content': user_prompt
        })
        CHAT_HISTORY_LIST.append({
            'role': 'assistant',
            'content': response.text
        })
        return response.text, 200


class NewChat(Resource):
    def get(self):
        global CHAT_HISTORY_LIST
        global GLOBAL_CHAT_ID
        CHAT_HISTORY_LIST = CHAT_HISTORY_LIST[1:]

        if GLOBAL_CHAT_ID is None:
            chat_id = str(uuid.uuid4().hex[-12:])
        else:
            chat_id = GLOBAL_CHAT_ID
            GLOBAL_CHAT_ID = None

        json_dict = {
            'chat_id': chat_id,
            'date': str(datetime.now().strftime('%d/%m/%Y||%H:%M:%S')),
            'messages': CHAT_HISTORY_LIST
        }

        CHAT_HISTORY_LIST = get_default_chat_history_list()

        if len(json_dict['messages']) > 1:
            with open(f"./chats/{json_dict['chat_id']}.json", "w") as f:
                json.dump(json_dict, f, indent=4)

        return json_dict, 200


class LoadChat(Resource):
    def post(self):
        global CHAT_HISTORY_LIST
        global GLOBAL_CHAT_ID

        json_data = request.get_json()
        chat_id = json_data['chat_id']
        print(f"Loading chat with ID: {chat_id}")
        GLOBAL_CHAT_ID = chat_id

        try:
            with open(f"./chats/{chat_id}.json", "r") as f:
                json_dict = json.load(f)
                CHAT_HISTORY_LIST = json_dict['messages']
                # we loaded the chat history list from file so now it is a global variable instead of new chat list
                # we can now use the global variable CHAT_HISTORY_LIST for GeminiChat API
            return json_dict, 200

        except FileNotFoundError:
            return {'message': 'Chat not found'}, 404


class GetAllChats(Resource):
    def get(self):
        chats = []
        files = os.listdir("./chats")

        for file_name in files:
            try:
                with open(f"./chats/{file_name}", "r") as f:
                    data = json.load(f)
                    chats.append({
                        'chat_id': data.get('chat_id', 'unknown'),
                        'date': data.get('date', ''),
                    })
            except Exception:
                continue

        chats.sort(key=lambda x: x.get('date', ''), reverse=True)
        # print(chats)
        return chats, 200