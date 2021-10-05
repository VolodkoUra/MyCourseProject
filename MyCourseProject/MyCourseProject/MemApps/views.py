from django.shortcuts import render, redirect
from .models import Users, Memasik, MyGallery, Roles, Tags, Massege
from .form import LoginForm, RegistrationForm, GalleryForm, MemIntermediate
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.views.generic import ListView
import time, datetime
from django.http import HttpResponse


# Функция для вывода картинок на дисплей
def func_display(r):
    mems = Memasik.objects.order_by('-date_mem')[:4]  # Берём из базы 4 самых свежих картинки
    data = []
    for i in mems:
        date_mem = int(time.mktime((i.date_mem).timetuple()))  # Перевод времени в секунды
        tags_list = Memasik.objects.filter(id=i.id)[0].tags
        obj = {
            'id': i.id,
            'url_image': i.url_image,
            'date_mem': date_mem,
            'tags': tags_list
        }
        print(tags_list)

        data.append(obj)

    user = Users.objects.filter(user_name=r.session.get('login'))

    """
    Роль конктретного пользователя, 
    для проверки в шаблоне, если админ 
    то показать кнопку для адмна
    """
    role = user[0].id_name_role.name_roles
    message_list = Massege.objects.filter(date_time_massege__gt=datetime.datetime.fromtimestamp(
        int(r.session.get('datetime', 0) - 3600)))  # Список сообщений для чата
    k = []
    for i in message_list:
        dat = int(time.mktime((i.date_time_massege).timetuple()))
        t = datetime.datetime.utcfromtimestamp(dat).strftime('%d-%m-%Y %H:%M')
        obj = {
            'id': i.id,
            'massege': i.massege,
            'date_time_massege': t,
            'user': i.user
        }
        k.append(obj)

    all_tags = Tags.objects.all()
    print(all_tags)

    return render(r, 'test.html',
                  {'images': data, 'role': role, 'message_list': k, 'login': r.session['login'], 'tags': all_tags})


# Функция загрузки картинок с локального компьютера на сайт
def model_form_upload(request):
    if request.method == 'GET':
        user = Users.objects.filter(user_name=request.session.get('login'))[0]
        my_add_new_image = MemIntermediate.objects.filter(
            id_user=user)  # загруженные на сайт, но еще не обработанные (без тегов)
        print(my_add_new_image)
        message_list = Massege.objects.filter(date_time_massege__gt=datetime.datetime.fromtimestamp(
            int(request.session.get('datetime') - 3600)))  # Список сообщений для чата

        role = user.id_name_role.name_roles
        message_list_parse = []
        for i in message_list:
            dat = int(time.mktime((i.date_time_massege).timetuple()))
            t = datetime.datetime.utcfromtimestamp(dat).strftime('%d-%m-%Y %H:%M')
            obj = {
                'id': i.id,
                'massege': i.massege,
                'date_time_massege': t,
                'user': i.user
            }
            message_list_parse.append(obj)
        return render(request, 'add_new.html',
                      {'my_add_new_image': my_add_new_image, 'role': role, 'message_list': message_list_parse,
                       'login': request.session['login']})
    elif request.method == 'POST':
        print(request.FILES.getlist('file'))  # Получаем загруженный файл
        user = Users.objects.filter(user_name=request.session.get('login'))[0]
        my_add_new_image = MemIntermediate.objects.filter(
            id_user=user)  # Список картинок, которые загрузил на сайт конкретный пользователь

        files = request.FILES.getlist('file')
        for i in files:  # Записываем новые (загруженные) мемы в базу (в промежуточную таюлицу)
            MemIntermediate.objects.create(url_image=i,
                                           id_user=Users.objects.filter(user_name=request.session.get('login'))[0])
        message_list = Massege.objects.filter(date_time_massege__gt=datetime.datetime.fromtimestamp(
            int(request.session.get('datetime') - 3600)))  # Список сообщений для чата
        role = user.id_name_role.name_roles
        return render(request, 'add_new.html',
                      {'my_add_new_image': my_add_new_image, 'role': role, 'message_list': message_list,
                       'login': request.session['login']})


# Базовое представление
def base(request):
    if request.session.get('login'):
        return func_display(request)
    else:
        mems = Memasik.objects.order_by('-date_mem')[:4]  # Берём из базы 4 самых свежих картинки
        data = []
        for i in mems:
            date_mem = int(time.mktime((i.date_mem).timetuple()))  # Перевод времени в секунды
            tags_list = Memasik.objects.filter(id=i.id)[0].tags
            obj = {
                'id': i.id,
                'url_image': i.url_image,
                'date_mem': date_mem,
                'tags': tags_list
            }
            print(tags_list)

            data.append(obj)
        print(data)
        return render(request, 'base.html', {'images': data})


# Функция регистрации
def registration(request):
    if request.method == 'GET':
        return render(request, 'registration.html')  # Переход к форме регистрации
    elif request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            new_user = Users.objects.filter(
                user_name=data.get('login'))  # Поиск пользователя в базе с введённым логином
            """
            Если такой логин есть в базе, 
            то происходит вывод сообщения, 
            что такой пользователь зарегистрирован
            """
            if new_user:
                message = "Пользоватедь с таким логином уже зарегистрирован"
                return render(request, 'registration.html', {'message': message})
            else:  # Если такого логина в базе нет, то создается новый пользователь
                my_user = Users.objects.create(user_name=data.get('login'),
                                               user_password=data.get('password'),
                                               email=data.get('email'),
                                               date=data.get('date'),
                                               id_name_role=Roles.objects.filter(name_roles='custom')[0])
                print(my_user)
                request.session['login'] = my_user.user_name  # Создаётся сессия
                request.session['datetime'] = time.mktime((datetime.datetime.now()).timetuple())
                return redirect('base')  # Переход на главную страницу
        else:
            message_valid = 'Введены не корректные данные'
            return render(request, 'registration.html', {'message': message_valid})


# Выход из сайта
def logout(request):
    del request.session['login']  # Удаляем сессию
    del request.session['datetime']  # Удаляем сессию
    return redirect('base')


# Вход на сайт для зарегестрированных пользлвателей
def login_user(request):
    if request.method == "GET":
        return redirect('base')

    elif request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():  # Проверяем валидна ли форма
            data = form.cleaned_data
            print(data)
            # Ищем в базе пользователя с введённым логином и паролем
            user = Users.objects.filter(user_name=data.get('login'), user_password=data.get('password')).first()
            print(user)
            if user:
                # Если такой пользователь есть, то создаём сессию и показываем главную страницу
                print(time.mktime((datetime.datetime.now()).timetuple()))
                request.session['login'] = user.user_name
                request.session['datetime'] = time.mktime((datetime.datetime.now()).timetuple())
                print(request.session.get('login'))
                return redirect('base')

        return redirect('base')


#   Функция для галлереи
def gallery(request):
    if request.method == 'GET':  # вход в галлерею
        name = request.session.get('login')
        user = Users.objects.filter(user_name=name)[0]
        print(user)
        gal = MyGallery.objects.filter(id_user=user)

        my_image = []  # Список картинок пользователя
        for index in gal:
            my_image.append(index.id_mem)
        print(my_image)
        message_list = Massege.objects.filter(date_time_massege__gt=datetime.datetime.fromtimestamp(
            int(request.session.get('datetime') - 3600)))  # Список сообщений для чата

        message_list_parse = []
        for i in message_list:
            dat = int(time.mktime((i.date_time_massege).timetuple()))
            t = datetime.datetime.utcfromtimestamp(dat).strftime('%d-%m-%Y %H:%M')
            obj = {
                'id': i.id,
                'massege': i.massege,
                'date_time_massege': t,
                'user': i.user
            }
            message_list_parse.append(obj)

        return render(request, 'gallery.html',
                      {'gallery': my_image, 'message_list': message_list_parse, 'login': request.session['login']})
    elif request.method == 'POST':  # Добавление картинки к себе в галлерею
        form = GalleryForm(request.POST)
        print(request.POST.get('mem_id'))
        if form.is_valid():
            # Добаавляем картинку в галлерею
            g = MyGallery.objects.create(id_mem=Memasik.objects.filter(id=request.POST.get('mem_id'))[0],
                                         id_user=Users.objects.filter(user_name=request.session.get('login'))[0])
            g.save()

            name = request.session.get('login')
            user = Users.objects.filter(user_name=name)[0]
            print(user)
            gal = MyGallery.objects.filter(id_user=user)

            my_image = []  # Список картинок пользователя
            for index in gal:
                my_image.append(index.id_mem)
            print(my_image)
            message_list = Massege.objects.filter(date_time_massege__gt=datetime.datetime.fromtimestamp(
                int(request.session.get('datetime') - 3600)))  # Список сообщений для чата

            message_list_parse = []
            for i in message_list:
                dat = int(time.mktime((i.date_time_massege).timetuple()))
                t = datetime.datetime.utcfromtimestamp(dat).strftime('%d-%m-%Y %H:%M')
                obj = {
                    'id': i.id,
                    'massege': i.massege,
                    'date_time_massege': t,
                    'user': i.user
                }
                message_list_parse.append(obj)

            return render(request, 'gallery.html',
                          {'gallery': my_image, 'message_list': message_list_parse, 'login': request.session['login']})

        else:
            return redirect('base')


# функция удаления картинок, из промежуточной таблицы
def delete_new(request):
    if request.method == 'GET':
        MemIntermediate.objects.filter(id=request.GET.get('mem_id')).delete()  # Удаляется выбраная картинка
    return redirect('upload')


# функция удаления картинок, из галереи
def delete_gallery(request):
    if request.method == 'GET':
        print(request.GET.get('mem_id'))
        MyGallery.objects.filter(id_mem=Memasik.objects.filter(id=request.GET.get('mem_id'))[0]).delete()
    return redirect('gallery')


# Функция добавления картинок из промежуточной таблиццы на сайт, с добавлением тегов
def add_mem_admin(request):
    if request.method == 'POST':
        print(request.POST.get('tags'))
        l = request.POST.get('tags').split(' ')  # список тегов
        print(request.POST.get('url_image'))
        tag_all = Tags.objects.all()
        tag_all_list = []
        for i in tag_all:
            tag_all_list.append(i.name_tag)
        print(tag_all_list)

        for i in l:
            # Проверка, есть ли такой тег в таблице, если нет, то добавить
            if i in tag_all_list:
                continue
            else:
                tag = Tags.objects.create(name_tag=i)
                tag.save()
        # Берём url из промежуточной таблицы и записываем его в главную
        url = MemIntermediate.objects.filter(id=request.POST.get('mem_id'))[0].url_image
        print(url)
        Memasik.objects.create(url_image=url,
                               tags=request.POST.get('tags'), date_mem=datetime.datetime.now())
        MemIntermediate.objects.filter(id=request.POST.get(
            'mem_id')).delete()  # удаляем из промежуточной таблицы картинку, которую добавили в главную
        return redirect('upload')


# Функция динамической подгрузки мемов
def dynamicImageLoad(request):
    if request.method == 'POST':
        print(request.POST.get('lastImage'))
        last_image = request.POST.get('lastImage')  # получаем дату последнего мема
        k = datetime.datetime.fromtimestamp(int(last_image))  # парсим дату

        more_image = Memasik.objects.filter(date_mem__lt=k).order_by('-date_mem').values('id', 'url_image', 'date_mem')[
                     :4]  # 4 картинки дата которых старше чем полученная из шаблона

        if not more_image:
            return JsonResponse({'data': False})
        data = []

        for i in more_image: #если такие картинки есть, то проходим по ним цикле
            date_mem = int(time.mktime((i['date_mem']).timetuple()))  # парсим дату
            tags_list = Memasik.objects.filter(id=i['id'])[0].tags
            obj = {
                'id': i['id'],
                'url_image': i['url_image'],
                'date_mem': date_mem,
                'tags': tags_list,
            }
            print(obj['date_mem'], obj['url_image'])
            print(tags_list)
            data.append(obj)
        data[-1]['last_image'] = True #Последнему добавляем атрибут last_image, нужно для отображениия в шаблоне

        return JsonResponse({'data': data})

#Функция для управления чатом (динамическая)
def chat(request):
    if request.method == "GET":
        id_last_message = request.GET.get('mass')  # id последнего сообщения
        # Берём все сообщения после последнего
        if id_last_message:
            message_list = Massege.objects.filter(id__gt=id_last_message).values('id', 'massege', 'user',
                                                                                 'date_time_massege')

            if not message_list:
                return JsonResponse({'data': False})
            data = []

            for i in message_list:
                date_time_massege = int(time.mktime((i['date_time_massege']).timetuple()))
                t = datetime.datetime.utcfromtimestamp(date_time_massege).strftime('%d-%m-%Y %H:%M')
                obj = {
                    'id': i['id'],
                    'massege': i['massege'],
                    'user': Users.objects.filter(id=i['user'])[0].user_name,
                    'date_time_massege': t
                }

                data.append(obj)
            data[-1]['last-message'] = True

            return JsonResponse({'data': data})
        else:
            return JsonResponse({'data': False})


    elif request.method == "POST":
        text_message = request.POST.get('message')
        print(Users.objects.filter(user_name=request.session.get('login')))
        if text_message:
            Massege.objects.create(massege=text_message,
                                   date_time_massege=datetime.datetime.now(),
                                   user=Users.objects.filter(user_name=request.session.get('login'))[0])


            return JsonResponse({'data': text_message})
        else:
            return JsonResponse({'data': text_message})

#Функция для изменения ролей рользователей
def add_admin(request):
    if request.method == "GET":
        users_all = Users.objects.order_by('user_name').all()  # Список всех пользователей отсартированный по алфавиту
        roles_all = Roles.objects.all()  # Список ролей
        message_list = Massege.objects.filter(date_time_massege__gt=datetime.datetime.fromtimestamp(
            int(request.session.get('datetime') - 3600)))  # Список сообщений для чата

        message_list_parse = []
        for i in message_list:
            dat = int(time.mktime((i.date_time_massege).timetuple()))
            t = datetime.datetime.utcfromtimestamp(dat).strftime('%d-%m-%Y %H:%M')
            obj = {
                'id': i.id,
                'massege': i.massege,
                'date_time_massege': t,
                'user': i.user
            }
            message_list_parse.append(obj)
        return render(request, 'add_admin.html',
                      {'login': request.session['login'], 'users': users_all, 'roles': roles_all,
                       'message_list': message_list_parse})
    elif request.method == 'POST':
        user = request.POST.get('user_name')
        role = request.POST.get('role')
        role_user = Users.objects.filter(user_name=user).first()
        print(Roles.objects.filter(name_roles=role_user.id_name_role.name_roles)[0])
        # Если роль пользователя отличается от введённой в форме, то изменяем её
        if role != role_user.id_name_role.name_roles:
            role_user.id_name_role = Roles.objects.filter(name_roles=role)[0]
            role_user.save()
        return redirect('add_admin')

#Функция удаления картинок с главной страницы (доступна только для админа)
def delete(request):
    if request.method == 'POST':
        print(request.POST.get('mem_id'))
        Memasik.objects.filter(id=request.POST.get('mem_id')).delete()
        print(request.POST.get('mem_id'))

    return redirect('base')

#Функция для отображения мемов по категориям
def select_category(request):
    if request.method == "GET":
        tag = request.GET.get('tags') #Получаем выбранный тег

        if tag == 'Категории': # Для вывода всех картинок
            return redirect('base')

        mem_all = Memasik.objects.all()

        mem_select_tag = [] #Список мемов у которых есть тег выбранный в шаблоне
        for i in mem_all:
            tag_list = i.tags
            if tag in tag_list:
                mem_select_tag.append(i)

        if not mem_select_tag: # Для картинок, которые без тегов
            mem_select_tag = Memasik.objects.filter(tags='')


        user = Users.objects.filter(user_name=request.session.get('login'))
        role = user[0].id_name_role.name_roles
        message_list = Massege.objects.filter(date_time_massege__gt=datetime.datetime.fromtimestamp(
            int(request.session.get('datetime', 0) - 3600)))  # Список сообщений для чата

        all_tags = Tags.objects.all()
        k = []
        for i in message_list:
            dat = int(time.mktime((i.date_time_massege).timetuple()))
            t = datetime.datetime.utcfromtimestamp(dat).strftime('%d-%m-%Y %H:%M')
            obj = {
                'id': i.id,
                'massege': i.massege,
                'date_time_massege': t,
                'user': i.user
            }
            k.append(obj)
        return render(request, 'test.html',
                      {'images': mem_select_tag, 'role': role, 'message_list': k, 'login': request.session['login'],
                       'tags': all_tags})
