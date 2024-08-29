from django.urls import path
from . import views
from django.views.generic.base import RedirectView
urlpatterns = [
	path('', views.test_creation_page, name='home'),
	path('test/', views.test_page, name='test'),
	path('tests/', views.tests_page, name='tests'),
	
	# path('signup/', views.signupuser, name='signup'),
	# path('logout/', views.logoutuser, name='logout'),
	# path('login/', views.loginuser, name='login'),

	path('signup/', RedirectView.as_view(url='/'), name='signup'),
	path('logout/', RedirectView.as_view(url='/'), name='logout'),
	path('login/', RedirectView.as_view(url='/'), name='login'),

	path('get_packs/<int:subsection_id>/', views.get_packs, name='get_packs'),
	path('get_subsections/<int:section_id>/', views.get_subsections, name='get_subsections'),
	path('get_tasks_for_pack/<int:pack_id>/', views.get_tasks_for_pack, name='get_tasks_for_pack'),
	# path('get_selected_tasks/', views.get_selected_tasks, name='get_selected_tasks'),
	path('get_correct_answers/', views.get_correct_answers, name='get_correct_answers'),
	path('get_tests/', views.get_tests, name='get_tests'),
]
