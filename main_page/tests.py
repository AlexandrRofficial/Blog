from django.test import TestCase

from django.urls import reverse

from django.contrib.auth.models import User

from .models import Article, Tag, Category

class MainPageViewTests(TestCase):

    def test_main_page_returns_200_and_template(self):
        response = self.client.get(reverse("main_page"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main_page/main_page.html")

    def test_anonymous_user_sees_only_published_articles(self):
        category = Category.objects.create(name="Test category")

        Article.objects.create(
            title="Published article",
            content="content",
            status=Article.STATUS_PUBLISHED,
            category=category,
            author=User.objects.create_user("author1")
        )

        Article.objects.create(
            title="Draft article",
            content="content",
            status=Article.STATUS_DRAFT,
            category=category,
            author=User.objects.create_user("author2")
        )

        response = self.client.get(reverse("main_page"))

        articles = response.context["articles"]

        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].status, Article.STATUS_PUBLISHED)