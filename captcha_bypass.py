from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import requests
import pytesseract
import base64


options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def connection():
    driver.get("http://challenge01.root-me.org/programmation/ch8/")

    # Get the captcha image
    captcha = driver.find_element(By.TAG_NAME, "img")
    src = captcha.get_attribute("src")


    # Remove the "data:image/png;base64," prefix
    base64_image = src.replace('data:image/png;base64,', '')

    # Decode the Base64 string
    image_data = base64.b64decode(base64_image)

    # Save the decoded image data to a file
    with open('image.png', 'wb') as file:
        file.write(image_data)

    # Use pytesseract to extract the text from the image
    captcha_text = pytesseract.image_to_string('image.png')
    # only keep alphanumeric characters
    captcha_text = ''.join(e for e in captcha_text if e.isalnum())

    print(captcha_text)

    captcha_box = driver.find_element(By.NAME, "cametu")
    captcha_box.send_keys(captcha_text)

    # click on Try button : <input type="submit" value="Try">

    try_button = driver.find_element(By.XPATH, "//input[@value='Try']")
    try_button.click()

    # receive response
    response = driver.find_element(By.TAG_NAME, "body")
    print(response.text)
    return response.text

while True:
    response = connection()
    # if Raté isn't in the response, we have the flag
    if "Raté" not in response:
        print(response)
        break

