from flask import Flask, request, render_template
import tempfile
import os
from autopep8 import fix_code
import subprocess

app = Flask(__name__)

def analyze_code(code):
    """Analyze the submitted Python code for issues."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
        temp_file.write(code.encode('utf-8'))
        temp_file_path = temp_file.name

    try:
        # Run flake8 to find potential bugs and style issues
        result = subprocess.run(
            ["flake8", temp_file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        feedback = result.stdout.strip()
        return feedback if feedback else "No issues found!"
    finally:
        os.remove(temp_file_path)

@app.route('/', methods=['GET', 'POST'])
def index():
    feedback = ""
    fixed_code = ""
    user_code = ""

    if request.method == 'POST':
        user_code = request.form['code']
        # Analyze code for bugs
        feedback = analyze_code(user_code)
        # Automatically fix code issues
        fixed_code = fix_code(user_code)

    return render_template('index.html', feedback=feedback, fixed_code=fixed_code, user_code=user_code)

if __name__ == '__main__':
    app.run(debug=True)
