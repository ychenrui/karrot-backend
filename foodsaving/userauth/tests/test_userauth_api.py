from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from foodsaving.groups.factories import GroupFactory
from foodsaving.stores.factories import StoreFactory, PickupDateFactory
from foodsaving.users.factories import UserFactory, VerifiedUserFactory
from foodsaving.utils.tests.fake import faker


class TestUsersAPI(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.url = '/api/auth/user/'
        self.user_data = {
            'email': faker.email(),
            'password': faker.name(),
            'display_name': faker.name(),
            'address': faker.address(),
            'latitude': faker.latitude(),
            'longitude': faker.longitude()
        }
        mail.outbox = []

    def test_create_user(self):
        response = self.client.post(self.url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], self.user_data['email'])
        self.assertAlmostEqual(response.data['latitude'], float(self.user_data['latitude']))
        self.assertEqual(response.data['description'], '')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Verify your email address')
        self.assertEqual(mail.outbox[0].to, [self.user_data['email']])
        self.assertIn('Thank you for signing up', mail.outbox[0].body)

    def test_retrieve_user_forbidden(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_user_allowed(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], self.user.description)

    def test_patch_user_forbidden(self):
        response = self.client.patch(self.url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_self_allowed(self):
        self.client.force_login(user=self.user)
        response = self.client.patch(self.url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_only_description(self):
        self.client.force_login(user=self.user)
        response = self.client.patch(self.url, {'description': ' test'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], ' test')

    def test_patch_too_long_description(self):
        self.client.force_login(user=self.user)
        response = self.client.patch(self.url, {'description': 'ab' * settings.DESCRIPTION_MAX_LENGTH}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestUserDeleteAPI(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user2 = UserFactory()
        self.group = GroupFactory(members=[self.user, self.user2])
        self.store = StoreFactory(group=self.group)
        self.pickupdate = PickupDateFactory(
            store=self.store,
            date=timezone.now() + relativedelta(days=1),
            collectors=[self.user, ])
        self.past_pickupdate = PickupDateFactory(
            store=self.store,
            date=timezone.now() - relativedelta(days=1),
            collectors=[self.user, ]
        )
        self.url = '/api/users/'

    def test_delete_self(self):
        self.assertEqual(self.pickupdate.collectors.count(), 1)
        self.assertEqual(self.past_pickupdate.collectors.count(), 1)

        self.client.force_login(self.user)
        url = self.url + str(self.user.id) + '/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response.data)

        self.assertFalse(self.group.members.get_queryset().filter(id=self.user.id).exists())
        self.assertFalse(self.pickupdate.collectors.get_queryset().filter(id=self.user.id).exists())
        self.assertTrue(self.past_pickupdate.collectors.get_queryset().filter(id=self.user.id).exists())

        # delete another user
        u2 = UserFactory()
        self.client.force_login(u2)
        url = '/api/users/{}/'.format(u2.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_remove_user_forbidden(self):
        url = self.url + str(self.user.id) + '/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_remove_different_user_forbidden(self):
        self.client.force_login(user=self.user)
        url = self.url + str(self.user2.id) + '/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestCreateUserErrors(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.url = '/api/users/'

    def test_create_user_with_similar_cased_email_fails(self):
        response = self.client.post(self.url, {
            'email': 'fancy@example.com',
            'password': faker.name(),
            'display_name': faker.name()
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(self.url, {
            'email': 'Fancy@example.com',
            'password': faker.name(),
            'display_name': faker.name()
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(response.data['email'], ['Similar e-mail exists: fancy@example.com'])


class TestChangePassword(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.url = '/api/users/'
        self.data = {'password': 'new_password'}

    def test_change_with_patch_succeeds(self):
        self.client.force_login(user=self.user)
        url = self.url + str(self.user.id) + '/'
        response = self.client.patch(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # logged out
        response = self.client.patch(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # test new password
        self.assertTrue(self.client.login(email=self.user.email, password='new_password'))

    def test_change_with_all_data_succeeds(self):
        self.client.force_login(user=self.user)
        url = self.url + str(self.user.id) + '/'

        # typical frontend use case of getting, modifying and sending data
        data = self.client.get(url).data
        data['password'] = 'really_new_shiny'
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

        # logged out
        response = self.client.patch(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # test new password
        self.assertTrue(self.client.login(email=self.user.email, password='really_new_shiny'))


class TestChangeMail(APITestCase):
    def setUp(self):
        self.verified_user = VerifiedUserFactory()
        self.another_user = VerifiedUserFactory()
        self.url = '/api/users/'
        self.user_url = self.url + str(self.verified_user.id) + '/'
        mail.outbox = []

    def test_change_succeeds(self):
        self.client.force_login(user=self.verified_user)
        self.assertTrue(self.verified_user.mail_verified)

        # typical frontend use case of getting, modifying and sending data
        data = self.client.get(self.user_url).data
        data['email'] = faker.email()
        response = self.client.patch(self.user_url, data, format='json')
        user = get_user_model().objects.get(id=self.verified_user.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(response.data['email'], self.verified_user.email)
        self.assertFalse(user.mail_verified)
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[0].subject, 'Your email address changed!')
        self.assertEqual(mail.outbox[0].to, [user.email])
        self.assertEqual(mail.outbox[1].subject, 'Please verify your email')
        self.assertEqual(mail.outbox[1].to, [user.unverified_email])
        self.assertNotIn('Thank you for signing up', mail.outbox[1].body)

        user.verify_mail()
        self.assertTrue(user.mail_verified)
        response = self.client.get(self.user_url)
        self.assertEqual(response.data['email'], data['email'])

    def test_change_to_existing_mail_fails(self):
        self.client.force_login(user=self.verified_user)
        data = {'email': self.another_user.email}
        response = self.client.patch(self.user_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(mail.outbox), 0)

    def test_change_to_existing_similar_mail_fails(self):
        self.client.force_login(user=self.verified_user)
        similar_mail = self.another_user.email[0].swapcase() + self.another_user.email[1:]
        data = {'email': similar_mail}
        response = self.client.patch(self.user_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'], ['Similar e-mail exists: ' + self.another_user.email])
        self.assertEqual(len(mail.outbox), 0)

    def test_change_to_similar_mail_succeeds(self):
        self.client.force_login(user=self.verified_user)
        similar_mail = self.verified_user.email[0].swapcase() + self.verified_user.email[1:]
        data = {'email': similar_mail}
        response = self.client.patch(self.user_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 2)