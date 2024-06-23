from django.urls import path
from .views import *

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('signup', SignUpView.as_view(), name = 'signup'),
    path('home', HomeView.as_view(), name = 'home'),
    path('logout', LogoutView.as_view(), name = 'logout'),

    path('createtask', CreateTaskView.as_view(), name = 'createtask'),
    path('filtertask', FilteredTaskView.as_view(), name = 'filtertask'),
    path('updatetask', UpdateTaskView.as_view(), name = 'updatetask'),
    path('updatestatus', UpdateStatusView.as_view(), name = 'updatestatus'),
    path('deletetask/<str:id>', DeleteTaskView.as_view(),  name = 'deletetask')
]
