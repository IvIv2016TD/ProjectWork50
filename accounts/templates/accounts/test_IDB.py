def test_IDB(request):
    numpoints = request.POST[number_of_points]
	print(numpoints)
	return  HttpResponse ('Тест test_IDB')
	