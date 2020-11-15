import os
from urllib.request import urlretrieve

from django.core.exceptions import ValidationError
from django.core.files import File
from django.test import TestCase

# Create your tests here.
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





    # def test_first_name_label(self):
    #     author = Author.objects.get(id=1)
    #     field_label = author._meta.get_field('first_name').verbose_name
    #     self.assertEqual(field_label, 'first name')
    #
    # def test_date_of_death_label(self):
    #     author=Author.objects.get(id=1)
    #     field_label = author._meta.get_field('date_of_death').verbose_name
    #     self.assertEqual(field_label, 'died')
    #
    # def test_first_name_max_length(self):
    #     author = Author.objects.get(id=1)
    #     max_length = author._meta.get_field('first_name').max_length
    #     self.assertEqual(max_length, 100)
    #
    # def test_object_name_is_last_name_comma_first_name(self):
    #     author = Author.objects.get(id=1)
    #     expected_object_name = f'{author.last_name}, {author.first_name}'
    #     self.assertEqual(expected_object_name, str(author))
    #
    # def test_get_absolute_url(self):
    #     author = Author.objects.get(id=1)
    #     # This will also fail if the urlconf is not defined.
    #     self.assertEqual(author.get_absolute_url(), '/catalog/author/1')


# class QuestionIndexViewTess(TestCase):
#     def test_no_questions(self):
#         """
#         If no questions exist, an appropriate message is displayed.
#         """
#         response = self.client.get(reverse('polls:index'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "No polls are available.")
#         self.assertQuerysetEqual(response.context['latest_question_list'], [])
#
#     def test_past_question(self):
#         """
#         Questions with a pub_date in the past are displayed on the
#         index page.
#         """
#         create_question(question_text="Past question.", days=-30)
#         response = self.client.get(reverse('polls:index'))
#         self.assertQuerysetEqual(
#             response.context['latest_question_list'],
#             ['<Question: Past question.>']
#         )
#
#     def test_future_question(self):
#         """
#         Questions with a pub_date in the future aren't displayed on
#         the index page.
#         """
#         create_question(question_text="Future question.", days=30)
#         response = self.client.get(reverse('polls:index'))
#         self.assertContains(response, "No polls are available.")
#         self.assertQuerysetEqual(response.context['latest_question_list'], [])
#
#     def test_future_question_and_past_question(self):
#         """
#         Even if both past and future questions exist, only past questions
#         are displayed.
#         """
#         create_question(question_text="Past question.", days=-30)
#         create_question(question_text="Future question.", days=30)
#         response = self.client.get(reverse('polls:index'))
#         self.assertQuerysetEqual(
#             response.context['latest_question_list'],
#             ['<Question: Past question.>']
#         )
#
#     def test_two_past_questions(self):
#         """
#         The questions index page may display multiple questions.
#         """
#         create_question(question_text="Past question 1.", days=-30)
#         create_question(question_text="Past question 2.", days=-5)
#         response = self.client.get(reverse('polls:index'))
#         self.assertQuerysetEqual(
#             response.context['latest_question_list'],
#             ['<Question: Past question 2.>', '<Question: Past question 1.>']
#         )
