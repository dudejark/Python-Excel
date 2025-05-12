from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# The input_box initialization will be moved to the appropriate location after the driver is defined.

# Step 1: Setup Chrome options and correct binary path
chrome_binary_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"  # OR the correct path

options = Options()
options.binary_location = chrome_binary_path

service = Service("/usr/local/bin/chromedriver")

# Step 2: Launch driver
driver = webdriver.Chrome(service=service, options=options)

# Step 3: Go to WhatsApp Web
driver.get("https://web.whatsapp.com")
print("🔒 Please scan the QR code with your phone.")
# time.sleep(20)  # Adjust if you need more time
input("✅ After scanning and chats are fully loaded, press Enter to continue...")
# Step 4: Prepare to send message
target_number = "+919971822900"
message = "Hello, this is an automated message from macOS using Python!"
url = f"https://web.whatsapp.com/send?phone={target_number}&text={message}"
driver.get(url)

# Step 5: Wait for WhatsApp to load and send message
time.sleep(10)
try:
    input_box = WebDriverWait(driver, 50).until(
    EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true' and @data-testid='conversation-compose-box-input']"))
)
    time.sleep(1)
    input_box.send_keys(Keys.ENTER)
    print("✅ Message sent successfully!")
except Exception as e:
    print("❌ Could not send the message:", e)

# Step 6: Clean up
time.sleep(10)
driver.quit()