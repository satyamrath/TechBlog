from blog.models import Post
from django.shortcuts import render, redirect
from django.http import  HttpResponse
from home.models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.


# HTML Pages
def home(request):
    # fetching top three posts based on the number of views
    allPosts = Post.objects.all().order_by("-noOfViews")[ : 3]
    context = {"allPosts": allPosts}
    return render(request, "home/home.html", context)

def about(request):
    return render(request, "home/about.html")

def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        if len(name) < 2 or len(email) < 4 or len(phone) < 10 or len(content) < 4 :
            messages.error(request, "Please fill the form correctly.")
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your message has been sent.")
    return render(request, "home/contact.html")

def search(request):
    query = request.GET.get("query")
    # allPosts = Post.objects.all()
    if len(query) > 78:
        allPosts = Post.objects.none()  # creating blank querySet
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)
    if allPosts.count() == 0:
        messages.warning(request, "No search result found. Please refine your query.")
    context = {"allPosts": allPosts, "query": query}
    return render(request, "home/search.html", context)

# Authentication APIs
def handleSignup(request):
    if request.method == "POST":
        # get the POST parameters
        username = request.POST["username"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]

        # check for errorneous inputs
        if len(username) > 10:
            messages.error(request, "Username must be under 10 character.")
            return redirect("home")

        if not username.isalnum():
            messages.error(request, "Username should not only contain letters and numbers.")
            return redirect("home")

        if pass1 != pass2:
            messages.error(request, "Passwords should match.")
            return redirect("home")
        # if len(username) > 10:
        #     messages.error(request, "Username must be under 10 character.")
        #     return redirect("home")
        # if len(username) > 10:
        #     messages.error(request, "Username must be under 10 character.")
        #     return redirect("home")
            
        # create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your iCoder account has been successfully created.")
        return redirect("home")
    else:
        return HttpResponse("404 - Not Found")

def handleLogin(request):
    if request.method == "POST":
        # get the POST parameters
        loginusername = request.POST["loginusername"]
        loginpassword = request.POST["loginpass"]

        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "successfully logged in.")
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials, please try again")
            return redirect("home")
            
    else:
        return HttpResponse("404 - Not Found")

def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out.")
    return redirect("home")

