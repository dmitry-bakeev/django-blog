from django import forms

from .models import Post, Blog


class PostForm(forms.ModelForm):

    def save(self, user, commit=True):
        post = super().save(commit=False)
        blog = Blog.objects.filter(user=user).first()
        post.blog = blog

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
