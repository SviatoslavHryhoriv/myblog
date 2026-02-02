#!/usr/bin/env python
import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from app_blog.models import Category, Article, ArticleImage
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO

# Clear existing data
Category.objects.all().delete()
Article.objects.all().delete()
ArticleImage.objects.all().delete()

# Create categories
categories_data = [
    {'name': 'Технологія', 'slug': 'technology'},
    {'name': 'Подорожі', 'slug': 'travel'},
    {'name': 'Їжа', 'slug': 'food'},
]

categories = {}
for cat_data in categories_data:
    cat = Category.objects.create(category=cat_data['name'], slug=cat_data['slug'])
    categories[cat_data['slug']] = cat
    print(f"✓ Created category: {cat.category}")

# Helper function to create test image
def create_test_image():
    img = Image.new('RGB', (400, 300), color='blue')
    img_io = BytesIO()
    img.save(img_io, format='JPEG')
    img_io.seek(0)
    return ContentFile(img_io.getvalue(), name='test_image.jpg')

# Create articles
articles_data = [
    {
        'title': 'Найновіші тренди в технології',
        'slug': 'latest-tech-trends',
        'category': 'technology',
        'description': 'Дізнайтесь про найновіші розробки у світі технологій.',
        'main_page': True,
        'pub_date': datetime.now() - timedelta(days=5),
    },
    {
        'title': 'Подорож до Палаєстини',
        'slug': 'palestine-journey',
        'category': 'travel',
        'description': 'Неймовірна подорож у святі місця.',
        'main_page': True,
        'pub_date': datetime.now() - timedelta(days=3),
    },
    {
        'title': 'Рецепт італійської пасти',
        'slug': 'italian-pasta-recipe',
        'category': 'food',
        'description': 'Як готувати автентичну італійську пасту.',
        'main_page': True,
        'pub_date': datetime.now() - timedelta(days=1),
    },
    {
        'title': 'Штучний інтелект у повсякденні',
        'slug': 'ai-everyday',
        'category': 'technology',
        'description': 'Як AI змінює наше життя.',
        'main_page': False,
        'pub_date': datetime.now() - timedelta(days=7),
    },
]

for article_data in articles_data:
    article = Article.objects.create(
        title=article_data['title'],
        slug=article_data['slug'],
        category=categories[article_data['category']],
        description=article_data['description'],
        main_page=article_data['main_page'],
        pub_date=article_data['pub_date'],
    )
    print(f"✓ Created article: {article.title}")
    
    # Add image to article
    article_image = ArticleImage.objects.create(
        article=article,
        image=create_test_image(),
    )
    print(f"  └─ Added image to article")

print("\n✓ Database populated successfully!")
