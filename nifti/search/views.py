from .models import Post, Tag, TagToPostTable
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
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
def user_search(search_string):
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
      is_service_provider: bool = 1 if search_option == "service" else 0
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

def get_post_distances(posts, request, search_lat, search_long):
  """Returns the distance associated to each post in the list. The distances are
  in the same order as the posts.

  Args:
      posts (list): The list of posts that match the search query.
  """
  # Create empty distance list.
  distances = []
  for post in posts:
    if(request.user.id != post.author_id and get_distance_between_coords(float(search_lat), float(search_long), post.latitude, post.longitude) == 0):
      distances.append("My Current Location.")
    else:
      distances.append(get_distance_between_coords(float(search_lat), float(search_long), post.latitude, post.longitude))

  #get distance list
  return distances

def get_posts_from_title(search_string, search_option):
  # Determine if search is for service provider.
  is_service_provider: bool = 1 if search_option == "service" else 0
  # Filter the posts using the title and service provider values.
  return Post.objects.filter(Q(title__icontains=search_string) &
                              Q(service_provider=is_service_provider))

#-- Service or Task
def service_or_task_search(request, search_lat, search_long, search_string, search_by, search_option):

  if search_by == 'tag':
    # Get posts associated to the tag.
    posts = get_posts_from_tag_name(search_string, search_option)
  elif search_by == 'title':
    # Get posts by title.
    posts = get_posts_from_title(search_string, search_option)

  # View the posts in the terminal.
  print("Posts:", posts)

  # Get the distance from current location for each post.
  distances = get_post_distances(posts, request, search_lat, search_long)
  print("Distances:", distances)

  # Convert lists to numpy arrays.
  posts = numpy.array(posts)
  distances = numpy.array(distances)

  #sort lists according to distance
  index_distance_order = distances.argsort()
  print("Index distance order", index_distance_order)

  #re-order arrays according to distance. Least to Greatest.
  # Convert numpy array to Python list.
  posts = posts[index_distance_order].tolist()
  distances = distances[index_distance_order].tolist()

  # Get the tags associated to each post after the posts have been
  # sorted by distance.
  post_tags = get_post_tags(posts)
  print("Post tags:", post_tags)

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
  # Get search by tag or title.
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
      user_context = user_search(search_string)
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

  # Get the results.
  if 'posts_with_tags_and_distances' in context.keys():
    # Get advertisement post results.
    object_list = context['posts_with_tags_and_distances']
  elif 'users' in context.keys():
    # Get user profile results.
    object_list = context['users']
  else:
    # Create empty results list.
    object_list=[]

  # If search results exist:
  if object_list:
    # Show 5 posts in each page.
    paginator = Paginator(object_list, 5)
    # Get the page number from the URL.
    page = request.GET.get('page')
    try:
        # Try to retrieve page.
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, then return first page.
        page_obj = paginator.page(1)
    except EmptyPage:
        # If page is out of range, then return last page.
        page_obj = paginator.page(paginator.num_pages)

    # Save variables in context that will be passed down to template.
    context.update({
      # The page object stores the page results.
      'page_obj': page_obj,
      # Only show pagination links when there is more than 1 page.
      'is_paginated': page_obj.has_other_pages()
    })
    print("\nContext:", context)

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
    # Print the address in the create form.
    print("form address:", form.instance.address)

    # Get the address from the submitted create form.
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
    messages.success(self.request, 'The post has been created.')
    return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  """The class inherits from UserPassesTestMixin because only the author of a post should be able to edit the post. Without this, anybody who is logged in can edit the post.
  """
  model = Post

  # The fields that need to be modified.
  fields = ['title', 'body', 'address', 'service_provider']

  def get_context_data(self, *args, **kwargs):
    context = super(PostUpdateView, self).get_context_data(*args, **kwargs)
    #Getting tags from DB
    self_post_id = self.get_object().id
    post_to_tag_query_set = TagToPostTable.objects.filter(
      Q(post_id=self_post_id)
    )
    post_tags = []
    #get tags associated with post
    for post_to_tag in post_to_tag_query_set:
      post_tags.append(Tag.objects.get(Q(id=post_to_tag.tag_id)))
    context['tags'] = post_tags
    context['tag_count'] = len(post_tags)
    context['update_post'] = True
    return context

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

    #Tag Operations---#
    arr_tags = self.request.POST.get("tagsToModifyInput").split("+")
    arr_tags.pop(0) #get rid of first empty '' element
    #print(arr_tags)

    #Remove deleted tags from TagToPostTable
    tag_to_post_entries_for_post = TagToPostTable.objects.filter(Q(post_id=self.get_object().id))
    for tag_to_post_entry in tag_to_post_entries_for_post:
      #get name from tag table
      temp_tag_name = Tag.objects.get(id=tag_to_post_entry.tag_id).tag_name
      if(temp_tag_name not in arr_tags):
        #waste the mf
        tag_to_post_entry.delete()

    #Add new tags.
    for tag in arr_tags:
      check_tag_id = -1
      #create new entry in Tag table if tag does not exist
      if(not Tag.objects.filter(Q(tag_name=tag))):
        new_tag = Tag(tag_name=tag)
        new_tag.save()
        check_tag_id = new_tag.id
      else:
        print("tag name: " + str(tag))
        check_tag_id = Tag.objects.get(Q(tag_name=tag)).id
      #check if there is a tag_to_post entry for the specific tag
      if(not TagToPostTable.objects.filter(Q(post_id= self.get_object().id) & Q(tag_id=check_tag_id))):
        new_tag_to_post_table_entry = TagToPostTable(post_id= self.get_object().id,tag_id=check_tag_id)
        new_tag_to_post_table_entry.save()
    #End Tag Operations---#

    # Make the form author be the user who is logged in and making the request.
    form.instance.author = self.request.user
    
    # Show a success message when the post is saved.
    messages.success(self.request, 'The post has been updated.')
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
  # This is overwritten by get_success_url.
  # success_url = '/'

  def get_success_url(self):
    # After deleting a post, resturn user to post list.
    return reverse('user-post-list', kwargs={'username': self.request.user })

  def test_func(self):
    # Get post trying to be delted.
    post = self.get_object()
    # Check that editor and author are the same.
    if self.request.user == post.author:
      return True
    return False