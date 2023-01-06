from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .models import Post
from .forms import EmailPostForm
from django.views import generic
from django.core.mail import send_mail


class PostListView(generic.ListView):
	queryset  = Post.objects.all()
	context_object_name = 'posts'
	paginate_by = 3
	template_name = 'post/list.html'


def share_posts(request,post_id):
	post = get_object_or_404(Post,id = post_id,
			status = Post.Status.PUBLISHED
		)

	if request.method == 'POST':
		form = EmailPostForm(request.POST)
		if form.is_valid():
			LANGUAGE_CODE = form.cleaned_data
			post_url = request.build_absolute_uri(
				post.get_absolute_url()
				)
			subject = f"{cd['name']} recommends you read {post.title}"
			message = f"Read {post.title} at {post_url} {cd['name']}\'s comments: {cd['comments']}"
			send_mail(subject,message,'tinsingjobs2k@gmail.com',cd['to'])
			sent = True

	else:
		form = EmailPostForm()
		context = {
				'post':post,
				'form':form}
		return render(request,'post/share_post.html',context)




def post_list(request):

	post_list   = Post.objects.all()
	paginator   = Paginator(post_list,3)
	page_number = request.GET.get('page',1)
	try:
		posts 	= paginator.page(page_number)
	except PageNotAnInteger:	
		posts   = paginator.page(1)

	except EmptyPage:
		posts   = paginator.page(paginator.num_pages)

	
	context = {'posts':posts}
	return render(request,'post/list.html',context)


def post_detail(request,year,month,day,post):
	print(dir(request))
	post = get_object_or_404(
			Post,
			slug=post,
			status = Post.Status.PUBLISHED,
			publish__year  = year,
			publish__month = month,
			publish__day   = day
			
		)
	context = {'post':post}
	return render(request,'post/detail.html',context)