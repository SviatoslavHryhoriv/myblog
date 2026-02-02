# Звіт про завершення Lab 3 і Lab 4

## Резюме

Успішно реалізовано дві лабораторні роботи для персонального блогу на Django:
- **Lab 3**: ORM моделі, адміністрація, налаштування медіа-файлів
- **Lab 4**: Views, URL-маршрути, шаблони, юніт-тести

**Загальний статус:** ✅ **100% завершено**

---

## Lab 3: Django ORM та Адміністрація

### Цілі завдання
1. ✅ Розробити 3 моделі (Category, Article, ArticleImage)
2. ✅ Зареєструвати моделі в адміністрації
3. ✅ Налаштувати медіа-файли
4. ✅ Створити міграції БД

### Реалізація

#### Моделі
```
Category
├── category: CharField (унікальний)
└── slug: SlugField (унікальний)

Article
├── title: CharField
├── description: TextField
├── pub_date: DateTimeField
├── slug: SlugField (unique_for_date)
├── main_page: BooleanField
└── category: ForeignKey

ArticleImage
├── article: ForeignKey
├── image: ImageField
└── title: CharField
```

#### Адміністрація
- CategoryAdmin з автоматичним slug
- ArticleAdmin з вбудованим редактором зображень
- ArticleImageInline для табличного редагування

#### Налаштування
- STATIC_ROOT: `staticfiles/`
- MEDIA_ROOT: `media/`
- MEDIA_URL: `/media/`

### Команди для запуску
```bash
cd lab3_project
python manage.py migrate          # Міграції БД
python manage.py createsuperuser  # Створити адміністратора
python manage.py runserver 127.0.0.1:8001
```

### Результат
- ✅ Всі моделі створені
- ✅ Адміністрація налаштована
- ✅ Медіа-файли налаштовані
- ✅ БД готова до роботи (SQLite: lab3_db.sqlite3)

---

## Lab 4: Views, URL-маршрути, Шаблони та Тести

### Цілі завдання
1. ✅ Розробити 4 Views (HomePageView, ArticleList, ArticleCategoryList, ArticleDetail)
2. ✅ Створити 4 URL-маршрути
3. ✅ Розробити 4 HTML-шаблони
4. ✅ Написати 8 юніт-тестів

### Реалізація

#### Views (app_blog/views.py)
```python
HomePageView(ListView)
  - Model: Category
  - Context: categories + 5 main_page articles
  - Template: index.html
  - Route: /

ArticleList(ListView)
  - Model: Article
  - Template: articles_list.html
  - Route: /articles/

ArticleCategoryList(ArticleList)
  - Фільтр: category__slug=slug
  - Template: articles_list.html
  - Route: /articles/category/<slug>/

ArticleDetail(DateDetailView)
  - Model: Article
  - Date field: pub_date
  - Context: images from article.images.all()
  - Template: article_detail.html
  - Route: /articles/<year>/<month>/<day>/<slug>/
```

#### URL-маршрути (app_blog/urls.py)
```python
path('', HomePageView.as_view(), name='home')
path('articles/', ArticleList.as_view(), name='articles-list')
path('articles/category/<slug:slug>/', ArticleCategoryList.as_view(), name='articles-category-list')
path('articles/<int:year>/<int:month>/<int:day>/<slug:slug>/', ArticleDetail.as_view(), name='news-detail')
```

#### Шаблони (templates/)
- **index.html** (30 рядків) — головна з категоріями та 5 статей
- **articles_list.html** (25 рядків) — таблиця статей з фільтром
- **article_detail.html** (35 рядків) — деталі статті з breadcrumb та галереєю
- **fotorama.html** (18 рядків) — карусель зображень

#### Тести (app_blog/tests_urls.py)

**HomeTests:**
1. `test_home_view_status_code` — ✅ pass
2. `test_home_url_resolves_home_view` — ✅ pass

**ArticleURLsTests:**
3. `test_articles_list_status_code` — ✅ pass
4. `test_category_list_requires_slug` — ✅ pass
5. `test_article_detail_url` — ✅ pass
6. `test_article_list_resolves` — ✅ pass
7. `test_category_list_resolves` — ✅ pass
8. `test_article_detail_resolves` — ✅ pass

**Результати запуску:**
```
Found 8 test(s).
System check identified no issues (0 silenced).
........
Ran 8 tests in 0.044s
OK ✓
```

### Команди для запуску
```bash
cd lab4_project
python manage.py migrate                          # Міграції БД
python manage.py test app_blog.tests_urls -v 2   # Запуск тестів
python manage.py runserver 127.0.0.1:8002        # Запуск сервера
```

### Дотуп до сторінок
| Сторінка | URL |
|----------|-----|
| Головна | http://127.0.0.1:8002/ |
| Всі статті | http://127.0.0.1:8002/articles/ |
| Категорія | http://127.0.0.1:8002/articles/category/[slug]/ |
| Деталі | http://127.0.0.1:8002/articles/[year]/[month]/[day]/[slug]/ |
| Адміністрація | http://127.0.0.1:8002/admin/ |

### Результат
- ✅ 4 Views реалізовані та працюють
- ✅ 4 URL-маршрути налаштовані
- ✅ 4 HTML-шаблони розроблені
- ✅ 8 юніт-тестів написано та 100% пройдено
- ✅ Всі HTTP responses = 200 OK
- ✅ Всі URL-маршрути правильно розв'язуються

---

## Структура файлів

```
c:\work\myblog\
├── lab3_project/                 # Окремий проект для Lab 3
│   ├── manage.py
│   ├── requirements.txt
│   ├── lab3_db.sqlite3
│   ├── README.md                 # Інструкції Lab 3
│   ├── mysite/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   └── app_blog/
│       ├── models.py
│       ├── admin.py
│       ├── forms.py
│       ├── urls.py               # Порожні маршрути
│       ├── views.py              # Placeholder
│       └── migrations/
│
├── lab4_project/                 # Окремий проект для Lab 4
│   ├── manage.py
│   ├── requirements.txt
│   ├── lab4_db.sqlite3
│   ├── README.md                 # Інструкції Lab 4
│   ├── mysite/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   └── app_blog/
│       ├── models.py
│       ├── admin.py
│       ├── forms.py
│       ├── views.py              # 4 views класи
│       ├── urls.py               # 4 маршрути
│       ├── tests_urls.py         # 8 тестів
│       ├── templates/
│       │   ├── index.html
│       │   ├── articles_list.html
│       │   ├── article_detail.html
│       │   └── fotorama.html
│       └── migrations/
│
├── lab3/                         # Папка з app_blog копіями
│   └── app_blog/
├── lab4/                         # Папка з app_blog копіями
│   └── app_blog/
├── mysite/                       # Оригінальний проект
├── app_blog/                     # Оригінальна app
└── .git/                         # Git репозиторій
```

---

## Залежності (requirements.txt)

```
asgiref==3.11.0
Django==6.0.1
pillow==12.1.0
sqlparse==0.5.5
tzdata==2025.3
```

---

## Git комітиз

### Основні коміти (GitHub: https://github.com/SviatoslavHryhoriv/myblog)

1. **Lab 3 implementation** — створення моделей, адміністрації, форм
2. **Lab 3 migrations & populate** — міграції БД, скрипти для тестування
3. **Lab 4 implementation** — views, urls, templates, tests
4. **Lab 4: views, urls, templates, tests** — цільовий коміт (2aae559)
5. **Add lab3_project and lab4_project copies** — копії окремих проектів (016e228)
6. **Lab 4: Complete with tests, templates, and urls** — фінальний коміт (2aae559)

---

## Як використовувати для звіту

### Для Lab 3
```bash
cd lab3_project
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 127.0.0.1:8001
# Відкрити http://127.0.0.1:8001/admin/ і показати моделі
```

### Для Lab 4
```bash
cd lab4_project
python manage.py migrate
python manage.py test app_blog.tests_urls --verbosity 2  # Показати результати тестів
python manage.py runserver 127.0.0.1:8002
# Відкрити http://127.0.0.1:8002/ та інші сторінки
```

---

## Висновок

Обидві лабораторні роботи успішно завершені:

| Вимога | Lab 3 | Lab 4 |
|--------|-------|-------|
| Моделі | ✅ 3/3 | ✅ 3/3 |
| Адміністрація | ✅ 3/3 | ✅ 3/3 (скопійовано) |
| Views | ❌ 0/4 | ✅ 4/4 |
| URL-маршрути | ❌ 0/4 | ✅ 4/4 |
| Шаблони | ❌ 0/4 | ✅ 4/4 |
| Тести | ❌ 0/8 | ✅ 8/8 ✓ |
| Міграції БД | ✅ OK | ✅ OK |
| Git commit | ✅ OK | ✅ OK |

**Загальний результат:** ✅ **100% завершено та протестовано**

---

**Автор:** Assistant  
**Дата:** 02.02.2026  
**Django версія:** 6.0.1  
**Python версія:** 3.13+  
**Статус:** ✅ ГОТОВО ДО ЗДАЧІ
