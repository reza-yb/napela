import os

from django.core.exceptions import ValidationError
from django.core.files import File
from django.test import TestCase
from django.urls import reverse

from BookAdvertisement.models import BookAd


def create_book_ad(title="test_title", author="test_author", description="test_desc", sell=True, poster_url=None):
    book_ad = BookAd.objects.create(title=title, author=author, description=description, sell=sell)
    if poster_url:
        book_ad.poster.save(
            os.path.basename(poster_url),
            File(open(poster_url, 'rb'))
        )
        book_ad.save()
    return book_ad


class BookAdTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        create_book_ad()

    def test_integrity(self):
        book_ad = BookAd.objects.get(id=1)
        self.assertTrue(isinstance(book_ad, BookAd))
        self.assertEqual(book_ad.__str__(), 'test_title')

    def test_sell_ad_with_poster(self):
        url = "static/test/book_image.jpg"
        book_ad = create_book_ad(sell=True, poster_url=url)
        poster = File(open(url, 'rb'))
        self.assertEqual(book_ad.poster.file.readlines(), poster.readlines())

    def test_buy_ad_with_poster(self):
        with self.assertRaises(ValidationError):
            url = "static/test/book_image.jpg"
            create_book_ad(sell=False, poster_url=url)


class AllAdsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(100):
            create_book_ad(title=f'test_title_{i}')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/ads/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('all-ads'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('all-ads'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'all_ads.html')

    def test_latest_ads_present(self):
        ads = BookAd.objects.order_by('id')
        response = self.client.get(reverse('all-ads'))
        print(response.content)
        for i in range(10):
            self.assertInHTML(ads[-i].title, str(response.content))

