import gradio as gr
from PIL import Image
from ocr_utils import extract_text
from prompts import get_explanation_prompt
from groq_llm import ask_groq
from deep_translator import GoogleTranslator
from langdetect import detect
import fitz  # PyMuPDF
import tempfile

# Translator
def translate_to_english(text):
    try:
        if detect(text) != 'en':
            return GoogleTranslator(source='auto', target='en').translate(text)
        return text
    except Exception as e:
        print("Translation Error:", e)
        return text

def convert_pdf_to_images(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    images = []
    for page in doc:
        pix = page.get_pixmap(dpi=300)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)
    return images

def extract_summary_and_flags(text):
    # Look for the part starting from "**Document Summary**"
    summary_start = text.find("Document Summary")
    if summary_start != -1:
        return text[summary_start:].strip()
    else:
        # Fallback: return everything
        return text.strip()


# Core logic to process each file
def process_documents(files):
    summaries = []

    for file in files:
        name = file.name
        extension = name.split('.')[-1].lower()

        with open(file.name, "rb") as f:
            content = f.read()

        if extension == "pdf":
            pdf_images = convert_pdf_to_images(content)
            all_text = ""
            for img in pdf_images:
                page_text = extract_text(img)
                all_text += "\n" + page_text

            translated_text = translate_to_english(all_text)
            prompt = get_explanation_prompt(translated_text)
            response = ask_groq(prompt)

            # Keep only from Summary onward
            cleaned_response = extract_summary_and_flags(response)
            summaries.append(cleaned_response)

        elif extension in ["png", "jpg", "jpeg"]:
            image = Image.open(file.name)
            text = extract_text(image)
            translated_text = translate_to_english(text)
            prompt = get_explanation_prompt(translated_text)
            response = ask_groq(prompt)

            # Keep only from Summary onward
            cleaned_response = extract_summary_and_flags(response)
            summaries.append(cleaned_response)

        else:
            summaries.append(f" Unsupported file type: {name}")

    return "\n\n---\n\n".join(summaries)

# Gradio Interface
demo = gr.Interface(
    fn=process_documents,
    inputs=gr.File(file_types=["image", ".pdf"], label="Upload Document Images or PDFs", file_count="multiple"),
    outputs=gr.Textbox(label="Explanation", lines=30),
    title="Bank Document Explainer",
    description="Upload scanned **images or PDF documents** related to banking, loans, or insurance. We’ll explain them clearly and highlight red flags."
)

if __name__ == "__main__":
    demo.launch()
