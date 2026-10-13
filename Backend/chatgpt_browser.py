import os
import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


# ============================================================
# CONFIG
# ============================================================

CHATGPT_URL = "https://chatgpt.com/"
PROMPT = """
Give me 5 real estate businesses in Nagercoil.

Return ONLY JSON in this format:

[
  {
    "name": "Business Name",
    "location": "Location",
    "contact": "Phone number",
    "own_website": true
  }
]

Do not add markdown.
Do not add explanations.
"""

OUTPUT_FILE = "chatgpt_output.txt"


# ============================================================
# MAIN
# ============================================================

def main():

    with sync_playwright() as p:

        # ----------------------------------------------------
        # Persistent browser
        # ----------------------------------------------------
        # Login/session will remain inside this folder.
        # First run: login manually.
        # Next runs: login usually remains.
        # ----------------------------------------------------

        user_data_dir = os.path.join(
            os.getcwd(),
            "chatgpt_browser"
        )

        context = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,
            viewport={
                "width": 1400,
                "height": 900
            }
        )

        page = context.pages[0] if context.pages else context.new_page()

        # ----------------------------------------------------
        # Open ChatGPT
        # ----------------------------------------------------

        print("\n==============================================")
        print("       CHATGPT BROWSER AUTOMATION")
        print("==============================================")

        print("\nOpening ChatGPT...")

        page.goto(
            CHATGPT_URL,
            wait_until="domcontentloaded",
            timeout=60000
        )

        time.sleep(5)

        print("\nIf login is required:")
        print("Login manually in the browser.")
        print("Then come back to this terminal.")

        input("\nPress ENTER after ChatGPT is ready... ")

        # ----------------------------------------------------
        # Find input box
        # ----------------------------------------------------

        print("\nFinding ChatGPT input box...")

        textarea = page.locator("textarea").first

        try:

            textarea.wait_for(
                state="visible",
                timeout=30000
            )

        except PlaywrightTimeoutError:

            print("\nERROR: ChatGPT input box not found.")

            print("\nVisible text:")
            print(page.locator("body").inner_text()[:3000])

            context.close()
            return

        print("Input box found.")

        # ----------------------------------------------------
        # Type prompt
        # ----------------------------------------------------

        print("\nTyping prompt...")

        textarea.fill(PROMPT)

        time.sleep(1)

        # ----------------------------------------------------
        # Send
        # ----------------------------------------------------

        print("Sending prompt...")

        textarea.press("Enter")

        # ----------------------------------------------------
        # Wait for response
        # ----------------------------------------------------

        print("\nWaiting for ChatGPT response...")

        time.sleep(5)

        # Wait until response appears
        for i in range(60):

            time.sleep(2)

            body_text = page.locator("body").inner_text()

            # Basic response detection
            if len(body_text) > 500:

                print(
                    f"Response detected after "
                    f"{(i + 1) * 2} seconds."
                )

                break

        # ----------------------------------------------------
        # Extract response
        # ----------------------------------------------------

        print("\nExtracting response...")

        # ChatGPT normally renders assistant messages
        # inside article elements.

        messages = page.locator(
            '[data-message-author-role="assistant"]'
        )

        count = messages.count()

        response_text = ""

        if count > 0:

            response_text = messages.nth(
                count - 1
            ).inner_text()

        else:

            # Fallback
            response_text = page.locator(
                "body"
            ).inner_text()

        # ----------------------------------------------------
        # Print
        # ----------------------------------------------------

        print("\n")
        print("=" * 60)
        print("CHATGPT RESPONSE")
        print("=" * 60)

        print(response_text)

        # ----------------------------------------------------
        # Save
        # ----------------------------------------------------

        with open(
            OUTPUT_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(response_text)

        print("\n" + "=" * 60)

        print(
            f"Response saved to: {OUTPUT_FILE}"
        )

        print("=" * 60)

        # ----------------------------------------------------
        # Keep browser open
        # ----------------------------------------------------

        input(
            "\nPress ENTER to close browser..."
        )

        context.close()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()

