import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .cart import Cart
from home.models import Product
from django.contrib import messages
from .forms import CartAddForm, CouponForm
from .models import Order, OrderItem, Coupon
import json, requests


class CartView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'orders/cart.html', {'cart': cart})

class CartAddView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(quantity=cd['quantity'], product=product)
            #messages.success(request, f'{cd["quantity"]} {product.name} was added to cart.')
        return redirect('orders:cart')

class CartRemoveView(LoginRequiredMixin, View):
    def get(self, request, product_slug):
        cart = Cart(request)
        product = get_object_or_404(Product, slug=product_slug)
        cart.remove(product)
        return redirect('orders:cart')

class OrderDetailView(LoginRequiredMixin, View):
    form_class = CouponForm

    def dispatch(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs['order_id'])
        if not request.user == order.user:
            messages.error(request, 'You can just see your orders!', 'danger')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        return render(request, 'orders/order_detail.html', {'order':order, 'form':self.form_class})

class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user)
        for item in cart:
            product = Product.objects.get(slug=item['product_slug'])
            OrderItem.objects.create(order=order, product=product, price=item['price'],
                                     quantity=item['quantity'])
        cart.clear()

        return redirect('orders:order_detail', order.id)

# ZARIN PAL PAYMENT
MERCHANT = '' # needs merchant to run
ZP_API_REQUEST = f"https://api.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://api.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://www.zarinpal.com/pg/StartPay/"
description = "The information about payment"
CallbackURL = 'http://127.0.0.1:8080/orders/verify/'

class OrderPayView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        request.session['order_pay']= {'order_id': order_id}
        data = {
            "MerchantID": MERCHANT,
            "Amount": order.get_total_cost(),
            "Description": description,
            "Phone": request.user.phone_number,
            "CallbackURL": CallbackURL,
        }
        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}
        try:
            response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

            if response.status_code == 200:
                response = response.json()
                if response['Status'] == 100:
                    return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']),
                            'authority': response['Authority']}
                else:
                    return {'status': False, 'code': str(response['Status'])}
            return response
        except requests.exceptions.Timeout:
            return {'status': False, 'code': 'timeout'}
        except requests.exceptions.ConnectionError:
            return {'status': False, 'code': 'connection error'}


class OrderVerifyView(LoginRequiredMixin, View):
    def get(self, request, authority):
       order_id = request.session['order_pay']['order_id']
       order = get_object_or_404(Order, id=int(order_id))
       data = {
           "MerchantID": MERCHANT,
           "Amount": order.get_total_cost(),
           "Authority": authority,
       }
       data = json.dumps(data)
       # set content length by data
       headers = {'content-type': 'application/json', 'content-length': str(len(data))}
       response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

       if response.status_code == 200:
           response = response.json()
           if response['Status'] == 100:
               return {'status': True, 'RefID': response['RefID']}
           else:
               return {'status': False, 'code': str(response['Status'])}
       return response

class CouponApplyView(LoginRequiredMixin, View):
    form_class = CouponForm

    def post(self, request, order_id):
        now = datetime.datetime.now()
        form = self.form_class(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code__exact=code,is_active=True, valid_from__lte=now, valid_to__gte=now)
                coupon.is_active = False
                coupon.save()
            except Coupon.DoesNotExist:
                messages.error(request, 'This coupon is not valid', 'warning')
                return redirect('orders:order_detail', order_id)
            order = Order.objects.get(id=order_id)
            order.discount = coupon.discount
            order.save()
            return redirect('orders:order_detail', order_id)



