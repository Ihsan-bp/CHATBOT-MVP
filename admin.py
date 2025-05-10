# admin.py
import gradio as gr
from config.config import PINECONE_API_KEY
from injestion.index.add_embd import advnce_new_embedding
from injestion.index.get_embd import fetch_data
from helpers.logger import setup_logging, get_logger

# Setup logging
setup_logging()
logger = get_logger(__name__)

# Function to handle adding new embeddings
def handle_add_entry(text_input, title_input, file_upload):
    if file_upload is not None:
        if not (file_upload.name.endswith(".txt") or file_upload.name.endswith(".json")):
            return "", "", "", "⚠️ Only .txt or .json files are supported."

        result = advnce_new_embedding(file_path=file_upload.name, title=title_input)
        if result["status"] == "success":
            return "", "", None, result
        else:
            return "", "", None, f"❌ Failed to add file: {result['detail']}"

    elif text_input.strip():
        result = advnce_new_embedding(text=text_input, title=title_input)
        if result["status"] == "success":
            return "", "", None, result
        else:
            return "", "", None, f"❌ Failed to add entry: {result['detail']}"
    else:
        return "", "", None, "⚠️ Please provide either text or a file."

# ✅ New function to view existing embedded data
def handle_view_embedded_data():
    try:
        data_response = fetch_data()
        data = data_response.get("data", [])
        formatted = [f"📌 **{item['title']}** | `{item['id']}`\n{text_wrap(item['text'])}" for item in data]
        return "\n\n---\n\n".join(formatted)
    except Exception as e:
        return f"❌ Error fetching embedded data: {str(e)}"

def text_wrap(text, width=100):
    # Utility to wrap long text lines nicely
    import textwrap
    return "\n".join(textwrap.wrap(text, width))

# UI Layout
with gr.Blocks() as demo:
    gr.Markdown("### 🔐 Admin Panel - Add New Embedding")

    with gr.Row():
        with gr.Column():
            text_input = gr.Textbox(label="Enter Text", placeholder="Type the FAQ answer or query...", lines=4)
            title_input = gr.Dropdown(
                label="Select Category",
                choices=["faq", "overview", "general", "other"],
                interactive=True
            )
            file_upload = gr.File(label="Or Upload a .txt File", type="filepath")
            submit_btn = gr.Button("Add Entry")
            view_btn = gr.Button("📄 View All Embedded Entries")
            status_output = gr.Textbox(label="Status", interactive=False)
            embedded_data_output = gr.Textbox(label="Embedded Data", lines=15, interactive=False)
    submit_btn.click(
        fn=handle_add_entry,
        inputs=[text_input, title_input, file_upload],
        outputs=[text_input, title_input, file_upload, status_output]
    )
    view_btn.click(
        fn=handle_view_embedded_data,
        inputs=[],
        outputs=[embedded_data_output]
    )
demo.launch(share=True)