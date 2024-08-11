from flask import Flask, render_template_string, request, redirect, url_for
import os
import signal

app = Flask(__name__)

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Message Reply System</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f0f0f0;
        }
        .chat-window {
            width: 300px;
            border: 1px solid #ccc;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }
        .messages {
            flex: 1;
            padding: 10px;
            overflow-y: auto;
        }
        .messages .message {
            margin: 5px 0;
            padding: 8px;
            border-radius: 5px;
            background: #f1f1f1;
        }
        .messages .message.user {
            background: #0078d7;
            color: white;
            align-self: flex-end;
        }
        .input-container {
            display: flex;
            padding: 10px;
            border-top: 1px solid #ccc;
        }
        .input-container input {
            flex: 1;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            margin-right: 5px;
        }
        .input-container button {
            padding: 10px;
            border: none;
            background: #0078d7;
            color: white;
            border-radius: 5px;
            cursor: pointer;
        }
        .input-container button.off {
            background: red;
        }
    </style>
</head>
<body>

<div class="chat-window">
    <div class="messages" id="messages">
        <div class="message">Hello! How can I help you today?</div>
    </div>
    <div class="input-container">
        <form action="/send_message" method="post" style="flex: 1; display: flex;">
            <input type="text" name="message" id="messageInput" placeholder="Type your message here..." required>
            <button type="submit">Send</button>
        </form>
        <form action="/off" method="post">
            <button type="submit" class="off">Off</button>
        </form>
    </div>
</div>

<script>
    const messageInput = document.getElementById('messageInput');
    const messages = document.getElementById('messages');
    document.querySelector('form[action="/send_message"]').addEventListener('submit', function(event) {
        event.preventDefault();
        const messageText = messageInput.value;
        const newMessage = document.createElement('div');
        newMessage.classList.add('message', 'user');
        newMessage.textContent = messageText;
        messages.appendChild(newMessage);
        messageInput.value = '';
        fetch('/send_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: `message=${messageText}`
        });
    });
</script>

</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    # Here you can add logic to handle the message
    print(f'Received message: {message}')
    return '', 204

@app.route('/off', methods=['POST'])
def off():
    os.kill(os.getpid(), signal.SIGINT)
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
