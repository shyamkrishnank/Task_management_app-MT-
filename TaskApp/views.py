from django.shortcuts import render,redirect
from django.views import View
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connections
from datetime import datetime, date
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
import uuid
import json





#--------------------------------------------------signup/login----------------------------
class SignUpView(View):
    def get(self,request):
        try:
           user = request.session['user']
           if user:
              return redirect('home')
           else:
               return render(request, 'Register/Signup.html')
        except:
             return render(request,'Register/Signup.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('confirmPassword')
        user = CustomUser.objects.filter(email=email)
        if user:
            message = 'Email already exists!'
            return render(request, 'Register/Signup.html', {'message':message})

        if password == cpassword:
            user = CustomUser.objects.create_user(username=username,
                                                  email=email,
                                                  password=password)
            user.save()
            return redirect('login')

        else:
            message = 'Please enter correct password!'
            return render(request, 'Register/Signup.html', {'message':message})
        return render(request,'Register/Signup.html')

class LoginView(View):
    def get(self,request):
        try:
            user = request.session['user']
            if user:
                return redirect('home')
            else:
                return render(request, 'Register/Login.html')
        except:
            return render(request, 'Register/Login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user:
            user_exists = user.username
            request.session['user'] = user_exists  #storing user on the session
            login(request, user)
            return redirect('home')
        else:
            message = 'Invalid email or password'
            return render(request, 'Register/Login.html', {'message':message})

class LogoutView(View):
    def get(self, request):
        request.session.flush()
        logout(request)
        return redirect('login')


#-------------------------------------------------------------------------------------
class HomeView(LoginRequiredMixin,View):
    def get(self, request):
        user_id = str(request.user.id).replace("-",'')
        filter_data = None
        today = date.today()
        try:
           filterd_tasks = request.session['tasks']
           filter_data = request.session['filter_data']
           tasks = json.loads(filterd_tasks)
           del request.session['tasks']
           del request.session['filter_data']
        except:
            try:
                cursor = connections['default'].cursor()
                cursor.execute("EXEC GetTasksByUser @user_id=%s", [user_id])
                tasks = cursor.fetchall()
            except:
                return render(request, 'Home/Home.html')
        return render(request, 'Home/Home.html', {'tasks': tasks,'filter_data':filter_data,'today':today})


class CreateTaskView(LoginRequiredMixin, View):
    def post(self, request):
        id = str(uuid.uuid4())
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date_str = request.POST.get('due_date')
        user_id = str(request.user.id).replace('-','')
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        status = 'Incomplete'

        try:
            cursor = connections['default'].cursor()
            cursor.execute("""EXEC CreateTask @id=%s, @title=%s, @description=%s, @due_date=%s, @status=%s, @user_id=%s
                          """, [id, title, description, due_date, status,user_id])
        except Exception as e:
            return redirect('home')

        return redirect('home')

class FilteredTaskView(View):
    def post(self, request):
        user_id = str(request.user.id).replace("-",'')
        status = request.POST.get('status')
        due_date = request.POST.get('due_date')
        tasks = None
        if due_date and status:
            cursor = connections['default'].cursor()
            cursor.execute("EXEC GetTasksByStatusAndDueDate @user_id=%s, @status=%s, @due_date=%s",
                           [user_id, status, due_date])
            tasks = cursor.fetchall()
        elif status:
            cursor = connections['default'].cursor()
            cursor.execute("EXEC GetTasksByStatus @user_id=%s, @status=%s",
                           [user_id, status])
            tasks = cursor.fetchall()

        elif due_date:
            cursor = connections['default'].cursor()
            cursor.execute("EXEC GetTasksByDueDate @user_id=%s, @due_date=%s",
                           [user_id, due_date])
            tasks = cursor.fetchall()
        if tasks is not None:
           serialized_tasks = json.dumps(tasks, cls=DjangoJSONEncoder)
           request.session['tasks'] = serialized_tasks
           request.session['filter_data'] = {
               'status':status,
               'due_date': due_date
           }
        return redirect('home')

class UpdateTaskView(View):
    def post(self,request):
        task_id = str(request.POST.get('id'))
        title = request.POST.get('title') if request.POST.get('title') else None
        description = request.POST.get('description') if request.POST.get('description') else None
        status = request.POST.get('status') if request.POST.get('status') else None
        due_date_str = request.POST.get('due_date')
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else None
        try:
            cursor = connections['default'].cursor()
            cursor.execute("""EXEC UpdateTask @task_id=%s, @status=%s, @due_date=%s, @title=%s, @description=%s
                           """, [task_id, status, due_date, title, description])

        except Exception as e:
            return redirect('home')

        return redirect('home')

class UpdateStatusView(View):
    def post(self, request):
        data = json.loads(request.body)
        task_id = data['id']
        status = data['status']
        try:
            cursor = connections['default'].cursor()
            cursor.execute("""EXEC UpdateTask @task_id=%s, @status=%s
                           """, [task_id, status])
            return JsonResponse({'message': 'status updated'})

        except Exception as e:
            return JsonResponse({'error': 'Status filled missing'}, status=400)

        return redirect('home')


class DeleteTaskView(View):
    def get(self,request,id):
        task_id = id

        try:
            cursor = connections['default'].cursor()
            cursor.execute("""EXEC DeleteTask @task_id=%s
                           """, [task_id])
        except Exception as e:
             return redirect('home')

        return redirect('home')








