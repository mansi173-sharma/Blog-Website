from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm, CreateUserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('post_list')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form=CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request,'Account was created for '+ user)
                return redirect('login')

    return render(request, 'blog/register.html',{'form':form})

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('post_list')
    else:
        if request.method == 'POST':
            username=request.POST.get('username')
            password=request.POST.get('password')
            user = authenticate(request,username=username, password=password)

            if user is not None:
                login(request,user)
                return redirect('post_list')
            else:
                messages.info(request,'Username or password is incorrect')

        return render(request, 'blog/login.html',{})

def logoutUser(request):
    logout(request)
    return redirect('post_list')

def post_list(request):
    posts=Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts':posts})

def post_details(request,pk):
    post = get_object_or_404(Post, pk= pk)
    return render(request, 'blog/post_details.html', {'post': post})

@login_required(login_url ='login')
def post_new(request):
    if(request.method == "POST"):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit = False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_details', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required(login_url ='login')
def post_edit(request,pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance = post)
        if form.is_valid():
            post = form.save(commit = False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_details', pk=post.pk)
    else:
        form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})


@login_required(login_url ='login')
def post_delete(request,pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')
    
