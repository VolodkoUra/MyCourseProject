from django.shortcuts import render, redirect
from .models import Users, Memasik, MyGallery, Roles, Tags, Massege
from .form import LoginForm, RegistrationForm, ImageForm, GalleryForm, MemIntermediate, ImageFormMain
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.views.generic import ListView
import time, datetime
from django.http import HttpResponse


def func_display(r):  # Функция для вывода картинок на дисплей
    mems = Memasik.objects.order_by('-date_mem')[:3]
    # mems = Memasik.objects.all()[:3]
    data = []
    for i in mems:
        print(i.id, i.url_image, i.date_mem, type(i.date_mem))
        date_mem = int(time.mktime((i.date_mem).timetuple()))
        obj = {
            'id': i.id,
            'url_image': i.url_image,
            'date_mem': date_mem
        }

        data.append(obj)
    print(data)
    print(len(data))
    print('!!!!!!!!!')
    print('DISPLAY')
    user = Users.objects.filter(user_name=r.session.get('login'))
    role = user[0].id_name_role.name_roles
    message_list = Massege.objects.all()
    return render(r, 'test.html', {'images': data, 'role': role, 'message_list': message_list})


# функция загрузки картинок с локального компьютера на сайт
def model_form_upload(request):
    if request.method == 'POST':
        print("1")
        form = ImageForm(request.POST, request.FILES)
        print(form)
        print(request.FILES)
        print("2")
        if form.is_valid():
            print("3")
            form.save()
            print("44")
            mems = Memasik.objects.order_by('-date_mem')[:3]  # Вывод всех картинок
            # mems = Memasik.objects.all()[:3]
            data = []
            for i in mems:
                print(i.id, i.url_image, i.date_mem, type(i.date_mem))
                date_mem = int(time.mktime((i.date_mem).timetuple()))
                obj = {
                    'id': i.id,
                    'url_image': i.url_image,
                    'date_mem': date_mem
                }

                data.append(obj)
            # print(mems[0].url_image.url)
            message_list = Massege.objects.all()
            return render(request, 'test.html', {'form': form, 'images': data, 'message_list': message_list})
        else:
            form = ImageForm()
            print("No VAlid")
            print(form)

        return render(request, 'test.html', {'form': form})


def base(request):
    if request.session.get('login'):
        return func_display(request)
    else:
        return render(request, 'base.html')


# Функция регистрации
def registration(request):
    if request.method == 'GET':
        return render(request, 'registration.html')
    elif request.method == 'POST':
        form = RegistrationForm(request.POST)
        print(form)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            new_user = Users.objects.filter(user_name=data.get('login'))
            if new_user:
                print('1')
                return redirect('base')
            else:
                print('2')
                my_user = Users.objects.create(user_name=data.get('login'),
                                               user_password=data.get('password'),
                                               email=data.get('email'),
                                               date=data.get('date'),
                                               id_name_role=Roles.objects.filter(name_roles='custom')[0])
                print(my_user)
                request.session['login'] = my_user.user_name
                return redirect('base')
                # return render(request, 'test.html', {'data': data})
        # return render(request, 'registration.html')


# Выход из сайта
def logout(request):
    print(request.session.get('login'))

    del request.session['login']
    print(request.session.get('login'))

    return redirect('base')


# Вход на сайт для зарегестрированных пользлвателей
def login_user(request):
    if request.method == "GET":
        if request.session.get('login'):
            return func_display(request)
        else:
            return render(request, 'base.html')

    if request.method == "POST":
        form = LoginForm(request.POST)
        print('1')
        print(form)
        if form.is_valid():
            print('2')
            data = form.cleaned_data
            print(data)

            user = Users.objects.filter(user_name=data.get('login', ''), user_password=data.get('password', '')).first()
            print(user)
            if user:
                print(request.session.get('login'))
                request.session['login'] = user.user_name
                print(request.session.get('login'))
                return func_display(request)
            else:
                return redirect('base')
        else:
            return redirect('base')


def gallery(request):
    if request.method == 'GET':
        name = request.session.get('login')
        user = Users.objects.filter(user_name=name)[0]
        print(user)
        gal = MyGallery.objects.filter(id_user=user)
        print(type(gal))
        k = []
        for index in gal:
            k.append(index.id_mem)
        print(k)

        return render(request, 'gallery.html', {'gallery': k})
    elif request.method == 'POST':  # Добавление картинки к себе в галлерею
        form = GalleryForm(request.POST)
        print(request.POST.get('mem_id'))
        print(request.POST)
        if form.is_valid():
            print(MemIntermediate.objects.filter(id=request.POST.get('mem_id'))[0])
            print("===============")
            print(MemIntermediate.objects.filter(id=request.POST.get('mem_id'))[0],
                  Users.objects.filter(user_name=request.session.get('login'))[0])

            g = MyGallery.objects.create(id_mem=Memasik.objects.filter(id=request.POST.get('mem_id'))[0],
                                         id_user=Users.objects.filter(user_name=request.session.get('login'))[0])
            g.save()

            name = request.session.get('login')
            user = Users.objects.filter(user_name=name)[0]
            print(user)
            gal = MyGallery.objects.filter(id_user=user)
            print(type(gal))
            k = []
            for index in gal:
                k.append(index.id_mem)
            print(k)

            return render(request, 'gallery.html', {'gallery': k})
        else:
            print('NO')
            return render(request, 'base.html')


# сделать эту функцию доступной только для админа ?
# меню админа, здесь он просмтаривает все добавленые картинки, и решает,что с ними делать
def add_new(request):
    mems = MemIntermediate.objects.all()
    for i in mems:
        print(i.id, i.url_image.url)
    print('!!!!!!!!!')
    return render(request, 'add_new.html', {'images': mems})


# функция удаления картинок, админом
def delete_new(request):
    if request.method == 'POST':
        MemIntermediate.objects.filter(id=request.POST.get('mem_id')).delete()
        print(request.POST.get('mem_id'))
        mems = MemIntermediate.objects.all()
        print(mems)
    return redirect('add_new')


# функция удаления картинок, из галереи
def delete_gallery(request):
    if request.method == 'POST':
        print(request.POST.get('mem_id'))
        MyGallery.objects.filter(id_mem=Memasik.objects.filter(id=request.POST.get('mem_id'))[0]).delete()
        print(request.POST.get('mem_id'))
        mems = MemIntermediate.objects.all()
        print(mems)
    return redirect('gallery')


def add_mem_admin(request):
    if request.method == 'POST':
        print(request.POST.get('tags'))
        print(type(request.POST.get('tags')))
        l = request.POST.get('tags').split(' ')  # список тегов
        print(l)

        print("1")
        form = ImageFormMain(request.POST, request.FILES)
        print(form)
        print(request.FILES)
        print("2")

        print(request.POST.get('url_image'))

        """if form.is_valid():
            print("3")
            form.save()
            print("4")"""

        tag_all = Tags.objects.all()
        tag_all_list = []
        for i in tag_all:
            tag_all_list.append(i.name_tag)
        print(tag_all_list)

        for i in l:
            # Сделать проверку, есть ли такой тег в таьлице, если нет, то добавить
            if i in tag_all_list:
                continue
            else:
                tag = Tags.objects.create(name_tag=i)
                tag.save()
        url = MemIntermediate.objects.filter(id=request.POST.get('mem_id'))[0].url_image
        print(url)

        Memasik.objects.create(url_image=url,
                               tags=request.POST.get('tags'), date_mem=datetime.now())
        MemIntermediate.objects.filter(id=request.POST.get('mem_id')).delete()
        return redirect('add_new')

    elif request.method == 'GET':
        print('GET')
        return redirect('add_new')
    else:
        print('OTHER')
        return redirect('add_new')


def dynamicImageLoad(request):
    if request.method == 'GET':
        print('oooooooooooo')
        last_image = request.GET.get('lastImage')
        print(last_image, type(last_image))
        # last_image = date_parse(last_image)
        # resultDate= datetime(*last_image)
        print('--------------------')
        # print(resultDate, type(last_image))
        k = datetime.datetime.fromtimestamp(int(last_image))
        print(k)
        # more_image = Memasik.objects.values('id', 'url_image')[:3]

        more_image = Memasik.objects.filter(date_mem__lt=k).order_by('-date_mem').values('id', 'url_image', 'date_mem')[
                     :3]
        print(Memasik.objects.all())
        print("-----")
        print(Memasik.objects.values('id', 'url_image', 'date_mem'))
        print("-----")
        print(Memasik.objects.filter(date_mem__lt=k).values('id', 'url_image', 'date_mem'))
        print("-----")
        print(Memasik.objects.filter(date_mem__gt=k).values('id', 'url_image', 'date_mem'))
        print('******')
        print(more_image)
        if not more_image:
            return JsonResponse({'data': False})
        data = []

        for i in more_image:
            date_mem = int(time.mktime((i['date_mem']).timetuple()))
            obj = {
                'id': i['id'],
                'url_image': i['url_image'],
                'date_mem': date_mem
            }
            print(obj['date_mem'], obj['url_image'])
            data.append(obj)
        data[-1]['last_image'] = True

        return JsonResponse({'data': data})


def chat(request):
    if request.method == "GET":

        id_last_message = int(request.GET.get('mass'))
        print(id_last_message, type(id_last_message))

        message_list = Massege.objects.filter(id__gt=id_last_message).values('id', 'massege', 'user',
                                                                             'date_time_massege')
        print('++++++++++++++++')
        print('!!!!!', message_list, "!!!!!")
        print('++++++++++++++++')
        if not message_list:
            return JsonResponse({'data': False})
        data = []

        for i in message_list:
            print(i)
            # date_mem = int(time.mktime((i['date_mem']).timetuple()))
            obj = {
                'id': i['id'],
                'massege': i['massege'],
                'user': Users.objects.filter(id=i['user'])[0].user_name,
                'date_time_massege': i['date_time_massege']
            }
            print(obj)
            data.append(obj)
        data[-1]['last-message'] = True
        # id_last_message = Massege.objects.order_by('-id')[0].id
        # print(id_last_message, type(id_last_message))

        return JsonResponse({'data': data})
        return render(request, 'test.html', {'data': data})
    elif request.method == "POST":
        print(request.session.get('login'), request.POST.get('message'))
        text_message = request.POST.get('message')
        print(Users.objects.filter(user_name=request.session.get('login')))

        if text_message:
            Massege.objects.create(massege=text_message,
                                   date_time_massege=datetime.datetime.now(),
                                   user=Users.objects.filter(user_name=request.session.get('login'))[0])

            # Что возвращать?
            message_list = Massege.objects.all()
            return render(request, 'test.html', {'message_list': message_list})
            return JsonResponse({'data': text_message})
        else:
            return JsonResponse({'data': text_message})
