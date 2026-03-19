from flask import Flask, request, render_template_string, send_file
from docx import Document
from docx.oxml.ns import qn
import subprocess
import os
from datetime import datetime

app = Flask(__name__)

HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
    <title>SOW Generator</title>
    <style>
        body { font-family: Arial; max-width: 500px; margin: 50px auto; padding: 20px; }
        label { display: block; margin-top: 15px; font-weight: bold; }
        input { width: 100%; padding: 10px; margin-top: 5px; font-size: 16px; box-sizing: border-box; }
        button { margin-top: 25px; padding: 15px 30px; background: #007bff; color: white; border: none; cursor: pointer; font-size: 16px; width: 100%; }
        button:hover { background: #0056b3; }
        h1 { text-align: center; }
    </style>
</head>
<body>
    <h1>📄 SOW Generator</h1>
    <form method="POST">
        <label>Client Name:</label>
        <input type="text" name="client_name" required placeholder="Enter client name">
        
        <label>Hours:</label>
        <input type="number" name="hours" required placeholder="Enter number of hours">
        
        <button type="submit">Generate SOW</button>
    </form>
</body>
</html>
'''

def fill_content_controls(doc_path, output_path, replacements):
    """
    Fill Word Content Controls in order of appearance.
    replacements = [client_name, hours]
    """
    doc = Document(doc_path)
    
    replacement_index = 0
    
    # Iterate through all content controls (sdt elements)
    for sdt in doc.element.iter(qn('w:sdt')):
        if replacement_index >= len(replacements):
            break
        
        # Find the content part of the control
        sdt_content = sdt.find(qn('w:sdtContent'))
        if sdt_content is not None:
            # Find text elements within the content control
            for text_elem in sdt_content.iter(qn('w:t')):
                if text_elem.text and 'Click or tap here' in text_elem.text:
                    text_elem.text = str(replacements[replacement_index])
                    replacement_index += 1
                    break
    
    doc.save(output_path)
    return replacement_index


def convert_to_pdf(docx_path, output_dir):
    """Convert DOCX to PDF using LibreOffice"""
    subprocess.run([
        'libreoffice', 
        '--headless', 
        '--convert-to', 'pdf',
        '--outdir', output_dir, 
        docx_path
    ], check=True)


@app.route('/', methods=['GET', 'POST'])
