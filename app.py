from flask import Flask, request, url_for
import random

app = Flask(__name__)

# pre-defined questions & answers
chat_data = {
    "ta randi hos?": "Umm ho.",
    "k ta xakka hos?": "Ho but how you know about that?",
    "tero naam k ho?": "Mero naam Kiran D ho.",
    "tel chadai ko kati linxas?": "Jamma 50Rs"
}

fallback_replies = [
    "Hmm... I'm not sure about that 😅",
    "Interesting question! Can you ask something else?",
    "I don't know the answer yet, but let's chat more!",
    "Haha, I wish I could answer that 😎"
]

conversation = []

def get_reply(user_text):
    text = user_text.lower()
    for key in chat_data:
        if key in text:
            return chat_data[key]
    return random.choice(fallback_replies)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_text = request.form.get("text", "").strip()
        if user_text:
            bot_reply = get_reply(user_text)
            conversation.append(("You", user_text))
            conversation.append(("Kiran D", bot_reply))

    # conversation bubbles
    chat_html = ""
    for speaker, message in conversation:
        if speaker == "You":
            color = "#ffffff"
            bg = "#1f7a8c"  # blue-green user bubble
        else:
            color = "#000000"
            bg = "#f1f1f1"  # white bot bubble
        chat_html += f'<p style="background:{bg}; color:{color}; padding:8px 12px; border-radius:12px; width:max-content; max-width:80%; margin:5px 0;"><b>{speaker}:</b> {message}</p>'

    logo_url = url_for('static', filename='kiran1.jpeg')

    # sidebar question list HTML
    questions_html = ""
    for q in chat_data:
        questions_html += f'<p style="padding:6px; margin:5px 0; cursor:pointer; border-radius:6px; background:#144552; color:white;" onclick="document.getElementById(\'user_input\').value=\'{q}\'">{q}</p>'

    return f"""
    <html>
        <head>
            <title>Kiran D</title>
        </head>
        <body style="
            margin:0;
            font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            color:white;
        ">
            <!-- Logo + Heading -->
            <div style="display:flex; align-items:center; justify-content:center; gap:15px; padding-top:20px;">
                <img src="{logo_url}" alt="Kiran D Logo"
                     style="width:60px; height:60px; border-radius:50%; object-fit:cover; border:2px solid white;">
                <h1 style="margin:0; color:white;">Kiran D</h1>
            </div>
            <p style="text-align:center; color:white; font-weight:bold; margin-top:10px;">Chat with Kiran D or click a question!</p>

            <!-- main content: chat + sidebar -->
            <div style="display:flex; justify-content:center; gap:20px; margin-top:20px;">
                
                <!-- Chat box -->
                <div style="
                    text-align:left; 
                    width:400px; 
                    border:1px solid #ccc; 
                    padding:10px; 
                    height:350px; 
                    overflow-y:scroll; 
                    background:white; 
                    color:black;
                    border-radius:12px;
                ">
                    {chat_html}
                </div>

                <!-- Question list sidebar -->
                <div style="
                    width:200px; 
                    padding:10px; 
                    background:#0f3b53; 
                    border-radius:12px;
                    height:350px;
                    overflow-y:auto;
                ">
                    <h3 style="color:white; margin-top:0; text-align:center;">Questions</h3>
                    {questions_html}
                </div>
            </div>

            <!-- input form -->
            <form method="post" style="text-align:center; margin-top:15px;">
                <input id="user_input" name="text" placeholder="Type your question..." 
                       style="padding:10px; width:300px; border-radius:20px; border:none; outline:none; background:#ffffff; color:black;">
                <button style="padding:10px 20px; border:none; border-radius:20px; background:#1E90FF; color:white; font-weight:bold; cursor:pointer;">Send</button>
            </form>
        </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)
