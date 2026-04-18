import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# ── Page Config ─────────────────────────────────────────────
st.set_page_config(
    page_title="Website Automation Tool",
    page_icon="🤖",
    layout="centered"
)

# ── Custom CSS ───────────────────────────────────────────────
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        background-color: #1a5276;
        color: white;
        border-radius: 8px;
        padding: 0.5em 2em;
        font-weight: bold;
        border: none;
        width: 100%;
    }
    .stButton>button:hover { background-color: #154360; }
    .result-box {
        background: #eaf4fb;
        border-left: 4px solid #1a5276;
        padding: 1em;
        border-radius: 6px;
        margin-top: 1em;
    }
    </style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────
st.title("🤖 Website Automation Tool")
st.caption("Automate website interactions — search, navigate, and extract results.")
st.divider()

# ── Sidebar Settings ─────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")
    headless = st.toggle("Run in headless mode (no browser window)", value=True)
    wait_time = st.slider("Wait time between actions (seconds)", 1, 5, 2)
    st.info("Headless mode is recommended for smooth operation.")

# ── Input Form ───────────────────────────────────────────────
st.subheader("🔗 Automation Setup")

col1, col2 = st.columns(2)
with col1:
    url = st.text_input("Website URL", placeholder="https://www.google.com")
with col2:
    search_query = st.text_input("Search Query", placeholder="e.g. Python jobs in India")

link_text = st.text_input("Link text to click after search (optional)", placeholder="e.g. Python Developer")
capture_results = st.checkbox("Show page title after automation", value=True)

# ── Core Automation Function ─────────────────────────────────
def run_automation(url, query, link_text, headless, wait_time, capture_results):
    logs = []
    page_title = None

    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        logs.append(("success", f"✅ Browser launched successfully"))

        driver.get(url)
        logs.append(("success", f"✅ Opened: {url}"))

        # Try to find search box
        try:
            wait = WebDriverWait(driver, 10)
            search_box = wait.until(EC.presence_of_element_located((By.NAME, 'q')))
            search_box.clear()
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            logs.append(("success", f"✅ Searched for: '{query}'"))
            time.sleep(wait_time)
        except Exception:
            logs.append(("warning", "⚠️ Could not find search box (site may not use 'q' field)"))

        # Try to click a link
        if link_text:
            try:
                wait = WebDriverWait(driver, 8)
                link = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, link_text)))
                link.click()
                logs.append(("success", f"✅ Clicked link: '{link_text}'"))
                time.sleep(wait_time)
            except Exception:
                logs.append(("warning", f"⚠️ Could not find link with text: '{link_text}'"))

        if capture_results:
            page_title = driver.title
            logs.append(("info", f"📄 Page title: {page_title}"))

        driver.quit()
        logs.append(("success", "✅ Browser closed successfully"))

    except Exception as e:
        logs.append(("error", f"❌ Error: {str(e)}"))

    return logs, page_title

# ── Run Button ───────────────────────────────────────────────
st.divider()
if st.button("🚀 Run Automation"):
    if not url:
        st.error("Please enter a website URL.")
    elif not search_query:
        st.error("Please enter a search query.")
    else:
        with st.spinner("Running automation... please wait."):
            logs, title = run_automation(url, search_query, link_text, headless, wait_time, capture_results)

        st.subheader("📋 Automation Log")
        for log_type, msg in logs:
            if log_type == "success":
                st.success(msg)
            elif log_type == "warning":
                st.warning(msg)
            elif log_type == "error":
                st.error(msg)
            else:
                st.info(msg)

        if title:
            st.markdown(f"""
            <div class="result-box">
                <b>Final Page Title:</b> {title}
            </div>
            """, unsafe_allow_html=True)

# ── Footer ───────────────────────────────────────────────────
st.divider()
st.caption("Built by Sourabh Saw | Python • Selenium • Streamlit")
