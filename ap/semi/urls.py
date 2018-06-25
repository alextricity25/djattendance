from django.conf.urls import url
from semi import views

urlpatterns = [
  url(r'^attendance/$', views.attendance_base, name='attendance-base'),
  url(r'^attendance/(?P<pk>\d+)$', views.AttendanceUpdate.as_view(), name='attendance'),
  url(r'^attendance-report/$', views.AttendanceReport.as_view(), name='attendance-report'),
]
