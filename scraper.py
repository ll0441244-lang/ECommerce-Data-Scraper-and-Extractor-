import requests
from bs4 import BeautifulSoup
import pandas as pd  # مكتبة أساسية لكل محللي البيانات

def scrape_books():
    url = "https://books.toscrape.com/"
    headers = {"User-Agent": "Mozilla/5.0"} # لحماية الكود من الحظر
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() # التأكد من أن الموقع يعمل (Status 200)
    except requests.exceptions.RequestException as e:
        print(f"خطأ في الاتصال بالموقع: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all('article', class_='product_pod')
    
    # قائمة لتخزين البيانات بدلاً من طباعتها فقط
    books_data = []

    for article in articles:
        title = article.h3.a['title']
        price = article.find('p', class_='price_color').text.strip()
        availability = article.find('p', class_='instock availability').text.strip()
        
        # حفظ البيانات في قاموس (Dictionary)
        books_data.append({
            "اسم الكتاب": title,
            "السعر": price,
            "حالة التوفر": availability
        })
    
    # تحويل البيانات إلى DataFrame (جدول بنظام بايثون)
    df = pd.DataFrame(books_data)
    
    # حفظ الجدول فوراً إلى ملف Excel وملف CSV
    df.to_csv("books_extracted.csv", index=False, encoding="utf-8-sig")
    df.to_excel("books_extracted.xlsx", index=False)
    
    print("✅ تم سحب البيانات بنجاح وحفظها في ملفات Excel و CSV!")

# تشغيل الدالة
if __name__ == "__main__":
    scrape_books()
