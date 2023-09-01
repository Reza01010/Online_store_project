from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.template import Context, Template


class ProductsViewTest(TestCase):

    # ++++++++++++++++++++++
    def setUp(self):
        # _____
        user = get_user_model().objects.create(username='gggggg',email="tyfyjeni6429@gmail.com", )
        user.set_password('yffufuf75757567465')
        user.save()
        # ----------------
        l = self.client.login(username='gggggg', password='yffufuf75757567465')
        self.assertTrue(l)

    # =======================
    def test_signup_url_name(self):
        # _____
        response = self.client.get('/accounts/signup/')
        # ----------------
        self.assertNotEqual(response.status_code, 200)
        self.client.logout()
        # _____
        response = self.client.get(reverse('account_signup'))
        # ----------------
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'SignUp')
        # _____
        response = self.client.post(reverse('account_signup'), {
            'email': 'testuser@example.com',
            'password1': 'testpassword',
        })
        # ----------------
        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_user_model().objects.all().count(), 2)
        self.assertEqual(self.longMessage, True)
        self.assertRedirects(response, expected_url=reverse('pages:home'))

    # =======================
    def test_login_url_name(self):
        # _____
        response = self.client.get('/accounts/login/')
        # ----------------
        self.assertNotEqual(response.status_code, 200)
        self.client.logout()
        # _____
        response = self.client.get(reverse('account_login'))
        # ----------------
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'LogIn')
        # _____
        response = self.client.post(reverse('account_login'), {
            'login': 'tyfyjeni6429@gmail.com',
            'password': 'yffufuf75757567465',
        })
        # ----------------
        self.assertEqual(get_user_model().objects.all()[0].email, 'tyfyjeni6429@gmail.com')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('pages:home'))

    # =======================
    def test_logout_url_name(self):
        # _____
        response = self.client.get('/accounts/logout/')
        # ----------------
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Log Out')
        self.client.logout()
        # _____
        response = self.client.get(reverse('account_logout'))
        # ----------------
        self.assertNotEqual(response.status_code, 200)
        # _____
        response = self.client.post(reverse('account_logout'),{})
        # _____
        response = self.client.get(reverse('account_logout'))
        # ----------------
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('pages:home'))

