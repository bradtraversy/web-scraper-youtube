import requests
from bs4 import BeautifulSoup
import json

def fetch_books(page_number):
  url = f"https://books.toscrape.com/catalogue/page-{page_number}.html"
  response = requests.get(url)
  soup = BeautifulSoup(response.text, 'html.parser')

  books = []
  book_elements = soup.find_all('article', class_='product_pod')

  for book in book_elements:
    title = book.find('h3').find('a')['title']
    price = book.find('p', class_='price_color').text
    stock = 'In stock' if 'In stock' in book.find('p', class_='instock availability').text else 'Out of stock'
    rating = book.find('p', class_='star-rating')['class'][1]
    link = book.find('h3').find('a')['href']

    books.append({
      'title': title,
      'price': price,
      'stock': stock,
      'rating': rating,
      'link': f"https://books.toscrape.com/catalogue/{link}"
    })

  return books

def main():
  all_books = []
  max_pages = 10

  for current_page in range(1, max_pages + 1):
    books_on_page = fetch_books(current_page)
    all_books.extend(books_on_page)
    print(f"Books on page {current_page}: {books_on_page}")

  # Save data to file
  with open('books.json', 'w') as f:
    json.dump(all_books, f, indent=2)

  print('Data is saved to books.json')

if __name__ == "__main__":
  main()