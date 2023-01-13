from django.shortcuts import render,get_object_or_404
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .models import Post,Comment
from .forms import EmailPostForm,CommentForm
from django.views import generic
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count


class PostListView(generic.ListView):
	queryset  = Post.objects.all()
	context_object_name = 'posts'
	paginate_by = 3
	template_name = 'post/list.html'


def share_posts(request,post_id):
	post = get_object_or_404(Post,id = post_id,
			status = Post.Status.PUBLISHED
		)
	sent = False
	context = {}

	if request.method == 'POST':
		form = EmailPostForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			post_url = request.build_absolute_uri(
				post.get_absolute_url()
				)
			subject = f"{cd['name']} recommends you read {post.title}"
			message = f"Read {post.title} at {post_url} {cd['name']}\'s comments: {cd['comments']}"
			send_mail(subject,message,'tinsingjobs2k@gmail.com',[cd['to']])
			sent = True
			context = {
				'post':post,
				'form':form,
				'sent':True
				}

	else:
		form = EmailPostForm()
		context = {
				'post':post,
				'form':form,
				}
	return render(request,'post/share.html',context)




def post_list(request,tag_slug=None):
	post_list   = Post.objects.all()
	tag = None

	if(tag_slug):
		tag = get_object_or_404(Tag,slug=tag_slug)
		post_list = post_list.filter(tags__in=[tag])

	paginator   = Paginator(post_list,3)
	page_number = request.GET.get('page',1)
	try:
		posts 	= paginator.page(page_number)
	except PageNotAnInteger:	
		posts   = paginator.page(1)

	except EmptyPage:
		posts   = paginator.page(paginator.num_pages)

	context = {
				'posts':posts,
				'tag':tag
				}
	return render(request,'post/list.html',context)


def post_detail(request,year,month,day,post):
	post = get_object_or_404(
			Post,
			slug=post,
			status = Post.Status.PUBLISHED,
			publish__year  = year,
			publish__month = month,
			publish__day   = day
			
		)

	post_tags_ids = post.tags.values_list('id',flat=True)
	similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)

	comments = post.comments.filter(active=True)
	commentForm = CommentForm()
	context = {
		'post':post,
		'similar_posts':similar_posts,
		'comments':comments,
		'commentForm':commentForm
		}
	return render(request,'post/detail.html',context)


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, \
                                   status=Post.Status.PUBLISHED)
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()
    return render(request, 'post/comment.html',
                           {'post': post,
                            'form': form,
                            'comment': comment})