from django.shortcuts import render,redirect
from .forms import Tweetform,UserRegistration
from .models import Tweet
from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required



def index(request):
    return render(request,'index.html')

 
def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    

    return render(request, "tweet_list.html", {'tweets':tweets})

@login_required
def tweet_create(request):
    if request.method=="POST":
        form=Tweetform(request.POST,request.FILES)
        if form.is_valid():
            tweet=form.save(commit=False)
            tweet.user=request.user
            tweet.save()
        return redirect('tweet_list')      

    else:
        form=Tweetform()
    return render(request, 'tweet_form.html',{'form':form})

@login_required
def tweet_edit(request,tweet_id):
    tweet=get_object_or_404(Tweet,pk=tweet_id,user=request.user)
    if request.method=="POST":
        form=Tweetform(request.POST,request.FILES,instance=tweet)
        if form.is_valid():

            form.save(commit=False)
            tweet.user=request.user
            tweet.save()
            return redirect('tweet_list')


    else:
        form=Tweetform(instance=tweet)
    return render(request, 'tweet_form.html', {'form': form})  

@login_required
def tweet_delete(request,tweet_id):
    tweet=get_object_or_404(Tweet,pk=tweet_id,user=request.user)
    if request.method=="POST":
        tweet.delete()
        return redirect("tweet_list")
    return render(request, 'confirm_delete.html',{'tweet':tweet})

def register(request):
    if request.method=="POST":
        form=UserRegistration(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request,user)
            return redirect('tweet_list')
    else:

        form=UserRegistration()
            

    return render(request, 'registration/register.html',{'form':form})


    
# Create your views here.
