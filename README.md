<h1 align="center" id="title">LegiTech-AI</h1>
<h2>Welcome to LegiTech-AI – Your AI-Powered Legal Assistant!</h2>

<p>LegiTech-AI is not just another application; it's an advanced legal platform designed to provide assistance in various legal tasks. Our mission is to make legal processes more efficient, accessible, and understandable for everyone.</p>


![gif](https://github.com/HamaRegaya/LegiTech-AI/assets/80254112/cdec2a52-2831-44dd-8072-bb6c7c8f429e)


<h2>🧐 Structure</h2>

```
|-- .venv/                                 # Virtual environment folder
|-- requirements.txt                      # App Dependencies
|-- app.py                                # Start the app - WSGI gateway
|
|-- app/
|    |
|    |
|    |    |
|    |    |-- static/
|    |    |    |    |-- css/
|    |    |    |    |-- img/
|    |    |    |    |-- js/
|    |    |    |-- back/
|    |    |    |    |-- css/
|    |    |    |    |-- img/
|    |    |    |    |--js/
|    |-- templates/                      # Templates used to render pages
|    |    |
|    |    |-- *.html                   # All HTML files


```



<h2>🔍 Features</h2>

* **Essay Correction:** LegiTech-AI can help grade student essays and provide feedback on grammar, style, and legal accuracy.
* **Legal Document Summarization:** LegiTech-AI can summarize complex legal documents into a concise and easy-to-understand format.
* **Chat with Legal Document:** LegiTech-AI can answer questions about legal documents and provide explanations of complex legal concepts.

<h2>🚀 Benefits</h2>

LegiTech-AI offers several advantages:

* **Increased Efficiency:** It assists in grading essays and summarizing legal documents faster and more efficiently than manual methods.
* **Improved Accuracy:** LegiTech-AI helps identify errors in grammar, style, and legal accuracy.
* **Enhanced Access to Legal Assistance:** It provides legal support to those who cannot afford a lawyer or lack access to traditional legal services.

<h2>🛠️ Installation Steps:</h2>

<p>1. Create a Virtual Environment</p>

```
python -m venv .venv
```

<p>2. Activate the Virtual Environment</p>

```
.venv\Scripts\activate
```

<p>3. Install Dependencies</p>

```
pip install -r requirements.txt
```

<p>4. Run the Application</p>

```
python app.py
```


  
<h2>💻 Built with</h2>

Technologies used in the project:

*   Flask
*   Jinja2
*   OpenAI API (GPT-3.5 Turbo)
*   Microsoft Trocr (Optical Character Recognition)
*   OpenCV-Python
