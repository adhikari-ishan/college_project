from django.shortcuts import render,redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.

def process_order(request):
    if request.POST:
        #getting cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()
        
        
        payment_form = PaymentForm(request.POST or None)
        #get shipping data session
        my_shipping = request.session.get('my_shipping')
        print(my_shipping)

        #collect order info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']

        #create shiping add from shipp info
        shipping_address = f"{ my_shipping['shipping_address1']}\n { my_shipping['shipping_address2'] }\n { my_shipping['shipping_city'] }\n { my_shipping ['shipping_state'] }\n { my_shipping['shipping_zipcode'] }\n { my_shipping['shipping_country'] }\n"

        amount_paid = totals

        #create order 
        if request.user.is_authenticated:
            #logged in 
            user = request.user
            #create order
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            messages.success(request,"Ordered placed")
            return redirect('home')

        else:
            # !logged in 
            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()

            messages.success(request,"Ordered placed")
            return redirect('home')


    else:
        messages.success(request,"Access Denied")
        return redirect('home')



def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()


        #creating session with shipping info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping


        #check to see if user is logged in 
        if request.user.is_authenticated:
            #get billing form
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {"cart_products": cart_products, "quantities" : quantities, "totals" : totals,"shipping_info":request.POST, "billing_form": billing_form})
        

        else:
            #not logged in 
            #get billing form
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {"cart_products": cart_products, "quantities" : quantities, "totals" : totals,"shipping_info":request.POST, "billing_form": billing_form})

        shipping_form = request.POST
        return render(request, 'payment/billing_info.html', {"cart_products": cart_products, "quantities" : quantities, "totals" : totals,"shipping_form":shipping_form})
    
    else:
        messages.success(request,"Access Denied")
        return redirect('home')


def checkout(request):
    #getting cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    if request.user.is_authenticated:  #checkout login user
         #shipping user
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
         #shipping form
        shipping_form = ShippingForm(request.POST or None,instance=shipping_user)
        return render(request, 'payment/checkout.html', {"cart_products": cart_products, "quantities" : quantities, "totals" : totals,"shipping_form":shipping_form})
    
    else:#checkout as guest
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'payment/checkout.html', {"cart_products": cart_products, "quantities" : quantities, "totals" : totals,"shipping_form":shipping_form})

    # return render(request,"payment/checkout.html",{})

def payment_success(request):
    return render (request, "payment/payment_success.html", {})
