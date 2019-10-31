from django.shortcuts import render
from . cadus_utilities.test import testfunc, openbrowser
from . cadus_utilities.maintest import main2

def home(request):
    # sendtohtml = [1,2,3,4]
    sendtohtml = testfunc
    openbrowser()
    main2()
    print('sendtohtml')
    print(sendtohtml)
    return render(request, 'home.html', {'sendtohtml' : sendtohtml})
