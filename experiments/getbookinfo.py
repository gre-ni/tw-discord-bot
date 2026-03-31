from playwright.sync_api import Page, expect, sync_playwright
import re

book_name = input("Book: ").title()
book_author = input("Author: ").title()

def main():
    # p is Playwright controller object, in testing initialisation + cleanup is handled by pytest
    with sync_playwright() as p:
        # Launching browser
        browser = p.chromium.launch(headless=False, slow_mo=500) # Options: chromium, firefox, webkit
        page = browser.new_page() # Like opening a new tab

        page.goto("https://app.thestorygraph.com/browse", wait_until="domcontentloaded")
        search_box = page.get_by_role("combobox", name="Search")
        search_box.click()
        search_box.fill(book_name)
        search_box.press("Enter")


        page.wait_for_load_state("networkidle")
        page.wait_for_selector(f".book-title-author-and-series:has-text('{book_name}')")
        # result = page.locator(".book-title-author-and-series").filter(has_text=re.compile(book_name, re.IGNORECASE)).filter(has_text=re.compile(book_author, re.IGNORECASE)).first
        # result = page.locator(".book-title-author-and-series").filter(
        #     has=page.locator("span a", has_text=re.compile(f"^{re.escape(book_name)}$", re.IGNORECASE))
        #     ).filter(
        #     has=page.locator("p a", has_text=re.compile(book_author, re.IGNORECASE))
        #     ).first
        
        title_matches = page.get_by_role("link", name=book_name, exact=True)
        
        if title_matches.count() == 0:
            raise ValueError("No book with this title found")
        elif title_matches.count() == 1:
            title_matches.click()
        else:
            print("I just clicked the first match, but there are more!")
            print(title_matches)
            author_matches = page.get_by_role("heading", name=f"{book_name} {book_author}", exact=True)        
            if author_matches.count() > 1:
                raise ValueError("hoenstly idk")
            elif author_matches.count() == 0:
                raise ValueError("No book of this name for this author")
            else:
                author_matches.click()
            
            
        page.wait_for_load_state("networkidle")

        # Contents are collapsed by default
        # page.wait_for_selector("turbo-frame#content_warnings_section[complete]", state="attached")  # frame loaded
        page.locator("turbo-frame#content_warnings_section .toggle-content-warnings-information-book").first.click()
        page.wait_for_selector(".content-warnings-information")

        warnings_text = page.locator("turbo-frame#content_warnings_section .content-warnings-information").first.inner_text()

        # Closing browser
        browser.close()

    print(warnings_text)

if __name__ == "__main__":
    main()