from django.shortcuts import render
from django.views.generic import ListView

from .models import (Book)


# Create your views here.
class BookListView(ListView):
    model = Book
    paginate_by = 2
    context_object_name = 'books'

    def get_queryset(self):
        q = self.request.GET.get('q', None)
        queryset = self.model.objects.all()

        if q:
            queryset = queryset.filter(title__icontains=q)

        return queryset.order_by('pk').reverse()
