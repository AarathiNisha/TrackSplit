from django.urls import path
from .import views

urlpatterns=[
    path("Home/",views.home,name="home"),
    path('Dashboard/', views.dashboard, name='dashboard'),
    path('Login/',views.user_login,name='login'),
    path('Signup/',views.signup,name='signup'),
    path('Profile/',views.profile,name='profile'),
    path('MyCircles/',views.my_circle,name='mycircles'),
    path('NewCircle/',views.new_circle,name='newcircle'),
    path('Addmembers/<int:circle_id>/add/',views.add_member,name='add_member'),
    path('Expenses/<int:circle_id>/add/',views.add_expense,name='add_expense'),
    path('MyExpense/<int:circle_id>/add/',views.my_expense,name='my_expense'),
    path('EditExpense/edit/<int:expense_id>/',views.edit_expense,name='edit_expense'),
    path('DeleteExpense/delete/<int:expense_id>/',views.delete_expense,name='delete_expense'),
    path('ViewGroup/<int:circle_id>/', views.view_group, name='view_group'),
    path('DeleteCircle/<int:circle_id>/', views.delete_circle, name='delete_circle'),
    path('AboutMe/details', views.about, name='about'),
    path('Filters/details/',views.filter,name='filter')
]