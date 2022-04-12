from django.shortcuts import render
from django.contrib.auth.models import User
from user.models import Profile
from .models import Post, Tag, TagToPostTable
from django.db.models import Q
from .distance_calculation import get_distance_between_coords

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
      #Query tag table for tags, then check posts associated with said tags, then get those posts.
      tags = Tag.objects.filter(Q(tag_name__icontains=search_string))
      posts = Post.objects.none()
      for tag in tags:
        tag_to_post_query_set = TagToPostTable.objects.filter(
          Q(tag_id=tag.id)
        )
        for tag_to_post in tag_to_post_query_set:
          serv_prov_bool = 1 if search_option == "service" else 0
          # adding to Post QuerySet
          posts = posts | Post.objects.filter(
            Q(id=tag_to_post.post_id) & 
            Q(service_provider=serv_prov_bool)
          )
      #Now we pass into context a list of all tags associated with one post.
      posts_and_their_tags = [] #list of [post_id, (list of tags)]
      temp_tags_from_post = [] #list of tags associated with one post
      for post in posts:
        post_to_tag_query_set = TagToPostTable.objects.filter(
          Q(post_id=post.id)
        )
        temp_tags_from_post = []
        for post_to_tag in post_to_tag_query_set:
          temp_tags_from_post.append(Tag.objects.get(
            Q(id=post_to_tag.tag_id)
          ))
        temp_post_and_tags_tuple = (post, temp_tags_from_post)
        posts_and_their_tags.append(temp_post_and_tags_tuple)

      search_type = "service" if search_option == "service" else "task"
      context = {
          'search_option': search_option,
          'search_order': search_order,
          'search_string': search_string,
          'search_type': search_type,
          'posts_and_their_tags': posts_and_their_tags,
      }
      return render(request, 'search/search.html', context)

  context = {
      'search_option': search_option,
      'search_order': search_order,
      'search_string': search_string,
  }
  return render(request, 'search/search.html', context)
