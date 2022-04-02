from django.urls import path
from admin_panel.views import account, home
from admin_panel.login.decorator import dashboard_logout,dashboard_login
from admin_panel.fillials.fillial import create_fillial, delete_fillial,list_fillial,edit_fillial
urlpatterns = [
    path('', home, name='home'),

    #login
    path('login', dashboard_login,name='login'),
    path('logout', dashboard_logout,name='logout'),

    #fillials
    path('fillials/create', create_fillial,name='create_fillial'),
    path('fillials/list', list_fillial,name='list_fillial'),
    path('fillials/edit/<int:id>', edit_fillial,name='edit_fillial'),
    path('fillials/delete/<int:id>', delete_fillial,name='delete_fillial'),

    #accounts
    path('account/', account, name='account'),
]