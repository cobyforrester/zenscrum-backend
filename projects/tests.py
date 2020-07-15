from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient

from .models import Project, UserProject
# Create your tests here.
User = get_user_model()
class ProjectTesctCase(TestCase):
    def setUp(self):
        self.num_of_projects = 3
        self.num_of_users = 2
        self.user1 = User.objects.create_user(first_name='Coby', last_name='Forrester', username='first', password='somepassword')
        self.user2 = User.objects.create_user(username='second', password='somepassword')
        self.proj1 = Project.objects.create(title='first proj', description='description', user=self.user1)
        self.proj2 = Project.objects.create(title='sceond proj', description='description', user=self.user1)
        self.proj3 = Project.objects.create(title='third proj', description='description', user=self.user2)

        client = self.get_client()
        data = {
            'id': self.proj2.id,
            'action': 'add',
            'member': 'second'
        }
        response = client.post('/api/projects/action/', data=data)
        print(response)



    def test_project_created(self):
        proj = Project.objects.create(title='fourth proj', description='description', user=self.user2)
        self.assertEqual(proj.id, 4)
        self.assertEqual(proj.user, self.user2)
    

    def get_client(self):
        client = APIClient()
        client.login(username=self.user1.username, password='somepassword')
        return client

    def test_project_list(self):
        client = self.get_client()
        response = client.get('/api/projects/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), self.num_of_projects)

    def test_project_action(self):
        client = self.get_client()
        #test add
        data = {
            'id': self.proj1.id,
            'action': 'add',
            'member': 'second'
        }
        response = client.post('/api/projects/action/', data=data)
        self.assertEqual(response.status_code, 200)
        response = client.get(f'/api/projects/{self.proj1.id}/')
        self.assertEqual(response.json()['members']['username'], 'second')
        self.assertEqual(response.status_code, 200)

        #test remove
        data['action'] = 'remove'
        response = client.post('/api/projects/action/', data=data)
        response = client.get(f'/api/projects/{self.proj1.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['members']['username'], '')

    def test_create_project_api(self):
        client = self.get_client()
        data = {
            'title': 'This is a title',
            'description': 'This is a description',
        }
        response = client.post('/api/projects/create/', data=data)
        self.assertEqual(response.status_code, 201)

        response = client.get('/api/projects/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), self.num_of_projects + 1)

    def test_view_project_api(self):
        client = self.get_client()
        response = client.get(f'/api/projects/{self.proj1.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], self.proj1.id)
        self.assertEqual(response.data['title'], self.proj1.title)

    def test_delete_project_api(self):
        client = self.get_client()
        response = client.delete(f'/api/projects/{self.proj1.id}/delete/')
        self.assertEqual(response.status_code, 200)

        response = client.get(f'/api/projects/{self.proj1.id}/')
        self.assertEqual(response.status_code, 404)

