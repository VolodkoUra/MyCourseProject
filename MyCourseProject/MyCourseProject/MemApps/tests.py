import datetime

from django.urls import reverse
from django.utils import timezone
from django.test import TestCase, Client, RequestFactory
from .models import Users, Roles, Memasik, MyGallery, MemIntermediate
from django.core.files.uploadedfile import SimpleUploadedFile
from .views import login_user
from .form import RegistrationForm, LoginForm


# Create your tests here.
# Проверка регистрации пользователя
class RegistrViewsTest(TestCase):
    def setUp(self):
        print('setUP')
        role_user = Roles.objects.create(name_roles='custom')
        user = Users.objects.create(
            user_name='Nikolay',
            user_password='Nikolay',
            email='nikolay@mail.ru',
            date=datetime.datetime(year=1992, month=8, day=12),
            id_name_role=role_user
        )
        # print(role_user)
        # print(user)
        user.save()

    def test_registr_views(self):
        print('test_registr_views')
        client = Client()
        self.assertEqual(Users.objects.count(), 1)
        response = self.client.post('/registration/', {'login': 'Mikola',
                                                       'password': 'Mikola',
                                                       'date': datetime.date(year=1993,
                                                                             month=9, day=17),
                                                       'email': 'mikola@mail.ru'
                                                       })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Users.objects.count(), 2)
        self.assertEqual(Users.objects.get(user_name='Mikola').user_name, 'Mikola')
        self.assertEqual(response.url, '/')

        response2 = self.client.post('/registration/', {'login': 'Mikola',
                                                        'password': 'Mikola123',
                                                        'date': datetime.date(year=1999,
                                                                              month=1, day=19),
                                                        'email': 'mikola@mail.ru'
                                                        })

        self.assertEqual(response2.status_code, 200)
        self.assertEqual(Users.objects.count(), 2)
        self.assertEqual(response2.context[-1]['message'], 'Пользоватедь с таким логином уже зарегистрирован')
        self.assertEqual(str(response2.context['user']), 'AnonymousUser')

        response3 = self.client.post('/registration/', {'login': 'Gnom',
                                                        'password': 'Gnom',
                                                        'date': datetime.date(year=1995,
                                                                              month=4, day=22),
                                                        'email': 'gnom@mail.ru'
                                                        })

        self.assertEqual(response3.status_code, 200)
        self.assertEqual(Users.objects.count(), 2)
        self.assertEqual(response3.context[-1]['message'], 'Введены не корректные данные')
        self.assertEqual(str(response3.context['user']), 'AnonymousUser')


class LoginUserTest(TestCase):

    def setUp(self) -> None:
        print('login_setUP')
        role_user = Roles.objects.create(name_roles='custom')
        user = Users.objects.create(
            user_name='Nikolay',
            user_password='Nikolay',
            email='nikolay@mail.ru',
            date=datetime.datetime(year=1992, month=8, day=12),
            id_name_role=role_user
        )
        # print(role_user)
        # print(user)
        user.save()

    def test_login_user(self):
        response = self.client.get('/login_user/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')

    def test_login_logout_post_user(self):
        response = self.client.post('/login_user/', {'login': 'Nikolay', 'password': 'Nikolay'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'test.html')

        response = self.client.get('/logout/', follow=True)
        print(response.status_code)
        self.assertTemplateNotUsed(response, 'test.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_login_post_false_user(self):
        response = self.client.post('/login_user/', {'login': 'Nikolay555', 'password': 'Nikolay555'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'test.html')


class TestGallery(TestCase):
    @classmethod
    def setUpTestData(cls):
        role_user = Roles.objects.create(name_roles='custom')
        cls.user = Users.objects.create(
            user_name='Nikolay',
            user_password='Nikolay',
            email='nikolay@mail.ru',
            date=datetime.datetime(year=1992, month=8, day=12),
            id_name_role=role_user
        )

        image = SimpleUploadedFile('mem.jpg', content=b'', content_type='image/jpg')
        mem = Memasik.objects.create(
            url_image=image,
            tags="#1 #2 #3",
            date_mem=datetime.datetime.now()
        )

    def test_gallery_get(self):
        response = self.client.post('/login_user/', {'login': 'Nikolay', 'password': 'Nikolay'}, follow=True)
        response2 = self.client.get('/gallery/')
        self.assertEqual(response2.status_code, 200)
        self.assertTemplateUsed(response2, 'gallery.html')

    def test_gallery_add_delete(self):
        response = self.client.post('/login_user/', {'login': 'Nikolay', 'password': 'Nikolay'}, follow=True)
        self.assertFalse(MyGallery.objects.all())
        response2 = self.client.post('/gallery/', {'mem_id': Memasik.objects.get(id=2).id})
        self.assertTrue(MyGallery.objects.all())
        print(response2.status_code)
        self.assertEqual(response2.status_code, 200)
        self.assertTemplateUsed(response2, 'gallery.html')



class AddNewMem(TestCase):
    @classmethod
    def setUpTestData(cls):
        role_user = Roles.objects.create(name_roles='custom')
        cls.user = Users.objects.create(
            user_name='Nikolay',
            user_password='Nikolay',
            email='nikolay@mail.ru',
            date=datetime.datetime(year=1992, month=8, day=12),
            id_name_role=role_user
        )


    def test_add_new_mem(self):
        response = self.client.post('/login_user/', {'login': self.user.user_name, 'password': self.user.user_password},
                                    follow=True)
        response2 = self.client.get('/upload/')
        self.assertEqual(response2.status_code, 200)
        self.assertTemplateUsed(response2, 'add_new.html')

    def test_add_new_mem_post(self):
        response = self.client.post('/login_user/', {'login': 'Nikolay', 'password': 'Nikolay'}, follow=True)
        image = SimpleUploadedFile('mem.jpg', content=b'', content_type='image/jpg')
        response2 = self.client.post('/upload/', {'file': image})  # Загрузка картинки на сайт (в промежуточную таблицу)
        self.assertEqual(response2.status_code, 200)
        self.assertTemplateUsed(response2, 'add_new.html')
        self.assertTrue(MemIntermediate.objects.all())
        self.assertFalse(Memasik.objects.all())
        response3 = self.client.post('/add_mem_admin/', {'tags': '#работа #дом',
                                                         'url_image': MemIntermediate.objects.get(id=1).url_image.url,
                                                         'mem_id': MemIntermediate.objects.get(id=1).id}, follow=True)
        print(response3.status_code)
        self.assertTrue(Memasik.objects.all())
        self.assertTemplateUsed(response3, 'add_new.html')


class AddAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        role_user = Roles.objects.create(name_roles='custom')
        cls.user = Users.objects.create(
            user_name='Nikolay',
            user_password='Nikolay',
            email='nikolay@mail.ru',
            date=datetime.datetime(year=1992, month=8, day=12),
            id_name_role=role_user
        )

    def add_admin(self):
        response = self.client.post('/login_user/', {'login': self.user.user_name, 'password': self.user.user_password},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        response2 = self.client.post('/add_admin/', {'user_name': self.user.user_name, 'role': Roles.objects.get(name_roles='admin')})
        self.assertEqual(response2.status_code, 200)
        self.assertTemplateUsed(response2, 'add_admin.html')


"""class RegistrModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print('setUpTestData')
        role_user = Roles.objects.create(name_roles='custom')
        cls.user = Users.objects.create(
            user_name='Nikolay',
            user_password='Nikolay',
            email='nikolay@mail.ru',
            date=datetime.datetime(year=1992, month=8, day=12),
            id_name_role=role_user
        )
        print(role_user)
        print(cls.user)

    def setUp(self) -> None:
        print('setUp')
        pass

    def test_t_t(self):
        print('t-t')
        self.assertTrue(True)

    def test_f_f(self):
        print('f-f')
        self.assertFalse(False)

    def test_one_two(self):
        print('one-two')
        self.assertEqual(1 + 1, 2)

    def test_model_user(self):
        print(self.user, "USER")
        field_name = self.user._meta.get_field('user_name').verbose_name
        print(field_name)
        self.assertEqual(field_name, 'user name')
        max_length = self.user._meta.get_field('user_name').max_length
        self.assertEqual(max_length, 255)


class RegistrFormTest(TestCase):

    def test_registr_form_login(self):
        form = RegistrationForm()
        print(form.fields['login'].label, '!!!!')

        self.assertEqual(form.fields['login'].label, None)
        self.assertEqual(form.fields['login'].help_text, "Введите логин, минимум 4 символа")




    def setUp(self):
        self.role_user = Roles.objects.filter(name_roles='custom').first()
        self.user = Users.objects.create(
            user_name='Nikolay',
            user_password='Nikolay',
            email='nikolay@mail.ru',
            date=datetime.datetime(year=1992, month=8, day=12),
            id_name_role=self.role_user
        )

    def test_registr_user(self):
        self.assertIn(self.user, Users.objects.all())

    def test_response_registr_user(self):
        client = Client()
        response = client.get('/registration/')
        self.assertEqual(response.status_code, 200)


    #????
    def test_user_name(self):
        u = Users.objects.get(id=1)
        print(u, '!!!')
        field_label = u._meta.get_field('user_name').verbose_name
        self.assertEqual(field_label, 'user_name')
        
        
        
        
        #print(response.url, '00000000000000')
        #self.assertTemplateUsed(response, 'test.html')
        #self.assertRedirects(response, '/')

        #print(response.content.template_name, '((((((((((((')
        #factory = RequestFactory()        print(response2.context.template_name)

        #request = factory.get('')
        #user = Users.objects.get(user_name='Nikolay')
        #request.user = user
        #response2 = factory.post('/login_user/', {'login': 'Nikolay', 'password': 'Nikolay'})
        #response2 = login_user(request)
        #print(response2.__dict__)
        #print(request.__dict__, '!!!!!!')
        #print(response2.status_code)
        #print(response2.url)
        #print(response2.status_code, '333333333')
        #self.assertTemplateUsed(response2, 'base.html')
        #print(self.user, "!!!!!!!!!!!!!!!!!!!!!!!!!!")
        #response2 = self.client.post('/login_user/', {'login': 'Nikolay', 'password': 'Nikolay'}, follow=True)
        #self.assertEqual(response2.status_code, 200)
        #print(response2.context['user'])
        #self.assertTemplateUsed(response2, 'test.html')
        #print(response2.context.template_name, 'REDIRECT_CHAIN2')
        #print(response2.context.url)
        users_all = Users.objects.all()
        print('////////////')
        for i in users_all:
            print(i.user_name, ':', i.user_password)
        print('///////////////')




        #response3 = self.client.get(reverse('base'), follow=True)
        #self.assertTemplateUsed(response3, 'base.html')
        #print(response3.context, "CONTEXT")
        #print(response2.context.template_name, "REDIRECT_CHAIN")
        
"""
