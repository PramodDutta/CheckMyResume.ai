import os
import re

from flask import Flask, request, render_template
from openai import OpenAI

app = Flask(__name__)


@app.route('/analyze', methods=['GET'])
def analyze_resume():
    # Extract the image URL from the query parameter
    image_url = request.args.get('image_url')
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = (
        "\"Analyze the attached resume image and provide a detailed review in the following format:\n\n"
        "1. Overall Result: [Score out of 10]\n"
        "2. Effectivity: [Score out of 10] with feedback on how effectively the resume presents the applicant's skills and experiences.\n"
        "3. Layout and Design: [Score out of 10] with comments on the visual appeal and organization of the resume.\n"
        "4. Content Relevance: [Score out of 10] with insights on the relevance and adequacy of the information provided.\n"
        "5. Grammar and Syntax: [Score out of 10] with observations on the language quality and readability.\n"
        "6. Impact: [Score out of 10] with thoughts on how the resume stands out or catches attention.\n\n"
        "Use symbols like ✅ for positive aspects and 🙈 for areas of improvement.\"\n\n"
        "\n"
    )
    response_data = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url,
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    data = response_data.choices[0].message.content
    category_data = re.split(r'\n?(?=\d+\.)', data)
    return render_template('result.html', category_data=category_data, image_url=image_url)


if __name__ == '__main__':
    app.run(debug=True)
