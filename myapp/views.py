from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .forms import UserCreationForm
from .forms import SignupForm
from django.contrib import messages
from django.core.mail import EmailMessage
from .forms import LoginForm
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.contrib.auth.decorators import login_required
from .forms import MyCircleForm
from .models import MyCircle
from .models import Expense
from .forms import ExpenseForm
from .forms import SignupForm
from django.http import HttpResponseForbidden
from django.db.models import Sum
from datetime import date
from .models import Category
from .models import Motivation


def signup(request):
    if request.method=='POST':
        form=SignupForm(request.POST)
        if form.is_valid():
            user=form.save()
            email=EmailMessage(subject=f'Welcome to TrackSplit! {user.username}',
            body=f'Hello {user.username}, Thank you for signing up! Stay Connected Always.',
            from_email='aarathisa@gmail.com',
            to=[user.email],)
            file=request.FILES.get('attachment')
            if file:
                email.attach(file.name,file.read(),file.content_type)
            email.send(fail_silently=False)
            messages.success(request,"Account created successfully")
            return redirect('login')
    else:
        form=SignupForm()
    return render(request,template_name='signup.html',context={'form':form})


def user_login(request):
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            user=authenticate(request,email=email,password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.error(request,'Invalid username or Password')
    else:
        form=LoginForm()
    return render(request,template_name='login.html',context={'form':form})

@login_required(login_url='login')
def home(request):
    return render(request,template_name='home.html')

def dashboard(request):
    return render(request,template_name='Dashboard.html')

def profile(request):
    if request.method == "POST":
        if 'signout' in request.POST:
            logout(request)
            return redirect('login')
    return render(request,template_name='profile.html')

def new_circle(request):
    if request.method == 'POST':
        form = MyCircleForm(request.POST)
        if form.is_valid():
            circle=form.save(commit=False)
            circle.created_by=request.user
            circle.save()
            return redirect('mycircles')
    else:
        form = MyCircleForm()
    return render(request, 'newcircle.html', {'form': form})

@login_required
def my_circle(request):
    user=request.user
    circles_creator = MyCircle.objects.filter(created_by=user)
    member_circles=MyCircle.objects.filter(members=user)
    all_circles=(circles_creator|member_circles).distinct()
    return render(request, 'mycircles.html', {'circles': all_circles})

User=get_user_model()
def add_member(request,circle_id):
    circle = get_object_or_404(MyCircle, id=circle_id)
    members = circle.members.all()

    if request.method == "POST":
        username = request.POST.get('username')
        try:
            user_to_add = User.objects.get(username=username)
            if user_to_add in members:
                messages.warning(request, f"{username} is already a member.")
            else:
                circle.members.add(user_to_add)
                messages.success(request, f"{username} added to the circle.")
        except User.DoesNotExist:
            messages.error(request, "User not found.")

        return redirect('add_member', circle_id=circle.id)

    return render(request, 'addmembers.html', {'circle': circle,'members':members})

@login_required
def add_expense(request,circle_id):
    circle=get_object_or_404(MyCircle,id=circle_id)
    if request.method=='POST':
            form=ExpenseForm(request.POST)
            if form.is_valid():
                expense=form.save(commit=False)
                expense.user=request.user
                expense.circle = circle   #link expense to the correct circle
                expense.save()
                return redirect('my_expense',circle_id=circle.id)
    else:
        form=ExpenseForm()
    return render(request,template_name='addexpense.html',context={'form':form,'circle':circle})

@login_required
def edit_expense(request,expense_id):
    expense = get_object_or_404(Expense, id=expense_id)

    if expense.user!=request.user:
        return HttpResponseForbidden("You're not allowed to edit a response")

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense) #copy same expense form
        if form.is_valid():
            form.save()
            return redirect('my_expense', circle_id=expense.circle.id)  # redirect to same circle
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'edit_expense.html', {'form': form, 'expense': expense})


@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)

    if expense.user != request.user:
        return HttpResponseForbidden("You're not allowed to delete this expense.")

    circle_id = expense.circle.id  # Save the circle ID before deleting
    expense.delete()
    return redirect('my_expense', circle_id=circle_id)

@login_required
def my_expense(request, circle_id):
    circle = get_object_or_404(MyCircle, id=circle_id)
    expenses = Expense.objects.filter(circle=circle)  #Only show expenses for this circle id
    return render(request, 'my_expense.html', {'circle': circle, 'expenses': expenses})


@login_required
def view_group(request, circle_id):
    circle = get_object_or_404(MyCircle, id=circle_id)
    members = circle.members.all()
    expenses = Expense.objects.filter(circle=circle)

    return render(request, 'view_group.html', {'circle': circle,'members': members,'expenses': expenses})

@login_required
def delete_circle(request, circle_id):
    circle = get_object_or_404(MyCircle, id=circle_id)

    if circle.created_by != request.user:
        return HttpResponseForbidden("You're not allowed to delete this expense.")
    circle.delete()
    messages.success(request,"Circle deleted successfully")
    return redirect('mycircles')

@login_required
def my_expense(request, circle_id):
    circle = get_object_or_404(MyCircle, id=circle_id)
    expenses = Expense.objects.filter(circle=circle)  #Only show expenses for this circle id
    return render(request, 'my_expense.html', {'circle': circle, 'expenses': expenses})

def home(request):
    joined_circles = MyCircle.objects.filter(members=request.user)
    joined_count = joined_circles.count()
    user_expenses = Expense.objects.filter(user=request.user)
    total_expenses = user_expenses.count()
    total_amount = sum(exp.amount for exp in user_expenses)
    quotes = Motivation.objects.all()

    if quotes.exists():
        quote_obj = quotes.first()
    else:
        quote_obj = "Keep tracking your expenses!"

    last_expense=user_expenses.order_by('-date').first()
    recent_date=last_expense.date

    highest_expense=user_expenses.order_by('-amount').first() #descending first one
    highest_amount=highest_expense.amount

    lowest_expense = user_expenses.order_by('amount').first() #ascending first one
    lowest_amount = lowest_expense.amount

    return render(request, 'home.html', {'joined_circles': joined_circles,'joined_count': joined_count,'total_amount': total_amount,
        'total_expenses':total_expenses,'quote_obj': quote_obj,'recent_date':recent_date,'highest_amount':highest_amount,'lowest_amount':lowest_amount})



def about(request):
    return render(request,template_name='About.html')

def filter(request):
        expenses = Expense.objects.filter(user=request.user)
        categories = Category.objects.all()

        category_id = request.GET.get('category')
        if category_id:
            expenses = expenses.filter(category_id=category_id)

        total_amount = sum(exp.amount for exp in expenses)

        return render(request, 'filters.html', {'expenses': expenses,'categories': categories,'total_amount': total_amount})

def dashboard(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    total_amount = sum(exp.amount for exp in expenses)
    total_expenses = expenses.count()
    category_count = Category.objects.count()

    # Optional: recent 5 expenses
    recent_expenses = expenses[:5]

    return render(request, 'Dashboard.html', {'total_amount': total_amount,'total_expenses': total_expenses,'category_count': category_count,'recent_expenses': recent_expenses,})