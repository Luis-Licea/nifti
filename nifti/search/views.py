from django.shortcuts import render
from django.contrib.auth.models import User
from user.models import Profile
from .models import Post, Tag, TagToPostTable
from django.db.models import Q


# Create your views here.
def search(request):
  #handle which queries to make based on checkboxes
  print('\n\n' + str(request.GET.get('flexSwitchUser')) + '\n\n')

  if(request.GET and 
    request.GET.get('search_bar') != "" and 
    request.GET.get('search_bar') != None
  ):
    results = True
    search_type = ''
    users = ''
    posts = ''
    searched_for = ''

    #User Search
    if(request.GET.get('flexSwitchUser') == "on"):
      users = User.objects.filter(Q(username__icontains=request.GET.get('search_bar')))
      search_type = 'user_search' #service_or_task_search, distance_search
      context = {
        'search_type': search_type,
        'users': users,
      }
      return render(request, 'search/search.html', context)

    #Service/Task Search
    elif(request.GET.get('flexSwitchService') == "on" or request.GET.get('flexSwitchTask') == "on"):
      #service provider
      if (request.GET.get('flexSwitchService') == "on"):
        #Check matching tags, then check posts associated with said tags, then get those posts.
        tags = Tag.objects.filter(Q(tag_name__icontains=request.GET.get('search_bar')))
        posts = Post.objects.none()
        for tag in tags:
          tag_to_post_query_set = TagToPostTable.objects.filter(Q(tag_id=tag.id)) 
          for tag_to_post in tag_to_post_query_set:
            posts = posts | Post.objects.filter(Q(id=tag_to_post.post_id)) #adding to Post QuerySet

        #TODO: now we want to pass into context a list of all tags associated with one post.
        #potentially double-array or a dictionary

      search_type = 'service_or_task_search'
      context = {
        'search_type': search_type,
        'posts': posts,
      }
      return render(request, 'search/search.html', context)


  return render(request, 'search/search.html')