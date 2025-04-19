import time
import random
import string
from playwright.sync_api import sync_playwright

def random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_strong_password(length=14):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.choices(chars, k=length))

EMAIL = f"{random_string(10)}@gmail.com"
DISPLAY_NAME = random_string(8)
USERNAME = random_string(8)
PASSWORD = generate_strong_password(16)
BIRTHDAY = {
    "day": str(random.randint(1, 28)),
    "month": random.randint(1, 12),
    "year": str(random.randint(1990, 2005))
}

def save_account(email, display_name, username, password, token):
    with open("accounts.txt", "a") as file:
        file.write(f"{email} | {display_name} | {username} | {password} | {token}\n")
    print("[💾] Account information saved!")

def create_discord_account():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)  
        page = browser.new_page()
        page.goto("https://discord.com/register")

        time.sleep(10) 

        print("[⏳] Filling out the form")

        try:
            page.fill("input[name='email']", EMAIL)
            page.fill("input[name='global_name']", DISPLAY_NAME)
            page.fill("input[name='username']", USERNAME)
            page.fill("input[name='password']", PASSWORD)

            print("[⏳] Filling in date of birth")

            day_input = page.locator("input[aria-label='Day']")
            day_input.click(force=True)
            day_input.fill(BIRTHDAY["day"])
            day_input.press("Enter")

            month_input = page.locator("input[aria-label='Month']")
            month_input.click(force=True)
            for _ in range(BIRTHDAY["month"]):  
                page.keyboard.press("ArrowDown")
                time.sleep(0.2)
            page.keyboard.press("Enter")

            year_input = page.locator("input[aria-label='Year']")
            year_input.click(force=True)
            year_input.fill(BIRTHDAY["year"])
            year_input.press("Enter")

            print(f"[✅] Set :  {BIRTHDAY['day']}/{BIRTHDAY['month']}/{BIRTHDAY['year']}")
            time.sleep(3)

            page.click("button[type='submit']")
            print("[✅] Request Sended Please Solver The Captcha")

            print("[⏳] Wait To Solver Captcha")
            time.sleep(60)  

            token_found = False
            token = ""

            def check_response(response):
                nonlocal token_found, token
                print(f"[🕵️] Check The Url: {response.url}") 
                
                if "/api/v9/auth/me" in response.url:
                    print("[🔍] Get Request Register Successfully")

                    try:
                        json_data = response.json()
                        print(f"[📝] Json File Open Successfully {json_data}") 

                        if "token" in json_data:
                            token = json_data["token"]
                            print(f"[✅] Token : {token[:20]}")
                            save_account(EMAIL, DISPLAY_NAME, USERNAME, PASSWORD, token)
                            token_found = True
                        else:
                            print("[⚠️] Token Not Into Request")

                    except Exception as e:
                        print(f"[❌] Error To Get Token :  {e}")

            print("[🔄] Lisinig To Response Requests")
            page.on("response", check_response)

            wait_time = 0
            max_wait = 90

            while not token_found and wait_time < max_wait:
                print("[⏳] Wait To Get Token")
                time.sleep(3)
                wait_time += 3

            if token_found:
                print("[✅] Token Collect Successfully")
            else:
                print("[❌] Token Not Found")

        except Exception as e:
            print(f"[❌] Error : {e}")

        try:
            if page.is_closed():
                print("Error To Get Information")
            else:
                print("[✅] Chrume Closed")
                page.close()
                browser.close()
        except Exception as e:
            print(f"Error When Close :  {e}")

create_discord_account()


