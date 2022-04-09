from django.shortcuts import render
from django.contrib.auth.models import User
from user.models import Profile
from .models import Post, Tag, TagToPostTable
from django.db.models import Q


# Create your views here.
def search(request):
  """Handle which queries to make based on checkboxes."""

  # Print all the variables in the request.
  print(f'\n{request.GET}\n')

  # Get either Service, Task, or User
  search_type: str = request.GET.get('search_type')

  # Get search string from search bar.
  search_str: str = request.GET.get('search_bar')

  # Get result ordering.
  search_ord: str = request.GET.get('ordering')


  # Verify that the query is not empty.
  if(request.GET and search_str):
    results = True
    users = ''
    posts = ''
    searched_for = ''

    #User Search
    if(search_type == "User"):
      users = User.objects.filter(Q(username__icontains=search_str))
      # service_or_task_search, distance_search
      search_type = 'user_search'
      context = {
          'search_type': search_type,
          'users': users,
      }
      return render(request, 'search/search.html', context)

    #Service/Task Search
    elif(search_type == "Service" or search_type == "Task"):
      #service provider
      if (search_type == "Service"):
        #Check matching tags, then check posts associated with said tags, then get those posts.
        tags = Tag.objects.filter(Q(tag_name__icontains=search_str))
        posts = Post.objects.none()
        for tag in tags:
          tag_to_post_query_set = TagToPostTable.objects.filter(
              Q(tag_id=tag.id))
          for tag_to_post in tag_to_post_query_set:
            # adding to Post QuerySet
            posts = posts | Post.objects.filter(
                Q(id=tag_to_post.post_id))

        #TODO: now we want to pass into context a list of all tags associated with one post.
        #potentially double-array or a dictionary

      search_type = 'service_or_task_search'
      context = {
          'search_type': search_type,
          'posts': posts,
      }
      return render(request, 'search/search.html', context)

  return render(request, 'search/search.html')