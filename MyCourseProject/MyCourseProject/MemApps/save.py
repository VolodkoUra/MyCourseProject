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














"""