from .models import Post, Tag, TagToPostTable
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import (
  CreateView,
  DetailView,
  ListView,
  UpdateView,
  DeleteView,
)
from user.models import Profile
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

# class PostListView(ListView):
#   model = Post
#   template_name = 'search/search.html'
#   context_object_name = 'posts'
#   # ordering = ['date_posted']
#   ordering = ['-date_posted']

#   def get_queryset(self):
#     # print(self.request.GET)
#     # return search(self.request)
#     # query = self.request.GET.get('q')
#     # return Post.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))

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
    # TODO: Validate address and get coordinates before posting the form.

    # Make the form author be the user who is logged in and making the
    # request.
    form.instance.author = self.request.user
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