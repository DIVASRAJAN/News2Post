import gradio as gr
import requests

# Function to call your API
def call_api(topic):
    # Replace with your actual API logic
    response = requests.post(
        "your_api_endpoint_here/generate-post",
        json={"topic": topic},
        headers={"Content-Type": "application/json"}
    )
    response.raise_for_status()
    result = response.json()
    # return result.get("linkedin_post", "No 'post' key in response."), result.get("news_sources", "No 'news_sources' key in response.")
    linkedin_post = result.get("linkedin_post", "No 'linkedin_post' key in response.")
    news_sources = result.get("news_sources", "No 'news_sources' key in response.")

    # ✅ Handle lists safely
    if isinstance(news_sources, list):
        # Option 1 — plain string
        news_sources = "https://".join(news_sources)
        # Option 2 — Markdown links (clickable)
        # news_sources = "\n".join([f"- [{src}]({src})" for src in news_sources])

    return linkedin_post, news_sources

# Using Gradio Blocks API (v5+ style)
with gr.Blocks(title="News2Post",css = "#custom-output {height: 500px; overflow-y: auto; border : 1px solid #ccc;}") as demo:
    gr.Markdown("## News2Post\nSend a topic and generate a post with the recent news.")

    with gr.Row():
        with gr.Column():
            input_box = gr.Textbox(label="Input Text", placeholder="Type your topic here", lines=2)
        with gr.Column(elem_id="custom-output"):
            # output_md = gr.Markdown(label="API Response",)  # ✅ This is rendered Markdown, NOT Textbox
            gr.Markdown("###   Generated Post")
            output_md = gr.Markdown()

        with gr.Column(elem_id="custom-output"):
            # output_sources = gr.Markdown(label="source links",)
            gr.Markdown("###   News Sources")
            output_sources = gr.Markdown()


    with gr.Row():
        clear_btn = gr.Button("Clear")
        submit_btn = gr.Button("Submit")
        flag_btn = gr.Button("Flag")

    # On click: call API
    submit_btn.click(fn=call_api, inputs=input_box, outputs=[output_md,output_sources])

    # Clear button
    clear_btn.click(lambda: ("", "", ""), inputs=None, outputs=[input_box, output_md,output_sources])

demo.launch()