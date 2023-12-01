import os
from playwright.sync_api import ViewportSize, sync_playwright

from auth import REDDIT_AUTH
from urllib.parse import urljoin

from settings import (
    COMMENT_CONFIG,
    VIDEO_OUTPUT_DIR,
)

base_url = "https://www.reddit.com/"

def capture_element_screenshot(urls):

    if not any(not os.path.exists(os.path.join(COMMENT_CONFIG['output_directory'], f"{comment.name}.png"))
               for comment in urls[:COMMENT_CONFIG['max_comments']]):
        print("Comments already screenshotted...")
        return


    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.set_viewport_size(ViewportSize(width=1920, height=1080))

        page.goto("https://www.reddit.com/login")

        # Check if the first set of selectors exist and fill in the username and password.
        if page.query_selector("#loginUsername"):
            page.type("#loginUsername", REDDIT_AUTH["username"])
            page.type("#loginPassword", REDDIT_AUTH["password"])
            page.click('button[type="submit"]')
            page.wait_for_url("https://www.reddit.com/")

        # If the first set of selectors don't exist, try the second set.
        elif page.query_selector("#login-username"):
            page.type("#login-username", REDDIT_AUTH["username"])
            page.type("#login-password", REDDIT_AUTH["password"])
            page.click('button[type="button"]')
            page.wait_for_url("https://www.reddit.com/")
        else:
            print("Username and password fields not found.")

        for i, comment in enumerate(urls, start=1):
            output_file_name = f"{comment.name}.png"
            output_image_path = os.path.join(COMMENT_CONFIG['output_directory'],
                                             output_file_name)

            # Skip if output_image_path already exists
            if os.path.exists(output_image_path):
                print(f"Skipping comment screenshot. File already exists: {output_image_path}")
                continue

            comment_url=urljoin(base_url, comment.permalink)
            print(f"Screenshotting Comment {str(i)} : {comment_url}")
            page.goto(comment_url)

            # Wait for the element to be present before taking a screenshot
            element_selector = f"id={comment.name}"
            page.wait_for_selector(element_selector)
            page.locator(element_selector).screenshot(path=output_image_path)

            # Break the loop if the number of comments reaches the maximum
            if i + 1 > COMMENT_CONFIG['max_comments']:
                print(f"Reached the maximum number of comments ({COMMENT_CONFIG['max_comments']}). Stopping.")
                break

        browser.close()

if __name__ == "__main__":
    reddit_comment_urls = [
        "https://www.reddit.com/r/QualityAssurance/comments/vy8596/comment/ig0qeih",
        "https://www.reddit.com/r/QualityAssurance/comments/vy8596/comment/ig14vcs",
        "https://www.reddit.com/r/QualityAssurance/comments/vy8596/comment/ig0uat3",
        "https://www.reddit.com/r/QualityAssurance/comments/vy8596/comment/ig3z55k"
        # Add more URLs as needed
    ]

    capture_element_screenshot(reddit_comment_urls)
    print("Screenshots saved.")
