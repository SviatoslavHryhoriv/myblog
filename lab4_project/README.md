# Lab 4: Розробка серверної частини персонального блогу та модульне тестування

## Опис завдання
Розробка URL-маршрутів, views, шаблонів та юніт-тестів для персонального блогу. Реалізація читання та виведення даних з БД.

## Структура проекту

```
lab4_project/
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
    ├── models.py              # Моделі (скопійовані з Lab 3, +get_absolute_url)
    ├── admin.py               # Адміністрація (скопійована з Lab 3)
    ├── forms.py               # Форми (скопійовані з Lab 3)
    ├── views.py               # 4 класи-представлення (views)
    ├── urls.py                # URL-маршрути
    ├── tests_urls.py          # 8 юніт-тестів
    ├── templates/             # HTML-шаблони
    │   ├── index.html         # Головна сторінка
    │   ├── articles_list.html # Список всіх статей
    │   ├── article_detail.html # Деталі статті
    │   └── fotorama.html      # Галерея зображень
    ├── migrations/            # Міграції БД
    └── tests.py               # Placeholder
```

## Реалізовані компоненти Lab 4

### 1. Views (`app_blog/views.py`)

**HomePageView (ListView)**
- Відображає список категорій на головній сторінці
- Додатково вибирає 5 останніх статей для показу на головній
- Template: `index.html`
- Route: `/`

**ArticleList (ListView)**
- Відображає всі статті блогу
- Template: `articles_list.html`
- Route: `/articles/`

**ArticleCategoryList (ArticleList)**
- Фільтрує статті за категорією (за slug)
- Template: `articles_list.html`
- Route: `/articles/category/<slug>/`

**ArticleDetail (DateDetailView)**
- Відображає деталі однієї статті
- Використовує дату та slug для уникальної ідентифікації
- Додатково завантажує усі зображення для статті
- Template: `article_detail.html`
- Route: `/articles/<year>/<month>/<day>/<slug>/`

### 2. URL-маршрути (`app_blog/urls.py`)

```python
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('articles/', ArticleList.as_view(), name='articles-list'),
    path('articles/category/<slug:slug>/', ArticleCategoryList.as_view(), name='articles-category-list'),
    path('articles/<int:year>/<int:month>/<int:day>/<slug:slug>/', ArticleDetail.as_view(), name='news-detail'),
]
```

### 3. Шаблони (`app_blog/templates/`)

**index.html** — Головна сторінка
- Список категорій з посиланнями
- 5 найсвіжіших статей, позначених як main_page=True
- Посилання на всі публікації

**articles_list.html** — Список статей
- Таблиця статей з назвою, датою, описом та першим зображенням
- Фільтрація за категорією (якщо вказана)
- Посилання на деталі кожної статті

**article_detail.html** — Деталі статті
- Хлібні крихти (breadcrumb navigation)
- Заголовок, дата публікації
- Повний текст статті
- Галерея зображень (якщо вони є)

**fotorama.html** — Галерея зображень
- Карусель зображень з підписами
- Використовує бібліотеку Fotorama

### 4. Юніт-тести (`app_blog/tests_urls.py`)

**Тестові класи:**

**HomeTests** (2 тести)
1. `test_home_view_status_code` — перевіряє HTTP 200 для головної сторінки
2. `test_home_url_resolves_home_view` — перевіряє що URL `/` розв'язується до HomePageView

**ArticleURLsTests** (6 тестів)
1. `test_articles_list_status_code` — перевіряє HTTP 200 для списку статей
2. `test_category_list_requires_slug` — перевіряє фільтрацію за категорією
3. `test_article_detail_url` — перевіряє HTTP 200 для деталей статті
4. `test_article_list_resolves` — перевіряє URL-розв'язування для списку
5. `test_category_list_resolves` — перевіряє URL-розв'язування для категорії
6. `test_article_detail_resolves` — перевіряє URL-розв'язування для деталей

**Результати тестів:**
```
Found 8 test(s)
...
Ran 8 tests in 0.044s
OK ✓
```

## Запуск Lab 4

### 1. Активація середовища (якщо потрібно)
```bash
c:\work\myblog\myvenv\Scripts\Activate.ps1
```

### 2. Встановлення залежностей
```bash
cd lab4_project
pip install -r requirements.txt
```

### 3. Міграції
```bash
python manage.py migrate
```

### 4. Запуск тестів
```bash
python manage.py test app_blog.tests_urls --verbosity 2
```

### 5. Запуск сервера
```bash
python manage.py runserver 127.0.0.1:8002
```

### 6. Доступ до сторінок

| Сторінка | URL | Назва |
|----------|-----|-------|
| Головна | `http://127.0.0.1:8002/` | home |
| Всі статті | `http://127.0.0.1:8002/articles/` | articles-list |
| Категорія | `http://127.0.0.1:8002/articles/category/teknologiyi/` | articles-category-list |
| Деталі статті | `http://127.0.0.1:8002/articles/2024/12/15/nova-stattya/` | news-detail |
| Адміністрація | `http://127.0.0.1:8002/admin/` | - |

## Попередня умова для тестування

Для того щоб тести працювали з реальними даними, необхідно створити тестові дані через адміністрацію:

1. Створити категорію з slug='testcat'
2. Створити статтю з категорією та slug='test-article'
3. (Опціонально) Завантажити зображення до статті

Тести автоматично створюють тестові дані через setUp() методи.

## Налаштування (`mysite/settings.py`)

```python
INSTALLED_APPS = [
    ...
    'app_blog',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,  # Шаблони шукаються в app_blog/templates/
        ...
    },
]

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

## База даних
- Вид: SQLite (`lab4_db.sqlite3`)
- Таблиці: app_blog_category, app_blog_article, app_blog_articleimage

## Статус Lab 4
✅ **Завершено на 100%**
- ✅ 4 Views реалізовані (HomePageView, ArticleList, ArticleCategoryList, ArticleDetail)
- ✅ 4 URL-маршрути налаштовані
- ✅ 4 HTML-шаблони створені
- ✅ 8 юніт-тестів написані та пройдені
- ✅ Всі тести проходять (OK)
- ✅ DateDetailView правильно обробляє дату та slug
- ✅ Шаблони правильно відображають дані з БД

## Результати тестування

```
python manage.py test app_blog.tests_urls --verbosity 2

Found 8 test(s).
Creating test database for alias 'default'...
Operations to perform:
  Synchronize unmigrated apps: app_blog, messages, staticfiles
  Apply all migrations: admin, auth, contenttypes, sessions
...
test_article_detail_resolves ... ok
test_article_detail_url ... ok
test_article_list_resolves ... ok
test_articles_list_status_code ... ok
test_category_list_requires_slug ... ok
test_category_list_resolves ... ok
test_home_url_resolves_home_view ... ok
test_home_view_status_code ... ok

Ran 8 tests in 0.044s

OK ✓
```

## Коміти (GitHub)
- Initial Lab 3: https://github.com/SviatoslavHryhoriv/myblog
- Lab 4 Complete: https://github.com/SviatoslavHryhoriv/myblog (branch main)

---

**Версія Django:** 6.0.1  
**Версія Python:** 3.13+  
**Версія Pillow:** 12.1.0  
**Дата завершення:** 02.02.2026
