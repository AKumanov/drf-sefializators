from django.urls import path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import renderers

from .views import SnippetViewSet, UserViewSet, OrderViewSet

snippet_list = SnippetViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

snippet_detail = SnippetViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})

orders_list = OrderViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

orders_detail = OrderViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})

snippet_highlight = SnippetViewSet.as_view({
    'get': 'highlight',
}, renderer_classes=[renderers.StaticHTMLRenderer])

user_list = UserViewSet.as_view({
    'get': 'list'
})

user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})

urlpatterns = [
    path('snippets/', snippet_list, name='snippet-list'),
    path('orders/', orders_list, name='orders-list'),
    path('orders/<int:pk>/', orders_detail, name='orders-detail'),
    path('snippets/<int:pk>/', snippet_detail, name='snippet-detail'),
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail'),
    path('', views.api_root),
    path('snippets/<int:pk>/highlight/', snippet_highlight, name='snippet-highlight'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
