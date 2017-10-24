from django.conf.urls import url

from chores import views

urlpatterns = [
    url(r'^children$', views.ChildList.as_view(), name='child_list'),
    url(r'^children/(?P<pk>\d+)$', views.ChildDetail.as_view(), name='child_detail'),
    url(r'^children/new$', views.ChildCreate.as_view(), name='child_new'),
    url(r'^children/edit/(?P<pk>\d+)$', views.ChildUpdate.as_view(), name='child_edit'),
    url(r'^children/delete/(?P<pk>\d+)$', views.ChildDelete.as_view(), name='child_delete'),

    url(r'^tasks$', views.TaskList.as_view(), name='task_list'),
    url(r'^tasks/(?P<pk>\d+)$', views.TaskDetail.as_view(), name='task_detail'),
    url(r'^tasks/new$', views.TaskCreate.as_view(), name='task_new'),
    url(r'^tasks/edit/(?P<pk>\d+)$', views.TaskUpdate.as_view(), name='task_edit'),
    url(r'^tasks/delete/(?P<pk>\d+)$', views.TaskDelete.as_view(), name='task_delete'),
]
