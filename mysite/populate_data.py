#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.core.files.base import ContentFile
from app_blog.models import Category, Article, ArticleImage
from datetime import datetime, timedelta
from PIL import Image, ImageDraw
from io import BytesIO

def create_test_image(text):
    """Створює тестове зображення"""
    img = Image.new("RGB", (800, 600), color=(73, 109, 137))
    draw = ImageDraw.Draw(img)
    x, y = 350, 250
    draw.text((x, y), text, fill=(255, 255, 255))
    img_io = BytesIO()
    img.save(img_io, format="JPEG")
    img_io.seek(0)
    return img_io

print("🔄 Додавання тестових даних...")

# Clear old data
Article.objects.all().delete()
ArticleImage.objects.all().delete()
Category.objects.all().delete()
print("✓ Старі дані видалені")

# Create categories
cats = {}
for name, slug in [("Технологія", "tehnologiya"), ("Спорт", "sport"), ("Культура", "kultura")]:
    cat = Category.objects.create(category=name, slug=slug)
    cats[name] = cat
    print(f"✓ Категорія: {name}")

# Create articles
articles_data = [
    ("Штучний інтелект змінює світ", "ШІ технології швидко розвиваються та знаходять застосування в різних галузях", "Технологія", True, 2),
    ("Квантові комп'ютери", "Революційні квантові обчислення змінять світ інформаційних технологій", "Технологія", True, 1),
    ("Чемпіонат світу з футзалу", "Найкращі команди світу змагаються за титул чемпіона", "Спорт", False, 3),
    ("Олімпійські ігри", "Найбільший спортивний форум світу з багатовіковою історією", "Спорт", True, 2),
    ("Новий театральний сезон", "Премієри найкращих театральних постановок цього сезону", "Культура", False, 0),
    ("Музика електронної сцени", "Найпопулярніші виконавці електронної музики виступлять на сцені", "Культура", True, 2),
]

base_date = datetime.now()
for i, (title, desc, cat_name, main, img_count) in enumerate(articles_data):
    pub_date = base_date - timedelta(days=i)
    article = Article.objects.create(
        title=title,
        description=desc,
        pub_date=pub_date,
        slug=title.lower().replace(" ", "-").replace("'", ""),
        main_page=main,
        category=cats[cat_name]
    )
    print(f"✓ Стаття: {title}")
    for j in range(img_count):
        img_io = create_test_image(f"{title} - Фото {j+1}")
        ArticleImage.objects.create(
            article=article,
            image=ContentFile(img_io.getvalue(), name=f"photo_{i}_{j}.jpg"),
            title=f"Зображення до {title} ({j+1})"
        )
        print(f"  ✓ Зображення {j+1}")

print(f"\n✅ Дані успішно додані!")
print(f"   Категорій: {Category.objects.count()}")
print(f"   Статей: {Article.objects.count()}")
print(f"   Зображень: {ArticleImage.objects.count()}")
