"""App entry point"""
import os
from flask import Flask, jsonify, request
from api.conversations import get_conversation, get_conversations, new_message

application = Flask(__name__)


@application.route('/')
def index():
    """Placeholder route"""
    return 'Hello, World!'


@application.route('/message', methods=['POST'])
def message():
    """Handle sending a new message to a conversation."""
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        return new_message()
    else:
        return jsonify({"success": False, "error": "Invalid content type"}), 400


@application.route('/user/<npub>/conversations', methods=['GET'])
def go_get_conversations(npub):
    """Fetch conversations for a user npub"""
    return get_conversations(npub)


@application.route('/conversation/<conversationId>', methods=['GET'])
def go_get_conversation(conversationId):
    return get_conversation(conversationId)


@application.route('/recording', methods=['POST'])
def upload_recording():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio = request.files['audio']

    if audio.filename == '':
        return jsonify({'error': 'No audio file provided'}), 400

    if audio:
        # Save audio file to uploads folder
        filename = os.path.join('uploads', audio.filename)
        audio.save(filename)

        return jsonify({'success': True}), 201
