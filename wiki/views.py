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
            'page': page
        })


class PageCreateView(CreateView):
    # Render template to display pageForm instance
    def get(self, request, *args, **kwargs):
        context = {'form': PageForm()}
        return render(request, 'create.html', context)

    def post(self, request, *args, **kwargs):
        form = PageForm(request.POST)
        # If true, save data and use logged-in user as page author --> then redirect to detail view for newly created page object
        # use reverse function to return path
        if form.is_valid():
            wiki = form.save()
            wiki.save()
            return HttpResponseRedirect(reverse('wiki-details-page'))
        return render(request, 'create.html', {'form': form})

        # if false, display errors in templates
