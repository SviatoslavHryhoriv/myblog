#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from app_blog.models import Category, Article, ArticleImage

print("🗑️  Видалення тестових записів...\n")

# Видаляємо деякі статті
articles_to_delete = Article.objects.filter(title__in=[
    "Квантові комп'ютери",
    "Новий театральний сезон"
])

deleted_articles = []
for article in articles_to_delete:
    deleted_articles.append(article.title)
    article.delete()

print(f"✓ Видалено статей: {len(deleted_articles)}")
for title in deleted_articles:
    print(f"  - {title}")

# Видаляємо одну категорію (яка пуста)
category_to_delete = Category.objects.filter(slug='sport').first()
if category_to_delete and category_to_delete.articles.count() == 0:
    print(f"✓ Видалено категорію: {category_to_delete.category}")
    category_to_delete.delete()
else:
    print(f"ℹ️  Категорія 'Спорт' не видалена, т.к. містить статті")

# Лічимо залишки
print(f"\n📊 Статус після видалення:")
print(f"   Категорій залишилось: {Category.objects.count()}")
print(f"   Статей залишилось: {Article.objects.count()}")
print(f"   Зображень залишилось: {ArticleImage.objects.count()}")

print(f"\n✅ Видалення завершено!")
