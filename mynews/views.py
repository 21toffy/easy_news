# from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from.models import Items, ParentChilRelationship
from mynews.tasks import get_all_items
from .managers import ItemManager #ItemManager
from django.views.generic.list import ListView 
from .pagination import MyPaginator


from django.views.generic.detail import DetailView
  
class ItemDetailView(DetailView):
    template_name = 'news_detail.html'
    context_object_name = 'item'
    model = Items
    # override context data
    def get_context_data(self, *args, **kwargs):
        context = super(ItemDetailView,
             self).get_context_data(*args, **kwargs)
        context["category"] = "MISC"
        context["children"] = ParentChilRelationship.objects.filter(parent= context["object"])   
        return context





class ItemList(ListView):
    model = Items
    template_name = 'news_list.html'
    context_object_name = 'items'
    paginate_by = 10
    paginator_class = MyPaginator

    def get_context_data(self, **kwargs):
        context = super(ItemList, self).get_context_data(**kwargs)
        filter_set = Items.objects.filter(deleted=False, dead=False)
        
        page = self.request.GET.get('page', 1)

        if self.request.GET.get('text'):
            text = self.request.GET.get('text')
            filter_set = filter_set.filter(title__icontains=text)

        if self.request.GET.get('type'):
            type = self.request.GET.get('type')
            filter_set = filter_set.filter(type=type)


        paginator = self.paginator_class(filter_set, self.paginate_by)
        filter_set = paginator.page(page)
        context['items'] = filter_set
        context['item_count'] = Items.objects.all().count()
        return context
