from django.urls import path
from . import views
from .views import PostListView,PostDetailView,PostDeleteView,PostCreateView,PostUpdateView

urlpatterns=[
    path('',PostListView.as_view(),name="home"),
    path('post/<int:pk>/',PostDetailView.as_view(),name='post-detail'),
    path('post/new/',PostCreateView.as_view(),name='post-create'),
    path('post/<int:pk>/delete',PostDeleteView.as_view(),name='post-delete'),
    path('post/<int:pk>/update',PostUpdateView.as_view(),name='post-update'),
    path('post/<int:pk>/approve',views.approve, name='post-approve'),
    path('post/<int:pk>/deny',views.deny, name='post-deny'),
    path('user/<str:username>', views.userDetail, name='user-detail'),
    path('all_donations/', views.get_all_donations, name='all-donations'),
    path('about/',views.about,name="about-us"),

]