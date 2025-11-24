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

# runtime-held API key (keeps key out of files). Initialized from env if present.
runtime_api_key = os.environ.get('OPENAI_API_KEY')


def _is_local_request():
    # Basic check to ensure admin endpoints are only callable from localhost
    addr = request.remote_addr
    return addr in ('127.0.0.1', '::1', 'localhost')


def rule_based_response(text: str) -> str:
    t = (text or '').lower()

    # quick per-model laptop info map (local responses)
    info_map = {
        'macbook air': 'MacBook Air — Apple M1/M2-based ultralight laptop. Great battery life, fanless designs on M1/M2, typically 8–16GB RAM depending on config. Good for everyday productivity and light creative work.',
        'dell xps 13': 'Dell XPS 13 — compact 13-inch Windows laptop with premium build and narrow bezels. Popular with developers and professionals; options for high-res displays and Intel CPUs.',
        'lenovo thinkpad x1 carbon': 'Lenovo ThinkPad X1 Carbon — business-class ultrabook with excellent keyboard, robust chassis, and strong battery life. Often praised for durability and enterprise features.',
        'hp spectre x360': 'HP Spectre x360 — convertible 2-in-1 with touchscreen and stylus support on some models. Sleek design, good performance for productivity, and flexible hinge for tablet mode.'
    }

    # greetings
    if any(x in t for x in ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]):
        return "Hi there! What kind of thrift item are you looking for?"

    # if user mentions a specific model, return the model info
    for name, info in info_map.items():
        if name in t:
            return info

    # laptop choices: return a dict with choices so caller can render buttons
    if 'laptop' in t:
        choices = [
            'MacBook Air',
            'Dell XPS 13',
            'Lenovo ThinkPad X1 Carbon',
            'HP Spectre x360'
        ]
        return {'reply': 'Which kind of laptop are you interested in? Choose one:', 'choices': choices}

    if "vintage" in t or "identify" in t or "what is this" in t:
        return "Tell me a bit about the item's markings, materials, and any labels — I can help identify it."
    if "value" in t or "estimate" in t or "worth" in t:
        return "I can give a rough estimate if you tell me the brand, condition, and approximate age."
    if "tips" in t or "thrift" in t:
        return "Look for solid construction, classic brands, and minimal staining — always inspect seams and zippers."
    if "bye" in t or "thanks" in t:
        return "You're welcome — happy thrifting!"

    # laptop detection handled separately; provide a generic fallback
    return "I don't have an exact answer for that, but I can help if you give more details about the thrift item."


@app.route('/admin/set_key', methods=['POST'])
def admin_set_key():
    """Set the OpenAI API key for the running server process at runtime.

    Security: requires an admin token (set in env `ADMIN_TOKEN`) and only
    accepts requests from localhost.
    """
    if not _is_local_request():
        return jsonify({'error': 'admin endpoints only allowed from localhost'}), 403
    admin_token = request.headers.get('X-Admin-Token') or (request.get_json() or {}).get('admin_token')
    if not admin_token or admin_token != os.environ.get('ADMIN_TOKEN'):
        return jsonify({'error': 'unauthorized'}), 401
    payload = request.get_json() or {}
    key = payload.get('key')
    if not key:
        return jsonify({'error': 'no key provided'}), 400
    global runtime_api_key
    runtime_api_key = key
    return jsonify({'ok': True})


@app.route('/admin/clear_key', methods=['POST'])
def admin_clear_key():
    if not _is_local_request():
        return jsonify({'error': 'admin endpoints only allowed from localhost'}), 403
    admin_token = request.headers.get('X-Admin-Token') or (request.get_json() or {}).get('admin_token')
    if not admin_token or admin_token != os.environ.get('ADMIN_TOKEN'):
        return jsonify({'error': 'unauthorized'}), 401
    global runtime_api_key
    runtime_api_key = None
    return jsonify({'ok': True})


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
    action = data.get('action')
    selection = data.get('selection')
    local_flag = data.get('local', False) or os.environ.get('FORCE_LOCAL', '0') == '1'
    if not message:
        return jsonify({'error': 'no message'}), 400

    # quick greeting handler: reply to simple salutations without requiring OpenAI
    greetings = ["hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening"]
    low = message.lower()
    if any(g in low for g in greetings) and action != 'select':
        return jsonify({'reply': "Hello! I'm QUPAL, your thrift shopping AI assistant. What are you looking for today?"})

    # prefer runtime_api_key (set via admin endpoint), otherwise read env on start
    api_key = runtime_api_key or os.environ.get('OPENAI_API_KEY')
    # If client requested local responses or server is configured to force local, use local responder
    if local_flag or not api_key:
        # Handle selection action (laptop info) locally
        if action == 'select' and selection:
            info_map = {
                'MacBook Air': 'MacBook Air — Apple M1/M2, lightweight, great battery life, starts around 8GB RAM. Good for everyday use and light creative work.',
                'Dell XPS 13': 'Dell XPS 13 — compact 13-inch Windows laptop, premium build, excellent screen options. Good for developers and professionals.',
                'Lenovo ThinkPad X1 Carbon': 'ThinkPad X1 Carbon — business laptop, excellent keyboard, durable chassis, available with Intel CPUs and long battery life.',
                'HP Spectre x360': 'HP Spectre x360 — convertible 2-in-1, sleek design, touch screen, good performance for productivity tasks.'
            }
            reply = info_map.get(selection, 'Sorry, I do not have details for that model.')
            return jsonify({'reply': reply})

        # If message mentions laptop, return choices
        if 'laptop' in (message or '').lower():
            choices = [
                'MacBook Air',
                'Dell XPS 13',
                'Lenovo ThinkPad X1 Carbon',
                'HP Spectre x360'
            ]
            return jsonify({'reply': 'Which kind of laptop are you interested in? Choose one:', 'choices': choices})

        # Otherwise return local rule-based reply (function may return dict)
        local_resp = rule_based_response(message)
        if isinstance(local_resp, dict):
            return jsonify(local_resp)
        return jsonify({'reply': local_resp})

    if api_key:
        try:
            import openai
            openai.api_key = api_key
            # Enforce thrift-only behavior via system prompt
            system_prompt = (
                "You are QUPAL, a thrift-shopping assistant. ONLY answer questions about thrifting, "
                "vintage item identification, estimating values, or thrifting tips. If the user asks anything "
                "unrelated to thrifting, politely refuse and ask them to ask a thrift-related question. "
                "Keep answers concise and focused on thrift topics."
            )
            # prefer ChatCompletion if available
            try:
                resp = openai.ChatCompletion.create(
                    model='gpt-3.5-turbo',
                    messages=[
                        {'role': 'system', 'content': system_prompt},
                        {'role': 'user', 'content': message},
                    ],
                    max_tokens=250,
                )
                reply = resp.choices[0].message.content.strip()
            except Exception:
                # fallback to text completion with an explicit prompt
                prompt = (
                    system_prompt + "\n\nUser: " + message + "\nAssistant:" 
                )
                resp = openai.Completion.create(
                    engine='text-davinci-003',
                    prompt=prompt,
                    max_tokens=250,
                )
                reply = resp.choices[0].text.strip()
            # Basic safeguard: if the model responds with unrelated content, replace with refusal
            thrift_keywords = [
                'thrift', 'vintage', 'antique', 'value', 'estimate', 'brand', 'condition', 'zippers', 'stains', 'identify', 'label', 'seams'
            ]
            if not any(k in reply.lower() for k in thrift_keywords) and not any(k in message.lower() for k in thrift_keywords):
                reply = "I can only assist with thrift-related questions. Please ask about vintage items, values, or thrifting tips."
            # Special handling: if the user asked about laptops, provide a choice list instead of AI reply
            if 'laptop' in message.lower() and action != 'select':
                choices = [
                    'MacBook Air',
                    'Dell XPS 13',
                    'Lenovo ThinkPad X1 Carbon',
                    'HP Spectre x360'
                ]
                return jsonify({'reply': 'Which kind of laptop are you interested in? Choose one:', 'choices': choices})
            # If this is a selection action, fall through to return the reply
            return jsonify({'reply': reply})
        except Exception as e:
            # log error server-side and return an error to the client
            print('OpenAI request error:', str(e))
            return jsonify({'error': 'OpenAI request failed', 'details': str(e)}), 500

    # If API key is not configured, we can still handle selection actions locally for basic laptop info
    # but otherwise inform the client to set the key.
    if action == 'select' and selection:
        # Provide basic laptop info mapping without OpenAI
        info_map = {
            'MacBook Air': 'MacBook Air — Apple M1/M2, lightweight, great battery life, starts around 8GB RAM. Good for everyday use and light creative work.',
            'Dell XPS 13': 'Dell XPS 13 — compact 13-inch Windows laptop, premium build, excellent screen options. Good for developers and professionals.',
            'Lenovo ThinkPad X1 Carbon': 'ThinkPad X1 Carbon — business laptop, excellent keyboard, durable chassis, available with Intel CPUs and long battery life.',
            'HP Spectre x360': 'HP Spectre x360 — convertible 2-in-1, sleek design, touch screen, good performance for productivity tasks.'
        }
        reply = info_map.get(selection, 'Sorry, I do not have details for that model.')
        return jsonify({'reply': reply})

    return jsonify({'error': 'OPENAI_API_KEY not set on server. Set the environment variable and restart the server.'}), 403


if __name__ == '__main__':
    # Only for local development. Do not use this server in production as-is.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port, debug=True)
