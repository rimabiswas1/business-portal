from django.shortcuts import render , redirect
from users.models import *

from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from decimal import Decimal, InvalidOperation




# Create your views here.

# def business_list(request):
#     search_query = request.GET.get('search', '')
#     sort_option = request.GET.get('sort', '')

#     businesses = Business.objects.all()
#     if search_query:
#         businesses = businesses.filter(name__icontains=search_query)
#     if sort_option:
#         businesses = businesses.order_by(sort_option)

    
#     paginator = Paginator(businesses, 6)  
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     context = {
#         'businesses': page_obj
#     }
#     return render(request, 'business/business_list.html', context)






def business_list(request):
   
    search_query = request.GET.get('search', '')
    sort_option = request.GET.get('sort', 'business_name')
    businesses = Business.objects.all()
    if search_query:
        businesses = businesses.filter(business_name__icontains=search_query)

    if sort_option:
        businesses = businesses.order_by(sort_option)
    paginator = Paginator(businesses, 6)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'businesses': page_obj,
        'search_query': search_query,
        'sort_option': sort_option,
    }
    return render(request, 'business/business_list.html', context)








def business_create(request):
    if request.method == 'POST':
       
        business_name = request.POST.get('business_name')
        description = request.POST.get('description')
        category = request.POST.get('category')
        address = request.POST.get('address')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        
        if Business.objects.filter(user=request.user).exists():
            messages.error(request, 'You already have a business.')
            return redirect('business_list')

        if not business_name or not category or not address or not phone or not email:
            messages.error(request, 'Please fill in all required fields.')
        else:
            try:
                latitude = Decimal(latitude) if latitude else None
            except InvalidOperation:
                messages.error(request, 'Invalid latitude value.')
                return render(request, 'business/business_create.html')

            try:
                longitude = Decimal(longitude) if longitude else None
            except InvalidOperation:
                messages.error(request, 'Invalid longitude value.')
                return render(request, 'business/business_create.html')

            Business.objects.create(
                user=request.user,
                business_name=business_name,
                description=description,
                category=category,
                address=address,
                latitude=str(latitude) if latitude else None,
                longitude=str(longitude) if longitude else None,
                phone=phone,
                email=email,
            )
            messages.success(request, 'Business created successfully!')
            return redirect('business_list')

    return render(request, 'business/business_create.html')





def business_detail(request, business_id):
    
    business = get_object_or_404(Business, id=business_id)

   
    context = {
        'business': business
    }
    return render(request, 'business/business_detail.html', context)







def business_registration(request):
    if request.method == 'POST':
        business_name = request.POST.get('business_name')
        description = request.POST.get('description')
        category = request.POST.get('category')
        address = request.POST.get('address')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        try:
            business = Business.objects.create(
                business_name=business_name,
                description=description,
                category=category,
                address=address,
                latitude=latitude,
                longitude=longitude,
                phone=phone,
                email=email,
                user=request.user  
            )
            messages.success(request, 'Your business has been successfully registered.')
            return redirect('business_information', business_id=business.id)
        except Exception as e:
            messages.error(request, f"Error registering business: {e}")

    return render(request, 'business/business_registration.html')





def business_information(request, business_id):
    
    business = get_object_or_404(Business, id=business_id)
    ratings = business.ratings.all()
    return render(request, 'business/business_information.html', {'business': business, 'ratings': ratings})
