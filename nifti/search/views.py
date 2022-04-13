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
      print(context)
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
      print(context)
      return render(request, 'search/search.html', context)

  context = {
      'search_option': search_option,
      'search_order': search_order,
      'search_string': search_string,
  }
  print(context)
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