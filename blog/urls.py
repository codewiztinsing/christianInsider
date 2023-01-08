from django.urls import path
from .views import  PostListView,post_list,post_detail,share_posts,post_comment

app_name = 'blog'
urlpatterns = [
	#path('',PostListView.as_view(),name = 'post_list'),
	path('',post_list,name = 'post_list'),
	path('tag/<slug:tag_slug>',post_list,name = 'post_list_by_tag'),
	path('<int:year>/<int:month>/<int:day>/<slug:post>/',
		post_detail,name = 'post-detail'),
	path('<int:post_id>/share/',share_posts,name = 'post_share'),
	path('<int:post_id>/comment/',post_comment,name = 'post_comment')
]