import re
from django.http import HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect 
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from models import Group, Policy, Enforcement, Device, Package, Product, File

@require_GET
@login_required
def search(request):
    context = {}
    context['group_title'] = _('Groups')
    context['policy_title'] = _('Policies')
    context['device_title'] = _('Devices')
    context['package_title'] = _('Packages')
    context['product_title'] = _('Products')
    context['file_title'] = _('Files')
    
    context['groups'] = Group.objects.all().order_by('name')
    context['policies'] = Policy.objects.all().order_by('name')
    context['devices'] = Device.objects.all().order_by('value')
    context['packages'] = Package.objects.all().order_by('name')
    context['products'] = Product.objects.all().order_by('name')
    context['files'] = File.objects.all().order_by('name')
    
    q = request.GET.get('q', '')
    if q != '':
        context['query'] = q
        context['groups'] = Group.objects.filter(name__icontains=q)
        context['policies'] = Policy.objects.filter(name__icontains=q)
        context['devices'] = Device.objects.filter(value__icontains=q)
        context['packages'] = Package.objects.filter(name__icontains=q)
        context['products'] = Product.objects.filter(name__icontains=q)
        context['files'] = File.objects.filter(name__icontains=q)

    groups = Group.objects.filter(name__icontains=q)
    policies = Policy.objects.filter(name__icontains=q)
    devices = Device.objects.filter(value__icontains=q)
    packages = Package.objects.filter(name__icontains=q)
    products = Product.objects.filter(name__icontains=q)
    files = File.objects.filter(name__icontains=q)
    
    return render(request, 'cygapp/search.html', context)