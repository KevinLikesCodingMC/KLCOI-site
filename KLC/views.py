from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from data import update_probs
from data import get_rd


def index(request):
    update_probs.update()
    con = {"probs": get_rd.get_list(20)}
    return render(request, 'index.html', con)


def random_purple_prob(request):
    name = get_rd.get_prob()
    return redirect('https://www.luogu.com.cn/problem/' + name)
