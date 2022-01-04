from django import forms

from .models import Post

from .services import get_user_blog


class PostForm(forms.ModelForm):

    def save(self, user, commit=True):
        post = super().save(commit=False)
        user_blog = get_user_blog(user=user)
        post.blog = user_blog

        if commit:
            post.save()
            self.save_m2m()

        return post

    class Meta:
        model = Post
        fields = (
            'title',
            'text',
        )
