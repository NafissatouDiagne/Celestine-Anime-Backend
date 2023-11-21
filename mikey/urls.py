from django.urls import path
from .views import CommentAPIView ,CommentDetailAPIView
from . import views
urlpatterns =[
    path('register/',views.register,name='register'),
    path('login_auth/',views.login_auth,name='login_auth'),
    path('updatephoto/<int:user_id>/',views.updatephoto,name='updatephoto'),
    path('api/comments/<int:pseudo_id>/', CommentAPIView.as_view(), name='comment_api'), 
    path('api/comments/<int:pseudo_id>/', CommentAPIView.as_view(), name='comment-list'),
    path('api/comments/<int:pseudo_id>/<int:comment_id>/', CommentDetailAPIView.as_view(), name='comment-detail'),

]