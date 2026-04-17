import json
import requests
from flask import Flask, render_template, request, Response, stream_with_context

app = Flask(__name__)

# --- CONFIGURATION (Matched to your local Ollama) ---
OLLAMA_URL = "http://localhost:11434/api/generate"
STEM_MODEL = "deepseek-r1:1.5b"  # Your reasoning model
GENERAL_MODEL = "gemma:2b"      # Your general purpose model

# Load Textbook Data
try:
    with open('chapter2.json', 'r') as f:
        TEXTBOOK_DATA = json.load(f)
except Exception as e:
    print(f"Warning: chapter2.json not found or corrupted. Error: {e}")
    TEXTBOOK_DATA = []

def get_routing_info(prompt):
    """Detects if query is STEM-based and finds PDF page."""
    prompt_l = prompt.lower()
    
    # 1. Model Routing Logic
    stem_keywords = ['solve', 'calculate', 'formula', 'acceleration', 'velocity', 'friction', 'force', 'math', 'physics', 'derive']
    use_stem = any(k in prompt_l for k in stem_keywords)
    model = STEM_MODEL if use_stem else GENERAL_MODEL
    
    # 2. PDF Context Retrieval (Handles List format)
    page_num = None
    if isinstance(TEXTBOOK_DATA, list):
        for entry in TEXTBOOK_DATA:
            keywords = entry.get('keywords', [])
            if any(k in prompt_l for k in keywords):
                page_num = entry.get('page')
                break
                
    return model, page_num

@app.route('/')
def index():
    return render_template('alexander_os_prototype2.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_data = request.json
    user_input = user_data.get('prompt', '')
    
    model, page = get_routing_info(user_input)
    print(f"DEBUG: Routing to {model} | PDF Page Target: {page}")

    # --- REINFORCED SYSTEM PROMPT ---
    system_instruction = (
        "You are Alexander, a K-12 AI tutor. "
        "Rules:\n"
        "1. If a formula is needed, use LaTeX $$ symbols.\n"
        "2. ALWAYS give a real-world example.\n"
        "3. If using DeepSeek, ignore the <thought> tags in your final output to the student.\n"
        "4. End with a simple question to test the student."
    )

    def generate():
        payload = {
            "model": model,
            "prompt": f"{system_instruction}\n\nStudent: {user_input}\nAlexander:",
            "stream": True
        }
        
        # Send PDF signal to HTML instantly
        if page:
            yield f"[SHOW_PDF:{page}]"

        try:
            # Setting a longer timeout for the i7 processor to wake up the model
            response = requests.post(OLLAMA_URL, json=payload, stream=True, timeout=120)
            
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    token = chunk.get("response", "")
                    # Visual feedback in your VS Code terminal
                    if token.strip():
                        print(".", end="", flush=True) 
                    yield token
            print("\nDEBUG: Response Complete.")
        except Exception as e:
            print(f"\nKERNEL ERROR: {e}")
            yield "Kernel Error: Ensure 'ollama serve' is active and models are pulled."

    return Response(stream_with_context(generate()), mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True, port=5000)