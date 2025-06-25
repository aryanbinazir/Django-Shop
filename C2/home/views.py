from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from .models import Product, Category, Comment
from . import tasks
from uttils import IsAdminUserMixin
from orders.forms import CartAddForm
from .forms import CommentAddForm
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class HomeView(View):
    template_class = 'home/home.html'

    def get(self, request, category_slug=None):
        products = Product.objects.filter(available=True)
        categories = Category.objects.filter(is_sub=False)
        if category_slug:
            category = Category.objects.get(slug=category_slug)
            products = Product.objects.filter(category=category)
        return render(request, self.template_class, {'products':products, 'categories':categories})

class ProductDetailView(View):
    template_class = 'home\product_detail.html'

    def setup(self, request, *args, **kwargs):
        self.product = get_object_or_404(Product, slug=kwargs['slug'])
        self.comments = Comment.objects.filter(product=self.product)
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        cart_form = CartAddForm
        comment_form = CommentAddForm

        return render(request, self.template_class, {'product':self.product, 'cart_form':cart_form,
                                                     'comment_form':comment_form, 'comments':self.comments})
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = CommentAddForm(request.POST)
        user = User.objects.get(id=request.user.id)
        product = self.product
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = user
            new_form.product = product
            new_form.save()
            messages.success(request, 'Your comment added successfully', 'success')
            return redirect('home:product_detail', product.slug)


class BucketHomeView(IsAdminUserMixin, View):
    template_class = 'home/bucket_home.html'

    def get(self, request):
        objects = tasks.get_all_objects_tasks()
        return render(request, self.template_class, {'objects':objects})

class DeleteBucketObjectView(IsAdminUserMixin, View):
    def get(self, request, key):
        tasks.delete_object_task.delay(key)
        messages.info(request, 'It will delete this soon', 'info')
        return redirect('home:bucket')

class DownloadBucketObjectView(IsAdminUserMixin, View):
    def get(self, request, key):
        tasks.download_object_task.delay(key)
        messages.info(request, 'It will download it soon', 'info')
        return redirect('home:bucket')




