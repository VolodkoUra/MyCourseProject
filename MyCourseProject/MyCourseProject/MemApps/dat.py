from datetime import datetime
from time import time
import time, datetime


def dat(x):
    d = x.replace(',', '')

    c = d.split(' ')
    resultList = c[:-1]
    print(resultList)

    if resultList[0] == 'Jan.':
        resultList[0] = 1
    elif resultList[0] == 'Feb.':
        resultList[0] = 2
    elif resultList[0] == 'Mar.':
        resultList[0] = 3
    elif resultList[0] == 'Apr.':
        resultList[0] = 4
    elif resultList[0] == 'May':
        resultList[0] = 5
    elif resultList[0] == 'Jun.':
        resultList[0] = 6
    elif resultList[0] == 'Jul':
        resultList[0] = 7
    elif resultList[0] == 'Aug.':
        resultList[0] = 8
    elif resultList[0] == 'Sep.':
        resultList[0] = 9
    elif resultList[0] == 'Oct.':
        resultList[0] = 10
    elif resultList[0] == 'Nov.':
        resultList[0] = 11
    elif resultList[0] == 'Dec.':
        resultList[0] = 12

    year = int(resultList[2])
    mounth = resultList[0]
    day = int(resultList[1])

    timeList = resultList[-1].split(':')
    print(timeList)
    hourse = int(timeList[0])
    minutes = int(timeList[1])
    print(year, mounth, day, hourse, minutes)
    return year, mounth, day, hourse, minutes


def dat2():
    #result = datetime(2021, 11, 10, 21, 15)
    x = datetime.datetime.now()
    print(x, type(x))
    #r = datetime.time(x).total_secondss()
    #print(r)
    #print(time())
    s = int(time.mktime(x.timetuple()))
    print(s, type(s))
    k = datetime.datetime.fromtimestamp(s)
    print(k)


# dat('Aug. 29, 2021, 12:55 p.m.')
dat2()



"""
def chat(request):
    if request.method == "GET":
        print(request.GET.get('mass'))
        message_list = Massege.objects.filter(id__gt=request.GET.get('mass')).values('massege', 'user', 'date_time_massege')

        data = []

        for i in message_list:
            #date_mem = int(time.mktime((i['date_mem']).timetuple()))
            obj = {
                'massege': i['massege'],
                'user': i['user'].user_name,
                'date_time_massege': i['date_time_massege']
            }
            print(obj)
            data.append(obj)
        data[-1]['last_image'] = True


        return render(request, 'test.html', {'data': data} )
    elif request.method == "POST":
        print(request.session.get('login'), request.POST.get('message'))
        text_message = request.POST.get('message')
        print(Users.objects.filter(user_name=request.session.get('login')))

        if text_message:
            Massege.objects.create(massege=text_message,
                                   date_time_massege=datetime.datetime.now(),
                                   user=Users.objects.filter(user_name=request.session.get('login'))[0])
            return JsonResponse({'data': text_message})
        else:
            return JsonResponse({'data': text_message})



chat(request):
    if request.method == "GET":
        print(request.GET.get('mass'))
        message_list = Massege.objects.all()
        return render(request, 'test.html', {'message_list': message_list} )
    elif request.method == "POST":
        print(request.session.get('login'), request.POST.get('message'))
        text_message = request.POST.get('message')
        print(Users.objects.filter(user_name=request.session.get('login')))

        if text_message:
            Massege.objects.create(massege=text_message,
                                   date_time_massege=datetime.datetime.now(),
                                   user=Users.objects.filter(user_name=request.session.get('login'))[0])
            return JsonResponse({'data': text_message})
        else:
            return JsonResponse({'data': text_message})



<script type="text/javascript">
    function show()
    {
        var mass = $('.last-message').attr('message-id');
        console.log(mass);
        data = {
            'mass': mass
        }
        console.log(data);
        $('.images').removeClass('last-message')
        $('.images').removeAttr('message-id')
        console.log('remove');
        $.ajax({
            method: "GET",
            dataType: "json",
            data: data,
            url: '{% url 'chat' %}',
            cache: false,

            success: function(data){
                console.log('func')
                console.log(data)
                let result = data['data']
                console.log(data)
                console.log('*****')
                console.log(result)
                if(result){
                    $.each(result, function(key, obj){
                    console.log(key, obj)
                    console.log(obj)
                    console.log(obj['massege'])
                    if(obj['massege']){
                        $('.all-massege').append(
                            '<div class="messages last-message" message-id="' + obj['id'] + '">'+
                                '<p>YES</p>' +
                                '<p>' + obj['user'] + obj['massege'] + obj['date_time_massege'] + '</p>'
                            '</div>')

                    } else {
                        $('.all-massege').append(
                            '<div class="messages last-message" message-id="' + obj['id'] + '">'+
                                '<p>NO</p>' +
                                '<p>' + obj['user'] + obj['massege'] + obj['date_time_massege'] + '</p>'
                            '</div>')
                        }

                    })

                }

            }
        })
    }




    $(document).ready(function(){

        show();
        setInterval('show()',1000);
    });


</script>





"""

def testing():
    k=5
    l=8
    return k, l

def main():
    y = testing().l
    print(y)

main()


""" 
       print("1")
        form = ImageForm(request.POST, request.FILES)
        print(form)
        print(request.FILES)
        print(request.POST)
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

        return render(request, 'test.html', {'form': form})"""