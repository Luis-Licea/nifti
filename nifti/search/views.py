from django.shortcuts import render

# Create your views her/e.
def search(request):
  users = [
    {
      'username': 'Username1',
      'first': 'First1',
      'middle': 'Middle1',
      'last': 'Last1',
      'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
      'image_url': 'https://upload.wikimedia.org/wikipedia/commons/0/0f/Grosser_Panda.JPG',
    },
    {
      'username': 'Username2',
      'first': 'First2',
      'middle': 'Middle2',
      'last': 'Last2',
      'description': 'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM',
      'image_url': 'https://upload.wikimedia.org/wikipedia/commons/0/0f/Grosser_Panda.JPG',
    },
    {
      'username': 'Username3',
      'first': 'First3',
      'middle': 'Middle3',
      'last': 'Last3',
      'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
      'image_url': 'https://upload.wikimedia.org/wikipedia/commons/0/0f/Grosser_Panda.JPG',
    },
    {
      'username': 'Username4',
      'first': 'First4',
      'middle': 'Middle4',
      'last': 'Last4',
      'description': '',
      'image_url': 'https://upload.wikimedia.org/wikipedia/commons/0/0f/Grosser_Panda.JPG',
    },
    {
      'username': 'Username5',
      'first': 'First4',
      'middle': 'Middle4',
      'last': 'Last4',
      'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
      'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Red_Panda_%2824986761703%29.jpg/1280px-Red_Panda_%2824986761703%29.jpg',
    },
    {
      'username': 'Username6',
      'first': 'First4',
      'middle': 'Middle4',
      'last': 'Last4',
      'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
      'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Red_Panda_%2824986761703%29.jpg/1280px-Red_Panda_%2824986761703%29.jpg',
    },
    {
      'username': 'Username6',
      'first': 'First4',
      'middle': 'Middle4',
      'last': 'Last4',
      'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
      'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Red_Panda_%2824986761703%29.jpg/1280px-Red_Panda_%2824986761703%29.jpg',
    },
    {
      'username': 'Username7',
      'first': 'First4',
      'middle': 'Middle4',
      'last': 'Last4',
      'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
      'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Red_Panda_%2824986761703%29.jpg/1280px-Red_Panda_%2824986761703%29.jpg',
    },
    {
      'username': 'Username8',
      'first': 'First4',
      'middle': 'Middle4',
      'last': 'Last4',
      'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
      'image_url': '',
    },
  ]
  context = {
    'users': users,
  }
  return render(request, 'search/search.html', context)