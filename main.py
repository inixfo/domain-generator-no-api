# Import necessary libraries
import openai
from flask import Flask, render_template, request
import requests
import creds

# Configure OpenAI API
openai.api_key = creds.OPENAI_API_KEY

# Configure GoDaddy API credentials
GODADDY_API_KEY = "gHVX42iz2oWP_RvpbQX8SHvcDfMNdKmbjV7"
GODADDY_API_SECRET = "iq4tkykCNLCJkEHYfgwCa"

# Initialize Flask application
app = Flask(__name__)

# Home page route
@app.route('/')
def home():
    return render_template('index.html')

# Domain suggestion and availability check route
@app.route('/suggest', methods=['POST'])
def suggest():
    # Get user inputs from the form
    domain_type = request.form.get('domain_type')
    prompt = request.form['prompt']
    domain_extension = request.form.get('domain_extension')

    # Generate domain name suggestions using OpenAI GPT-3.5
    if domain_type == 'Brandable':
        prompt = f"I want a brandable domain name related to {prompt}. Please give it without extension"
    elif domain_type == 'Random':
        prompt = f"I want a random domain name suggestion related to {prompt}. Please give it without extension"
    elif domain_type == 'Two-word Combination':
        prompt = f"I want a domain name that is a combination of two words related to {prompt}. Please give it without extension"
    elif domain_type == 'Portmanteau':
        prompt = f"I want a portmanteau domain name related to {prompt}. Please give it without extension"
    elif domain_type == 'Alternate Spelling':
        prompt = f"I want a domain name with an alternate spelling related to {prompt}. Please give it without extension"
    elif domain_type == 'Non-English Names':
        prompt = f"I want a non-English domain name related to {prompt}. Please give it without extension"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=30,
        n=50,
        stop=None,
        temperature=0.5,
    )
    suggestions = list(set([choice['text'].strip() for choice in response.choices if choice['text'].strip()]))
    print("Domain Suggestions:", suggestions)

    # Check availability of domain name suggestions using GoDaddy API
    available_domains = []
    for suggestion in suggestions:
        url = f"https://api.godaddy.com/v1/domains/available?domain={suggestion}{domain_extension}"
        headers = {
            "Authorization": f"sso-key {GODADDY_API_KEY}:{GODADDY_API_SECRET}"
        }
        response = requests.get(url, headers=headers)
        print("GoDaddy API Response:", response.json())

        if response.status_code == 200:
            data = response.json()
            if data.get('available'):
                available_domains.append(suggestion + domain_extension)

    # If no available domains found for the chosen extension, suggest other extensions
    if not available_domains:
        alternative_extensions = ['.net', '.co', '.org', '.ai', '.io']
        for extension in alternative_extensions:
            url = f"https://api.godaddy.com/v1/domains/available?domain={suggestion}{extension}"
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data.get('available'):
                    available_domains.append(suggestion + extension)
                    break

    # Pass the suggestions and availability to the template
    return render_template('suggestions.html', suggestions=available_domains)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
