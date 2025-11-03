# from playwright.sync_api import sync_playwright
# import json
# import time
# from dotenv import load_dotenv
# import os

# # Load credentials from .env file
# load_dotenv()

# # USERNAME = os.getenv("SITE_USERNAME", "Ali")
# # PASSWORD = os.getenv("SITE_PASSWORD", "123456")

# def extract_header_links(username, password, headless=False):
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=headless, slow_mo=200)
#         context = browser.new_context()
#         page = context.new_page()

#         print("🌐 Navigating to login page...")
#         page.goto("https://www.340bpriceguide.net/login", wait_until="domcontentloaded")

#         # ✅ Wait for visible input fields
#         page.wait_for_selector("input[name='username']:visible", timeout=10000)
#         page.wait_for_selector("input[name='password']:visible", timeout=10000)

#         print("🔐 Filling in login credentials...")
#         page.locator("input[name='username']:visible").fill(username)
#         page.locator("input[name='password']:visible").fill(password)

#         # Optional: click Remember Me checkbox
#         try:
#             page.locator("input[type='checkbox']:visible").check()
#         except:
#             print("⚠️ Remember me checkbox not found, skipping.")

#         print("➡️ Clicking 'Log In' button...")
#         page.locator("button:has-text('Log In'):visible").click()

#         # ✅ Wait for redirect after login
#         try:
#             page.wait_for_url("**/my-profile", timeout=15000)
#             print("✅ Login successful, redirected to profile page.")
#         except:
#             print("⚠️ Login may not have redirected yet, waiting for network idle.")
#             page.wait_for_load_state("networkidle")
#             time.sleep(3)

#         # Optional: take screenshot after login
#         # page.screenshot(path="after_login.png", full_page=True)
#         # print("📸 Screenshot saved after login.")

#         # ✅ Extract header links
#         print("🔗 Extracting header links...")
#         links = page.eval_on_selector_all(
#             "header a",
#             "els => els.map(e => ({text: e.innerText.trim(), href: e.href}))"
#         )

#         with open("header_links_After_Login.json", "w", encoding="utf-8") as f:
#             json.dump(links, f, indent=2, ensure_ascii=False)

#         print(f"✅ Extracted {len(links)} header links. Saved to header_links.json")

#         browser.close()

# def clean_header_links(input_file="header_links_After_Login.json", output_file="header_links_After_Login.json"):
#     # Load the header links JSON
#     with open(input_file, "r", encoding="utf-8") as f:
#         links = json.load(f)

#     # Filter out entries where "text" is empty or only spaces
#     cleaned_links = [link for link in links if link["text"].strip()]

#     # Save the cleaned JSON
#     with open(output_file, "w", encoding="utf-8") as f:
#         json.dump(cleaned_links, f, indent=2, ensure_ascii=False)

#     print(f"✅ Cleaned {len(links) - len(cleaned_links)} invalid entries.")
#     print(f"💾 Saved cleaned links to {output_file}")

# def login_section(username=None, password=None, headless=False):
#     from dotenv import load_dotenv # type: ignore
#     from Header_Links_Ectractor_After_Login import extract_header_links_and_screenshots
#     from Header_mindmaps_after_login import header
#     from Merge_all_header_mindmap_After_Login import merge_mindmaps
#     import asyncio
#     from Validation_Mindmap_After_login import validation_after_login
#     import os
#     load_dotenv()

#     env_user = os.getenv("SITE_USERNAME")
#     env_pass = os.getenv("SITE_PASSWORD")

#     # If credentials not provided, fall back to .env
#     username = username or env_user
#     password = password or env_pass

#     if not username or not password:
#         raise ValueError("❌ Username and Password are required (either from input or .env).")

#     extract_header_links(username, password, headless=headless) #1
#     clean_header_links()
#     print("✅ Login section completed successfully")

#     print("########## start header_link_extractor after login #######")

#     extract_header_links_and_screenshots(username, password, headless=headless) #2

#     print("######## Header mindmap after login ##########")
#     asyncio.run(header()) #3

#     print("######## Start Merging mindmap after login #########")
#     merge_mindmaps() # 4
#     print("Mindmapp after login merged Sucessfully")

#     print("###### Validating after login ##########")
#     validation_after_login() #5

   

#     print("Fully Mindmapp is created")
# # if __name__ == "__main__":
#     # def login_section():
#     #     if not USERNAME or not PASSWORD:
#     #         raise ValueError("❌ Please set SITE_USERNAME and SITE_PASSWORD in your .env file")

#     #     extract_header_links(USERNAME, PASSWORD, headless=False)
#     #     clean_header_links()
#     #     print("login section completed")
