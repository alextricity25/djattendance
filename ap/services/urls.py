from django.conf.urls import url
from . import views
from . import worker_select_views as wviews

urlpatterns = [
  url(r'^$', views.services_view, name='services_view'),
  url(r'^assign$', views.services_view, {'run_assign': True}, name='services_assign_view'),
  url(r'^generate_leaveslips$', views.services_view, {'generate_leaveslips': True}, name='services_generate_leaveslips'),
  url(r'^add_exception/$', views.AddExceptionView.as_view(), name='services-exception-add'),
  url(r'^update_exception/(?P<pk>\d+)$', views.UpdateExceptionView.as_view(), name='services-exception-update'),
  url(r'^delete_exception/(?P<pk>\d+)$', views.UpdateExceptionView.as_view(), name='services-exception-delete'),
  url(r'^generate_schedule_house$', views.generate_report, {'house': True}, name='services_schedule_house'),
  url(r'^generate_schedule$', views.generate_report, name='services_schedule'),
  url(r'^generate_signinr$', views.generate_signin, {'r': True}, name='rservices_signin'),
  url(r'^generate_signink$', views.generate_signin, {'k': True}, name='kservices_signin'),
  url(r'^generate_signino$', views.generate_signin, {'o': True}, name='oservices_signin'),
  url(r'^designated_service_hours/(?P<service_id>\d+)/(?P<week>\d+)', views.ServiceHours.as_view(), name='designated_service_hours'),
  url(r'^designated_service_hours$', views.ServiceHours.as_view(), name='designated_service_hours'),
  url(r'^service_hours_ta_view/(?P<week>\d+)', views.ServiceHoursTAView.as_view(), name='service_hours_ta_view'),
  url(r'^service_hours_ta_view$', views.ServiceHoursTAView.as_view(), name='service_hours_ta_view'),
  url(r'^designated_services_viewer$', views.DesignatedServiceViewer.as_view(), name='designated_services_viewer'),

  # Worker api
  url(r'^workers/gender/(?P<gender>[BS])/$', wviews.TraineesByGender.as_view()),
  url(r'^workers/term/(?P<term>[1234])/$', wviews.TraineesByTerm.as_view()),
  url(r'^workers/team/(?P<pk>\d+)/$', wviews.WorkersByTeam.as_view()),
  url(r'^workers/teamtype/(?P<type>\w+)/$', wviews.WorkersByTeamType.as_view()),
  url(r'^workers/house/(?P<pk>\d+)/$', wviews.WorkersByHouse.as_view()),
  url(r'^workers/locality/(?P<pk>\d+)/$', wviews.WorkersByLocality.as_view()),
  url(r'^workers/hc/$', wviews.WorkersHouseCoordinators.as_view()),
]
