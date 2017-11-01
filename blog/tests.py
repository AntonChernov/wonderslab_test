from django.contrib.auth import get_user_model
from django.test import Client
from django.test import TestCase

# Create your tests here.
from django.urls import reverse_lazy

from blog.models import Post


class PostTests(TestCase):

    def setUp(self):
        self.user1 = get_user_model().objects.create(
            username='test1',
            email='test1@gmail.com',
            first_name='Billy',
            last_name='Dodson'
        )
        self.user1.set_password('test1pass')
        self.user2 = get_user_model().objects.create(
            username='test2',
            email='test2@gmail.com',
            first_name='Jilian',
            last_name='Sommers'
        )
        self.user2.set_password('test2pass')

        Post.objects.bulk_create(
            [
                Post(author=self.user1, title='Some title 1', text='some text 1'),
                Post(author=self.user2, title='Some title 2', text='some text 2'),
                Post(author=self.user2, title='Some title 3', text='some text 3'),
                Post(author=self.user1, title='Some title 4', text='some text 4'),
                Post(author=self.user1, title='Some title 5', text='some text 5'),
                Post(author=self.user2, title='Some title 6', text='some text 6'),
            ]
        )

        self.client = Client()

    def test_login(self):
        response = self.client.post(reverse_lazy('login'), data={
            'username': self.user1.username,
            'password': 'test1pass'
        })
        self.assertEqual(response.status_code, 200)

    def show_post_authenticate_user(self):
        user = self.client.force_login(user=self.user1)
        response = self.client.get(reverse_lazy('user_posts', kwargs={'pk': self.user1.id}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse_lazy('user_posts', kwargs={'pk': 12}))
        self.assertEqual(response.status_code, 404)
        self.client.logout()

    def test_redirect_to_login(self):
        response = self.client.get(reverse_lazy('user_posts', kwargs={'pk': self.user1.id}), follow=True)
        last_url, status_code = response.redirect_chain[-1]
        self.assertEqual(last_url, reverse_lazy('login') + '?next=/blog/users/1/')
        self.assertEqual(status_code, 302)

    def test_change_if_not_post_owner(self):
        user = self.client.post(reverse_lazy('login'), {'username': self.user1.username,
                                                        'password': 'test1pass'})
        response = self.client.post(reverse_lazy('update_post', kwargs={'pk': 3}), follow=True)
        print(response)
        self.assertEqual(response.status_code, 200)
