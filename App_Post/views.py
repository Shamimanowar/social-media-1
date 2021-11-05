from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from App_Post.models import Post,Like
from App_Login.models import Follow
# Create your views here.

@login_required
def home(request):
    dict = {}

    following_list = Follow.objects.filter(follower=request.user)
    posts = Post.objects.filter(author__in=following_list.values_list('following'))
    dict.update({'posts': posts})

    liked_post = Like.objects.filter(user=request.user)
    liked_post_list = liked_post.values_list('post', flat=True)
    dict.update({'liked_post_list': liked_post_list})

    if request.method == 'GET':
        search = request.GET.get('search')
        dict.update({'search': search})
        if search:
            result = User.objects.filter(username__icontains=search)
            dict.update({'result': result})
    dict.update({'title': 'Home'})
    return render(request, 'App_Post/home.html', context=dict)


@login_required
def like(request, pk):
    post = Post.objects.get(pk=pk)
    already_liked = Like.objects.filter(post=post, user=request.user)
    if not already_liked:
        like = Like(user=request.user, post=post)
        like.save()
    return HttpResponseRedirect(reverse('home'))

@login_required
def unlike(request, pk):
    post = Post.objects.get(pk=pk)
    already_liked = Like.objects.filter(post=post, user=request.user)
    if already_liked:
        already_liked.delete()
    return HttpResponseRedirect(reverse('home'))
