from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .models import Item, Maker,Category, Comment
from django.core.exceptions import PermissionDenied
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
# Create your views here.

def new_comment(request, pk):
    if request.user.is_authenticated:
        item = get_object_or_404(Item, pk=pk)
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.item = item
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else:
            return redirect(item.get_absolute_url())
    else:
        raise PermissionDenied

class ItemCreate(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = Item
    fields = ['item_name','explanation','item_price','maker','category','head_image','item_state','item_receipt']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            return super(ItemCreate,self).form_valid(form)
        else :
            return redirect('/computer/')

class ItemUpdate(LoginRequiredMixin,UpdateView):
    model = Item
    fields = ['item_name','explanation','item_price','maker','category','head_image','item_state','item_receipt']

    template_name = 'computer/item_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(ItemUpdate,self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

class CommentUpdate(LoginRequiredMixin,UpdateView):
    model = Comment
    fields = ['content']

    template_name = 'computer/comment_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate,self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class ItemList(ListView) :
    model = Item
    ordering = '-pk'
    paginate_by = 8

    def get_context_data(self, *, object_list=None, **kwargs):
        c_context = super(ItemList,self).get_context_data()
        c_context['categories'] = Category.objects.all()
        c_context['no_category'] = Item.objects.filter(category=None).count()
        c_context['makers'] = Maker.objects.all()
        c_context['no_maker'] = Item.objects.filter(maker=None).count()
        return c_context

#    template_name = 'computer/item_list.html'
# item_list.html

class ItemDetail(DetailView) :
    model = Item

    def get_context_data(self, *, object_list=None, **kwargs):
        c_context = super(ItemDetail,self).get_context_data()
        c_context['categories'] = Category.objects.all()
        c_context['no_category'] = Item.objects.filter(category=None).count()
        c_context['makers'] = Maker.objects.all()
        c_context['no_maker'] = Item.objects.filter(maker=None).count()
        c_context['comment_form'] = CommentForm
        return c_context

class ItemSearch(ItemList) :
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q']
        item_list = Item.objects.filter(
            Q(item_name__contains=q) | Q(explanation__contains=q)
        ).distinct()
        return item_list

    def get_context_data(self, **kwargs):
        context = super(ItemSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search : {q}({self.get_queryset().count()})'
        return context

def category_page(request, slug):
    if slug == 'no_category' :
        category = '미분류'
        item_list = Item.objects.filter(category=None)
    else :
        category = Category.objects.get(slug=slug)
        item_list = Item.objects.filter(category=category)

    return render(request, 'computer/item_list.html',
                  {
                      'item_list' : item_list,
                      'categories' : Category.objects.all(),
                      'no_category' : Item.objects.filter(category=None).count(),
                      'category' : category
                  }
                  )

def maker_page(request, slug):
    if slug == 'no_maker' :
        maker = '미분류'
        item_list = Item.objects.filter(maker=None)
    else :
        maker = Maker.objects.get(slug=slug)
        item_list = Item.objects.filter(maker=maker)

    return render(request,  'computer/item_list.html',
                  {
                      'item_list' : item_list,
                      'makers' : Maker.objects.all(),
                      'no_maker' : Item.objects.filter(maker=None).count(),
                      'maker' : maker
                  }
                  )



# item_detail.html

#def index(request) :
#    items = Item.objects.all().order_by('pk')

#    return render(request, 'computer/item_list.html',
#                  {
#                      'items' : items
#                  }
#                  )

#def single_computer_page(request, pk) :
#    item = Item.objects.get(pk=pk)

#    return render(request, 'computer/item_detail.html',
#                  {
#                      'item' : item
#                  }
#                  )