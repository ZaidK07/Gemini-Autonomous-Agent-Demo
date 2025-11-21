from views import *
from app import app, api

api.add_resource(GeminiChat, '/gemini-chat')
api.add_resource(NewChat, '/new-chat')
api.add_resource(LoadChat, '/load-chat')
api.add_resource(GetAllChats, '/all-chats')
