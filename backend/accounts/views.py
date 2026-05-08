from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg
from transactions.models import Transaction
from .models import User
# Create your views here.
def signup(request):
    """
    Handles the user registration process.

    Extracts user details from a POST request, validates that the passwords match, 
    and creates a new User instance in the database.
    Logs the user in upon successful creation and redirects to the dashboard.
    """
    if request.method =='POST':

        firstName = request.POST.get('first_name')
        lastName = request.POST.get('last_name')
        birthDate = request.POST.get('birth_date')
        userName = request.POST.get('username')
        Email = request.POST.get('email')
        passWord = request.POST.get('password')
        confirmPassWord = request.POST.get('confirm_password')
        phoneNumber = request.POST.get('phone_number')
        if passWord != confirmPassWord:
            return render(request,'signup.html',{'error':'password do not match'}) 
        try:
            user = User.objects.create_user(
                username=userName,
                email=Email,
                password=passWord,
                birth_date= birthDate,
                phone_number = phoneNumber,
                first_name = firstName,
                last_name = lastName
            )
            login(request,user)
            return redirect('dashboard')
        except Exception as e:
            print("======== THE REAL ERROR ========")
            print(e)
            print("================================")
            return render(request, 'signup.html', {'error': 'Username already exists or invalid data!'})
    
    return render(request,'signup.html')

def login_view(request):
    """
    Handles user authentication and login using email and password.

    Finds the user by email, authenticates them using Django's built-in 
    authenticate method, and redirects to the dashboard if successful.
    """
    if request.method =='POST':
        Email = request.POST.get('email')
        passWord = request.POST.get('password')

        user_obj = User.objects.filter(email =Email).first() 

        if user_obj:

            user = authenticate(request,username= user_obj.username,password = passWord)
            if user is not None:
                login(request,user)
                return redirect('dashboard')
            
        return render(request,'login.html',{'error':'Invalid email or password'})
    return render(request,'login.html')

def logout_view(request):
    """
    Logs out the currently authenticated user and redirects to the login page.
    """
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    """
    Renders the main dashboard for the user with financial summaries.

    Calculates and provides the following context to the template:
    - Total and average income/expenses.
    - Total current balance and savings rate percentage.
    - Expense totals grouped by category (for chart rendering).
    - A list of the 5 most recent transactions.
    """
    user_transactions = Transaction.objects.filter(user=request.user)
    avg_income = user_transactions.filter(type='i').aggregate(Avg('amount'))['amount__avg']or 0
    avg_expenses = user_transactions.filter(type='e').aggregate(Avg('amount'))['amount__avg']or 0
    total_income = user_transactions.filter(type='i').aggregate(Sum('amount'))['amount__sum']or 0
    total_expenses = user_transactions.filter(type='e').aggregate(Sum('amount'))['amount__sum']or 0
    total_balance = total_income-total_expenses

    if total_income>0:
        saving_rate = (total_balance/total_income)*100
    else:
        saving_rate = 0
    
    spending_category = user_transactions.filter(type='e').values('category__name').annotate(total=Sum('amount'))
    spending_category_name = [item['category__name'] for item in spending_category]
    spending_category_total = [float(item['total']) for item in spending_category]
    recent_transactions = user_transactions.order_by('-date_time')[:5]
    context = {
        'avg_income':round(avg_income,2),
        'avg_expenses':round(avg_expenses,2),
        'total_balance':float(total_balance),
        'saving_rate':round(saving_rate,2),
        'spending_category_name':spending_category_name,
        'spending_category_total':spending_category_total,
        'total_income':float(total_income),
        'total_expenses':float(total_expenses),
        'recent_transactions':recent_transactions,
    }
    return render(request, 'dashboard.html',context)