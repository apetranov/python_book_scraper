import requests
from bs4 import BeautifulSoup
import cv2
import os
import re

BASE_URL = "https://books.toscrape.com"
book_number = 0
def scrape_book(title, save_as=None):
    """
    Scrape cover + title + price + rating + availability.
    If save_as is falsy, auto-generate book{n}.png.
    Handles invalid filenames by sanitizing and ensures .png extension.
    """
    global book_number
    page = requests.get(BASE_URL)
    soup = BeautifulSoup(page.content, "html.parser")

    # Find the book <a> tag by title
    book_a_tag = soup.find("a", {"title": title})
    if not book_a_tag:
        print(f"❌ Book '{title}' not found on page!")
        return None

    # Get <img> src for the cover
    img_tag = book_a_tag.find_previous("img")
    img_src = BASE_URL + "/" + img_tag["src"].replace("../", "")

    # Find the parent <article> to extract rating, price, availability
    article = book_a_tag.find_parent("article")

    # ⭐ Extract rating (class "star-rating <rating>")
    # rating_class = article.find("p", class_="star-rating")["class"]
    # rating = [r for r in rating_class if r != "star-rating"][0]  # get actual rating text
    # ⭐ Extract rating text and convert to stars
    rating_text = [c for c in article.find("p", class_="star-rating")["class"] if c != "star-rating"][0]
    rating_map = {"One": "★☆☆☆☆", "Two": "★★☆☆☆", "Three": "★★★☆☆",
                  "Four": "★★★★☆", "Five": "★★★★★"}
    rating = rating_map.get(rating_text, "☆☆☆☆☆")

    # 💰 Extract price
    price = article.find("p", class_="price_color").text.strip()

    # 📦 Extract availability (in stock or not)
    availability_text = article.find("p", class_="instock availability").text.strip()
    in_stock = "Yes" if "In stock" in availability_text else "No"

    # Auto-generate filename if needed
    if not save_as:
        save_as = f"book{book_number}.png"
        book_number += 1

    # Sanitize filename
    safe_name = re.sub(r'[<>:"/\\|?*]', "_", save_as).strip()
    if safe_name == "":
        safe_name = f"book{book_number}.png"
        book_number += 1
    if not safe_name.lower().endswith(".png"):
        safe_name += ".png"

    os.makedirs("book_images", exist_ok=True)
    filepath = os.path.join("book_images", safe_name)

    #  return {
    #     "title": title,
    #     "image_url": img_src,
    #     "saved_path": filepath,
    #     "price": price,
    #     "rating": rating,
    #     "in_stock": in_stock
    # }

    print(f"title: {title}")
    print(f"image link: {img_src}")
    print(f"saved path: {filepath}")
    print(f"price: {price}")
    print(f"rating: {rating}")
    print(f"in_stock: {in_stock}")

    # Save image
    with open(filepath, "wb") as f:
        f.write(requests.get(img_src).content)

    print("Image saved successfully in folder book_images!!!😁💪❤️‍🔥🎨😀📁📂")
    print("Close the popped up image file to continue... <333")

    # Display image
    img = cv2.imread(filepath)
    if img is not None:
        resized = cv2.resize(img, (400, 600))
        cv2.imshow(title, resized)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # ✅ Return all info
    return {
        "title": title,
        "image_url": img_src,
        "saved_path": filepath,
        "price": price,
        "rating": rating,
        "in_stock": in_stock
    }

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
