"""Handle all the conversation stuff"""
import datetime
import os
import uuid

from dotenv import load_dotenv
from flask import jsonify, request
from supabase import create_client, Client


load_dotenv()


url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def get_conversations(npub):
    """Return conversations and lastmessage for an npub"""
    conversations = supabase.table('conversations').select(
        '*').filter('user_npub', npub).execute()

    for conversation in conversations.data:
        messages = supabase.table('messages').select('*,').filter('conversation_id',
                                                                  conversation['id']).order('timestamp', ascending=False).limit(1).execute()
        conversation['latest_message'] = messages.data[0]

    return jsonify({"success": True, "conversations": conversations.data}), 200


def new_message():
    """Handle sending a new message"""

    # Get the message from the request body
    data = request.json
    conversation_id = data.get('conversationId')
    message = data.get('message')
    npub = data.get('npub')

    # Check that all required fields are present
    if conversation_id is None or message is None or npub is None:
        return jsonify({"success": False, "error": "Error"}), 400

    # Upsert this user into users table
    supabase.table('users').upsert({
        'name': 'User ' + npub,
        'npub': npub,
    }).execute()

    # Set the conversation (which will create it if it doesn't exist)
    supabase.table('conversations').upsert({
        'id': conversation_id,
        'user_npub': npub,
        # 'timestamp': datetime.datetime.now().isoformat()
    }).execute()

    # Create a new message
    supabase.table('messages').insert({
        'id': uuid.uuid4().hex,
        'conversation_id': conversation_id,
        'sender': 'user',
        'message': message,
        'user_npub': npub,
        'timestamp': datetime.datetime.now().isoformat()
    }).execute()

    return jsonify({"success": True, "response": "sending " + message, "conversationId": conversation_id}), 200
