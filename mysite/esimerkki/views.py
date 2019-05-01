from django.shortcuts import render, redirect
import requests
from .models import Product
from .forms import ProductForm
from django.shortcuts import render_to_response

import urllib.request
import xmltodict



def stops(request):

	file = urllib.request.urlopen('http://api.publictransport.tampere.fi/prod/?request=stops_area&user=username&pass=password&bbox=3328253,6823773,3331775,6826815&center_coordinate=3331810,6823852&diameter=1500&format=xml')
	data = file.read()
	file.close()
	
	data = xmltodict.parse(data)
	return render_to_response('stops.html', {'data' : data})

def list_products(request):

	if(request.GET.get('mybtn')):
		stops(int(request.GET.get('mytextbox')) )
	return render(request,'stops.html')
	
	products = Product.objects.all()
	return render(request, 'products.html', {'products' : products})
	
def create_product(request):
	form = ProductForm(request.POST or None)
	
	if form.is_valid():
		form.save()
		return redirect('list_products')
		
	return render(request, 'products-form.html', {'form' : form})
	
def update_product(request, id):

	product = Product.objects.get(id=id)
	form = ProductForm(request.POST or None, instance=product)
	
	if form.is_valid():
		form.save()
		return redirect('list_products')
		
	return render(request, 'products-form.html', {'form': form, 'product': product})
	
def delete_product(request, id):
	product = Product.objects.get(id=id)
	
	if request.method == 'POST':
		product.delete()
		return redirect('list_products')
		
	return render (request, 'prod-delete-confirm.html', {'product': product})