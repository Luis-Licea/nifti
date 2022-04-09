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
  search_option: str = request.GET.get('search_option')

  # Get search string from search bar if it exists, else get an empty string.
  search_string: str = request.GET.get('search_string') if request.GET.get('search_string') else "";

  # Get result ordering.
  search_order: str = request.GET.get('search_order')


  # Verify that the query is not empty.
  if(request.GET and search_string):
    results = True
    search_type = ''
    users = ''
    posts = ''
    searched_for = ''

    #User Search
    if(search_option == "user"):
      users = User.objects.filter(Q(username__icontains=search_string))
      # service_or_task_search, distance_search
      search_type = 'user_search'
      context = {
          'search_option': search_option,
          'search_order': search_order,
          'search_string': search_string,
          'search_type': search_type,
          'users': users,
      }
      return render(request, 'search/search.html', context)

    #Service/Task Search
    elif(search_option == "service" or search_option == "task"):
      #service provider
      if (search_option == "service"):
        #Check matching tags, then check posts associated with said tags, then get those posts.
        tags = Tag.objects.filter(Q(tag_name__icontains=search_string))
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
          'search_option': search_option,
          'search_order': search_order,
          'search_string': search_string,
          'search_type': search_type,
          'posts': posts,
      }
      return render(request, 'search/search.html', context)

  context = {
      'search_option': search_option,
      'search_order': search_order,
      'search_string': search_string,
  }
  return render(request, 'search/search.html', context)
