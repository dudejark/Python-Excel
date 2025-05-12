from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from urllib.parse import quote
import time
import os
import subprocess
import re

def get_chrome_version():
    """Get the version of Chrome installed on macOS"""
    try:
        # Use system_profiler to get Chrome version on macOS
        result = subprocess.run(
            ['system_profiler', 'SPApplicationsDataType', '-xml'], 
            capture_output=True, text=True
        )
        match = re.search(r'Google Chrome\.app.*?<string>(\d+\.\d+\.\d+\.\d+)</string>', 
                          result.stdout, re.DOTALL)
        if match:
            return match.group(1)
        return None
    except Exception as e:
        print(f"Error getting Chrome version: {e}")
        return None

def download_matching_chromedriver(chrome_version):
    """Instructions to download matching ChromeDriver"""
    major_version = chrome_version.split('.')[0] if chrome_version else "unknown"
    print(f"\n⚠️ ChromeDriver might be incompatible with Chrome version {chrome_version}")
    print(f"Please download ChromeDriver matching Chrome version {major_version} from:")
    print("https://chromedriver.chromium.org/downloads")
    print("Then update the chromedriver_path in this script\n")

def main():
    # Get Chrome version
    chrome_version = get_chrome_version()
    if chrome_version:
        print(f"Detected Chrome version: {chrome_version}")
    
    # Step 1: Setup Chrome options with correct binary path
    chrome_binary_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    chromedriver_path = "/usr/local/bin/chromedriver"  # Update this path if needed
    
    # Check if chromedriver exists
    if not os.path.exists(chromedriver_path):
        print(f"❌ ChromeDriver not found at {chromedriver_path}")
        print("Please download ChromeDriver and update the path in this script")
        return
    
    options = Options()
    options.binary_location = chrome_binary_path
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    
    # Add user-agent to help avoid detection
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Initialize the Chrome driver
    try:
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=options)
    except WebDriverException as e:
        print(f"❌ ChromeDriver error: {e}")
        download_matching_chromedriver(chrome_version)
        return
    
    try:
        # Step 2: Go to WhatsApp Web
        driver.get("https://web.whatsapp.com")
        print("🔒 Please scan the QR code with your phone.")
        
        # Wait for manual QR code scanning
        input("✅ After scanning and chats are fully loaded, press Enter to continue...")
        
        # Step 3: Prepare message and recipient
        target_number = "+919971822900"  # Replace with your target number
        message = "Hello, this is an automated message from macOS using Python!"
        
        # URL encode the message
        encoded_message = quote(message)
        url = f"https://web.whatsapp.com/send?phone={target_number}&text={encoded_message}"
        
        # Navigate to the specific chat
        driver.get(url)
        
        # Step 4: Wait for chat to load and send message
        print("Waiting for chat to load...")
        
        # Locate the message input field
        input_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@title='Type a message']"))
        )
        print("✅ Message input field located.")

        # Enter the message into the input field
        input_field.click()
        input_field.send_keys(message)
        print("✅ Message entered into input field.")

        # Try multiple possible selectors for the send button
        selectors = [
            "//button[@aria-label='Send']",
            "//div[@role='button' and @aria-label='Send']",
            "//span[contains(@data-testid, 'send')]",
            "//button[@data-testid='compose-btn-send']",
            "//button[contains(@class, 'send')]"
        ]

        send_button = None
        for selector in selectors:
            try:
                print(f"Trying selector: {selector}")
                send_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                print(f"✅ Found send button with selector: {selector}")
                break
            except TimeoutException:
                print(f"❌ Selector not found: {selector}")
                continue

        if not send_button:
            # If no button found, try to use keyboard shortcut
            print("Trying keyboard shortcut...")
            input_field.send_keys(Keys.ENTER)
            print("✅ Sent message using keyboard shortcut")
        else:
            # Click the send button
            send_button.click()
            print("✅ Message sent successfully!")

        # Wait a moment to see the message delivered
        time.sleep(5)
        
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        
    finally:
        # Always clean up resources
        print("Closing browser...")
        driver.quit()

if __name__ == "__main__":
    main()