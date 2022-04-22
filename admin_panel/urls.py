from django.urls import path
from admin_panel.category.categories import create_category, delete_category, edit_category, list_category
from admin_panel.product.products import create_product, delete_product, edit_product, list_product, one_product
from admin_panel.sub_category.sub_categories import create_sub_category, delete_sub_category, edit_sub_category, list_sub_category
from admin_panel.views import account, home,list_operators,create_operator,edit_operator,delete_operator
from admin_panel.login.decorator import dashboard_logout,dashboard_login
from admin_panel.fillials.fillial import create_fillial, delete_fillial,list_fillial,edit_fillial, one_fillial
from admin_panel.clients.all_clients import clients_list,send_telegram
from admin_panel.orders.order import orders_list, update_order_status, one_order, reject_order
from admin_panel.statistics.statistika import all_statistika
from admin_panel.settings.bot_settings import texts,settings
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
    path('fillial/one/<int:pk>', one_fillial,name='one_fillial'),

    #category
    path('category/create', create_category,name='create_category'),
    path('category/list', list_category,name='list_category'),
    path('category/edit/<int:pk>', edit_category,name='edit_category'),
    path('category/delete/<int:pk>', delete_category,name='delete_category'),

    #sub_category
    path('sub_category/create/<int:pk>', create_sub_category,name='create_sub_category'),
    path('sub_category/list/<int:pk>', list_sub_category,name='list_sub_category'),
    path('sub_category/edit/<int:pk>', edit_sub_category,name='edit_sub_category'),
    path('sub_category/delete/<int:pk>', delete_sub_category,name='delete_sub_category'),

    #product
    path('product/create/<int:pk>', create_product,name='create_product'),
    path('product/list/<int:pk>',list_product,name="list_product"),
    path('product/edit/<int:pk>', edit_product,name="edit_product"),
    path('product/delete/<int:pk>', delete_product,name="delete_product"),
    path('product/one_product/<int:pk>', one_product,name="one_product"),

    #operators
    path('operator/create', create_operator,name='create_operator'),
    path('operator/list/',list_operators,name="list_operator"),
    path("operator/edit/<int:pk>",edit_operator,name="edit_operator"),
    path("operator/delete/<int:pk>",delete_operator,name="delete_operator"),

    #clients
    path('clients/list',clients_list,name="clients_list"),
    path('clients/send_msg/<int:pk>',send_telegram,name="send_telegram"),


    #orders
    path('orders/list',orders_list,name="orders_list"),
    path('order/update/accept/<int:pk>',update_order_status,name="update_order"),
    path('orders/one/<int:pk>',one_order,name="one_order"),


    path('orders/reject/<int:pk>', reject_order),

    #accounts
    path('account/', account, name='account'),


    #statistics
    path('statistics/', all_statistika, name='statistics'),


    #settings
    path("settings",settings,name="settings"),
    path("texts",texts,name="texts"),
]
