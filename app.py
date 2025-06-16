import gradio as gr
from PIL import Image
from ocr_utils import extract_text
from prompts import get_explanation_prompt
from groq_llm import ask_groq
from deep_translator import GoogleTranslator
import fitz  # PyMuPDF

# Convert PDF to images
def convert_pdf_to_images(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    images = []
    for page in doc:
        pix = page.get_pixmap(dpi=300)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)
    return images

# Translate to English (used only if user selects English)
def translate_to_english(text):
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except Exception as e:
        print("Translation Error:", e)
        return text

# Extract only the Document Summary section onward
def extract_summary_and_flags(text):
    summary_start = text.find("Document Summary")
    if summary_start != -1:
        return text[summary_start:].strip()
    else:
        return text.strip()

# Main logic
def process_documents(files, language_choice):
    summaries = []

    for file in files:
        name = file.name
        extension = name.split('.')[-1].lower()

        with open(file.name, "rb") as f:
            content = f.read()

        # Step 1: OCR
        if extension == "pdf":
            pdf_images = convert_pdf_to_images(content)
            all_text = ""
            for img in pdf_images:
                all_text += "\n" + extract_text(img)
        elif extension in ["png", "jpg", "jpeg"]:
            image = Image.open(file.name)
            all_text = extract_text(image)
        else:
            summaries.append(f"❌ Unsupported file type: {name}")
            continue

        # Step 2: Use raw Urdu or translated English based on user choice
        if language_choice == "English":
            processed_text = translate_to_english(all_text)
        else:  # Urdu
            processed_text = all_text

        # Step 3: Prompt LLM
        prompt = get_explanation_prompt(processed_text, language_choice)
        response = ask_groq(prompt)
        cleaned_response = extract_summary_and_flags(response)

        summaries.append(cleaned_response)

    return "\n\n---\n\n".join(summaries)

# Gradio UI
demo = gr.Interface(
    fn=process_documents,
    inputs=[
        gr.File(file_types=["image", ".pdf"], label="Upload Document Images or PDFs", file_count="multiple"),
        gr.Radio(["English", "Roman Urdu"], label="Select Output Language", value="English")
    ],
    outputs=gr.Textbox(label="Document Explanation", lines=30),
    title="📄 Bank Document Explainer",
    description="Upload scanned documents related to **banking, loans, or insurance**. Get a clear explanation and red flag summary in English or Urdu."
)

if __name__ == "__main__":
    demo.launch()
