"""Handle all the conversation stuff"""
import datetime
import os

from dotenv import load_dotenv
from flask import jsonify, request
from supabase import create_client, Client


load_dotenv()


url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def new_message():
    """Handle sending a new message"""

    # Get the message from the request body
    data = request.json
    conversation_id = data.get('conversationId')
    message = data.get('message')
    user_id = data.get('userId')

    # Check that all required fields are present
    if conversation_id is None or message is None or user_id is None:
        return jsonify({"success": False, "error": "Error"}), 400

    # Set the conversation (which will create it if it doesn't exist)
    supabase.from_('conversations').upsert({
        'id': conversation_id,
        'user_id': user_id,
        'timestamp': datetime.datetime.now()
    })

    # Create a new message
    supabase.from_('messages').insert({
        'conversation_id': conversation_id,
        'sender': 'user',
        'message': message,
        'user_id': user_id,
        'timestamp': datetime.datetime.now()
    })

    return jsonify({"success": True, "response": "sending " + message, "conversationId": conversation_id}), 200
