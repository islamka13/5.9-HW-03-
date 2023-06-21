from django.urls import path, include
from .forms import upgrade_me, subscribe
from django.contrib.auth.views import LoginView, LogoutView
from .views import PostList, AuthorList, PostDetail,\
     IndexView, BaseRegisterView, CategoryList, AuthorDetail, PostCategory, \
     PostCreateView, PostDeleteView, PostUpdateView, AppointmentView


urlpatterns = [path('', IndexView.as_view()),
               path('upgrade/', upgrade_me, name='upgrade'),
               path('login/', LoginView.as_view(template_name='login.html'), name='login'),
               path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
               path('signup/', BaseRegisterView.as_view(template_name='signup.html'), name='signup'),
               path('news/', PostList.as_view(), name='posts-list'),
               path('author/', AuthorList.as_view(), name='authors'),
               path('author/<int:pk>', AuthorDetail.as_view(), name='author'),
               path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
               path('news/create/', PostCreateView.as_view(), name='post_create'),
               path('news/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
               path('news/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
               path('category/', CategoryList.as_view(), name='categories'),
               path('category/<int:pk>', PostCategory.as_view(), name='posts_of_category_list'),
               path('category/<int:pk>/', subscribe, name='subscribers'),
               path('accounts/', include('allauth.urls')),
               path('appoinment/', AppointmentView.as_view(), name='make_appointment'),
               ]
