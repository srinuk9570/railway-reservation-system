from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import trains, person

# ✅ Index
def index(request):
    lis = trains.objects.all()
    return render(request, 'viewtrains.html', {"lis": lis})

# ✅ Login Form
def loginform(request):
    return render(request, 'login.html')

# ✅ Login Handler
def login(request):
    if request.method == 'POST':
        u = request.POST
        user = authenticate(request, username=u.get('name'), password=u.get('password'))
        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            return render(request, 'error.html', {'msg': "Invalid username or password."})
    return redirect('loginform')

# ✅ Register Form
def registerform(request):
    return render(request, 'register.html')

# ✅ Register Handler (FIXED)
def register(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'error.html', {'msg': "Username already exists. Choose another."})

        if User.objects.filter(email=email).exists():
            return render(request, 'error.html', {'msg': "Email already registered. Try logging in."})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        return render(request, 'error.html', {'msg': "Registration Successful"})
    return redirect('registerform')

# ✅ Logout
def logout(request):
    auth_logout(request)
    return render(request, 'error.html', {'msg': "Logout Successful"})

# ✅ Admin Train Form
def trainform(request):
    if request.user.is_superuser:
        return render(request, 'addtrain.html')
    return render(request, 'error.html', {'msg': "Access Denied. Admin Only"})

# ✅ Add Train
def addtrain(request):
    if request.method == 'POST':
        l = trains(
            source=request.POST['source'],
            destination=request.POST['destination'],
            time=request.POST['time'],
            seats_available=request.POST['seats_available'],
            train_name=request.POST['train_name'],
            price=request.POST['price']
        )
        l.save()
        return render(request, 'error.html', {'msg': "Train Successfully Added"})
    return redirect('trainform')

# ✅ View passengers of a train
def train_id(request, train_id):
    if not request.user.is_superuser:
        return render(request, 'error.html', {'msg': "Access Denied. Admin Only"})
    l = trains.objects.get(pk=train_id)
    persons = l.person_set.all()
    return render(request, 'viewperson.html', {'train': l, 'persons': persons})

# ✅ Book Temp Storage
temp = {}

# ✅ Search for Trains
def book(request):
    global temp
    if request.user.is_authenticated and request.method == 'POST':
        source = request.POST.get('source')
        destination = request.POST.get('destination')

        t = trains.objects.filter(source=source, destination=destination)
        if t.exists():
            temp['name'] = request.POST.get('name')
            temp['age'] = request.POST.get('age')
            temp['gender'] = request.POST.get('gender')
            return render(request, 'trainsavailable.html', {'trains': t})
        else:
            return render(request, 'error.html', {'msg': "No trains found for this route."})
    return render(request, 'error.html', {'msg': "Please login to book tickets."})

# ✅ Book Specific Train
def booking(request, train_id):
    if not request.user.is_authenticated:
        return render(request, 'error.html', {'msg': "Login required."})

    train = trains.objects.get(pk=train_id)
    if train.seats_available == 0:
        return render(request, 'error.html', {'msg': "Seats are full for this train."})

    p = person(
        train=train,
        name=temp.get('name'),
        age=temp.get('age'),
        gender=temp.get('gender'),
        email=request.user.email
    )
    p.save()

    train.seats_available -= 1
    train.save()

    return render(request, 'error.html', {'msg': f"Booking Successful! Price: ₹{train.price}"})

# ✅ Booking Form
def bookform(request):
    if not request.user.is_authenticated:
        return render(request, 'error.html', {'msg': "Please login to continue."})

    t = trains.objects.all()
    sources = list(set([i.source for i in t]))
    destinations = list(set([i.destination for i in t]))

    return render(request, 'booking.html', {'sources': sources, 'destinations': destinations})

# ✅ My Bookings
def mybooking(request):
    if not request.user.is_authenticated:
        return render(request, 'error.html', {'msg': "Please login to view your bookings."})
    
    p = person.objects.filter(email=request.user.email)
    return render(request, 'mybooking.html', {'persons': p})
