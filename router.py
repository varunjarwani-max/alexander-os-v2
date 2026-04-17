from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)
OLLAMA_URL = "http://localhost:11434/api/generate"

HTML_UI = """
<!DOCTYPE html>
<html>
<head>
<title>Alexander OS</title>
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: #000; color: #fff; max-width: 600px; margin: 40px auto; padding: 20px; }
  #chat { height: 60vh; overflow-y: auto; border: 1px solid #333; padding: 15px; margin-bottom: 15px; border-radius: 10px; background: #111; }
  .user-msg { color: #aaa; margin-bottom: 10px; }
  .ai-msg { color: #fff; margin-bottom: 20px; padding-left: 10px; border-left: 2px solid #555; }
  .model-tag { font-size: 0.8em; color: #888; text-transform: uppercase; letter-spacing: 1px; }
  .input-area { display: flex; gap: 10px; }
  input { flex-grow: 1; padding: 15px; background: #222; color: #fff; border: 1px solid #444; border-radius: 8px; outline: none; }
  button { padding: 15px 25px; background: #fff; color: #000; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; }
</style>
</head>
<body>
  <h2>Alexander OS</h2>
  <div id="chat"></div>
  <div class="input-area">
    <input type="text" id="prompt" placeholder="Ask your tutor..." onkeypress="if(event.key === 'Enter') ask()">
    <button onclick="ask()">Send</button>
  </div>

  <script>
    async function ask() {
      const promptInput = document.getElementById('prompt');
      const prompt = promptInput.value;
      if (!prompt) return;
      
      const chat = document.getElementById('chat');
      chat.innerHTML += `<div class="user-msg"><b>You:</b> ${prompt}</div>`;
      promptInput.value = '';
      chat.scrollTop = chat.scrollHeight;
      
      const res = await fetch('/ask', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({prompt: prompt})
      });
      const data = await res.json();
      
      let formattedAnswer = data.answer.replace(/\\n/g, '<br>').replace(/\\*\\*(.*?)\\*\\*/g, '<b>$1</b>');
      chat.innerHTML += `<div class="ai-msg"><span class="model-tag">${data.model}</span><br>${formattedAnswer}</div>`;
      chat.scrollTop = chat.scrollHeight;
    }
  </script>
</body>
</html>
"""

def route_model(prompt):
    math_words = ["math", "physics", "equation", "solve", "calculate", "velocity"]
    if any(word in prompt.lower() for word in math_words):
        return "deepseek-r1:1.5b"
    return "gemma:2b"

@app.route('/')
def home():
    return render_template_string(HTML_UI)

@app.route('/ask', methods=['POST'])
def ask_alexander():
    user_prompt = request.json.get("prompt", "")
    active_model = route_model(user_prompt)
    
    print(f"\n[ROUTING] Swapping to: {active_model}...")
    
    payload = {
        "model": active_model,
        "prompt": f"You are a strict Socratic tutor. Do not give direct answers. Guide the student to figure it out: {user_prompt}",
        "stream": False
    }
    
    response = requests.post(OLLAMA_URL, json=payload)
    answer = response.json().get("response", "Error.")
    
    return jsonify({"model": active_model, "answer": answer})

if __name__ == '__main__':
    print("Alexander OS UI Live on port 5000...")
    app.run(port=5000)