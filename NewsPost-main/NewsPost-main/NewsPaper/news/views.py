from django.views.generic import ListView, DetailView, CreateView,\
    TemplateView, UpdateView, DeleteView
from .models import Post, Author, Category, Appointment
from .filters import PostFilter
from datetime import datetime
from django.views import View
from django.core.mail import EmailMultiAlternatives, mail_admins, send_mail
from django.template.loader import render_to_string
from .forms import PostForm,  BaseRegisterForm
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView as AuthLoginView
#from django.db.models.signals import post_save


class LoginView(AuthLoginView):
    template_name = 'account/login.html'

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(0)
        return super().form_valid(form)


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'endex.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()
        return context


class AuthorList(ListView):
    model = Author
    ordering = '-user'
    template_name = 'author/authors.html'
    context_object_name = 'authors'
    paginate_by = 10


class AuthorDetail(DetailView):
    model = Author
    template_name = 'author/author.html'
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Author.objects.get(pk=self.kwargs['pk']).post_set.all().order_by('-id')
        return context


class PostList(ListView):
    model = Post
    ordering = '-date_in'
    template_name = 'post/news.html'
    context_object_name = 'posts'
    paginate_by = 15

    # def __init__(self, **kwargs):
    #     super().__init__(kwargs)
    #     self.filterset = None

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post/posts.html'
    context_object_name = 'posts'


def create_post(request):
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('news/')

    return render(request, 'post/post_edit.html', {'form': form})


# class PostCreate(CreateView):
#     form_class = PostForm
#     model = Post
#     template_name = 'post_edit.html'
#
#     def form_valid(self, form):
#         new = form.save(commit=False)
#         if self.request.path == '/news/create/':
#             new.post_tip_id = 1
#         elif self.request.path == '/state/create/':
#             new.post_tip_id = 2
#             new.save()
#         return super().form_valid(form)
#


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    model = Post
    template_name = 'post/post_edit.html'
    permission_required = ('news.update_post',)
    form_class = PostForm
    success_url = 'news/'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_tip = 'NW'
        return super().form_valid(form)


class PostCreateView(PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'post/post_edit.html'
    permission_required = ('news.create_post',)
    form_class = PostForm
    success_url = 'news/'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_tip = 'NW'
        return super().form_valid(form)


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post/state_delete.html'
    permission_required = ('post/post_delete',)
    form_class = PostForm
    success_url = reverse_lazy('post_list')


class CategoryList(ListView):
    model = Category
    template_name = 'category/categories.html'
    context_object_name = 'categories'


class PostCategory(ListView):
    model = Post
    ordering = '-id'
    template_name = 'post/news.html'
    context_object_name = 'posts'

    def get_queryset(self):
        self.queryset = Category.objects.get(pk=self.kwargs['pk']).PostCategory.all()
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscribers'] = self.request.user not in Category.objects.get(pk=self.kwargs['pk']).subscribers.all()
        context['category'] = self.queryset
        return context


class AppointmentView(View):
    def bick(self, request, *args, **kwargs):
        return render(request, 'make_appointment.html', {})

    def bick_post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        appointment.save()

        # получаем наш html
        html_content = render_to_string(
            'appointment_created.html',
            {
                'appointment': appointment,
            }
        )

        # в конструкторе уже знакомые нам параметры, да? Называются правда немного по-другому, но суть та же.
        msg = EmailMultiAlternatives(
            subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
            body=appointment.message,  # это то же, что и message
            from_email='colif74@yandex.ru',
            to=['colif@mail.ru', 'colif74@gmail.com'],  # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html

        msg.send()  # отсылаем
        send_mail(
                    subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
                    # имя клиента и дата записи будут в теме для удобства
                    message=appointment.message,  # сообщение с кратким описанием проблемы
                    from_email='colif74@yandex.ru',
                    # здесь указываете почту, с которой будете отправлять (об этом попозже)
                    recipient_list=['colif@mail.ru', 'colif74@gmail.com']
                    # здесь список получателей. Например, секретарь, сам врач и т. д.
                )

        mail_admins(
            subject=f'{appointment.client_name} {appointment.date.strftime("%d %m %Y")}',
            message=appointment.message,
        )

        return redirect('news:make_appointment')
