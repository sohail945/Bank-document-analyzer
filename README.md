# 🏦 Bank Document Analyzer

![Banner](Bank_document_analyzer.png)

> 🔍 Upload banking, loan, or insurance documents (PDF/image) and get an instant AI-generated explanation in simple terms. Red flags? We’ll highlight them too — now in English **or** Roman Urdu.

---

## 🚀 Features

- 📷 Upload **images or PDFs**
- 🧠 **OCR** extracts text from scanned documents
- 🗣️ Choose **output language**: English or Roman Urdu
- 🤖 **LLM summaries** powered by Groq API (LLaMA/Mistral)
- 🚩 Highlights risky terms with **Red Flag Points**
- 📎 Supports **multiple documents** at once
- ❓ Ask **follow-up questions** about the uploaded document

---

## 💡 How It Works

1. 📤 Upload document(s) (PDF or image)
2. 🔍 OCR extracts all text
3. 🌐 LLM interprets the document based on selected language
4. ✍️ Returns:
   - 📄 **Summary** in paragraph form
   - 🚩 **Red Flag Points** as bullet points
5. ❓ Then switch to the **Q&A tab** to ask questions from the document (auto-detects language)

---

## 🖼️ Response Language Options

- **English** → Simple English explanations  
- **Roman Urdu** → Urdu written in English alphabet (e.g., _"Loan ki fees zyada hai"_)

---

## 💬 Ask a Question

After getting the summary, go to the **"Ask a Question"** tab and type any query like:

- `"Is there any late payment fee?"`
- `"Loan ka duration kitna hai?"`

The assistant will reply based on both:
- OCR-extracted original content
- LLM-generated explanation

---

## 🛠️ Setup Instructions

```bash
# 1. Clone the repo
git clone https://github.com/sohail945/Bank-document-analyzer.git
cd Bank-document-analyzer

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your Groq API key
Create a .env file and include:
GROQ_API_KEY=your_key_here
