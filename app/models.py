from django.db import models
from tensorflow import keras


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


class Laptops(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


class loadModel:

    reconstructed_model = keras.models.load_model("my_model")

    def __str__(self):
        return self.reconstructed_model
