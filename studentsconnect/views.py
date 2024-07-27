from pyexpat.errors import messages
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
import requests
from studentsconnect.models import Category, ContactMessage, Page
from studentsconnect.forms import CategoryForm, PageForm
from studentsconnect.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from studentsconnect.google_search import run_query
from django.contrib import messages




def index(request):
    top_categories = Category.objects.order_by('-likes')[:5]
    all_categories = Category.objects.all()

    page_list = Page.objects.order_by('-views')[:5]
    

    
    context_dict = {
        'boldmessage': 'YOUR ONE STOP SOLUTION TO A SEAMLESS INTERNATIONAL EXPERIENCE',
        'top_categories': top_categories,

        'all_categories': all_categories,
        'pages': page_list
    }
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    response = render(request, 'studentsconnect/index.html', context=context_dict)
    return response

def about(request):
    print(request.method)
    print(request.user)
    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()
    return render(request, 'studentsconnect/about.html', {})

def show_category(request, category_name_slug):
    context_dict = {}
    
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
    
    return render(request, 'studentsconnect/category.html', context=context_dict)

def add_category(request): 
    form = CategoryForm()
    
    if request.method == 'POST':
        form = CategoryForm(request.POST,)
        
        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('studentsconnect:index'))
        else:
            print(form.errors)
    
    return render(request, 'studentsconnect/add_category.html', {'form': form})

def add_page(request, category_name_slug): 
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return render(reverse('studentsconnect:index'))
    
    form = PageForm()
    
    if request.method == 'POST':
        form = PageForm(request.POST)
        
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                
                return render(reverse('studentsconnect:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)
    
    context_dict = {'form': form, 'category': category}
    return render(request, 'studentsconnect/add_page.html', context=context_dict)


@login_required
def restricted(request):
    return render(request, 'studentsconnect/restricted.html')

def home(request):
    return render(request, "home.html", {})

def detail(request):
    return render(request, "detail.html", {})

def posts(request):
    return render(request, "posts.html", {})



def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request,
                                               'last_visit',
                                               str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
    
    request.session['visits'] = visits

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

# def search(request):
#     result_list = []
#     if request.method == 'POST':
#         query = request.POST['query'].strip()
#         if query:
# Run our Bing function to get the results list!
            # result_list = run_query(query)
    # return render(request, 'studentsconnect/search.html', {'result_list': result_list})

def contact_admin(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        
        # Save the contact message to the database
        ContactMessage.objects.create(name=name, email=email, message=message)
        
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('studentsconnect:index')
    else:
        return redirect('studentsconnect:index')

