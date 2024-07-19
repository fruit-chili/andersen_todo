"""
URL configuration for andersen_todo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from tasks.views import TasksView, Registration, TaskView, CompleteTaskView

urlpatterns = [
    path('paniniminimoneymore/', admin.site.urls),
    path('registration/', Registration.as_view(), name='registration'), #POST
    path('login/', TokenObtainPairView.as_view(), name='login'), #POST
    path('tasks/', TasksView.as_view(), name='tasks_list'), #GET, POST 
    # path('tasks/<str:username>/', tasks.xxx.as_view(), name='user_tasks_list'), #GET
    path('task/<int:task_id>/', TaskView.as_view(), name='task_details'), #GET, PATCH, DELETE
    path('task/<int:task_id>/completed/', CompleteTaskView.as_view(), name='mark_task_completed'), #PATCH
]
