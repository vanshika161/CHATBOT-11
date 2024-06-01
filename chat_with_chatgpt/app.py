from flask import Flask, render_template, request, jsonify
import wikipedia
from transformers import GPT2LMHeadModel, GPT2Tokenizer

app = Flask(__name__)

# Load the pre-trained GPT-2 model and tokenizer
model_name = "gpt2"  # You can use "gpt2-medium", "gpt2-large", etc., if your system can handle it
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

def get_wikipedia_summary(topic):
    try:
        summary = wikipedia.summary(topic, sentences=2)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        # If Wikipedia cannot determine the correct article due to disambiguation, return the suggestion
        return f"Wikipedia suggests: {e.options[0]}"
    except Exception as e:
        # If there's any other error, return None
        print(f"Error: {e}")
        return None

def chat_with_gpt(prompt):
    # Normalize prompt to lowercase
    lower_prompt = prompt.lower()
    
    # Check if the prompt contains any predefined key phrases
    if "python" in lower_prompt:
        return get_wikipedia_summary("Python (programming language)")
    elif "prime number code" in lower_prompt:
        return get_wikipedia_summary("Prime number")
    elif "prime number" in lower_prompt:
        return get_wikipedia_summary("Prime number")
    elif "animal" in lower_prompt:
        return get_wikipedia_summary("Animal")
    elif "animal welfare" in lower_prompt:
        return get_wikipedia_summary("Animal welfare")
    elif "javascript" in lower_prompt:
        return get_wikipedia_summary("JavaScript")
    
    # Fetch Wikipedia summary for other questions
    return get_wikipedia_summary(prompt)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.json.get("message")
    response = chat_with_gpt(user_input)
    
    # If response is None, handle it appropriately
    if response is None:
        response = "I'm sorry, I couldn't find information about that topic."
    
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
