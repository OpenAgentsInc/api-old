"""Handle all the conversation stuff"""
from flask import jsonify, request


def new_message():
    """Handle sending a new message"""
    # Get the message from the request body
    data = request.json
    # conversationId = data.get('conversationId')
    # conversationType = data.get('conversationType')
    message = data.get('message')
    # userId = data.get('userId')
    # plan = data.get('plan')

    return jsonify({"success": True, "response": "sending " + message}), 200
