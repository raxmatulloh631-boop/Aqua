from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from .models import Product, Customer, Invoice, InvoiceItem


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, "Foydalanuvchi nomi yoki parol xato!")
    return render(request, 'water/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='/dashboard/login/')
def dashboard(request):
    today = timezone.now().date()
    month_start = today.replace(day=1)

    stats = {
        'products': Product.objects.count(),
        'customers': Customer.objects.count(),
        'invoices_today': Invoice.objects.filter(created_at__date=today).count(),
        'revenue_month': Invoice.objects.filter(
            created_at__date__gte=month_start
        ).aggregate(total=Sum('total_price'))['total'] or 0,
        'low_stock': Product.objects.filter(stock__lt=10).count(),
    }
    recent_invoices = Invoice.objects.select_related('customer').prefetch_related('items__product').order_by(
        '-created_at')[:8]
    context = {'stats': stats, 'recent_invoices': recent_invoices}
    return render(request, 'water/dashboard.html', context)


@login_required(login_url='/dashboard/login/')
def product_list(request):
    products = Product.objects.all()
    return render(request, 'water/product_list.html', {'products': products})


@login_required(login_url='/dashboard/login/')
def product_create(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        price = request.POST.get('price')
        stock = request.POST.get('stock', 0)
        if name and price:
            product = Product(name=name, price=price, stock=stock)
            if request.FILES.get('image'):
                product.image = request.FILES['image']
            product.save()
            messages.success(request, f"'{name}' mahsuloti qo'shildi!")
            return redirect('product_list')
        messages.error(request, "Barcha maydonlarni to'ldiring!")
    return render(request, 'water/product_form.html', {'action': "Qo'shish", 'product': None})


@login_required(login_url='/dashboard/login/')
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.name = request.POST.get('name', product.name).strip()
        product.price = request.POST.get('price', product.price)
        product.stock = request.POST.get('stock', product.stock)
        if request.FILES.get('image'):
            product.image = request.FILES['image']
        product.save()
        messages.success(request, "Mahsulot yangilandi!")
        return redirect('product_list')
    return render(request, 'water/product_form.html', {'action': 'Tahrirlash', 'product': product})


@login_required(login_url='/dashboard/login/')
def product_delete(request, pk):
    if not request.user.is_superuser:
        messages.error(request, "Sizda mahsulotlarni o'chirish huquqi yo'q!")
        return redirect('product_list')

    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Mahsulot o'chirildi!")
        return redirect('product_list')
    return render(request, 'water/confirm_delete.html', {'object': product, 'type': 'mahsulot'})


@login_required(login_url='/dashboard/login/')
def customer_list(request):
    customers = Customer.objects.annotate(invoice_count=Count('invoices'))
    return render(request, 'water/customer_list.html', {'customers': customers})


@login_required(login_url='/dashboard/login/')
def customer_create(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        if name and phone:
            Customer.objects.create(name=name, phone=phone, address=address)
            messages.success(request, f"'{name}' mijozi qo'shildi!")
            return redirect('customer_list')
        messages.error(request, "Ism va telefon majburiy!")
    return render(request, 'water/customer_form.html', {'action': "Qo'shish", 'customer': None})


@login_required(login_url='/dashboard/login/')
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.name = request.POST.get('name', customer.name)
        customer.phone = request.POST.get('phone', customer.phone)
        customer.address = request.POST.get('address', customer.address)
        customer.save()
        messages.success(request, "Mijoz ma'lumotlari yangilandi!")
        return redirect('customer_list')
    return render(request, 'water/customer_form.html', {'action': 'Tahrirlash', 'customer': customer})


@login_required(login_url='/dashboard/login/')
def customer_delete(request, pk):
    if not request.user.is_superuser:
        messages.error(request, "Sizda mijozlarni o'chirish huquqi yo'q!")
        return redirect('customer_list')

    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        messages.success(request, "Mijoz o'chirildi!")
        return redirect('customer_list')
    return render(request, 'water/confirm_delete.html', {'object': customer, 'type': 'mijoz'})


@login_required(login_url='/dashboard/login/')
def invoice_list(request):
    invoices = Invoice.objects.select_related('customer').prefetch_related('items__product').order_by('-created_at')
    total = invoices.aggregate(t=Sum('total_price'))['t'] or 0
    return render(request, 'water/invoice_list.html', {'invoices': invoices, 'total': total})


@login_required(login_url='/dashboard/login/')
def invoice_create(request):
    customers = Customer.objects.all()
    products = Product.objects.all()
    if request.method == 'POST':
        customer_id = request.POST.get('customer')
        customer = get_object_or_404(Customer, pk=customer_id)

        product_ids = request.POST.getlist('product[]')
        quantities = request.POST.getlist('quantity[]')

        if not product_ids or not quantities:
            messages.error(request, "Kamida bitta mahsulot tanlang!")
            return render(request, 'water/invoice_form.html', {'customers': customers, 'products': products})

        invoice = Invoice.objects.create(customer=customer)

        for p_id, qty in zip(product_ids, quantities):
            if not p_id or not qty:
                continue
            product = get_object_or_404(Product, pk=p_id)
            quantity = int(qty)

            if quantity > product.stock:
                invoice.delete()
                messages.error(request, f"Omborda yetarli {product.name} yo'q! Qoldi: {product.stock} dona")
                return render(request, 'water/invoice_form.html', {'customers': customers, 'products': products})

            InvoiceItem.objects.create(invoice=invoice, product=product, quantity=quantity)
            product.stock -= quantity
            product.save()

        invoice.update_total_price()
        messages.success(request, f"Faktura #{invoice.pk} muvaffaqiyatli yaratildi!")
        return redirect('invoice_list')

    return render(request, 'water/invoice_form.html', {
        'customers': customers, 'products': products
    })


@login_required(login_url='/dashboard/login/')
def invoice_delete(request, pk):
    if not request.user.is_superuser:
        messages.error(request, "Sizda buyurtmalarni o'chirish huquqi yo'q!")
        return redirect('invoice_list')

    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == 'POST':
        invoice.delete()
        messages.success(request, "Faktura o'chirildi!")
        return redirect('invoice_list')
    return render(request, 'water/confirm_delete.html', {'object': invoice, 'type': 'faktura'})