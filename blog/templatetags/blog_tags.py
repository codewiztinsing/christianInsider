from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown
from ..models import Post

register = template.Library()

@register.simple_tag
def total_post():
    return Post.objects.count()


@register.inclusion_tag('post/latest_post.html')
def show_latest_posts(count = 3):
    latest_posts = Post.published.order_by('-publish')[:count]
    for post in latest_posts:
        print(post)
    return {'latest_post':latest_posts}


@register.simple_tag
def get_most_commented_posts(count = 3):
    return Post.objects.annotate(total_comments = Count('comments')).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
