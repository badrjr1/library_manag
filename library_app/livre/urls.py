from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import Register , logIn , home , logOut , profile_view , pagelivre , book_search , update_user,dashboard_page
urlpatterns=[
    path("",home,name='home'),
    path('login/', logIn, name='login'),
    path('logout/', logOut, name='logout'),
    path('register/', Register, name='register'),
    path('profile/', profile_view, name='profile'),
    path('livre/<int:livre_id>/', pagelivre, name='pagelivre'),
    path('search/', book_search, name='book_search'), 
    path('update_user/', update_user, name='update_user'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
