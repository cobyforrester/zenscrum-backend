from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient

from .models import Project, UserProject
# Create your tests here.
User = get_user_model()
class ProjectTesctCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(first_name='Coby', last_name='Forrester', username='first', password='somepassword')
        self.user2 = User.objects.create_user(username='second', password='somepassword')
        Project.objects.create(title='first proj', description='description', user=self.user1)
        Project.objects.create(title='sceond proj', description='description', user=self.user1)
        Project.objects.create(title='third proj', description='description', user=self.user1)
        
    def test_project_created(self):
        proj1 = Project.objects.create(title='fourth proj', description='description', user=self.user2)
        self.assertEqual(proj1.id, 4)
        self.assertEqual(proj1.user, self.user2)
    

    def get_client(self):
        client = APIClient()
        client.login(username=self.user1.username, password='somepassword')
        return client

    def test_project_list(self):
        client = self.get_client()
        response = client.get('/api/projects/')
        self.assertEqual(response.status_code, 200)
        print(response.json())
