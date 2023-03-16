from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Groups, Apps, Comment
from .forms import AddComment

class GroupsListView(ListView):
    model = Groups
    template_name = 'main/home.html'
    context_object_name = 'groups'

    def get_context_data(self, **kwargs):
        ctx = super(GroupsListView, self).get_context_data(**kwargs)
        
        apps = Apps.objects.all()
        ctx['apps'] = apps
        ctx['title'] = 'ruStore - приложения'
        ctx['title_view_groups'] = 'Группы'
        ctx['title_view_apps'] = 'Приложения'

        return ctx
    
def groups(request):
    return redirect('home')

class GroupsDetailView(DetailView):
    model = Groups
    template_name = 'main/group.html'
    context_object_name = 'group'

    def get_context_data(self, **kwargs):
        ctx = super(GroupsDetailView, self).get_context_data(**kwargs)
        ctx['title'] = Groups.objects.filter(slug=self.kwargs['slug']).first()
        group = Groups.objects.filter(slug=self.kwargs['slug']).first()
        groups = Groups.objects.all()
        ctx['groups'] = groups
        ctx['apps'] = Apps.objects.filter(group=group)

        return ctx

class AppsDetailView(DetailView):
    model = Groups
    template_name = 'main/app.html'

    def get_context_data(self, **kwargs):
        ctx = super(AppsDetailView, self).get_context_data(**kwargs)
        group = Groups.objects.filter(slug=self.kwargs['slug']).first()
        app = Apps.objects.filter(slug=self.kwargs['slug_app']).first()
        groups = Groups.objects.all()
        comment = Comment.objects.filter(app=app)
        form_comment = AddComment()
        ctx['groups'] = groups
        ctx['group'] = group
        ctx['app'] = app
        ctx['comment'] = comment
        ctx['form'] = form_comment
        return ctx

    def post(self, request, *args, **kwargs):

        app = Apps.objects.filter(slug=self.kwargs['slug_app']).first()

        post = request.POST.copy()
        post['avtor'] = request.user
        post['app'] = app
        request.POST = post

        form = AddComment(request.POST)
        
        if form.is_valid():
            form.save()
        
        url = self.kwargs['slug'] + '/' + self.kwargs['slug_app']
        return redirect('/groups/' + url)


    

