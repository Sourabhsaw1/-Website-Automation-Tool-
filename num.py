import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# ── Page Config ─────────────────────────────────────────────
st.set_page_config(
    page_title="Web Scraping & Automation Tool",
    page_icon="🤖",
    layout="centered"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

    @keyframes gradientBG {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    @keyframes flicker {
        0%, 100% { opacity: 1; }
        92% { opacity: 1; }
        93% { opacity: 0.4; }
        94% { opacity: 1; }
        96% { opacity: 0.6; }
        97% { opacity: 1; }
    }

    .stApp {
        background: linear-gradient(-45deg, #000000, #001a00, #000d1a, #0a0010, #001a00, #000000) !important;
        background-size: 400% 400% !important;
        animation: gradientBG 8s ease infinite !important;
        font-family: 'Share Tech Mono', monospace !important;
    }

    section[data-testid="stSidebar"] {
        background: rgba(0, 8, 0, 0.95) !important;
        border-right: 1px solid #00ff41 !important;
    }

    html, body, p, label, span, div, .stMarkdown, .stText {
        color: #00ff41 !important;
        font-family: 'Share Tech Mono', monospace !important;
    }

    h1 {
        color: #00ff41 !important;
        text-shadow: 0 0 10px #00ff41, 0 0 30px #00ff41 !important;
        font-family: 'Share Tech Mono', monospace !important;
        letter-spacing: 3px;
        animation: flicker 5s infinite;
    }

    h2, h3 {
        color: #00ff41 !important;
        text-shadow: 0 0 8px #00ff41 !important;
        font-family: 'Share Tech Mono', monospace !important;
        letter-spacing: 2px;
    }

    .stTextInput input {
        background: #001200 !important;
        color: #00ff41 !important;
        border: 1px solid #00ff41 !important;
        border-radius: 4px !important;
        font-family: 'Share Tech Mono', monospace !important;
        caret-color: #00ff41;
        box-shadow: inset 0 0 6px rgba(0,255,65,0.15) !important;
    }
    .stTextInput input:focus {
        box-shadow: 0 0 10px #00ff41, inset 0 0 6px rgba(0,255,65,0.2) !important;
    }

    .stButton>button {
        background: transparent !important;
        color: #00ff41 !important;
        border: 2px solid #00ff41 !important;
        border-radius: 4px !important;
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 1rem !important;
        letter-spacing: 3px;
        text-transform: uppercase;
        width: 100%;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background: #00ff41 !important;
        color: #000 !important;
        box-shadow: 0 0 20px #00ff41, 0 0 40px rgba(0,255,65,0.4) !important;
    }

    hr { border-color: #00ff41 !important; opacity: 0.2 !important; }

    .result-box {
        background: rgba(0, 20, 0, 0.8);
        border-left: 3px solid #00ff41;
        padding: 1em;
        border-radius: 4px;
        margin-top: 1em;
        font-family: 'Share Tech Mono', monospace;
        color: #00ff41;
        box-shadow: 0 0 15px rgba(0,255,65,0.15);
    }

    .stDownloadButton>button {
        background: transparent !important;
        color: #00ff41 !important;
        border: 1px solid #00ff41 !important;
        font-family: 'Share Tech Mono', monospace !important;
    }

    .stSuccess { background: rgba(0,20,0,0.8) !important; border: 1px solid #00ff41 !important; color: #00ff41 !important; }
    .stError   { background: rgba(20,0,0,0.8) !important; border: 1px solid #ff4444 !important; color: #ff4444 !important; }
    .stInfo    { background: rgba(0,20,0,0.8) !important; border: 1px solid #00ff41 !important; }
    .stWarning { background: rgba(20,15,0,0.8) !important; border: 1px solid #ffaa00 !important; color: #ffaa00 !important; }
    </style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────
st.title("🤖 Web Scraping & Automation Tool")
st.caption("Scrape any public website — extract links, headings, paragraphs, images and more.")
st.divider()

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")
    timeout = st.slider("Request timeout (seconds)", 5, 30, 10)
    max_results = st.slider("Max results to show", 5, 100, 20)
    st.divider()
    st.header("📌 What to Extract")
    extract_links = st.checkbox("Links (href)", value=True)
    extract_headings = st.checkbox("Headings (h1, h2, h3)", value=True)
    extract_paragraphs = st.checkbox("Paragraphs", value=False)
    extract_images = st.checkbox("Image URLs", value=False)
    st.divider()
    st.info("Only works on public websites. Login-required pages cannot be scraped.")

# ── Input ────────────────────────────────────────────────────
st.subheader("🔗 Enter Website URL")
url = st.text_input("Website URL", placeholder="https://example.com")
keyword_filter = st.text_input("Filter results by keyword (optional)", placeholder="e.g. python, jobs, news")

# ── Scrape Function ──────────────────────────────────────────
def scrape_website(url, timeout, max_results, keyword_filter,
                   extract_links, extract_headings, extract_paragraphs, extract_images):

    results = {}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        page_title = soup.title.string.strip() if soup.title else "No title found"
        results["page_title"] = page_title
        results["status_code"] = response.status_code

        def apply_filter(text):
            if keyword_filter:
                return keyword_filter.lower() in text.lower()
            return True

        if extract_links:
            links = []
            for a in soup.find_all("a", href=True):
                href = a["href"]
                text = a.get_text(strip=True) or href
                if href.startswith("http") and apply_filter(text):
                    links.append({"Text": text[:80], "URL": href})
                if len(links) >= max_results:
                    break
            results["links"] = links

        if extract_headings:
            headings = []
            for tag in soup.find_all(["h1", "h2", "h3"]):
                text = tag.get_text(strip=True)
                if text and apply_filter(text):
                    headings.append({"Tag": tag.name.upper(), "Text": text[:120]})
                if len(headings) >= max_results:
                    break
            results["headings"] = headings

        if extract_paragraphs:
            paras = []
            for p in soup.find_all("p"):
                text = p.get_text(strip=True)
                if len(text) > 30 and apply_filter(text):
                    paras.append({"Paragraph": text[:200]})
                if len(paras) >= max_results:
                    break
            results["paragraphs"] = paras

        if extract_images:
            images = []
            for img in soup.find_all("img", src=True):
                src = img["src"]
                alt = img.get("alt", "No alt text")
                if src.startswith("http") and apply_filter(alt):
                    images.append({"Alt Text": alt[:80], "URL": src})
                if len(images) >= max_results:
                    break
            results["images"] = images

        return results, None

    except requests.exceptions.Timeout:
        return None, "❌ Request timed out. Try increasing timeout in settings."
    except requests.exceptions.ConnectionError:
        return None, "❌ Could not connect to the website. Check the URL."
    except requests.exceptions.HTTPError as e:
        return None, f"❌ HTTP Error: {e}"
    except Exception as e:
        return None, f"❌ Error: {str(e)}"

# ── Run Button ───────────────────────────────────────────────
st.divider()
if st.button("🚀 Start Scraping"):
    if not url:
        st.error("Please enter a website URL.")
    elif not url.startswith("http"):
        st.error("URL must start with http:// or https://")
    else:
        with st.spinner("Scraping website... please wait."):
            start = time.time()
            data, error = scrape_website(
                url, timeout, max_results, keyword_filter,
                extract_links, extract_headings, extract_paragraphs, extract_images
            )
            elapsed = round(time.time() - start, 2)

        if error:
            st.error(error)
        else:
            st.success(f"✅ Scraped successfully in {elapsed}s")

            st.markdown(f"""
            <div class="result-box">
                <b>Page Title:</b> {data.get('page_title', 'N/A')}<br>
                <b>Status Code:</b> {data.get('status_code', 'N/A')}
            </div>
            """, unsafe_allow_html=True)

            st.divider()

            if extract_links and data.get("links"):
                st.subheader(f"🔗 Links Found ({len(data['links'])})")
                df_links = pd.DataFrame(data["links"])
                st.dataframe(df_links, use_container_width=True)
                csv = df_links.to_csv(index=False)
                st.download_button("⬇️ Download Links as CSV", csv, "links.csv", "text/csv")

            if extract_headings and data.get("headings"):
                st.subheader(f"📋 Headings Found ({len(data['headings'])})")
                df_h = pd.DataFrame(data["headings"])
                st.dataframe(df_h, use_container_width=True)

            if extract_paragraphs and data.get("paragraphs"):
                st.subheader(f"📝 Paragraphs Found ({len(data['paragraphs'])})")
                df_p = pd.DataFrame(data["paragraphs"])
                st.dataframe(df_p, use_container_width=True)

            if extract_images and data.get("images"):
                st.subheader(f"🖼️ Images Found ({len(data['images'])})")
                df_i = pd.DataFrame(data["images"])
                st.dataframe(df_i, use_container_width=True)

            if not any([
                data.get("links"), data.get("headings"),
                data.get("paragraphs"), data.get("images")
            ]):
                st.warning("No results found. Try removing the keyword filter or selecting different extraction options.")

# ── Footer ───────────────────────────────────────────────────
st.divider()
st.caption("Built by Sourabh Saw | Python • BeautifulSoup • Streamlit")
