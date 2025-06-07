
import requests
import json
import gradio as gr

# Ollama API endpoint
url = "http://localhost:11434/api/generate"

headers = {
    'Content-Type': 'application/json'
}

# For maintaining conversation history
history = []

def generate_response(prompt):
    history.append(f"User: {prompt}")
    final_prompt = "\n".join(history)

    # Request payload for Ollama
    data = {
        "model": "zencode",
        "prompt": final_prompt,
        "stream": False
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            data = response.json()
            actual_response = data.get('response', 'No response found.')

            history.append(f"Zencode: {actual_response}")
            return actual_response
        else:
            return f"❌ Error: {response.status_code} - {response.text}"

    except Exception as e:
        return f"❌ Exception: {str(e)}"

# Gradio interface
interface = gr.Interface(
    fn=generate_response,
    inputs=gr.Textbox(lines=4, placeholder="Enter your prompt here...", label="Your Question"),
    outputs=gr.Textbox(label="Zencode's Response"),
    title="💡 Zencode - AI Coding Assistant"
)

interface.launch()