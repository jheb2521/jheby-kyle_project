#!/usr/bin/env python3
"""
Simple Flask server to serve the static frontend and proxy chat requests to OpenAI.

Security notes:
- The server reads the OpenAI API key from the environment variable `OPENAI_API_KEY`.
- Do NOT store your API key in source files or paste it into chat. Set it locally in your shell.

Run:
  pip install -r requirements.txt
  set the env var (PowerShell): $env:OPENAI_API_KEY = 'sk-...'
  python server.py

Then open http://127.0.0.1:5000 in your browser.
"""
import os
import json
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder="frontend", static_url_path="")


def rule_based_response(text: str) -> str:
    t = text.lower()
    if any(x in t for x in ["hello", "hi", "hey"]):
        return "Hi there! What kind of thrift item are you looking for?"
    if "vintage" in t or "identify" in t or "what is this" in t:
        return "Tell me a bit about the item's markings, materials, and any labels — I can help identify it."
    if "value" in t or "estimate" in t or "worth" in t:
        return "I can give a rough estimate if you tell me the brand, condition, and approximate age."
    if "tips" in t or "thrift" in t:
        return "Look for solid construction, classic brands, and minimal staining — always inspect seams and zippers."
    if "bye" in t or "thanks" in t:
        return "You're welcome — happy thrifting!"
    return "I don't have an exact answer for that, but I can help if you give more details."


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/<path:path>')
def static_proxy(path):
    # serve static files
    return send_from_directory(app.static_folder, path)


@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.get_json() or {}
    message = data.get('message', '')
    if not message:
        return jsonify({'error': 'no message'}), 400

    api_key = os.environ.get('OPENAI_API_KEY')
    if api_key:
        try:
            import openai
            openai.api_key = api_key
            # prefer ChatCompletion if available
            try:
                resp = openai.ChatCompletion.create(
                    model='gpt-3.5-turbo',
                    messages=[{'role': 'user', 'content': message}],
                    max_tokens=250,
                )
                reply = resp.choices[0].message.content.strip()
            except Exception:
                # fallback to text completion
                resp = openai.Completion.create(
                    engine='text-davinci-003',
                    prompt=f"You are a helpful thrift-shopping assistant. Reply concisely to: {message}",
                    max_tokens=250,
                )
                reply = resp.choices[0].text.strip()
            return jsonify({'reply': reply})
        except Exception as e:
            # log error server-side and fall back to rule-based
            print('OpenAI request error:', str(e))

    # fallback to local rule-based reply
    reply = rule_based_response(message)
    return jsonify({'reply': reply})


if __name__ == '__main__':
    # Only for local development. Do not use this server in production as-is.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port, debug=True)
