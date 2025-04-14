import gradio as gr
from flask import Flask, render_template_string
import threading

app = Flask(__name__)

# Placeholder function for AI responses
def chatbot(query, uploaded_files):
    if uploaded_files:
        file_names = uploaded_files.name if isinstance(uploaded_files, list) else uploaded_files.name
    else:
        file_names = "No files uploaded."
    
    return f"📝 AI response for: {query}\n\n📂 Files: {file_names}"

# UI Layout with Gradio
def create_gradio_interface():
    with gr.Blocks(css="body {font-family: Arial, sans-serif;}") as demo:
        gr.Markdown("# 🧠 SMRT Knowledge Assistant")
        gr.Markdown("**Your AI-powered research assistant to organize, analyze, and chat with your knowledge sources.**")

        with gr.Row():
            with gr.Column(scale=2):
                gr.Markdown("## 📂 Upload & Select Sources")
                file_upload = gr.File(label="Upload Your Documents", interactive=True, file_types=[".txt", ".pdf", ".png", ".jpg", ".mp3", ".mp4"])

                gr.Markdown("### 📌 Select Knowledge Sources")
                source_buttons = [
                    gr.Checkbox(label="📖 Getting Started Guide", value=True),
                    gr.Checkbox(label="⚙️ SMRT Assistant Features", value=True),
                    gr.Checkbox(label="🗂️ Knowledge Glossary", value=True),
                    gr.Checkbox(label="❓ Troubleshooting & FAQ", value=True),
                ]

            with gr.Column(scale=6):
                gr.Markdown("## 💬 Chat with SMRT Assistant")
                gr.Markdown("Type a question below to interact with your knowledge sources.")
                user_query = gr.Textbox(label="Ask something...", placeholder="Type your question here...")
                chat_output = gr.Textbox(label="AI Response", interactive=False, lines=5)

                with gr.Row():
                    chat_button = gr.Button("🚀 Send", size="md")
                    clear_chat_button = gr.Button("🔄 Clear Chat", size="md")

                gr.Markdown("## 📝 Notes & Actions")
                notes = gr.Textbox(label="Save your notes here", interactive=True, lines=4)

        chat_button.click(fn=chatbot, inputs=[user_query, file_upload], outputs=chat_output)
        clear_chat_button.click(fn=lambda: "", inputs=[], outputs=[chat_output, user_query])

    return demo

# Start Gradio on a different port
def run_gradio():
    gradio_interface = create_gradio_interface()
    gradio_interface.launch(server_name="0.0.0.0", server_port=7860, share=False)

# Run Gradio in a background thread
threading.Thread(target=run_gradio).start()

# Flask main route
@app.route("/")
def home():
    return """<h1>SMRT Knowledge Assistant</h1>
              <iframe src="http://127.0.0.1:7860" width="100%" height="800px"></iframe>"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
