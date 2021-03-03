def test_IDB(numpoints):
    one = open("One.txt", 'a')
    for item in range(numpoints):
        one.write("item #" + "\n")
    one.flush()
    one.close()
#def test_IDB(request):
    #numpoints = request.POST[number_of_points]
    #print("Количество точек ", numpoints)
    #return  HttpResponse ('Тест test_IDB')


test_IDB(3)
