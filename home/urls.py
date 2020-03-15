from django.urls import path
from . import views
from .views import PostListView,PostDetailView,PostDeleteView,PostCreateView

urlpatterns=[
    path('',PostListView.as_view(),name="home"),
    path('post/<int:pk>/',PostDetailView.as_view(),name='post-detail'),
    path('post/new/',PostCreateView.as_view(),name='post-create'),
    path('post/<int:pk>/delete',PostDeleteView.as_view(),name='post-delete'),
    path('post/<int:pk>/approve',views.approve, name='post-approve'),
    path('post/<int:pk>/deny',views.deny, name='post-deny')

]