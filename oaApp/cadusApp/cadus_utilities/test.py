import webbrowser


def testfunc():
    mylist = []
    for i in range(5):
        # print(i)
        mylist.append(i)
    
    print(mylist)
    return mylist

def openbrowser():
    webbrowser.open('http://google.com') 

# openbrowser()


# test()