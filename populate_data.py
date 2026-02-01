#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт для додавання тестових даних в базу даних
"""

import os
import sys
import django
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.core.files.base import ContentFile
from app_blog.models import Category, Article, ArticleImage
from datetime import datetime, timedelta


def create_test_image(text, width=800, height=600, filename=None):
    """Створює тестове зображення з текстом"""
    # Створюємо зображення
    img = Image.new('RGB', (width, height), color=(73, 109, 137))
    draw = ImageDraw.Draw(img)
    
    # Намагаємося использовувати вбудований шрифт
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    # Малюємо текст в центр
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    draw.text((x, y), text, fill=(255, 255, 255), font=font)
    
    # Зберігаємо в BytesIO
    img_io = BytesIO()
    img.save(img_io, format='JPEG')
    img_io.seek(0)
    
    return img_io


def populate_database():
    """Додає тестові дані в базу"""
    
    print("🔄 Починаємо додавання тестових даних...")
    
    # Очищаємо старі дані
    Article.objects.all().delete()
    ArticleImage.objects.all().delete()
    Category.objects.all().delete()
    print("✓ Старі дані видалені")
    
    # Создаємо категорії
    categories_data = [
        {'name': 'Технологія', 'slug': 'tehnologiya'},
        {'name': 'Спорт', 'slug': 'sport'},
        {'name': 'Культура', 'slug': 'kultura'},
    ]
    
    categories = {}
    for cat_data in categories_data:
        cat = Category.objects.create(
            category=cat_data['name'],
            slug=cat_data['slug']
        )
        categories[cat_data['name']] = cat
        print(f"✓ Категорія створена: {cat_data['name']}")
    
    # Статті з даними
    articles_data = [
        {
            'title': 'Штучний інтелект змінює світ',
            'description': 'ШІ технології швидко розвиваються і знаходять застосування в різних галузях.',
            'category': 'Технологія',
            'main_page': True,
            'images_count': 2,
        },
        {
            'title': 'Квантові комп\'ютери: майбутнє обчислень',
            'description': 'Дізнайтесь про революційні квантові обчислення.',
            'category': 'Технологія',
            'main_page': True,
            'images_count': 1,
        },
        {
            'title': 'Чемпіонат світу з футзалу 2026',
            'description': 'Найкращі команди світу змагаються за титул чемпіона.',
            'category': 'Спорт',
            'main_page': False,
            'images_count': 3,
        },
        {
            'title': 'Олімпійські ігри: історія та традиції',
            'description': 'Розповідь про найбільший спортивний форум світу.',
            'category': 'Спорт',
            'main_page': True,
            'images_count': 2,
        },
        {
            'title': 'Новий театральний сезон',
            'description': 'Премієри найкращих театральних постановок.',
            'category': 'Культура',
            'main_page': False,
            'images_count': 0,
        },
        {
            'title': 'Музика електронної сцени',
            'description': 'Найпопулярніші виконавці електронної музики.',
            'category': 'Культура',
            'main_page': True,
            'images_count': 2,
        },
    ]
    
    # Додаємо статті з різними датами
    base_date = datetime.now()
    for i, article_data in enumerate(articles_data):
        pub_date = base_date - timedelta(days=i)
        
        article = Article.objects.create(
            title=article_data['title'],
            description=article_data['description'],
            pub_date=pub_date,
            slug=article_data['title'].lower().replace(' ', '-').replace('\'', ''),
            main_page=article_data['main_page'],
            category=categories[article_data['category']]
        )
        print(f"✓ Стаття створена: {article_data['title']}")
        
        # Додаємо зображення до статті
        for j in range(article_data['images_count']):
            img_text = f"{article_data['title']} - Фото {j+1}"
            img_io = create_test_image(img_text)
            
            img_file = ContentFile(img_io.getvalue(), name=f'photo_{i}_{j}.jpg')
            
            article_image = ArticleImage.objects.create(
                article=article,
                image=img_file,
                title=f"Зображення до: {article_data['title']} ({j+1})"
            )
            print(f"  ✓ Зображення додано: {article_image.title}")
    
    print("\n✅ Тестові дані успішно додані!")
    print(f"   - Категорій: {Category.objects.count()}")
    print(f"   - Статей: {Article.objects.count()}")
    print(f"   - Зображень: {ArticleImage.objects.count()}")


if __name__ == '__main__':
    populate_database()
