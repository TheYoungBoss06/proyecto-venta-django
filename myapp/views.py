from django.shortcuts import render,redirect,get_object_or_404
from .models import FurnitureCategory,FurnitureProduct,Promotion,BlogPost,ShoppingCart,CartItem,Review,Order,OrderItem
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.models import User
from django.contrib import messages # Import messages framework
from .forms import ShippingForm # Import ShippingForm

from django.db import IntegrityError
from django.db import transaction # Import transaction for atomic operations
from django.contrib.auth.decorators import login_required, user_passes_test # Import user_passes_test

from django.db.models import Q

from django.conf import settings

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from decimal import Decimal # Import Decimal
import datetime # Import datetime module

# Create your views here.
def register(request):
    user =None
    error_message=None


    if request.POST:
        try:

            email = request.POST['email']
            username=request.POST['username']
            password = request.POST['password']



            user = User.objects.create_user(email=email,username=username,password=password)
            user.save()
            return redirect('user_login')
        except IntegrityError:
            error_message = "Ya existe un usuario con este correo electrónico o nombre de usuario"


    return render(request,'register.html',{'user':user, 'error_message':error_message})



def user_login(request):
     user= None
     error_message =None
     if request.POST:
         username=request.POST['username']
         password = request.POST['password']
         user = authenticate(request,username=username,password=password)

         if user:
             login(request,user)
             return redirect('view_products')
         else:
             error_message ='Credenciales no válidas'
     return render(request,'login.html',{'error_message':error_message})


def user_logout(request):
    logout(request)
    return redirect('index')




def index(request):
    products_featured = FurnitureProduct.objects.all()[:4] # Renamed for clarity
    promotions = Promotion.objects.all()
    trending_products = FurnitureProduct.objects.all()[2:5] # Renamed for clarity
    categories = FurnitureCategory.objects.exclude(slug__isnull=True).exclude(slug__exact='') # Fetch all categories with a non-empty slug

    context = {
        'products': products_featured,
        'promotions': promotions,
        'trend': trending_products,
        'categories': categories # Pass categories to the index template
    }
    return render(request,'index.html', context)


@login_required(login_url='user_login')
def view_products(request, category_slug=None): # Added category_slug parameter
    categories = FurnitureCategory.objects.all() # Fetch all categories
    
    if category_slug:
        category = get_object_or_404(FurnitureCategory, slug=category_slug)
        products = FurnitureProduct.objects.filter(category=category)
    else:
        products = FurnitureProduct.objects.all()
        
    return render(request, 'product.html',{'products':products, 'categories': categories})



def search_products(request):
    query = request.GET.get('q')

    if query:
        results = FurnitureProduct.objects.filter(
            Q(name__icontains=query) | Q(category__name__icontains=query)
        )
    else:
        results = FurnitureProduct.objects.all()

    return render(request,'product.html',{'products':results,'query':query})




def view_product_details(request,product_id):
    product = FurnitureProduct.objects.get(id=product_id)

    review =Review.objects.filter(product=product)
    return render(request,'product_details.html',{'products':product,'reviews':review})

def contact(request):
    return render(request,'contact.html')

def about_us(request):
    return render(request, 'about.html')

def view_blog(request):
    blog= BlogPost.objects.all()
    return render(request,'blog.html',{'blogs':blog})



@login_required(login_url='user_login')
def add_to_cart(request, product_id):
    product = get_object_or_404(FurnitureProduct, id=product_id)
    user = request.user

    shopping_cart, created = ShoppingCart.objects.get_or_create(user=user)

    # Get quantity from POST data, default to 1 if not provided or invalid
    quantity = int(request.POST.get('quantity', 1))
    if quantity < 1:
        quantity = 1

    cart_item, item_created = CartItem.objects.get_or_create(product=product, shopping_cart=shopping_cart)

    # Check for active promotions for the product
    today = datetime.date.today()
    active_promotion = Promotion.objects.filter(
        start_date__lte=today,
        end_date__gte=today
    ).first() # Get the first active promotion, or None

    if active_promotion:
        cart_item.promotion = active_promotion
    else:
        cart_item.promotion = None # No active promotion

    if item_created:
        cart_item.quantity = quantity # Set quantity for new item
    else:
        cart_item.quantity += quantity # Add to existing quantity
    
    cart_item.save()

    return redirect('view_shopping_cart')



@login_required(login_url='user_login')
def view_shopping_cart(request):
    user = request.user
    shopping_cart, created = ShoppingCart.objects.get_or_create(user=user)

    cart_items = CartItem.objects.filter(shopping_cart=shopping_cart)

    total_quantity = 0
    total_amount = Decimal('0.00') # Initialize as Decimal

    for item in cart_items:
        item_price = item.product.price
        discount_amount = Decimal('0.00') # Initialize discount_amount for each item

        if item.promotion:
            # Limitar el descuento al 20%
            discount_percentage = min(item.promotion.discount_percentage, Decimal('20'))
            # Calculate discount amount using Decimal for precision
            discount_amount = (item_price * discount_percentage) / Decimal('100')
            # Assign the calculated discount amount to the item for template access
            item.discount_amount = discount_amount
        else:
            # If no promotion, discount is 0
            item.discount_amount = Decimal('0.00')

        # Calculate the price after discount
        discounted_price = item_price - item.discount_amount
        
        # Add to total amount and total quantity
        total_amount += discounted_price * item.quantity
        total_quantity += item.quantity

    context = {
        'cart_items': cart_items,
        'total_quantity': total_quantity,
        'total_amount': total_amount,
    }
    return render(request,'shop-cart.html', context)


@login_required(login_url='user_login')
def remove_cart_item(request,item_id):
    item = get_object_or_404(CartItem,id=item_id)
    item.delete()

    return redirect('view_shopping_cart')

@login_required(login_url='user_login')
def add_review(request,product_id):
    user=request.user
    product=FurnitureProduct.objects.get(id=product_id)
    if request.POST:
        comment = request.POST['comment']


        review = Review.objects.create(user=user,comment=comment,product=product)
        review.save()


    return render(request,'index.html')



@login_required(login_url='user_login')
def buynow(request, item_id):
    user = request.user
    cart_item = get_object_or_404(CartItem, id=item_id, shopping_cart__user=user)

    item_price = cart_item.product.price
    discount = Decimal('0.00') # Initialize discount
    total_amount = Decimal('0.00') # Initialize total_amount

    if cart_item.promotion:
        # Limitar el descuento al 20%
        discount_percentage = min(cart_item.promotion.discount_percentage, Decimal('20'))
        # Calculate discount amount using Decimal for precision
        discount = (item_price * discount_percentage) / Decimal('100')
        discounted_price = item_price - discount
        total_amount = discounted_price * cart_item.quantity
    else:
        total_amount = item_price * cart_item.quantity
    
    # Instantiate the shipping form
    shipping_form = ShippingForm()

    context = {
        'cart_item': cart_item,
        'discount': discount, # Pass the calculated discount
        'total_amount': total_amount,
        'razorpay_api_key': settings.RAZORPAY_API_KEY,
        'user': user,
        'shipping_form': shipping_form, # Pass the shipping form to the template
    }

    return render(request, 'payment.html', context)


@login_required(login_url='user_login')
def apply_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        user = request.user
        shopping_cart = get_object_or_404(ShoppingCart, user=user)
        
        today = datetime.date.today()
        
        try:
            coupon = Promotion.objects.get(
                code=coupon_code,
                start_date__lte=today,
                end_date__gte=today
            )
            
            # Calculate current cart total to check against minimum_cart_total
            cart_items = CartItem.objects.filter(shopping_cart=shopping_cart)
            current_cart_total = Decimal('0.00')
            for item in cart_items:
                item_price = item.product.price
                # Assuming item.promotion is already applied for individual item discounts
                # For coupon, we apply it to the total, so we need the subtotal without item-specific promotions
                current_cart_total += item_price * item.quantity 
            
            if coupon.minimum_cart_total and current_cart_total < coupon.minimum_cart_total:
                messages.error(request, f"El cupón requiere un total de carrito mínimo de ${coupon.minimum_cart_total}.")
            else:
                # Apply coupon to all items in the cart
                for item in cart_items:
                    item.promotion = coupon
                    item.save()
                messages.success(request, f"Cupón '{coupon_code}' aplicado exitosamente.")
                
        except Promotion.DoesNotExist:
            messages.error(request, "Código de cupón inválido o expirado.")
        except Exception as e:
            messages.error(request, f"Ocurrió un error al aplicar el cupón: {e}")
            
    return redirect('view_shopping_cart')


def handle_payment(request):
    if request.method == 'POST':
        user = request.user
        total_amount_str = request.POST.get('total_amount')
        payment_id = request.POST.get('payment_id')

        shipping_form = ShippingForm(request.POST)
        if shipping_form.is_valid():
            shipping_name = shipping_form.cleaned_data['shipping_name']
            shipping_address = shipping_form.cleaned_data['shipping_address']
            shipping_phone = shipping_form.cleaned_data['shipping_phone']
        else:
            messages.error(request, "Por favor, complete los detalles de envío correctamente.")
            return redirect('view_shopping_cart')

        try:
            total_amount_from_post = Decimal(total_amount_str)
        except (ValueError, TypeError):
            messages.error(request, "Monto total inválido.")
            return redirect('view_shopping_cart')

        try:
            with transaction.atomic():
                shopping_cart = get_object_or_404(ShoppingCart, user=user)
                cart_items = CartItem.objects.filter(shopping_cart=shopping_cart)

                if not cart_items.exists():
                    messages.error(request, "Tu carrito está vacío.")
                    return redirect('view_shopping_cart')

                calculated_total_amount = Decimal('0.00')
                applied_coupon_for_order = None
                
                if cart_items.first() and cart_items.first().promotion:
                    applied_coupon_for_order = cart_items.first().promotion

                for item in cart_items:
                    item_price = item.product.price
                    discount_amount = Decimal('0.00')
                    if item.promotion:
                        # Limitar el descuento al 20%
                        discount_percentage = min(item.promotion.discount_percentage, Decimal('20'))
                        discount_amount = (item_price * discount_percentage) / Decimal('100')
                    
                    discounted_price = item_price - discount_amount
                    calculated_total_amount += discounted_price * item.quantity

                order = Order.objects.create(
                    user=user,
                    total_amount=calculated_total_amount,
                    payment_id=payment_id,
                    shipping_name=shipping_name,
                    shipping_address=shipping_address,
                    shipping_phone=shipping_phone,
                    coupon=applied_coupon_for_order,
                    status='PROCESSING'
                )

                for item in cart_items:
                    if item.product.stock < item.quantity:
                        messages.error(request, f"Stock insuficiente para {item.product.name}. Solo quedan {item.product.stock} unidades.")
                        transaction.set_rollback(True)
                        return redirect('view_shopping_cart')

                    item_price = item.product.price
                    discount_amount = Decimal('0.00')
                    if item.promotion:
                        discount_percentage = item.promotion.discount_percentage
                        discount_amount = (item_price * Decimal(discount_percentage)) / Decimal('100')

                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price_at_purchase=item_price,
                        discount_at_purchase=discount_amount
                    )
                    item.product.stock -= item.quantity
                    item.product.save()

                cart_items.delete()
                messages.success(request, "¡Tu pedido ha sido realizado exitosamente!")

                return redirect('view_invoice', order_id=order.id)

        except Exception as e:
            messages.error(request, f"Ocurrió un error al procesar el pago: {e}")
            print(f"Error processing payment: {e}")
            return redirect('view_shopping_cart')

    return redirect('view_shopping_cart')

def view_invoice(request, order_id):
    try:
        order = get_object_or_404(Order, id=order_id)
        order_items = order.items.all()

        for item in order_items:
            item.subtotal = (item.quantity * item.price_at_purchase) - item.discount_at_purchase
        
        context = {
            'order': order,
            'order_items': order_items,
        }
        return render(request, 'invoice.html', context)
    except Order.DoesNotExist:
        return render(request, 'error.html', {'message': 'Factura no encontrada.'})


@login_required(login_url='user_login')
def warehouse_order_list(request):
    orders = Order.objects.filter(status='PROCESSING').order_by('-created_at')
    context = {
        'orders': orders
    }
    return render(request, 'warehouse_order_list.html', context)

@login_required(login_url='user_login')
def view_all_invoices(request):
    user = request.user
    orders = Order.objects.filter(user=user).exclude(status='DISPATCHED')
    return render(request, 'all_invoices.html', {'orders': orders})

@login_required(login_url='user_login')
@user_passes_test(lambda u: u.is_staff) # Restrict to staff users
def warehouse_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = order.items.all()
    context = {
        'order': order,
        'order_items': order_items
    }
    return render(request, 'warehouse_order_detail.html', context)

# New view for dispatch success message with delay
def dispatch_success_message(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    messages.success(request, f"La orden #{order.id} ha sido despachada exitosamente.")
    # The template will handle the delay and redirect to view_all_invoices
    return render(request, 'dispatch_success.html', {'order_id': order_id})

@login_required(login_url='user_login')
def dispatch_order(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        # Check if the order is already dispatched or shipped to avoid re-dispatching
        if order.status not in ['SHIPPED', 'DISPATCHED']:
            order.status = 'DISPATCHED' # Changed status to DISPATCHED
            order.save()
            messages.success(request, f"La orden #{order.id} ha sido despachada exitosamente.")
        else:
            messages.warning(request, f"La orden #{order.id} ya ha sido despachada o enviada.")
    # Redirect to the new success message view
    return redirect('dispatch_success_message', order_id=order_id)
