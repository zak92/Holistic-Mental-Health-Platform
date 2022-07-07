# from django.test import TestCase, RequestFactory
# from django.urls import reverse, resolve
# from ...views import * 
# from django.core.files.uploadedfile import SimpleUploadedFile

# class TestForms(TestCase):
#   def setUp(self):
#     self.factory = RequestFactory()
#     self.data={
#       'first_name': 'John',
#       'last_name': 'Smith',
#       'username': 'j_smith', 
#       'email': 'test@mail.com',
#       'country': 'Spain',
#       'city': 'Seville',
#       'profile_picture': 'user.png'
#     }
#     self.user = User.objects.create_user( 
#       id=1,
#       username='kristy',
#       password='12test12', 
#       email='test@example.com',
#       country='Spain',
#       city='Madrid',
#       profile_picture=SimpleUploadedFile(name='hello.jpg', content=b'content', content_type='image/jpeg')
#     )
#     self.user.save()
#     self.client_user = Client.objects.create(
#       user=self.user,
#       bio="My name is Kristy",
#       status='Busy!'
#     )
#     self.client_user.save()
#     self.good_url = reverse('client-profile', kwargs={ 'username': 'kristy'})
#     self.bad_url = '/client-profiles/x'

#   def tearDown(self):
#     self.user.delete()
#     self.client_user.delete()

#   # def test_update_user_profile_form(self):
    
#   #   form = UpdateClientProfileForm(instance=self.client_user)
#   #   form.save()
#   #   # check if the form is valid
#   #   self.assertTrue(form.is_valid())

#   ## ADD TESTS HERE