from django.urls import path
from .views import *
urlpatterns = [
    path('', StartPageView.as_view(), name='content_creator_dashboard'),
    path('add_math_course/', CreateNewCourseView, name='add_math_course'),
    path('add_module/<int:pk>/', CreateModuleView, name='add_module'),
    path('all_author_courses/<int:id>/', AllAuthorCoursesView.as_view(), name='all_author_courses'),
    path('course_detail/<int:pk>/', AuthorDetailCourseView.as_view(), name='course_detail'),
    path('module_detail/<int:pk>/', ModuleDetailView.as_view(), name='module_detail'),
    path('update_course/<int:pk>/', UpdateCourseView.as_view(), name='update_course'),
    path('delete_course/<int:pk>/', DeleteCourseView.as_view(), name='delete_course'),
    path('update_module/<int:pk>/', UpdateModuleView.as_view(), name='update_module'), 
    path('delete_module/<int:pk>/', DeleteModuleView.as_view(), name='delete_module'),
    path('add_lecture/<int:pk>/', AddLectureView, name='add_lecture'),
    path('lecture_detail/<int:pk>/', LectureDetailView.as_view(), name='lecture_detail'),
    path('add_test/<int:pk>/', AddCommonTestView, name='add_common_test'),
    path('add_choice_test/<int:pk>/', AddChoiceTestView, name='add_choice_test'),
    path('test_choice_detail/<int:pk>/', ChoiceTestDetail.as_view(), name='choice_test_detail'),
    path('add_answer/<int:pk>/', AddAnswerView, name='add_answer')

]