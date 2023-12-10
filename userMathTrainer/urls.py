from django.urls import path
from userMathTrainer.views import *

urlpatterns = [
    path('', StartPageView, name='start_page'),
    path('court_us/', AboutUsView.as_view(), name='about_us'),
    path('course_detail/<int:pk>/', CourseDetail.as_view(), name='user_course_detail'),
    path('about_us/', ContactsView.as_view(), name='contacts'),
    path('all_courses/', ShowAllCourses.as_view(), name='courses'),
    path('lecture_detail/<int:pk>/', LectureDetailView.as_view(), name='lecture_detail'),
    path('module_detail/<int:pk>/', module_detail, name='module_detail'),
    path('add_data/', create_course_with_modules_and_lectures, name='add'),
    path('sign_up/', SignUpView.as_view(), name='sign_up'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='profile'),
    path('show_my_courses/', UserCoursesView.as_view(), name='user_courses'),
    path('get_course/<int:pk>/', GetCourse, name='get_course'),
    path('my_education/<int:pk>/', UserCoursesView.as_view(), name='my_education'), 
    path('to_favorites/<int:pk>/', ToFavorites, name='to_favorites'),
    path('favorite_courses/<int:pk>/', UserFavoriteCoursesView.as_view(), name='favorite_courses')

]
