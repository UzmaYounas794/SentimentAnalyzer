from django.shortcuts import render
import matplotlib

matplotlib.use("Agg")
from .sentiment import *
from .models import *
from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse


import numpy as np

# Create your views here.
def home(request):
    return render(request, "app/home.html")


def mobile_store(request):
    products = Product.objects.all()
    paginator = Paginator(products, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"products": page_obj}
    return render(request, "app/mobile.html", context)


def laptop_store(request):

    products = Laptops.objects.all()
    paginator = Paginator(products, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"products": page_obj}
    return render(request, "app/laptop.html", context)


def mobile_score(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        weights = get_score(product_id)
        li = weights[2]

        max_len = 40
        lik = []
        for ele in li:
            if len(ele) >= max_len:
                lik.append(ele)
        lit = lik[:4]
        weightage = round((weights[0] / len(weights[2])) * 5, 1)

    except Product.DoesNotExist:
        raise Http404("details not found.")

    return render(
        request,
        "app/MobileScore.html",
        {
            "product": product,
            "data": weightage,
            "review": lit,
            "t": weights[0],
            "f": weights[1],
        },
    )


def laptop_score(request, product_id):
    try:
        product = Laptops.objects.get(id=product_id)
        weights = get_score_laptop(product_id)
        li = weights[2]
        max_len = 40
        lik = []
        for ele in li:
            if len(str(ele)) >= max_len:
                lik.append(ele)
        lit = lik[:4]
        weightage = round((weights[0] / len(weights[2])) * 5, 1)

    except Product.DoesNotExist:
        raise Http404("details not found.")

    return render(
        request,
        "app/LaptopScore.html",
        {
            "product": product,
            "data": weightage,
            "review": lit,
            "t": weights[0],
            "f": weights[1],
        },
    )
