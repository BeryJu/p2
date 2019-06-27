"""p2 ui API-Key tests"""
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import TestCase
# from guardian.shortcuts import assign_perm

# from p2.api.forms import APIKeyForm
# from p2.api.models import APIKey, get_access_key, get_secret_key


class APIViewTests(TestCase):
    """Test API-Key related views"""

    def setUp(self):
        self.user, _ = User.objects.get_or_create(
            username='p2-unittest')
        self.client.force_login(self.user)

    def test_api_key_list(self):
        """Check api-key listing"""
        response = self.client.get(reverse('p2_ui:api-key-list'))
        self.assertEqual(response.status_code, 200)

    # def test_api_key_create(self):
    #     assign_perm('p2_api.add_apikey', self.user)
    #     form = APIKeyForm(data={
    #         'name': 'test',
    #         'user': str(self.user.pk),
    #         'access_key': get_access_key(),
    #         'secret_key': get_secret_key(),
    #     })
    #     self.assertTrue(form.is_valid())
    #     response = self.client.post(reverse('p2_ui:api-key-create'), data=form.cleaned_data)
    #     self.assertEqual(response.status_code, 200)
    #     print(response.content)
    #     print(APIKey.objects.all())
    #     self.assertTrue(APIKey.objects.filter(name=form.cleaned_data['name']).exists())
