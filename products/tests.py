
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from acconts.models import CustomUser
from .models import (Comment, Product)


class TestListAndDetailView(TestCase):
    # --------------------------------------------------------------------------------
    def setUp(self):

        # user 1
        user = get_user_model().objects.create(email='t.hgfsrb4567@gmail.com', username='reza')
        user.set_password('12345')
        user.save()

        l = self.client.login(email="t.hgfsrb4567@gmail.com", password="12345")
        self.assertTrue(l)
        self.client.logout()
        # product 1
        self.product1 = Product.objects.create(
            title='book1',
            description='qwertyuiop[[[[[[asdfghjkl;;;;;zxcvbnm,./////09876543212345678',
            price=11.11,
        )

        # comment 1 for product1
        self.comment1 = Comment.objects.create(
            product=self.product1,
            body='QWERTY{zxcvbnm},[09876543212345678]',
            author_id=1,
            starts=1,
        )
    # -------------------------------------------------------------------------------
    def test_list_view(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product1.title)
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        # -----------------------------------------------
    def test_detail_view(self):
        response = self.client.get(reverse('product_detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product1.title)
        self.assertContains(response, 'QWERTY{zxcvbnm},[09876543212345678]')
        response = self.client.get('/products/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')
        # -----------------------------------------------
    def test_comment_view(self):
        response = self.client.get(reverse('product_detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product1.title)
        self.assertContains(response, self.comment1.body)
        response = self.client.get('/products/1/')
        self.assertEqual(response.status_code, 200)
    #     -----------------------------------------------
        l = self.client.login(email="t.hgfsrb4567@gmail.com", password="12345")
        self.assertTrue(l)
        response = self.client.post(reverse('product_comment', args=[self.product1.id]),
                                    data={'body': '---0987654321---', 'starts': '1'})
        self.assertRedirects(response,f"/products/{self.product1.id}/")
        response = self.client.get(reverse('product_detail', args=[1]))
        self.assertContains(response, '---0987654321---')






