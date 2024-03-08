from flask import Flask, render_template, request
import openai
from dotenv import dotenv_values
import json

config = dotenv_values(".env")
openai.api_key = config["OPENAPI_KEY"]

app = Flask(__name__, template_folder='templates')

def get_colors_for_prompt(msg):
    prompt = f"""You are a color palette generating assistant that responds to text prompts for color palettes Your should generate color palettes that fit the theme, mood, or instructions in the prompt.
    The palettes should be between 2 and 8 colors.

    Q: Convert the following verbal description of a color palette into a list of colors: The Mediterranean sea
    A: ["#006699", "#66CCCC", "#F0E68C", "#008000", "#F08080"]
    Q: Convert the following verbal description of a color palette into a list of colors: sage, nature, earth
    A: ["#EDF1D6", "#9DC08B", "#609966", "#40513B" )

    Desired Format: a JSON array of hexadecimal color codes

    Text: {msg}

    Result:
    """

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=100, # for each completion max tokens is 100
    )
    return json.loads(response.choices[0].message.content)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/palette", methods=["POST"])
def get_colors():
    msg = request.form.get("query")
    colors = get_colors_for_prompt(msg)
    return {"colors":colors}

if __name__ == "__main__":
    app.run(debug=True)