from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.contrib.auth.decorators import login_required
from adminMathTrainer.models import *
from .forms import *


def simplified_path(path: str):
    return f'userMathTrainer/{path}.html'


def StartPageView(request):
    user_auth = request.user.is_authenticated
    user = request.user if user_auth else None

    if user_auth and request.user.is_author:
        return redirect('content_creator_dashboard')

    context = {'user': user, 'user_auth': user_auth}
    return render(request, simplified_path('startPage'), context)


class ShowAllCourses(ListView):
    template_name = simplified_path('allCourses')
    model = MathCourse

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context



class AboutUsView(TemplateView):
    template_name = simplified_path('aboutUs')


class ContactsView(TemplateView):
    template_name = simplified_path('contacts')


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signUp.html'
    success_url = '/login/'


class LectureDetailView(DetailView):
    template_name = simplified_path('lectureDetail')
    model = Lecture


class CourseDetail(DetailView):
    template_name = simplified_path('course_detail')
    model = MathCourse
    context_object_name = 'course'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.object

        modules = CourseModule.objects.filter(math_course=course)
        lectures = Lecture.objects.filter(course_module__in=modules)

        context['modules'] = modules
        context['lectures'] = lectures
        return context


def module_detail(request, pk):
    module = get_object_or_404(CourseModule, id=pk)
    context = {'lectures_list': Lecture.objects.filter(course_module=module)}

    return render(request, simplified_path('moduleDetail'), context)


class UserProfileView(DetailView):
    template_name = simplified_path('userProfile')
    model = User


@login_required
def GetCourse(request, pk):
    course = get_object_or_404(MathCourse, id=pk)
    course.course_user.add(request.user)
    return redirect('courses')

@login_required
def ToFavorites(request, pk):
    course = get_object_or_404(MathCourse, id=pk)
    course.user_favorites.add(request.user)
    return redirect('courses')


def create_course_with_modules_and_lectures(request):
    math_course = MathCourse.objects.create(
        title="Math Course 1",
        description="This is a math course.",
        author=1,
    )

    module1 = CourseModule.objects.create(
        title="Module 1",
        description="This is module 1 of the math course.",
        math_course=math_course,
    )

    module2 = CourseModule.objects.create(
        title="Module 2",
        description="This is module 2 of the math course.",
        math_course=math_course,
    )

    for module in [module1, module2]:
        for i in range(2):
            Lecture.objects.create(
                title=f"Lecture {i + 1} for {module.title}",
                description=f"This is small description of  lecture {i + 1} for {module.title}.",
                paragraph=f"This is paragraph {i + 1} for {module.title}. I am fairly new to django and creating a website that involves account creation. The standard form UserCreationForm is fairly ugly. My main issue with it is that it displays a list of information under the password field. It displays the code in html as follows:",
                course_module=module,
            )

    return redirect('start_page')


class UserCoursesView(ListView):
    template_name = simplified_path('userCourses')
    model = MathCourse

    def get_queryset(self):
        user_id = self.request.user.id
        return MathCourse.objects.filter(course_user=user_id)

class UserFavoriteCoursesView(ListView):
    template_name = simplified_path('userCourses')
    model = MathCourse

    def get_queryset(self):
        user_id = self.request.user.id
        return MathCourse.objects.filter(user_favorites=user_id)

class MyEducationView(PermissionsMixin, ListView):
    template_name = simplified_path('userCourses')
    model = MathCourse

    def get_queryset(self):
        user_id = self.request.user.id
        return MathCourse.objects.filter(course_user=user_id)
