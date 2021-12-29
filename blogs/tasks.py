from main.celery import app

from .models import Post
from .services import send_html_email


@app.task
def send_email_to_subscribers(post_pk):
    post = Post.objects.get(pk=post_pk)
    send_html_email(post)
