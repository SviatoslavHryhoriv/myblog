# Lab 3: Django ORM та Адміністрація

## Опис завдання
Розробка моделей для персонального блогу з використанням Django ORM, реєстрація моделей у адміністрації та налаштування медіа-файлів.

## Структура проекту

```
lab3_project/
├── manage.py
├── requirements.txt
├── mysite/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── app_blog/
    ├── __init__.py
    ├── models.py          # Моделі: Category, Article, ArticleImage
    ├── admin.py           # Реєстрація в адміністрації
    ├── forms.py           # Form для завантаження зображень
    ├── views.py           # Placeholder (не реалізовано)
    ├── urls.py            # Порожні URL-маршрути
    ├── migrations/        # Міграції БД
    └── tests.py           # Placeholder для тестів
```

## Реалізовані компоненти Lab 3

### 1. Моделі (`app_blog/models.py`)

**Category** — категорія для публікацій:
```python
- category: CharField (max 250 символів, унікальний)
- slug: SlugField (унікальний для організації URL)
```

**Article** — стаття блогу:
```python
- title: CharField (max 250 символів)
- description: TextField (довгий текст, опціонально)
- pub_date: DateTimeField (дата публікації, за замовчуванням - теперішній час)
- slug: SlugField (унікальний для дати публікації)
- main_page: BooleanField (показувати на головній сторінці)
- category: ForeignKey (посилання на категорію)
- get_absolute_url(): генерує URL для статті
```

**ArticleImage** — зображення для статті:
```python
- article: ForeignKey (посилання на статтю)
- image: ImageField (фото, завантажується в папку 'photos')
- title: CharField (опис зображення)
```

### 2. Адміністрація (`app_blog/admin.py`)

- **CategoryAdmin**: список категорій з автоматичним заповненням slug з назви категорії
- **ArticleAdmin**: список статей з вбудованим редактором зображень (ArticleImageInline)
- **ArticleImageInline**: табличне редагування зображень всередині редактора статей

### 3. Форми (`app_blog/forms.py`)

- **ArticleImageForm**: ModelForm для завантаження зображень до статей

### 4. Налаштування (`mysite/settings.py`)

```python
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
```

## Запуск Lab 3

### 1. Активація середовища (якщо потрібно)
```bash
# На Windows з venv
c:\work\myblog\myvenv\Scripts\Activate.ps1
```

### 2. Встановлення залежностей
```bash
cd lab3_project
pip install -r requirements.txt
```

### 3. Міграції
```bash
python manage.py migrate
```

### 4. Запуск сервера
```bash
python manage.py runserver 127.0.0.1:8001
```

### 5. Доступ до адміністрації
- URL: `http://127.0.0.1:8001/admin/`
- Користувач за замовчуванням: `admin`
- Пароль: створити через `python manage.py createsuperuser`

## База даних
- Вид: SQLite (`lab3_db.sqlite3`)
- Таблиці: app_blog_category, app_blog_article, app_blog_articleimage

## Статус Lab 3
✅ **Завершено**
- ✅ Моделі розроблені
- ✅ Адміністрація налаштована
- ✅ Міграції застосовані
- ✅ Медіа-файли налаштовані

## Коміти (GitHub)
- Lab 3 implementation: https://github.com/SviatoslavHryhoriv/myblog/commit/[commit-hash]
- Lab 4 completion: https://github.com/SviatoslavHryhoriv/myblog

---

**Версія Django:** 6.0.1  
**Версія Python:** 3.13+  
**Дата завершення:** 02.02.2026
