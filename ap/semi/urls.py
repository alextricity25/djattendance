from django.conf.urls import url
from semi import views

urlpatterns = [
  # url(r'^admin/$', views.GospelTripView.as_view(), name='admin-create'),
  # url(r'^admin/(?P<pk>\d+)$', views.gospel_trip_admin_update, name='admin-update'),
  # url(r'^upload/$', views.upload_image, name='upload-image'),
  # url(r'^admin/(?P<pk>\d+)/delete$', views.gospel_trip_admin_delete, name='admin-delete'),
  # url(r'^admin/(?P<pk>\d+)/duplicate$', views.gospel_trip_admin_duplicate, name='admin-duplicate'),
  url(r'^attendance/$', views.attendance_base, name='attendance-base'),
  url(r'^attendance/(?P<pk>\d+)$', views.AttendanceUpdate.as_view(), name='attendance'),
  # url(r'^report/(?P<pk>\d+)$', views.GospelTripReportView.as_view(), name='report'),
  # url(r'^admin/(?P<pk>\d+)/destinations/$', views.DestinationEditorView.as_view(), name='destination-editor'),
  # url(r'^admin/(?P<pk>\d+)/destinations/add$', views.destination_add, name='destination-add'),
  # url(r'^admin/(?P<pk>\d+)/destinations/remove$', views.destination_remove, name='destination-remove'),
  # url(r'^admin/(?P<pk>\d+)/destinations/edit$', views.destination_edit, name='destination-edit'),
  # url(r'^admin/(?P<pk>\d+)/destinations/team-contact$', views.assign_team_contact, name='assign-team-contact'),
  # url(r'^admin/(?P<pk>\d+)/destinations/assign-destination$', views.assign_destination, name='assign-destination'),
  # url(r'^admin/(?P<pk>\d+)/by-preference/$', views.DestinationByPreferenceView.as_view(), name='by-preference'),
  # url(r'^admin/(?P<pk>\d+)/by-group/$', views.DestinationByGroupView.as_view(), name='by-group'),
  # url(r'^admin/(?P<pk>\d+)/rosters-all/$', views.RostersAllTeamsView.as_view(), name='rosters-all'),
  # url(r'^admin/(?P<pk>\d+)/rosters-individual/$', views.RostersIndividualTeamView.as_view(), name='rosters-individual'),
]
