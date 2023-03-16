from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Groups, Apps, Comment
from .forms import AddComment


###### ТЕСТИРУЕМ MODELS.PY ##################

class GroupsModelTestCase(TestCase):
    def setUp(self):
        self.group = Groups.objects.create(slug='test-group', title='Test Group', desc='This is a test group.')

    def test_group_str_method(self):
        self.assertEqual(str(self.group), 'Test Group')

    def test_group_get_absolute_url_method(self):
        url = reverse('group', kwargs={'slug': 'test-group'})
        self.assertEqual(self.group.get_absolute_url(), url)


class AppsModelTestCase(TestCase):
    def setUp(self):
        self.group = Groups.objects.create(slug='test-group', title='Test Group', desc='This is a test group.')
        self.app = Apps.objects.create(slug='test-app', title='Test App', desc='This is a test app.', group=self.group)

    def test_app_str_method(self):
        self.assertEqual(str(self.app), 'Test App')

    def test_app_get_absolute_url_method(self):
        url = reverse('app', kwargs={'slug': 'test-group', 'slug_app': 'test-app'})
        self.assertEqual(self.app.get_absolute_url(), url)


class CommentModelTestCase(TestCase):
    def setUp(self):
        self.group = Groups.objects.create(slug='test-group', title='Test Group', desc='This is a test group.')
        self.app = Apps.objects.create(slug='test-app', title='Test App', desc='This is a test app.', group=self.group)
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.comment = Comment.objects.create(text='This is a test comment.', avtor=self.user, app=self.app)

    def test_comment_str_method(self):
        self.assertEqual(str(self.comment), 'В Test App написал testuser')

class GroupsModelTestCase(TestCase):
    def test_create_group(self):
        Groups.objects.create(slug='new-group', title='New Group', desc='This is a new group.')
        self.assertEqual(Groups.objects.count(), 1)

    def test_update_group(self):
        group = Groups.objects.create(slug='test-group', title='Test Group', desc='This is a test group.')
        group.title = 'Updated Test Group'
        group.save()
        updated_group = Groups.objects.get(slug='test-group')
        self.assertEqual(updated_group.title, 'Updated Test Group')

    def test_delete_group(self):
        group = Groups.objects.create(slug='test-group', title='Test Group', desc='This is a test group.')
        group.delete()
        self.assertEqual(Groups.objects.count(), 0)





###### ТЕСТИРУЕМ VIEWS.PY ##################

class GroupsListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем две группы и два приложения
        group1 = Groups.objects.create(slug='group1', title='Group 1', desc='Description 1')
        group2 = Groups.objects.create(slug='group2', title='Group 2', desc='Description 2')
        app1 = Apps.objects.create(slug='app1', title='App 1', desc='App description 1', group=group1)
        app2 = Apps.objects.create(slug='app2', title='App 2', desc='App description 2', group=group2)

    def test_view_url_exists_at_desired_location(self):
        # Проверяем, что представление доступно по адресу /groups/
        response = self.client.get('/groups/')
        self.assertEqual(response.status_code, 302)

    def test_view_url_accessible_by_name(self):
        # Проверяем, что представление доступно по имени 'home'
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        # Проверяем, что представление использует правильный шаблон
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/home.html')

    def test_view_returns_groups(self):
        # Проверяем, что представление возвращает список групп
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('groups' in response.context)
        groups = response.context['groups']
        self.assertEqual(groups.count(), 2)

    def test_view_returns_apps(self):
        # Проверяем, что представление возвращает список приложений
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('apps' in response.context)
        apps = response.context['apps']
        self.assertEqual(apps.count(), 2)

    def test_view_returns_title(self):
        # Проверяем, что представление возвращает правильный заголовок
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('title' in response.context)
        title = response.context['title']
        self.assertEqual(title, 'ruStore - приложения')

    def test_view_returns_title_view_groups(self):
        # Проверяем, что представление возвращает правильный заголовок для списка групп
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('title_view_groups' in response.context)
        title_view_groups = response.context['title_view_groups']
        self.assertEqual(title_view_groups, 'Группы')

    def test_view_returns_title_view_apps(self):
        # Проверяем, что представление возвращает правильный заголовок для списка приложений
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('title_view_apps' in response.context)
        title_view_apps = response.context['title_view_apps']
        self.assertEqual(title_view_apps, 'Приложения')



class GroupsDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создание тестовых данных для использования во всех тестах
        cls.group = Groups.objects.create(
            slug='test-slug',
            title='Test Group',
            desc='Test Group Description',
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/groups/test-slug')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('group', kwargs={'slug': 'test-slug'}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('group', kwargs={'slug': 'test-slug'}))
        self.assertTemplateUsed(response, 'main/group.html')

    def test_view_contains_group(self):
        response = self.client.get(reverse('group', kwargs={'slug': 'test-slug'}))
        self.assertEqual(response.context['group'], self.group)

    def test_view_contains_groups(self):
        response = self.client.get(reverse('group', kwargs={'slug': 'test-slug'}))
        self.assertTrue('groups' in response.context)

    def test_view_contains_apps(self):
        response = self.client.get(reverse('group', kwargs={'slug': 'test-slug'}))
        self.assertTrue('apps' in response.context)

    def test_view_contains_title(self):
        response = self.client.get(reverse('group', kwargs={'slug': 'test-slug'}))
        self.assertTrue('title' in response.context)
        print(response.context)




class AppsDetailViewTestCase(TestCase):
    def setUp(self):
        self.group = Groups.objects.create(
            title='Test group', 
            slug='test-group', 
            desc='Test group description'
        )
        self.app = Apps.objects.create(
            title='Test app', 
            slug='test-app', 
            desc='Test app description',
            group=self.group
        )
        self.comment_text = 'Test comment text'
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.url = reverse('app', kwargs={'slug': self.group.slug, 'slug_app': self.app.slug})
        
    def test_app_detail_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/app.html')
        self.assertContains(response, self.app.title)
        self.assertContains(response, self.app.desc)
        self.assertContains(response, self.group.title)
        # self.assertContains(response, self.comment_text)
        
    def test_app_detail_view_with_post(self):
        response = self.client.post(self.url, {'text': self.comment_text})
        self.assertEqual(response.status_code, 302)
        comment = Comment.objects.first()
        self.assertEqual(comment.text, self.comment_text)
        self.assertEqual(comment.avtor, self.user)
        self.assertEqual(comment.app, self.app)
    
