from flask import Flask, request, Response, render_template
import requests
import json
import os
import fitz  # PyMuPDF

app = Flask(__name__)

# --- GRANT CONFIGURATION ---
# Toggle between "deepseek-r1:1.5b" and "gemma:2b" here
ACTIVE_MODEL = "deepseek-r1:1.5b" 

OLLAMA_URL = "http://localhost:11434/api/generate"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BOOK_PATH = os.path.join(BASE_DIR, "static", "physics_full_book.pdf")

def search_pdf_with_page(query):
    if not os.path.exists(BOOK_PATH):
        print(f"❌ PDF MISSING: {BOOK_PATH}")
        return None, ""
    try:
        doc = fitz.open(BOOK_PATH)
        query_terms = [w.lower() for w in query.split() if len(w) > 3]
        # Skip Page 1-2 (TOC/Intro) to find real physics content
        for page_index in range(2, len(doc)):
            page = doc[page_index]
            text = page.get_text().lower()
            if any(term in text for term in query_terms):
                print(f"✅ CONTEXT FOUND: Page {page_index + 1}")
                return (page_index + 1), page.get_text()[:3000]
        return None, ""
    except Exception as e:
        print(f"❌ SEARCH ERROR: {e}")
        return None, ""

@app.after_request
def apply_caching(response):
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    return response

@app.route('/')
def home():
    return render_template('alexander_os_prototype2.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    user_query = data.get("prompt", "")
    page_num, pdf_text = search_pdf_with_page(user_query)
    
    system_instruction = r"""
    You are Alexander OS, a professional Physics Tutor. 
    Use clear spacing, newlines, and bullet points.
    MANDATORY: Always provide a real-world example for every physics concept.
    Math Rules: Use \( ... \) for inline and \[ ... \] for standalone equations.
    """
    
    context = f"TEXTBOOK PAGE {page_num}:\n{pdf_text}" if page_num else "Use internal knowledge."
    final_prompt = f"### Instruction:\n{system_instruction}\n\n### Context:\n{context}\n\n### Student:\n{user_query}\n\n### Alexander OS:"

    def generate():
        payload = {
            "model": ACTIVE_MODEL,
            "prompt": final_prompt,
            "stream": True,
            "options": {"temperature": 0.3}
        }
        try:
            r = requests.post(OLLAMA_URL, json=payload, stream=True, timeout=20)
            for line in r.iter_lines():
                if line:
                    chunk = json.loads(line).get("response", "")
                    yield chunk
            
            # --- THE "REVEAL": Send PDF Trigger ONLY after the text is finished ---
            if page_num:
                yield f"\n\n[SHOW_PDF:{page_num}]"
                
        except Exception as e:
            yield f"\n[CONNECTION ERROR] Ollama is unreachable. Ensure 'ollama serve' is running."

    return Response(generate(), mimetype='text/plain')

if __name__ == '__main__':
    print(f"🚀 Alexander OS Engine active on {ACTIVE_MODEL}")
    app.run(port=5000, debug=True)