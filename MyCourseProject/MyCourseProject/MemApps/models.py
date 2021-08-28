from django.db import models

class Roles(models.Model):
    name_roles = models.CharField(max_length=50)


class Users(models.Model):
    user_name = models.CharField(max_length=255)
    user_password = models.CharField(max_length=100)
    email = models.EmailField()
    date = models.DateField()
    id_name_role = models.ForeignKey(Roles, null=True, on_delete=models.PROTECT)


class Massege(models.Model):
    massege = models.TextField()
    date_time_massege = models.DateTimeField()
    user = models.ForeignKey(Users, on_delete=models.CASCADE)


# Промежуточная таблица для картинок, которые добавляют все пользователи
class MemIntermediate(models.Model):
    url_image = models.ImageField(null=True, blank=False, upload_to="download/", max_length=255)



class Memasik(models.Model):
    #url_image = models.ForeignKey(MemIntermediate, on_delete=models.DO_NOTHING)
    url_image = models.ImageField(null=True, blank=False, upload_to="download/", max_length=255)
    tags = models.CharField(max_length=255)
    date_mem = models.DateTimeField()
    # cat = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='memasik_category')


class MyGallery(models.Model):
    id_mem = models.ForeignKey(Memasik, on_delete=models.CASCADE)
    id_user = models.ForeignKey(Users, on_delete=models.CASCADE)


class Tags(models.Model):
    name_tag = models.CharField(max_length=50)


class MemTags(models.Model):
    id_mem = models.ForeignKey(Memasik, on_delete=models.CASCADE)
    id_tag = models.ForeignKey(Tags, on_delete=models.CASCADE)

