"""
{% extends "base.html" %}

{% block registration %}
<p>Hello world</p>
{% endblock %}

{% block main %}


<div class="row allimages">
    {% for i in images %}
        {% if forloop.last %}
            <div class="card images last-image" style="width: 100%;" data-imageid="{{i.id}}">
        {% else %}
             <div class="card images" style="width: 100%;">
        {% endif %}
          <img src="{{ i.url_image.url }}" class="card-img-top" alt="...">
          <div class="card-body">
            <h5 class="card-title">Картинка</h5>
            <a href="#" class="btn btn-primary">Добавить</a>
          </div>
            </div>
    {% endfor %}
</div>

{% if images.count >= 3 %}
    <p class="text-center mt-2"><button class="btn btn-success load-more" id="load-more">Хочу еще мамасиков</button></p>
{% endif %}

{% endblock %}


{% block context %}
<script>
    $('load-more).on('click',function () {
        let lastImageId = $('.last-image').attr('data-imageid')
        let data = {
            lastImageId: lastImageId
        }
        $('.images').removeClass('last-image')
        $('.images').removeAttr('data-imageid')
        $.ajax({
            method: "GET",
            dataType: "json",
            data: data,
            url: '{% url "load-more-image" %}',
            success: function (data){
                console.log(data)
                let result = data['data']
                if(!result){
                    $('.load-more').css('display', 'none')
                } else {
                    $.each(result, function(key, obj){
                        if(obj[last_images']){
                            $('.allimages').append(
                            '<div class="card images last-image" style="width: 100%;" data-imageid="{{i.id}} + '">' +
                            '<img src="{{ i.url_image.url }}" class="card-img-top" alt="...">' +
                            '<div class="card-body">' +
                            '<h5 class="card-title">Картинка</h5>' +
                            '<a href="#" class="btn btn-primary">Добавить</a>' +
                            '</div>'+
                            '</div>')
                        } else {
                            $('.allimages').append(
                            '<div class="card images " style="width: 100%;">' +
                            '<img src="{{ i.url_image.url }}" class="card-img-top" alt="...">' +
                            '<div class="card-body">' +
                            '<h5 class="card-title">Картинка</h5>' +
                            '<a href="#" class="btn btn-primary">Добавить</a>' +
                            '</div>'+
                            '</div>'
                            )
                        }

                    })

            }
        })
    })
</script>
{% endblock %}


{% block left %}
<br>
<br>
<br>
<a href="{% url 'gallery' %}" class="btn btn-primary btn-lm">Мои мемы</a><br>
<br>
<form method="POST" action="{% url 'logout' %}" class="row g-3" novalidate>
    {% csrf_token %}
    <button type="submit" class="btn btn-primary">Выйти</button>
    <br>
</form>


<form method="POST" action="{% url 'upload' %}" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn btn-primary btn-lm">Добавить новые</button>
    <br>
</form>
<br>
{% if role == "admin" %}
    <a href="{% url 'add_new' %}" class="btn btn-primary btn-lm">Просмотреть добавленые другими пользователями</a><br>
    <br>
    <a href="#" class="btn btn-primary btn-lm">Добавить админа</a><br>
{% endif %}
<a href="{% url 'login_user' %}" class="btn btn-primary btn-lm">Назад</a><br>


{% endblock %}



def dynamicImageLoad(request):
    if request.method == 'GET':
        last_image_id = request.GET.get('lastImageId')
        more_image = Memasik.objects.filter(pk__gt=int(last_image_id)).values('id', 'url_image')[:3]
        if not more_image:
            return JsonResponse({'data': False})
        data = []

        for i in more_image:
            obj = {
                'id': i['id'],
                'url_imagee': i['url_image']
            }
            data.append(obj)
        data[-1]['last_image'] = True
        return JsonResponse({'data': data})



<form>
                    <div id="s">
                        <button class="btn btn-outline-info style-button2" type="submit" >OK</button>
                    </div>
                    <div  id="o">
                        <select class="btn btn-outline-info style-button">
                            <option selected>Категории</option>
                            {% for i in tags %}
                                <option value="{{i.name_tag}}">{{i.name_tag}}</option>

                            {% endfor %}

                        </select>
                    </div>


                </form>







#скролл
<script type="text/javascript">
    $(document).ready(function(){

        /* Переменная-флаг для отслеживания того, происходит ли в данный момент ajax-запрос. В самом начале даем ей значение false, т.е. запрос не в процессе выполнения */
        var inProgress = false;
        /* С какой статьи надо делать выборку из базы при ajax-запросе */
        var startFrom = 10;

            /* Используйте вариант $('#more').click(function() для того, чтобы дать пользователю возможность управлять процессом, кликая по кнопке "Дальше" под блоком статей (см. файл index.php) */
            $(window).scroll(function() {

                /* Если высота окна + высота прокрутки больше или равны высоте всего документа и ajax-запрос в настоящий момент не выполняется, то запускаем ajax-запрос */
                if($(window).scrollTop() + $(window).height() >= $(document).height() - 200 && !inProgress) {

                $.ajax({
                    /* адрес файла-обработчика запроса */
                    url: '{% url "load-more-image" %}',
                    /* метод отправки данных */
                    method: 'POST',
                    /* данные, которые мы передаем в файл-обработчик */
                    data: {"startFrom" : startFrom},
                    /* что нужно сделать до отправки запрса */
                    beforeSend: function() {
                    /* меняем значение флага на true, т.е. запрос сейчас в процессе выполнения */
                    inProgress = true;}
                    /* что нужно сделать по факту выполнения запроса */
                    }).done(function(data){

                    /* Преобразуем результат, пришедший от обработчика - преобразуем json-строку обратно в массив */
                    data = jQuery.parseJSON(data);

                    /* Если массив не пуст (т.е. статьи там есть) */
                    if (data.length > 0) {

                    /* Делаем проход по каждому результату, оказвашемуся в массиве,
                    где в index попадает индекс текущего элемента массива, а в data - сама статья */
                    $.each(data, function(index, data){

                    /* Отбираем по идентификатору блок со статьями и дозаполняем его новыми данными */
                    $("#articles").append("<p><b>" + data.title + "</b><br />" + data.text + "</p>");
                    });

                    /* По факту окончания запроса снова меняем значение флага на false */
                    inProgress = false;
                    // Увеличиваем на 10 порядковый номер статьи, с которой надо начинать выборку из базы
                    startFrom += 10;
                    }});
                }
            });
        });



</script>


#кнопка
<script type="text/javascript">
    $('#load-more').on('click', function () {
        let lastImage = $('.last-image').attr('image-data')
        console.log(lastImage)
        let data = {
            lastImage: lastImage
        }
        $('.images').removeClass('last-image')
        $('.images').removeAttr('image-data')
        $.ajax({
            method: "GET",
            dataType: "json",
            data: data,
            url: '{% url "load-more-image" %}',
            success: function (data){
                console.log(data)
                let result = data['data']
                console.log(data)
                console.log('*****')
                console.log(result)
                if(!result){
                    $('.load-more').css('display', 'none')
                } else {
                    $.each(result, function(key, obj){
                    console.log(key, obj)
                    console.log(obj)
                    console.log(obj['last_image'])
                     if(obj['last_image']){
                        $('.allimages').append(
                            '<div class="images last-image" style="width: 49%;" image-data="' + obj['date_mem'] + '">' +
                            '<div class="div-img-top">'+
                            '<img src="media/' + obj['url_image'] + '" id="div-img-top">' +
                            '</div>'+
                            '<div class="img-body">' +
                            '<h5 class="img-title">' + obj['tags'] + '</h5>' +
                            '<div class="form1">'+
                            '<form method="POST" action="{% url 'gallery' %}">' +
                            '<input type="hidden" name="mem_id" value="' + obj['id'] + '">' +
                            '<input class="btn btn-outline-secondary" type="submit" id="button-add" value="Добавить">' +
                            '</form>' +
                            '</div>'+
                            '{% if role == "admin" %}' +
                                '<div class="form2">'+
                                '<form method="POST" action="{% url 'delete' %}">' +
                                    '<input type="hidden" name="mem_id" value="' + obj['id'] + '">' +
                                    '<input class="btn btn-dark" type="submit" value="Удалить">' +
                                '</form>' +
                                '</div>' +
                            '{% endif %}' +
                            '</div>'+
                            '</div>')
                            console.log(obj['url_image'] )
                     } else {
                       $('.allimages').append(
                            '<div class="images " style="width: 49%;">' +
                            '<div class="div-img-top">'+
                            '<img src="media/' + obj['url_image'] + '" id="div-img-top">' +
                            '</div>'+
                            '<div class="img-body">' +
                            '<h5 class="img-title">' + obj['tags'] + '</h5>' +
                            '<form method="POST" action="{% url 'gallery' %}">' +
                            '<div class="form1">'+
                            '<input type="hidden" name="mem_id" value="' + obj['id'] + '">' +
                            '<input class="btn btn-outline-secondary" id= "button-add" type="submit" value="Добавить">' +
                            '</form>' +
                            '</div>'+
                            '{% if role == "admin" %}' +
                            '<div class="form2">'+
                                '<form method="POST" action="{% url 'delete' %}">' +
                                    '<input type="hidden" name="mem_id" value="' + obj['id'] + '">' +
                                    '<input class="btn btn-dark" type="submit" value="Удалить">' +
                                '</form>' +
                            '</div>'+
                            '{% endif %}' +
                            '</div>'+
                            '</div>')
                            console.log(obj['url_image'] )
                     }

                    })
                }

            }
        })
    })
</script>

"""