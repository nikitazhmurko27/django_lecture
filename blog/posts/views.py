from django.forms import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.views import View
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView


from .models import Post

"""
Post.objects.all().count() instead len()
Post.objects.filter(headline='test'), 
Lookups:
Post.objects.filter(headline__contains='test') #icontains - non register
Post.objects.filter(headline__lte='test') - less than equal, gte - great than equal
Post.objects.filter(date__gte='2021') - less than equal, gte - great than equal
Post.objects.filter(id__in=[1,2,3]) - in
Post.objects.filter(category__cluster__name__{lookup}) - connections
class Car():
    manufacture = models.ForeignKey('Manufacture', on_delete=models.CASCADE, related_name='cars')
    
class Manufacture(Model):
    pass
"""


def index(request):
    p = Post.objects.all()
    cats = p.values_list('categories', flat=True)
    context = {
        'posts': Post.objects.all(),
        'cats': cats
    }
    return render(
        request,
        'post/index.html',
        context
    )


def add(request):
    if request.method == 'GET':
        form = PostForm()
        context = {
            'form': form
        }
        return render(
            request,
            'post/add_post.html',
            context
        )
    if request.method == 'POST':

        fields = request.POST
        form = PostForm(fields)
        if form.is_valid():
            new_post = Post(title=form.cleaned_data['title'], content=form.cleaned_data['content'])
            new_post.save()
            return redirect('../') #from django url reverse
        else:
            context = {
                'form': form
            }
            return render(
                request,
                'post/add_post.html',
                context
            )


def single_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "GET":
        form = PostForm(initial={'title': post.title, 'content': post.content})
        context = {
            'post': Post.objects.get(id=post_id),
            'form': form,
        }
        return render(
            request,
            'post/single_post.html',
            context
        )
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post.title = request.POST['title']
            post.content = request.POST['content']
            post.save()
            return redirect('../')


class PostForm(forms.Form):
    """
    Field args:
    -required, -label, -initial, -widget, -validators
    Field types:
    Boolean, Choice(select), Date, Integer, Email
    Validation:
    Field.to_python, Field.validate ; Form.clean_{fieldname}, Form.clean()
    """
    title = forms.CharField(label='Enter title:', min_length=2)
    content = forms.CharField(label='Enter content:', max_length=100)

    def clean_title(self):
        title = self.cleaned_data['title']
        max_length = 5
        if len(title) > max_length:
            raise ValidationError(f'Title should be less than {max_length}')
        return title


class AddPostView (View):
    def get(self, request, *args, **kwargs):
        form = PostForm()
        context = {
            'form': form
        }
        return render(
            request,
            'post/add_post.html',
            context
        )

    def post(self, request, *args, **kwargs):
        fields = request.POST
        form = PostForm(fields)
        if form.is_valid():
            new_post = Post(title=form.cleaned_data['title'], content=form.cleaned_data['content'])
            new_post.save()
            return HttpResponseRedirect(reverse('posts:index'))
        else:
            context = {
                'form': form
            }
            return render(
                request,
                'post/add_post.html',
                context
            )


class PostsListView(ListView):
    model = Post
    template_name = 'post/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        # return Post.objects.all()
        return Post.objects.prefetch_related(
            'post_categories',
            'post_categories__category'
        )


class PostDetailView(DetailView):
    model = Post
    template_name = 'post/single_post.html'
    context_object_name = 'post'


class PostsCreateView(CreateView):
    model = Post
    template_name = 'post/add_post.html'
    context_object_name = 'post'
    fields = ['title', 'content']
