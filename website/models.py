from django.db import models


# Create your models here.

class Controller(models.Model):
    hostname = models.CharField(max_length=45, unique=True)
    ip = models.CharField(max_length=15, unique=True)
    status = models.BooleanField(default=False)
    temp = models.CharField(max_length=10)
    humidity = models.CharField(max_length=10)
    power = models.CharField(max_length=10)


class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, unique=True)


class Devices(models.Model):
    name = models.CharField(max_length=45, unique=True)


class Model(models.Model):
    name = models.CharField(max_length=45, unique=True)
    devID = models.ForeignKey(Devices, on_delete=models.CASCADE)


class Network_devices(models.Model):
    ser_num = models.CharField(primary_key=True, max_length=20)
    hostname = models.CharField(max_length=255, unique=True)
    con_id = models.ForeignKey(Controller, on_delete=models.CASCADE)
    devID = models.ForeignKey(Devices, on_delete=models.CASCADE)
    modID = models.ForeignKey(Model, on_delete=models.CASCADE)


class Detail(models.Model):
    ser_num = models.OneToOneField(
        Network_devices,
        on_delete=models.CASCADE,
        primary_key=True,
        max_length=20
    )
    status = models.CharField(max_length=10)
    manufacturer = models.CharField(max_length=25)
    up_time = models.CharField(max_length=25)
    interface_using = models.CharField(max_length=255)
    sw_image = models.CharField(max_length=25)
    sw_version = models.CharField(max_length=25)
    last_reset = models.CharField(max_length=15)
    fan = models.CharField(max_length=5)
    temp = models.CharField(max_length=5)
    power = models.CharField(max_length=5)
    ip = models.CharField(max_length=15)
    serial_port = models.CharField(max_length=10)


class Base_template(models.Model):
    name = models.CharField(max_length=45)
    create_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255)
    upload = models.FileField(blank=True, null=True)
    modID = models.ForeignKey(Model, on_delete=models.CASCADE)


class Management(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    ser_num = models.ForeignKey(Network_devices, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    desc = models.CharField(max_length=255)