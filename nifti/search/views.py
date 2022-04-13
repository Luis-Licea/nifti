from django.shortcuts import render
from django.contrib.auth.models import User
from user.models import Profile
from .models import Post, Tag, TagToPostTable
from django.db.models import Q
from .distance_calculation import get_distance_between_coords

#-- User
def user_search(search_string, search_order):
  users = User.objects.filter(Q(username__icontains=search_string))
  search_type = "user"
  user_context = {
    'search_type': search_type,
    'users': users,
  }
  return user_context

#-- Service or Task
def service_or_task_search(search_string, search_order, search_option):
  #-Get posts from searched string
  tags = Tag.objects.filter(Q(tag_name__icontains=search_string))
  posts = Post.objects.none()
  #check posts associated with tags
  for tag in tags:
    tag_to_post_query_set = TagToPostTable.objects.filter(
      Q(tag_id=tag.id)
    )
    #get posts associated with tags
    for tag_to_post in tag_to_post_query_set:
      serv_prov_bool = 1 if search_option == "service" else 0
      # adding to Post QuerySet
      posts = posts | Post.objects.filter(
        Q(id=tag_to_post.post_id) & 
        Q(service_provider=serv_prov_bool)
      )
  #-Get tags associated with each post
  posts_and_their_tags = [] #list of type: [post_id, (list of tags)]
  temp_tags_from_post = [] #list of tags per each post
  #check tags associated with posts
  for post in posts:
    post_to_tag_query_set = TagToPostTable.objects.filter(
      Q(post_id=post.id)
    )
    temp_tags_from_post = []
    #get tags associated with posts
    for post_to_tag in post_to_tag_query_set:
      temp_tags_from_post.append(Tag.objects.get(
        Q(id=post_to_tag.tag_id)
      ))
    temp_post_and_tags_tuple = (post, temp_tags_from_post)
    posts_and_their_tags.append(temp_post_and_tags_tuple)
  
  search_type = "service" if search_option == "service" else "task"
  service_or_task_context = {
    'search_type': search_type,
    'posts_and_their_tags': posts_and_their_tags,
  }
  return service_or_task_context

#-- Generic
def search(request):
  # Print all the variables in the request.
  print(f'\n{request.GET}\n')

  # Get either Service, Task, or User
  search_option: str = request.GET.get('search_option')
  # Get search string from search bar if it exists, else get an empty string.
  search_string: str = request.GET.get('search_string') if request.GET.get('search_string') else "";
  # Get result ordering.
  search_order: str = request.GET.get('search_order')

  context = {
    'search_option': search_option,
    'search_order': search_order,
    'search_string': search_string,
  }
  
  # Verify that the search is not empty.
  if(request.GET and search_string):
    if(search_option == "user"):
      user_context = user_search(search_string, search_order)
      context.update(user_context) #merge user's context with generic context

    elif(search_option == "service" or search_option == "task"):
      service_or_task_context = service_or_task_search(search_string, search_order, search_option)
      context.update(service_or_task_context) #merge service/task's context with generic context

  return render(request, 'search/search.html', context)
