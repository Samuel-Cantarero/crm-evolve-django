from django.shortcuts import render, get_object_or_404, redirect
from .models import User, Invoice
from .forms import UserForm, InvoiceForm
from django.db.models import Sum, Q

# Usuarios
def user_list(request):
    query = request.GET.get('q')
    if query:
        users = User.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(email__icontains=query)
        ).order_by('-id')
    else:
        users = User.objects.all().order_by('-id')
    return render(request, 'crm/user_list.html', {'users': users})

def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'crm/user_form.html', {'form': form})

def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'crm/user_form.html', {'form': form, 'edit': True})

def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'crm/user_confirm_delete.html', {'user': user})

def user_invoices(request, pk):
    user = get_object_or_404(User, pk=pk)
    invoices = Invoice.objects.filter(user=user)
    return render(request, 'crm/user_invoices.html', {'user': user, 'invoices': invoices})

# Facturas
def invoice_list(request):
    invoices = Invoice.objects.select_related('user').all().order_by('-id')
    return render(request, 'crm/invoice_list.html', {'invoices': invoices})

def invoice_create(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('invoice_list')
    else:
        form = InvoiceForm()
    return render(request, 'crm/invoice_form.html', {'form': form})

def invoice_edit(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            return redirect('invoice_list')
    else:
        form = InvoiceForm(instance=invoice)
    return render(request, 'crm/invoice_form.html', {'form': form, 'edit': True})

def invoice_delete(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == 'POST':
        invoice.delete()
        return redirect('invoice_list')
    return render(request, 'crm/invoice_confirm_delete.html', {'invoice': invoice})

def financial_summary(request):
    users = User.objects.all().annotate(total=Sum('invoices__amount'))
    return render(request, 'crm/financial_summary.html', {'users': users})
