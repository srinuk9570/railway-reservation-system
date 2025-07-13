from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),

    # Authentication
    path('loginform/', views.loginform, name="loginform"),
    path('login/', views.login, name="login"),
    path('registerform/', views.registerform, name="registerform"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout, name="logout"),

    # Train Management
    path('trainform/', views.trainform, name="trainform"),
    path('addtrain/', views.addtrain, name="addtrain"),  # ✅ fixed name from "addtrains" to "addtrain"

    # Booking
    path('bookform/', views.bookform, name="bookform"),
    path('book/', views.book, name="book"),
    path('mybooking/', views.mybooking, name="mybooking"),
    path('booking/<int:train_id>/', views.booking, name="booking"),  # ✅ fixed: added int and slash

    # Train Detail
    path('train/<int:train_id>/', views.train_id, name="train_id"),  # ✅ clearer path name and fixed format
]
