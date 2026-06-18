from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/scrape", methods=["GET"])
def scrape():

    url = request.args.get("url")

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.text if soup.title else "No title found"

    description = ""

    meta = soup.find("meta", attrs={"name": "description"})

    if meta:
        description = meta.get("content", "")

    h1_headings = [
        h.get_text(strip=True)
        for h in soup.find_all("h1")
    ]

    h2_headings = [
        h.get_text(strip=True)
        for h in soup.find_all("h2")
    ]

    paragraphs = [
        p.get_text(strip=True)
        for p in soup.find_all("p")
    ]

    full_text = " ".join(paragraphs)

    links = [
        a.get("href")
        for a in soup.find_all("a", href=True)
    ]

    return jsonify({
        "website": url,
        "title": title,
        "description": description,
        "h1_headings": h1_headings,
        "h2_headings": h2_headings,
        "paragraphs": paragraphs[:20],
        "full_text": full_text,
        "links": links[:20]
    })

if __name__ == "__main__":
    app.run(debug=True)
