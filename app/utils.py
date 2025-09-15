from bs4 import BeautifulSoup
import html2text

def html_to_text(html: str) -> str:
    if html is None:
        return ""
    # Prefer BeautifulSoup to strip tags, fallback to html2text for better formatting
    try:
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text("\n")
        return text.strip()
    except Exception:
        h = html2text.HTML2Text()
        h.ignore_links = False
        return h.handle(html).strip()
