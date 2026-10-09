import pdfplumber
import requests
from bs4 import BeautifulSoup


def extract_text_from_pdf(uploaded_file):
    text = ""
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        return f"Error: {e}"
    return text.strip()


def extract_text_from_url(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        parts = soup.find_all(["p", "li", "h1", "h2", "h3"])
        text = "\n".join(p.get_text(strip=True) for p in parts if p.get_text(strip=True))

        if not text.strip():
            return "Error: এই URL থেকে কোনো readable text পাওয়া যায়নি"

        return text
    except requests.exceptions.RequestException as e:
        return f"Error: URL-এ পৌঁছানো যায়নি — {e}"
    except Exception as e:
        return f"Error: {e}"