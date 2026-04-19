from flask import Flask, request, render_template
from openai import OpenAI

app = Flask(__name__)
import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        code = request.form["code"]
        error = request.form["error"]
        prompt = ("Explain the error in this code without fixing it:" f"\n\n{code}\n\nError:\n\n{error}")
        model_engine="gpt-4o-mini"
        explanation_completion = client.chat.completions.create(
            model= model_engine,
            messages=[{"role": "user", "content": f"{prompt}"}],
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.2,

        )
        explanation = explanation_completion.choices[0].message.content

        fixed_code_prompt = (f"Fix this code: \n\n{code}\n\nError: \n\n{error}." f"\n Respond only with the fixed code.")

        fixed_code_completions = client.chat.completions.create(
            model= model_engine,
            messages= [{"role": "user", "content": f"{fixed_code_prompt}"}],
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.2,
        )
        fixed_code = fixed_code_completions.choices[0].message.content
        return render_template("index.html",
                               explanation=explanation,
                               fixed_code = fixed_code)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)
