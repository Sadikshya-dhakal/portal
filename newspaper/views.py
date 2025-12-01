from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from newspaper.forms import CommentForm, ContactForm
from newspaper.models import Post, OurTeam, Category, Tag, Contact
from django.views.generic import TemplateView, ListView, DetailView, CreateView, View
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import FormMixin
from django.http import JsonResponse
from newspaper.forms import NewsletterForm

class SidebarMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popular_posts"] = Post.objects.filter(
            published_at__isnull=False, status="active"
        ).order_by("-published_at")[:5]
        context["categories"] = Category.objects.all() 
        context["tags"] = Tag.objects.all()  
        return context

class HomeView(SidebarMixin, TemplateView):
    template_name = "newsportal/home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breaking_news"] = Post.objects.filter(
            published_at__isnull=False, status="active", is_breaking_news=True
        ).order_by("-published_at")[:3]
        context["featured_post"] = (
            Post.objects.filter(published_at__isnull=False, status="active")
            .order_by("-published_at", "-views_count")
            .first()
        )
        context["trending_news"] = Post.objects.filter(
            published_at__isnull=False, status="active"
        ).order_by("-published_at")[:4]
        one_week_ago = timezone.now() - timedelta(days=7)
        context["weekly_top_posts"] = Post.objects.filter(
            published_at__isnull=False, status="active", published_at__gte=one_week_ago
        ).order_by("-published_at", "-views_count")[:5]
        return context

class PostListView(SidebarMixin, ListView):
    model = Post
    template_name = "newsportal/list/list.html"
    context_object_name = "posts"
    paginate_by = 1
    def get_queryset(self):
        return Post.objects.filter(
            published_at__isnull=False, status="active"
        ).order_by("-published_at")

class PostDetailView(SidebarMixin,FormMixin, DetailView):
    model = Post
    template_name = "newsportal/detail/detail.html"
    context_object_name = "post"
    form_class = CommentForm

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(published_at__isnull=False, status="active")
        return query
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        current_post = self.object
        current_post.views_count += 1
        current_post.save()

        context["related_articles"] = (
            Post.objects.filter(
                published_at__isnull=False,
                status="active",
                category=self.object.category,
            )
            .exclude(id=self.object.id)
            .order_by("-published_at", "-views_count")[:2]
        )
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.object
        comment.user = self.request.user
        comment.save()
        messages.success(self.request, "Your comment has been added successfully.")
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.object.pk})


class AboutView(TemplateView):
    template_name = "newsportal/about.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["our_teams"] = OurTeam.objects.all()
        return context
    
class CategoryListView(ListView):
    model =  Category
    template_name = "newsportal/categories.html"
    context_object_name = "categories"

    

class ContactCreateView(SuccessMessageMixin, CreateView):
    model = Contact
    template_name = "newsportal/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact")
    success_message = "Your message has been sent successfully!"

    def form_invalid(self, form):
        messages.error(
            self.request,
            "There was an error sending your message. Please check the form.",
        )
        return super().form_invalid(form)

class TagListView(ListView):
    model = Tag
    template_name = "newsportal/tags.html"
    context_object_name = "tags"


class TagPostsView(SidebarMixin, ListView):
    model = Post
    template_name = "newsportal/list/tag_posts.html"
    context_object_name = "posts"
    paginate_by = 1 

    def get_queryset(self):
        tag_id = self.kwargs["pk"]
        return Post.objects.filter(
            published_at__isnull=False,
            status="active",
            tag__id=tag_id   
        ).order_by("-published_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = Tag.objects.get(pk=self.kwargs["pk"])
        return context
    
class CategoryPostsView(SidebarMixin, ListView):
    model = Post
    template_name = "newsportal/list/category_posts.html"
    context_object_name = "posts"
    paginate_by = 1  

    def get_queryset(self):
        category_id = self.kwargs["pk"]
        return Post.objects.filter(
            published_at__isnull=False,
            status="active",
            category__id=category_id
        ).order_by("-published_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.get(pk=self.kwargs["pk"])
        return context


class NewsletterView(View):

    def post(self, request):
        is_ajax = request.headers.get("x-requested-with")
        if is_ajax == "XMLHttpRequest":
            form = NewsletterForm(request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse(
                    {
                    "success": True,
                    "message": "Successfully subscribed to the newsletter.",
                    },
                    status=201
               )
            else:
                return JsonResponse(
                    {
                      "success": False,
                      "message": "Cannot suscribe to the newsletter.", 
                    },
                    status=400,
                )
        else:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Cannot process. Must be an AJAX XMLHttpRequest",
                
                },
                status=400,
            )
