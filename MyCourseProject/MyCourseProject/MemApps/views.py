from django.shortcuts import render, redirect
from .models import Users, Memasik, MyGallery, Roles, Tags
from .form import LoginForm, RegistrationForm, ImageForm, GalleryForm, MemIntermediate, ImageFormMain
from datetime import datetime
from django.contrib.auth import authenticate, login
from django.views.generic import ListView


def func_display(r):  # Функция для вывода картинок на дисплей
    mems = Memasik.objects.all()
    for i in mems:
        print(i.id, i.url_image)
    print('!!!!!!!!!')
    print('DISPLAY')
    user = Users.objects.filter(user_name=r.session.get('login'))
    role = user[0].id_name_role.name_roles

    return render(r, 'index.html', {'images': mems, 'role': role})

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
            mems = Memasik.objects.all() #Вывод всех картинок
            #print(mems[0].url_image.url)
            return render(request, 'index.html', {'form': form, 'images': mems})
        else:
            form = ImageForm()
            print("No VAlid")
            print(form)

        return render(request, 'index.html', {'form': form})


def base(request):
    if request.session.get('login'):
        return func_display(request)
    else:
        return render(request, 'base.html')

#Функция регистрации
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
                                              date=data.get('date'))
                print(my_user)
                request.session['login'] = my_user.user_name
                return render(request, 'index.html', {'data': data})
        return render(request, 'registration.html')


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
        return render(request, 'gallery.html')
    elif request.method == 'POST':     # Добавление картинки к себе в галлерею
        form = GalleryForm(request.POST)
        print(request.POST.get('mem_id'))
        print(request.POST)
        if form.is_valid():
            print(MemIntermediate.objects.filter(id=request.POST.get('mem_id'))[0])
            print("===============")
            print(MemIntermediate.objects.filter(id=request.POST.get('mem_id'))[0], Users.objects.filter(user_name=request.session.get('login'))[0])

            g = MyGallery.objects.create(id_mem=MemIntermediate.objects.filter(id=request.POST.get('mem_id'))[0],
                                       id_user= Users.objects.filter(user_name=request.session.get('login'))[0])
            g.save()
            gallery_all = MyGallery.objects.all()
            print(gallery_all)

            return render(request, 'gallery.html', {'gallery': gallery_all})
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


def add_mem_admin(request):
    if request.method == 'POST':
        print(request.POST.get('tags'))
        print(type(request.POST.get('tags')))
        l = request.POST.get('tags').split(' ') # список тегов
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


        for i in l:
            tag = Tags.objects.create(name_tag=i)
            tag.save()
        #????? как передать ссылку из таблицы MemIntermediate в Memasik
        mem = Memasik.objects.create(url_image=MemIntermediate.objects.filter(id=request.POST.get('mem_id')),
                                     tags=request.method.POST.get('tags'), date_mem=datetime.now())
        return redirect('add_new')

    elif request.method == 'GET':
        print('GET')
        return redirect('add_new')
    else:
        print('OTHER')
        return redirect('add_new')
