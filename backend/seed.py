"""Seed script — populates the database with Persian bookstore data."""
import hashlib
from datetime import datetime, timedelta
from app.database import SessionLocal, engine, Base
from app.models import Admin, Customer, Category, Product, Order, OrderItem

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Clear existing data to reseed with Persian bookstore data
db.query(OrderItem).delete()
db.query(Order).delete()
db.query(Product).delete()
db.query(Category).delete()
db.query(Customer).delete()
db.query(Admin).delete()
db.commit()

# --- Admin ---
admin = Admin(
    username="admin",
    password_hash=hashlib.sha256("admin123".encode()).hexdigest(),
    created_at=datetime.utcnow(),
)
db.add(admin)
db.flush()

# --- Customers (Persian translated) ---
customers_data = [
    ("آلیس جانسون", "alice@example.com", "۰۹۱۲-۵۵۵۰۱۰۱"),
    ("باب اسمیت", "bob@example.com", "۰۹۱۲-۵۵۵۰۱۰۲"),
    ("کارول وایت", "carol@example.com", "۰۹۱۲-۵۵۵۰۱۰۳"),
    ("دن براون", "dan@example.com", "۰۹۱۲-۵۵۵۰۱۰۴"),
    ("ایو دیویس", "eve@example.com", "۰۹۱۲-۵۵۵۰۱۰۵"),
]
customers = []
for name, email, phone in customers_data:
    c = Customer(name=name, email=email, phone=phone, created_at=datetime.utcnow())
    db.add(c)
    customers.append(c)
db.flush()

# --- Categories (Bookstore only) ---
categories_data = [
    ("رمان و ادبیات داستانی", "شاهکارهای ادبیات داستانی، رمان‌های کلاسیک و معاصر ایران و جهان"),
    ("علوم کامپیوتر و برنامه‌نویسی", "کتاب‌های تخصصی مهندسی نرم‌افزار، هوش مصنوعی، داده و وب"),
    ("تاریخ و فلسفه", "پژوهش‌های تاریخی، اندیشه‌های کهن و فلسفه تحلیلی و اگزیستانسیالیسم"),
    ("روانشناسی و خودسازی", "کتاب‌های موفقیت فردی، تفکر مثبت، بهبود فردی و مدیریت ذهن"),
    ("شعر و ادب کهن", "دیوان اشعار شعرای بزرگ پارسی، مثنوی، گلستان و شاهنامه"),
]
categories = []
for name, desc in categories_data:
    cat = Category(name=name, description=desc)
    db.add(cat)
    categories.append(cat)
db.flush()

# --- Products (Persian & English books only, prices in Tomans) ---
products_data = [
    ("The Great Gatsby", "Classic novel by F. Scott Fitzgerald - رمان جاودانه آمریکایی", 130000, 200, categories[0].id),
    ("Python for Data Science", "راهنمای جامع علم داده و یادگیری ماشین با پایتون", 390000, 100, categories[1].id),
    ("شازده کوچولو", "اثر جاودانه آنتوان دو سنت اگزوپری با ترجمه احمد شاملو", 95000, 76, categories[0].id),
    ("صد سال تنهایی", "شاهکار رئالیسم جادویی گابریل گارسیا مارکز", 220000, 30, categories[0].id),
    ("1984 - George Orwell", "رمان پادآرمان‌شهری کلاسیک درباره نظارت و آزادی اندیشه", 185000, 15, categories[0].id),
    ("Clean Code - Robert C. Martin", "راهنمای جامع مهندسی نرم‌افزار چابک و کدهای تمیز", 420000, 60, categories[1].id),
    ("بوف کور", "معروف‌ترین رمان معاصر ایرانی اثر ماندگار صادق هدایت", 110000, 150, categories[0].id),
    ("جنایت و مکافات", "رمان روانشناختی و فلسفی فئودور داستایفسکی درباره وجدان و عدالت", 290000, 25, categories[0].id),
    ("انسان خردمند (Sapiens)", "تاریخ مختصر بشر از آغاز تا امروز اثر یووال نوح هراری", 270000, 40, categories[2].id),
    ("چنین گفت زرتشت", "کتابی برای همه و هیچ‌کس اثر فیلسوف برجسته فریدریش نیچه", 240000, 80, categories[2].id),
    ("Designing Data-Intensive Applications", "اصول بنیادی سیستم‌های داده‌ای مطمئن، مقیاس‌پذیر و پایدار", 450000, 120, categories[1].id),
    ("چشم‌هایش", "شاهکار ادبی بزرگ علوی درباره عشق، راز و مبارزه", 140000, 45, categories[0].id),
    ("عادت‌های اتمی (Atomic Habits)", "راهکاری ساده و کاربردی برای ایجاد عادت‌های کوچک و نتایج چشمگیر", 195000, 90, categories[3].id),
    ("هنر شفاف اندیشیدن", "شناخت ۹۹ خطای شناختی ذهن انسان اثر رولف دوبلی", 175000, 70, categories[3].id),
    ("سووشون", "نخستین رمان برجسته نویسنده توانای ایرانی سیمین دانشور", 165000, 110, categories[0].id),
    ("Introduction to Algorithms (CLRS)", "کتاب جامع طراحی و تحلیل الگوریتم‌های محاسباتی", 490000, 35, categories[1].id),
    ("قلعه حیوانات (Animal Farm)", "رمان تمثیلی سیاسی و انتقادی جورج اورول", 120000, 65, categories[0].id),
    ("کیمیاگر (The Alchemist)", "داستان دل‌انگیز و عرفانی سفر سانتیاگو اثر پائولو کوئلیو", 145000, 85, categories[3].id),
    ("دیوان حافظ شیرازی", "مجموعه نفیس غزلیات خواجه شمس‌الدین محمد حافظ با شرح ابیات", 260000, 55, categories[4].id),
    ("شاهنامه فردوسی", "حماسه بزرگ ملی ایرانیان سروده حکیم ابوالقاسم فردوسی طوسی", 480000, 40, categories[4].id),
    ("To Kill a Mockingbird", "شاهکار هارپر لی برنده جایزه پولیتزر در دفاع از انسانیت", 170000, 20, categories[0].id),
]

products = []
for name, desc, price, stock, cat_id in products_data:
    p = Product(
        name=name,
        description=desc,
        price=price,
        stock=stock,
        category_id=cat_id,
        created_at=datetime.utcnow(),
    )
    db.add(p)
    products.append(p)
db.flush()

# --- Orders (9 orders matching screenshot exactly) ---
# Image table for orders:
# #9: Alice Johnson, date: 1404/05/16, items: 1, status: "لغو شده"
# #8: Carol White, date: 1404/05/16, items: 2, status: "تکمیل شده"
# #7: Bob Smith, date: 1404/05/16, items: 3, status: "تکمیل شده"
# #6: Eve Davis, date: 1404/05/16, items: 2, status: "تکمیل شده"
# #5: Dan Brown, date: 1404/05/16, items: 3, status: "تکمیل شده"
# #4: Carol White, date: 1404/05/16, items: 2, status: "تکمیل شده"
# #3: Alice Johnson, date: 1404/05/16, items: 3, status: "تکمیل شده"
# #2: Bob Smith, date: 1404/05/16, items: 2, status: "تکمیل شده"
# #1: Alice Johnson, date: 1404/05/16, items: 2, status: "تکمیل شده"

orders_plan = [
    # (customer, [(product, qty), ...], status, days_ago)
    (customers[0], [(products[2], 2), (products[1], 1)], "completed", 8), # #1
    (customers[1], [(products[4], 1), (products[7], 1)], "completed", 7), # #2
    (customers[0], [(products[0], 1), (products[10], 2), (products[15], 1)], "completed", 6), # #3
    (customers[2], [(products[3], 3), (products[17], 1)], "completed", 5), # #4
    (customers[3], [(products[6], 2), (products[8], 1), (products[13], 1)], "completed", 4), # #5
    (customers[4], [(products[5], 1), (products[9], 1)], "completed", 3), # #6
    (customers[1], [(products[11], 1), (products[18], 2), (products[20], 1)], "completed", 2), # #7
    (customers[2], [(products[14], 2), (products[16], 1)], "completed", 1), # #8
    (customers[0], [(products[3], 1)], "cancelled", 0), # #9
]

for customer, line_items, status, days_ago in orders_plan:
    total = sum(qty * p.price for p, qty in line_items)
    order = Order(
        customer_id=customer.id,
        order_date=datetime.utcnow() - timedelta(days=days_ago),
        total_amount=round(total, 2),
        status=status,
    )
    db.add(order)
    db.flush()

    for product, qty in line_items:
        oi = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=qty,
            unit_price=product.price,
        )
        db.add(oi)

db.commit()
db.close()
print("Bookstore database seeded successfully with Persian and English books!")
