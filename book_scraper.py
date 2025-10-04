import requests
from bs4 import BeautifulSoup
import cv2
import os
import re

BASE_URL = "https://books.toscrape.com"
book_number = 0

def scrape_book(title, save_as=None):
    """
    Scrape cover + title. If save_as is falsy, auto-generate book{n}.png.
    Handles invalid filenames by sanitizing and ensures .png extension.
    """
    global book_number
    page = requests.get(BASE_URL)
    soup = BeautifulSoup(page.content, "html.parser")

    book_a_tag = soup.find("a", {"title": title})
    if not book_a_tag:
        print(f"❌ Book '{title}' not found on page!")
        return None

    img_tag = book_a_tag.find_previous("img")
    img_src = BASE_URL + "/" + img_tag["src"].replace("../", "")

    # auto-generate filename if none provided
    if not save_as:
        save_as = f"book{book_number}.png"
        book_number += 1

    # ✅ sanitize filename (remove invalid chars)
    safe_name = re.sub(r'[<>:"/\\|?*]', "_", save_as).strip()

    # if empty, fallback to auto
    if safe_name == "":
        safe_name = f"book{book_number}.png"
        book_number += 1

    # ✅ ensure it ends with .png
    if not safe_name.lower().endswith(".png"):
        safe_name += ".png"

    os.makedirs("book_images", exist_ok=True)
    filepath = os.path.join("book_images", safe_name)

    # Save image
    with open(filepath, "wb") as f:
        f.write(requests.get(img_src).content)

    print("Image saved succesfully in folder book_images!!!😁💪❤️‍🔥🎨😀📁📂")


    # Show image
    img = cv2.imread(filepath)
    if img is not None:
        resized = cv2.resize(img, (400, 600))
        cv2.imshow(title, resized)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return {"title": title, "image_url": img_src, "saved_path": filepath}

# 🎯 Example usage
# book1 = scrape_book("A Light in the Attic", "attic.png")
# book2 = scrape_book("Tipping the Velvet", "velvet.png")
# book3 = scrape_book("Scott Pilgrim's Precious Little Life (Scott Pilgrim #1)")

# custom_book = scrape_book(input("Enter book title: "))
# custom_book2 = scrape_book(input("Enter book title: "))

# print(book1)
# print(book2)
# print(book3)
# print(custom_book)
# print(custom_book2)
def get_all_book_titles():
    """
    Scrape all book titles from the homepage of Books to Scrape.
    
    Returns:
        list: A list of book titles (strings).
    """
    # 1️⃣ Fetch the page
    page = requests.get(BASE_URL)
    soup = BeautifulSoup(page.content, "html.parser")

    # 2️⃣ Find all <h3> tags (each contains an <a> with the book title)
    h3_tags = soup.find_all("h3")

    # 3️⃣ Extract the "title" attribute from each <a> inside <h3>
    titles = [h3.a["title"] for h3 in h3_tags]

    return titles


# 🎯 Example usage
books = get_all_book_titles()


while True:
    print(f"All available book titles:")
    print(books)
    book_title = input("Enter book title or 'Q' to quit: ")
    if book_title == 'Q' or book_title == 'q':
        break
    filename = input("Enter file save name for book image or 'Q' to quit: ")
    if filename == 'Q' or filename == 'q':
        break

    book = scrape_book(book_title,filename)
    print(book)
