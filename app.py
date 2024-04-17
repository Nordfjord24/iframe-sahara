from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
import re
import { SpeedInsights } from "@vercel/speed-insights/next"

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan_website():
    url_to_scan = request.form['url']
    api_key = 'D5QVJKKD7EJ1DJRQ3GSZ7617L3U6JENC10YZXGF223HPLNKWXW6FJCP9QU6ZGMW006UJKOWMS98D2CCM'
    response = requests.get(f"https://app.scrapingbee.com/api/v1/", params={'api_key': api_key, 'url': url_to_scan})
    
    #Google Tag Manager Check
    gtm_id = "Not Found"  # Default value if not found
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find GTM ID using regular expression
        matches = re.findall(r'googletagmanager\.com/ns\.html\?id=(GTM-\w+)', response.text)
        if matches:
            gtm_id = matches[0]  # Assuming the first match is the desired GTM ID

    # Enhanced check for Cookie Consent Tools/Platforms
        cookie_consent_keywords = ["cookieconsent", "cookiebot", "cookiehub", "consent"]
        cookie_consent = any(bool(soup.find_all(string=lambda text: keyword in text.lower())) for keyword in cookie_consent_keywords)

        
    # Pass the GTM ID and cookie consent check result to the template
        return render_template('results.html', url=url_to_scan, gtm_id=gtm_id, cookie_consent=cookie_consent)
    else:
        return f"Failed to fetch website: {response.status_code}"

if __name__ == '__main__':
    app.run(debug=True)
