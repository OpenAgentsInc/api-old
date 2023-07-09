"""Handle all the conversation stuff"""
import datetime
import os
import uuid

from dotenv import load_dotenv
from flask import jsonify, request
from supabase import create_client, Client

from .llms.openai_helpers import complete, chat_complete


load_dotenv()


url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def get_conversation(conversation_id):
    """Return messages for a conversation"""
    messages = supabase.table('messages').select(
        '*').eq('conversation_id', conversation_id).order('timestamp.desc').execute()  # .order('timestamp', ascending=False) # .limit(50)
    return jsonify({"success": True, "messages": messages.data}), 200


def get_conversations(npub):
    """Return conversations and lastmessage for an npub"""

    print("npub is " + npub)

    conversations = supabase.table('conversations').select(
        '*').eq('user_npub', npub).execute()

    print(conversations.data)

    for conversation in conversations.data:
        messages = supabase.table('messages').select('*').eq('conversation_id',
                                                             conversation['id']).order('timestamp.desc').limit(1).execute()  #
        conversation['latest_message'] = messages.data[0]

    return jsonify({"success": True, "conversations": conversations.data}), 200


def new_message():
    """Handle sending a new message"""

    # Get the message from the request body
    data = request.json
    conversation_id = data.get('conversationId')
    message = data.get('message')
    user_message = message
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

    # Fetch the conversation from the database
    result = supabase.table('conversations').select().eq(
        'id', conversation_id).single()
    if result.error:
        return jsonify({"error": str(result.error)}), 404

    # Extract the conversation messages
    messages = result.data.get('messages', [])

    # Append the user's message to the messages
    messages.append({
        "role": "user",
        "content": user_message,
    })

    # Generate the assistant's response using chat_complete
    assistant_message = chat_complete(messages)

    # Append the assistant's response to the messages
    messages.append({
        "role": "assistant",
        "content": assistant_message,
    })

    # Update the conversation in the database
    result = supabase.table('conversations').update(
        {"messages": messages}).match({'id': conversation_id})
    if result.error:
        return jsonify({"error": str(result.error)}), 500

    # Return the assistant's response
    return jsonify({
        # "id": str(uuid4()),
        "conversationId": conversation_id,
        # "created": datetime.now().isoformat(),
        "role": "assistant",
        "response": assistant_message,
    }), 201

    # # Get the last 10 messages from the conversation
    # last_messages = supabase.table('messages').select("*").eq(
    #     'conversation_id', conversation_id).execute()  # .order('timestamp', ascending=False)

    # # Loop through messages, adding each to a string
    # convo_history = ''
    # for fbmessage in last_messages.data:
    #     print(fbmessage)
    #     convo_history += fbmessage['sender'] + \
    #         ': ' + fbmessage['message'] + '\n\n'

    # # If convo_history is greater than 1000 characters, truncate it and append "(...truncated)"
    # if len(convo_history) > 1000:
    #     convo_history = convo_history[:1000] + "(...truncated)"

    # prompt = 'You are Faerie, a magical faerie having a conversation with a user. You know a lot of things and are very good at producing code. Answer factual questions concisely. Only give the next answer of Faerie, nothing else, but it can be very long - like multiple paragraphs. \n\n Conversation History:\n' + convo_history + '\n\n faerie: '

    # completion_model = 'text-davinci-003'
    # tokens_response = 2000

    # response = complete(prompt, tokens_response, completion_model)

    # print(prompt)

    # # Create a new message
    # supabase.table('messages').insert({
    #     'id': uuid.uuid4().hex,
    #     'conversation_id': conversation_id,
    #     'sender': 'faerie',
    #     'message': response,
    #     'user_npub': npub,
    #     'timestamp': datetime.datetime.now().isoformat()
    # }).execute()

    # return jsonify({"success": True, "response": response, "conversationId": conversation_id}), 200
