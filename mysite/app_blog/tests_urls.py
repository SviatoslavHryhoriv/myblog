from django.test import TestCase
from django.urls import reverse, resolve
from .views import HomePageView, ArticleList, ArticleCategoryList, ArticleDetail
from .models import Category, Article
from django.utils import timezone

class HomeTests(TestCase):
    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEqual(view.func.view_class, HomePageView)

class ArticleURLsTests(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(category='TestCat', slug='testcat')
        self.article = Article.objects.create(
            title='Test Article',
            description='Desc',
            pub_date=timezone.now(),
            slug='test-article',
            main_page=False,
            category=self.cat
        )

    def test_articles_list_status_code(self):
        url = reverse('articles-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_category_list_requires_slug(self):
        url = reverse('articles-category-list', args=('testcat',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_article_detail_url(self):
        d = self.article.pub_date
        url = reverse('news-detail', kwargs={
            'year': d.year,
            'month': "%02d" % d.month,
            'day': "%02d" % d.day,
            'slug': self.article.slug
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_article_list_resolves(self):
        view = resolve('/articles/')
        self.assertEqual(view.func.view_class, ArticleList)

    def test_category_list_resolves(self):
        view = resolve('/articles/category/testcat/')
        self.assertEqual(view.func.view_class, ArticleCategoryList)

    def test_article_detail_resolves(self):
        d = self.article.pub_date
        path = f'/articles/{d.year}/{d.month:02d}/{d.day:02d}/{self.article.slug}/'
        view = resolve(path)
        self.assertEqual(view.func.view_class, ArticleDetail)
