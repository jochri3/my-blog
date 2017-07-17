from django.shortcuts import render,get_object_or_404
from .models import Post,Comment
from django.http import Http404
from .forms import PostForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from .forms import EmailPostForm,CommentForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from .forms import EmailPostForm, CommentForm, SearchForm
from haystack.query import SearchQuerySet






def list(request,tag_slug=None):
    object_list = Post.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])


    paginator = Paginator(object_list, 2) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        posts= paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    
    
    return render(request,'list.html',{'page': page,'posts': posts,'tag':tag})





def detail(request,id = None):
    post = get_object_or_404(Post,id=id)
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
            messages.success(request, 'Commented successfully!! It will be published by the Admin after approval', extra_tags='alert alert-success')
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        comment_form = CommentForm()

    # List of similar posts
        post_tags_ids = post.tags.values_list('id', flat=True)
        similar_posts = Post.objects.filter(tags__in=post_tags_ids)\
        .exclude(id=post.id)
        similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
        .order_by('-same_tags','-createtime')[:4]

    return render(request,'detail.html',{'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'similar_posts': similar_posts})
    
	
def create(request):
	create_form = PostForm(request.POST or None, request.FILES or None)
	if create_form.is_valid():
		create_form.save(commit = False)
		create_form.user = request.user
		post = create_form.save()
		messages.success(request, _('create successfully!!'), extra_tags='alert alert-success')
		return HttpResponseRedirect(post.get_absolute_url())
	context = {
        'form': create_form,
    }
	return render(request,'create.html', context)
	
    
def edit(request, id=None):
    instance = get_object_or_404(Post, id=id)
    edit_form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if edit_form.is_valid():
        edit_form.save()
        messages.success(request, _('updated successfully!!'), extra_tags='alert alert-success')
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
    'form': edit_form 
    }
    return render(request, 'edit.html', context)
    


def delete(request,id = None):
	post = get_object_or_404(Post,id=id)
	if post.delete():
		messages.success(request, _('delete successfully!!'), extra_tags='alert alert-success')
		return HttpResponseRedirect('/')


	return render(request,'delete.html',)


def post_share(request, post_id):
# Retrieve post by id
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
# Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
# Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com',[cd['to']])
            sent = True
            messages.success(request, 'shared successfully!!', extra_tags='alert alert-success')
            return HttpResponseRedirect(post.get_absolute_url())
# ... send email
    else:
        form = EmailPostForm()
    return render(request, 'share.html', {'post': post,'form': form})








def post_search(request):
    form = SearchForm()
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            results = SearchQuerySet().models(Post)\
            .filter(content=cd['query']).load_all()
            # count total results
            total_results = results.count()
        return render(request, 'search.html', {'form': form,
                                                         'cd': cd,
                                                         'results': results,
                                                         'total_results': total_results})


    return render(request, 'search.html', {'form': form,})