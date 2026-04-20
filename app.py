from flask import Flask, request, render_template
from openai import OpenAI
import os

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return "API key missing in Azure", 500

        client = OpenAI(api_key=api_key)

        code = request.form["code"]
        error = request.form["error"]

        prompt = f"Explain the error in this code without fixing it:\n\n{code}\n\nError:\n\n{error}"

        model_engine = "gpt-4o-mini"

        explanation = client.chat.completions.create(
            model=model_engine,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024,
            temperature=0.2,
        ).choices[0].message.content

        fixed_code_prompt = f"Fix this code:\n\n{code}\n\nError:\n\n{error}\nRespond only with the fixed code."

        fixed_code = client.chat.completions.create(
            model=model_engine,
            messages=[{"role": "user", "content": fixed_code_prompt}],
            max_tokens=1024,
            temperature=0.2,
        ).choices[0].message.content

        return render_template("index.html",
                               explanation=explanation,
                               fixed_code=fixed_code)

    return render_template("index.html")