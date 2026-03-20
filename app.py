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
    <h1>SOW Generator</h1>
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
    doc = Document(doc_path)
    replacement_index = 0
    
    for sdt in doc.element.iter(qn('w:sdt')):
        if replacement_index >= len(replacements):
            break
        
        sdt_content = sdt.find(qn('w:sdtContent'))
        if sdt_content is not None:
            for text_elem in sdt_content.iter(qn('w:t')):
                if text_elem.text and 'Click or tap here' in text_elem.text:
                    text_elem.text = str(replacements[replacement_index])
                    replacement_index += 1
                    break
    
    doc.save(output_path)
    return replacement_index


def convert_to_pdf(docx_path, output_dir):
    subprocess.run([
        'libreoffice',
        '--headless',
        '--convert-to', 'pdf',
        '--outdir', output_dir,
        docx_path
    ], check=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        client_name = request.form['client_name']
        hours = request.form['hours']
        
        replacements = [client_name, hours]
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = 'output'
        output_docx = f'{output_dir}/SOW_{timestamp}.docx'
        output_pdf = f'{output_dir}/SOW_{timestamp}.pdf'
        
        os.makedirs(output_dir, exist_ok=True)
        
        fill_content_controls('template.docx', output_docx, replacements)
        convert_to_pdf(output_docx, output_dir)
        
        return send_file(
            output_pdf,
            as_attachment=True,
            download_name=f'SOW_{client_name}.pdf'
        )
    
    return render_template_string(HTML_FORM)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
