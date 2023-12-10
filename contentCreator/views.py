from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import *
from django.core.paginator import Paginator
from contentCreator.forms import *
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin


def simplified_path(path: str):
    return f'contentCreator/{path}.html'


# Create your views here.
class StartPageView(ListView):
    template_name = simplified_path('startPage')
    model = MathCourse
    context_object_name = 'courses_list'

    def get_queryset(self):
        user_id = self.request.user.id
        return MathCourse.objects.filter(author=user_id)


def CreateNewCourseView(request):
    if request.method == 'POST':
        form = CreateCourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.author = request.user
            course.save()
            return redirect('content_creator_dashboard')
    else:
        form = CreateCourseForm()

    return render(request, simplified_path('createCoursePage'), {'form': form})


def CreateModuleView(request, pk):
    if request.method == 'POST':
        form = CreateModuleForm(request.POST, request.FILES)
        if form.is_valid():
            module = form.save(commit=False)
            math_course = get_object_or_404(MathCourse, id=pk)
            module.math_course = math_course
            module.save()

            return redirect('content_creator_dashboard')

    else:
        form = CreateModuleForm
    return render(request, simplified_path('createModulePage'), {'form': form})


class UpdateModuleView(UpdateView):
    template_name = simplified_path('updateModule')
    model = CourseModule
    fields = ('title', 'module_image', 'description',)

    def get_success_url(self):
        module = self.object
        return reverse('module_detail', args=[module.id])


class DeleteModuleView(DeleteView):
    template_name = simplified_path('deleteModule')
    model = CourseModule
    success_url = reverse_lazy('content_creator_dashboard')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Delete all lectures associated with the CourseModule
        Lecture.objects.filter(course_module=self.object).delete()

        success_url = self.get_success_url()
        self.object.delete()

        return HttpResponseRedirect(success_url)


def AddLectureView(request, pk):
    if request.method == 'POST':
        form = CreateLectureForm(request.POST, request.FILES)

        if form.is_valid():
            lecture = form.save(commit=False)
            module = get_object_or_404(CourseModule, id=pk)
            lecture.course_module = module
            lecture.save()
            return redirect(reverse('module_detail', args=[module.id]))

    else:
        form = CreateLectureForm(request.POST, request.FILES)
    return render(request, simplified_path('addLecture'), {'form': form})


def AddCommonTestView(request, pk):
    if request.method == 'POST':
        form = CreateCommonTestForm(request.POST, request.FILES)

        if form.is_valid():
            test = form.save(commit=False)
            lecture = get_object_or_404(Lecture, id=pk)
            test.lecture = lecture
            test.save()
            return redirect(reverse('lecture_detail', args=[lecture.id]))

    else:
        form = CreateCommonTestForm(request.POST, request.FILES)
    return render(request, simplified_path('addCommonTest'), {'form': form})


def AddChoiceTestView(request, pk):
    if request.method == 'POST':
        form = CreateChoiceTestForm(request.POST, request.FILES)

        if form.is_valid():
            test = form.save(commit=False)
            lecture = get_object_or_404(Lecture, id=pk)
            test.lecture = lecture
            test.save()
            return redirect(reverse('lecture_detail', args=[lecture.id]))

    else:
        form = CreateChoiceTestForm(request.POST, request.FILES)
    return render(request, simplified_path('addChoiceTest'), {'form': form})


class ChoiceTestDetail(DetailView):
    template_name = simplified_path("choiceTestDetail")
    model = ChoiceTest
    context_object_name = 'choice_test'


def AddAnswerView(request, pk):
    if request.method == 'POST':
        form = CreateAnswerForm(request.POST)

        if form.is_valid():
            answer = form.save(commit=False)
            choice_test = get_object_or_404(ChoiceTest, id=pk)
            answer.choice_test = choice_test
            answer.save()
            return redirect(reverse('choice_test_detail', args=[choice_test.id]))

    else:
        form = CreateAnswerForm(request.POST, request.FILES)
    return render(request, simplified_path('addAnswer'), {'form': form})


class LectureDetailView(DetailView):
    template_name = simplified_path('lectureDetail')
    model = Lecture
    context_object_name = 'lecture'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tests = CommonTest.objects.filter(lecture=self.object)
        context['tests'] = tests
        return context


class AllAuthorCoursesView(ListView):
    template_name = simplified_path('allAuthorCourses')
    model = MathCourse

    def get_queryset(self):
        user_id = self.request.user.id
        return MathCourse.objects.filter(author=user_id)


# def CreateLectureView(request):
#     if request.method == 'POST':
#         form = CreateLectureForm(request.POST, request.FILES)
#         if form.is_valid():
#             module = form.save(commit=False)
#             module.save()
#
#             return redirect('content_creator_dashboard')
#
#     else:
#         form = CreateLectureForm
#     return render(request, simplified_path('createLecturePage'), {'form': form})

# def form_valid(self, form):
#     form.instance.author = self.request.user
#     return super().form_valid(form)


class AuthorDetailCourseView(DetailView):
    template_name = simplified_path('authorCourseDetail')
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


class ModuleDetailView(DetailView):
    template_name = simplified_path('moduleDetail')
    model = CourseModule
    context_object_name = 'module'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        module = self.object

        lectures = Lecture.objects.filter(course_module=module)

        context['lectures'] = lectures
        return context


class DeleteCourseView(DeleteView):
    template_name = simplified_path('deleteCourse')
    model = MathCourse
    success_url = reverse_lazy('content_creator_dashboard')


class UpdateCourseView(UpdateView):
    template_name = simplified_path('updateCourse')
    model = MathCourse
    fields = ('title', 'course_image', 'description', 'price',)

    def get_success_url(self):
        return reverse_lazy('content_creator_dashboard')

#
# def createTestView(request, pk):
#     if request.method == "POST":
#         form = CreateLectureForm(request.POST, request.FILES)
#         if form.is_valid():
#             test = form.save(commit=False)
#             test.lecture = pk
#             test.save()
#
#             return redirect('content_creator_dashboard')
#     else:
#         form = CreateLectureForm
#     return render(request, simplified_path('createLecturePage'), {'form': form})
