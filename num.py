import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def automate_website(url, search_query, link):
    # Set up the WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    try:
        # Open the website
        driver.get(url)
        
        # Perform a search operation (example for Google)
        search_box = driver.find_element(By.NAME, 'q')
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)
        
        time.sleep(2)  # Wait for the search results to load
        
        # Click on the provided link if available
        if link:
            desired_link = driver.find_element(By.PARTIAL_LINK_TEXT, link)
            desired_link.click()
        
        time.sleep(2)  # Wait for the page to load
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        # Close the driver
        driver.quit()

def main():
    st.title('Website Automation Tool')

    url = st.text_input('Enter the website URL')
    search_query = st.text_input('Enter the search query')
    link = st.text_input('Enter the link text to click (optional)')

    if st.button('Automate'):
        if url and search_query:
            st.write(f'Automating {url} with search query "{search_query}"')
            automate_website(url, search_query, link)
            st.success('Automation completed')
        else:
            st.error('Please provide both URL and search query')

if __name__ == "__main__":
    main()
