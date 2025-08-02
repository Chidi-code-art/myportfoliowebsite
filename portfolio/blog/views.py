from django.shortcuts import render, get_object_or_404
from .models import Posts

# Create your views here.
#for the home page:
def home(request):
        #collecting all data from the database using a query
        all_posts = Posts.objects.all().order_by('-post_date') #then put this in the posts.html template
        return render(request, 'index.html', {'posts': all_posts}) #refrencing it as posts


#for the single post:
def post_single(request, post):
    post = get_object_or_404(Posts, slug=post)
    return render(request, 'post.html', {'post':post})



#for the likes button
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Posts
import json

@require_POST
def like_post(request, post_id):
    try:
        post = Posts.objects.get(id=post_id)

        # Track likes via session for anonymous users
        liked_posts = request.session.get('liked_posts', [])
        if post_id in liked_posts:
            return JsonResponse({'status': 'error', 'message': 'Already liked'}, status=400)

        post.likes += 1
        post.save()

        liked_posts.append(post_id)
        request.session['liked_posts'] = liked_posts
        request.session.modified = True

        return JsonResponse({'status': 'success', 'likes': post.likes})

    except Posts.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Post not found'}, status=404)


def get_likes(request, post_id):
    try:
        post = Posts.objects.get(id=post_id)
        return JsonResponse({'status': 'success', 'likes': post.likes})
    except Posts.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Post not found'}, status=404)
