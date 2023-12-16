import os
from playwright.sync_api import ViewportSize, sync_playwright

from auth import REDDIT_AUTH
from urllib.parse import urljoin

from settings import (
    COMMENT_CONFIG,
)

base_url = "https://www.reddit.com/"

class RedditScreenshotCapture:
    def __init__(self):
        self.browser = None

    def _login(self, page):
        # Assuming there is a login form with username and password fields
        if page.query_selector("#loginUsername"):
            page.type("#loginUsername", REDDIT_AUTH["username"])
            page.type("#loginPassword", REDDIT_AUTH["password"])
            page.click('button[type="submit"]')
            page.wait_for_url("https://www.reddit.com/")
        elif page.query_selector("#login-username"):
            page.type("#login-username", REDDIT_AUTH["username"])
            page.type("#login-password", REDDIT_AUTH["password"])
            page.click('button[type="button"]')
            page.wait_for_url("https://www.reddit.com/")
        else:
            print("Username and password fields not found.")

    def _skip_comment_if_exists(self, comment, output_image_path):
        if os.path.exists(output_image_path):
            print(f"Skipping comment screenshot. File already exists: {output_image_path}")
            return True
        return False

    def _capture_screenshot_legacy_layout(self, page, comment, output_image_path):
        page.locator(f"#t1_{comment.id}").screenshot(path=output_image_path)

    def _capture_screenshot_new_layout(self, page, comment, output_image_path):
        page.wait_for_selector('shreddit-comment')
        selector = f'shreddit-comment[thingid="t1_{comment.id}"]'
        entry_element = page.wait_for_selector(selector)

        collapsed_attribute_exists = page.eval_on_selector(
            selector, '(comment) => comment.hasAttribute("collapsed")'
        )

        children_attribute_exists = page.eval_on_selector(
            selector, '(comment) => comment.hasAttribute("has-children")'
        )

        if collapsed_attribute_exists:
            button_selector = f'{selector} details summary div button'
            page.wait_for_selector(button_selector)
            page.click(button_selector)
            print(f"Expanded the collapsed shreddit-comment with thingid t1_{comment.id}.")

        if children_attribute_exists:
            comment_fold_button_selector = f'#comment-fold-button'
            page.wait_for_selector(comment_fold_button_selector)
            page.click(comment_fold_button_selector)

        if entry_element.is_visible():
            entry_element.screenshot(path=output_image_path)

    def _capture_element_screenshot(self, page, comment, output_image_path):
        if self._is_new_layout(page):
            self._capture_screenshot_new_layout(page, comment, output_image_path)
        else:
            self._capture_screenshot_legacy_layout(page, comment, output_image_path)

    def _is_new_layout(self, page):
        page.wait_for_selector('html')
        return 'is-shredtop-pdp' in page.eval_on_selector('html', '(htmlElement) => htmlElement.className')

    def capture_element_screenshot(self, urls):
        with sync_playwright() as p:
            self.browser = p.chromium.launch(headless=False)
            context = self.browser.new_context()
            page = context.new_page()
            page.set_viewport_size(ViewportSize(width=1920, height=1080))

            page.goto("https://www.reddit.com/login")
            self._login(page)

            for i, comment in enumerate(urls, start=1):
                output_file_name = f"{comment.name}.png"
                output_image_path = os.path.join(COMMENT_CONFIG['output_directory'], output_file_name)

                if self._skip_comment_if_exists(comment, output_image_path):
                    continue

                comment_url = urljoin(base_url, comment.permalink)
                print(f"Screenshotting Comment {str(i)} : {comment_url}")
                page.goto(comment_url)

                self._capture_element_screenshot(page, comment, output_image_path)

                if i + 1 > COMMENT_CONFIG['comment_limit']:
                    print(f"Reached the maximum number of comments ({COMMENT_CONFIG['comment_limit']}). Stopping.")
                    break

            self.browser.close()


if __name__ == "__main__":
    reddit_comment_urls = [
        "https://www.reddit.com/r/QualityAssurance/comments/vy8596/comment/ig0qeih",
        "https://www.reddit.com/r/QualityAssurance/comments/vy8596/comment/ig14vcs",
        "https://www.reddit.com/r/QualityAssurance/comments/vy8596/comment/ig0uat3",
        "https://www.reddit.com/r/QualityAssurance/comments/vy8596/comment/ig3z55k"
        # Add more URLs as needed
    ]

    screenshot_capture = RedditScreenshotCapture()
    screenshot_capture.capture_element_screenshot(reddit_comment_urls)
    print("Screenshots saved.")