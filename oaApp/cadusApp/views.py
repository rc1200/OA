from django.shortcuts import render, redirect
from . cadus_utilities.test import runSuperCode



def home(request):
    sendtohtml = [1,2,3,4]
    print('sendtohtml')
    print(sendtohtml)
    return render(request, 'home.html', {'sendtohtml' : sendtohtml})


# def super(request):
#     # sendtohtml = [1,2,3,4]
#     sendtohtml = ['all','done','now',4]
#     # runSuperCode()
#     print('sendtohtml')
#     print(sendtohtml)
#     return render(request, 'home.html', {'sendtohtml' : sendtohtml})
#     # return redirect(home)