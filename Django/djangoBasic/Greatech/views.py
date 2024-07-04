from django.shortcuts import render, redirect, HttpResponse


# Create your views here.
def login(request):
	# return HttpResponse("<h1>Welcome to Greatech</h1>")
	message = "daito..."
	data_list = ["贺东", "邓凯", "叶婷"]
	mapping = {"name": "贺东", "age": 29, "gemal": "male"}
	if request.method == "GET":
		print("get login 进来...")
		return render(request, "login.html")
	else:
		print(request.POST.get("user"))
		print(request.POST.get("pwd"))
		if request.POST.get("user") == "admin" and request.POST.get("pwd") == "123":
			return redirect('/index/')
		else:
			return render(request, 'login.html', {'error': "用户名或者密码出错，请重试。"})


def index(request):
	if request.method == "GET":
		print("进入index。。。。。。")
		return render(request, "index.html")
	else:
		print("POST http")

def phone_list(request):
	# 1.获取数据
	queryset = [
		{"id": 1, "phone": "18281813342", "city": "上海"},
		{"id": 2, "phone": "18285432342", "city": "北京"},
		{"id": 3, "phone": "18281778342", "city": "苏州"},
		{"id": 4, "phone": "18281823342", "city": "成都"},
		{"id": 5, "phone": "18285613342", "city": "重亲"},
		{"id": 6, "phone": "18231813342", "city": "北海"}
	]
	return render(request, "phone_list.html", {'queryset': queryset})
