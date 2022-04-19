from .models import Post, Tag, TagToPostTable
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from django.contrib import messages
from django.views.generic import (
  CreateView,
  DetailView,
  ListView,
  UpdateView,
  DeleteView,
)
from user.models import Profile
from .distance_calculation import get_distance_between_coords, check_address_valid
import numpy

#-- User
def user_search(search_string, search_by):
  users = User.objects.filter(Q(username__icontains=search_string))
  search_type = "user"
  user_context = {
    'search_type': search_type,
    'users': users,
  }
  return user_context

def get_posts_from_tag_name(search_string, search_option):
  """Gets the posts associated to the tag in the search string.

  This is a helper function, not a view function.

  Args:
      search_string (str): A string that contains any of the tags in the
      database, such as 'gardening', 'cooking', 'construction', etc.
      search_option (str): Whether the search is for a task, service or user.
  """
  #-Get tags from searched string
  tags = Tag.objects.filter(Q(tag_name__icontains=search_string))
  posts = Post.objects.none()
  #check posts associated with tags
  for tag in tags:
    tag_to_post_query_set = TagToPostTable.objects.filter(
      Q(tag_id=tag.id)
    )
    #get posts associated with tags
    for tag_to_post in tag_to_post_query_set:
      is_service_provider = 1 if search_option == "service" else 0
      # adding to Post QuerySet
      posts = posts | Post.objects.filter(
        Q(id=tag_to_post.post_id) &
        Q(service_provider=is_service_provider)
      )
  return posts

def get_post_tags(posts):
  """Returns a 2-dimensional array of post tags. Each tag list corresponds to a
  post that was passed in. For example:

  # Post 1,        Post 2,     Post 3.
  [[Tag1, Tag2], [Tag1, Tag3], [Tag4]]

  Args:
      posts (list): The list of posts that match the search.
  """
  #-Get tags associated with each post
  temp_tags_from_post = [] #list of tags per each post
  post_tags = [] #double list of all tags per each post
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
    post_tags.append(temp_tags_from_post)
  return post_tags

#-- Service or Task
def service_or_task_search(request, search_lat, search_long, search_string, search_by, search_option):

  # Get the posts associated to the tag in search string.
  posts = get_posts_from_tag_name(search_string, search_option)
  print("Posts:", posts)

  post_tags = get_post_tags(posts)
  print("Post tags:", post_tags)

  #-Calculate and Order results based on distance
  #get distance list
  distances = []
  for post in posts:
    if(request.user.id != post.author_id and get_distance_between_coords(float(search_lat), float(search_long), post.latitude, post.longitude) == 0):
      distances.append("My Current Location.")
    else:
      distances.append(get_distance_between_coords(float(search_lat), float(search_long), post.latitude, post.longitude))

  #sort lists according to distance
  distances = numpy.array(distances)
  index_distance_order = distances.argsort()

  #re-order arrays according to distance. Least to Greatest.
  post_tags = numpy.array(post_tags,dtype=object)
  posts = numpy.array(posts)
  distances = numpy.array(distances)

  post_tags = post_tags[index_distance_order].tolist()
  posts = posts[index_distance_order].tolist()
  distances = distances[index_distance_order].tolist()

  #Put all the values into one big list. Because don't know how to iterate by index in templates.
  posts_with_tags_and_distances = [] #array of type: post, list of tags, distance
  for i in range(len(distances)):
    temp_list = []
    temp_list.append(posts[i])
    temp_list.append(post_tags[i])
    temp_list.append(distances[i])
    posts_with_tags_and_distances.append(temp_list)

  #-Context
  search_type = "service" if search_option == "service" else "task"
  service_or_task_context = {
    'search_type': search_type,
    'posts_with_tags_and_distances': posts_with_tags_and_distances,
    #'posts': posts,
    #'post_tags': post_tags,
    #'distances': distances,
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
  search_by: str = request.GET.get('search_by')
  # Get user's latitude.
  search_latitude: str = request.GET.get('search_latitude') if request.GET.get('search_latitude') else "";
  # Get user's longitude.
  search_longitude: str = request.GET.get('search_longitude') if request.GET.get('search_longitude') else "";

  context = {
    'search_option': search_option,
    'search_by': search_by,
    'search_string': search_string,
    'search_latitude': search_latitude,
    'search_longitude': search_longitude,
  }

  # Verify that the search is not empty.
  if(request.GET and search_string):
    if(search_option == "user"):
      user_context = user_search(search_string, search_by)
      context.update(user_context) #merge user's context with generic context

    elif(search_option == "service" or search_option == "task"):
      service_or_task_context = service_or_task_search(
        request,
        search_latitude,
        search_longitude,
        search_string,
        search_by,
        search_option
      )
      context.update(service_or_task_context) #merge service/task's context with generic context

  return render(request, 'search/search.html', context)

class PostDetailView(DetailView):
  model = Post

  # The template that should be rendered when accessing url pattern. By
  # default the template that is rendered follows the naming convention
  # '<app>/<model>_detail.html'.
  # template_name = 'search/post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
  """The class inherits the LoginRequiredMixin because the user must be logged
  in before creating advertisement posts, and we cannot use the @login_required
  decorator on a class.
  """
  model = Post

  # The fields to include in the post-creation page.
  fields = ['title', 'body', 'address', 'service_provider']

  # The template that should be rendered when accessing url pattern. By
  # default the template that is rendered follows the naming convention
  # '<app>/<model>_form.html'.
  # template_name = ''

  # The URL to which the user should be redirected upon successful creation of a post.
  # By default the user is redirected to the URL the post, given that the Post
  # model implements the get_absolute_url method.
  # success_url = ''

  def form_valid(self, form):
    """Validate address and assign author to post before creating it.

    The address needs to be converted into a coordinate and then saved before
    creating the advertisement post.

    This method needs to be overridden because a post needs an author before
    being created.
    """
    # TODO: Validate address and get coordinates before posting the form.

    # Make the form author be the user who is logged in and making the
    # request.
    form.instance.author = self.request.user
    return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  """The class inherits from UserPassesTestMixin because only the author of a post should be able to edit the post. Without this, anybody who is logged in can edit the post.
  """
  model = Post

  # The fields that need to be modified.
  fields = ['title', 'body', 'address', 'service_provider']

  def form_valid(self, form):
    """Validate address and assign author to post before updating it.

    The address needs to be converted into a coordinate and then saved before
    updating the advertisement post.

    This method needs to be overridden because a post needs an author before
    being created.
    """

    # Print the address in the update form.
    print("form address:", form.instance.address)

    # Get the address from the submitted update form.
    address = form.instance.address

    # Validate the address.
    is_address_valid = check_address_valid(address)

    # If the address is not valid:
    if not is_address_valid:
      # Show a warning saying the address is invalid.
      messages.warning(self.request, f'The address "{address}" is not valid.')

      # Pass the existing form as the context, otherwise the post update form
      # will be empty when the user is redirected to the form.
      context = { 'form': form }
      return render(self.request, 'search/post_form.html', context)

    # Make the form author be the user who is logged in and making the
    # request.
    form.instance.author = self.request.user

    # Show a success message when the post is saved.
    messages.success(self.request, f'The post has been updated.')
    return super().form_valid(form)

  def test_func(self):
    """The function is inherited from UserPassesTestMixin. The post can only be
    updated if the function returns True.

    Returns:
        boolean: Whether or not the person trying to update the post is the
        author.
    """
    # Get post trying to be update.
    post = self.get_object()
    # Check that editor and author are the same.
    if self.request.user == post.author:
      return True
    return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  model = Post
  # Send the users to the home page when the deletion is successful.
  success_url = '/'

  def test_func(self):
    # Get post trying to be delted.
    post = self.get_object()
    # Check that editor and author are the same.
    if self.request.user == post.author:
      return True
    return False