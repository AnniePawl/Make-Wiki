from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import CreateView
from django.http import HttpResponseRedirect

from django.urls import reverse
from django.urls import reverse_lazy

from wiki.models import Page
from .forms import PageForm


class PageListView(ListView):
    """ Renders a list of all Pages. """
    model = Page

    def get(self, request):
        """ GET a list of Pages. """
        pages = self.get_queryset().all()
        return render(request, 'list.html', {
            'pages': pages
        })


class PageDetailView(DetailView):
    """ Renders a specific page based on it's slug."""
    model = Page

    def get(self, request, slug):
        """ Returns a specific wiki page by slug. """
        page = self.get_queryset().get(slug__iexact=slug)
        return render(request, 'page.html', {
            'page': page,
            'form': PageForm()
        })

    # Edit
    def post(self, request, slug):
        # Allow eidt of page info
        form = PageForm(request.POST)
        page = self.get_queryset().get(slug__iexact=slug)
        # Get page info
        page.title = request.POST['title']
        page.author = request.user
        page.content = request.POST['content']
        page.save

        return HttpResponseRedirect(reverse('wiki:wiki-details-page'))


class PageCreateView(CreateView):
    # Render template to display pageForm instance
    def get(self, request, *args, **kwargs):
        context = {'form': PageForm()}
        return render(request, 'create.html', context)

    def post(self, request, *args, **kwargs):
        form = PageForm(request.POST)
        # If true, save data and use logged-in user as page author --> then redirect to detail view for newly created page object
        if form.is_valid():
            page = form.save()
            # use reverse function to return path
            return HttpResponseRedirect(reverse('wiki:wiki-details-page', args=[page.slug]))
        return render(request, 'create.html', {'form': form})

        # if false, display errors in templates
