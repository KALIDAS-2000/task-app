
from django.shortcuts import render,redirect
from django.views.generic import View,ListView,DetailView,UpdateView
from task.models import Task
from task.forms import RegistrationForms,LoginForm,TaskUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return fn(request,*args,**kwargs)
        else:
            messages.error(request,"you must login first")
            return redirect('signin')
    return wrapper


class IndexView(View):
    def get(self,request,*args,**kwargs):
        return render(request,"index.html")


class LoginView(View):
    def get(Self,request,*arg,**kwargs):
        return render(request,"login.html")


class RegisterView(View):
    def get(Self,request,*arg,**kwargs):
        return render(request,"registration.html")



class RegistrationView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForms()
        return render(request,"register.html",{'form':form})


    def post(self,request,*args,**kwargs):
        form=RegistrationForms(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            messages.success(request,"registration compleated")
            return redirect('signin')
        else:
            messages.error(request,"invalid activity")
            return redirect('register')


class LogginView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"loggin.html",{"form":form})

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get('username')
            pwd=form.cleaned_data.get('password')
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                messages.success(request,"login success")
                return redirect('task-all')
            else:
                messages.error(request,"invalid activity")
                return render(request,"loggin.html",{"form":form})
        

@method_decorator(signin_required,name="dispatch")
class AddTaskView(View):
    def get(Self,request,*arg,**kwargs):
        return render(request,"add_task.html")

    def post(Self,request,*arg,**kwargs):
        name=request.user
        task=request.POST.get('task')
        Task.objects.create(user=name,task_name=task)
        messages.success(request,"task created")
        return redirect('task-all')


        

# localhost:8000/addtask/
@method_decorator(signin_required,name="dispatch")
class TaskListView(ListView):
    model=Task
    template_name="task_list.html"
    context_object_name="tlist"

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    # def get(self,request,*args,**kwargs):
    #     if request.user.is_authenticated:
    #         qs=Task.objects.filter(user=request.user)
    #         return render(request,"task_list.html",{"tlist":qs})
    #     else:
    #         return redirect('signout')


# 8000/task/id
@method_decorator(signin_required,name="dispatch")
class TaskDetailView(DetailView):
    model=Task
    template_name="taskdetail.html"
    context_object_name="tlist"
    pk_url_kwarg="id"
    
    # def get(self,request,*args,**kwargs):
    #     id=kwargs.get("id")
    #     task=Task.objects.get(id=id)
    #     return render(request,'taskdetail.html',{'tlist':task})


class TaskUpdateView(UpdateView):
    model=Task
    form_class=TaskUpdateForm
    pk_url_kwarg="id"
    template_name="taskupdate.html"
    success_url=reverse_lazy('task-all')


# 8000/task/id/remove
@method_decorator(signin_required,name="dispatch")
class TaskDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('id')
        task=Task.objects.filter(id=id).delete()
        messages.success(request,"task deleted")
        return redirect('task-all')




# @method_decorator(signin_required,name="dispatch")
def signout_view(request,*args,**kwargs):
    logout(request)
    return redirect('signin')





