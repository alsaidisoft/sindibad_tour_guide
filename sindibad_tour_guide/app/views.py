from django.shortcuts import render, redirect
from app.forms import CountryForm,CityForm,CategoryForm,SubCatForm,UserForm
from app.models import Countries,Cities,Categories,SubCategories,Users,Roles
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from itertools import chain



# Create your views here.

#this prt to get date and time in this moment to use it later for any CRUD actions
now = datetime.now()
#this to view home page of website for normal users
def homepage(request):
    return render(request,'home.html')
#to logout from control panel
def logout(request):
    check = request.session.is_empty()
    if check != False:
        del request.session['username']
        del request.session['name']
    return render(request,'login/log.html')
#this view is for log in form
def loginpage(request):
    #first we need to check if session is empety, if not we can enter login page directly, no need to log in every time
    check = request.session.is_empty()
    if check:
        return render(request,'login/log.html')
    else:
        return render(request,'index.html')

#this view for index page
def indexpage(request):
     check = request.session.is_empty()
     if check:
        return render(request,'login/log.html')
     else:
        return render(request,'index.html')
#show the main view of countries to control add, edit , view and elete
def showcountries(request):
    count = Countries.objects.filter(active =1)
    return render(request,'countries/show.html',{'count':count})

#show the main view of cities to control add, edit , view and elete
def showcities(request):
    count = Cities.objects.filter(active =1)
    return render(request,'cities/show.html',{'count':count})
#show the main view of categories to control add, edit , view and elete
def showcategories(request):
    count = Categories.objects.filter(active =1)
    return render(request,'categories/show.html',{'count':count})
#show the main view of sub_categories to control add, edit , view and elete
def showsubcat(request):
    count = SubCategories.objects.filter(active =1)
    return render(request,'sub_cat/show.html',{'count':count})
#show the main view of users to control add, edit , view and elete
def showusers(request):
    count = Users.objects.filter(active =1)
    return render(request,'users/show.html',{'count':count})
#show tresult of search, this is main method to search for any subcategory (hotels,restaurants,entertainments, tour_guide companies) 
# by entering country or city in search engine
@csrf_exempt
def result(request):
    if request.method == "POST":
       # get the keyword of search
       city = request.POST['city']
       #check first in citis if the keyword is city
       c = Cities.objects.filter(name__contains = city)
       if c.count() >0:
          # search in every sub_category for that city
          for i in c:
            cc = i.id
            hotels = SubCategories.objects.filter(city_id = cc,cat=9,active =1)
            restaurants = SubCategories.objects.filter(city_id = cc,cat=10,active =1)
            entertainments = SubCategories.objects.filter(city_id = cc,cat=12,active =1)
            tour_guide = SubCategories.objects.filter(city_id = cc,cat=13,active =1)
            return render(request,'result.html',{'hotels':hotels,'restaurants':restaurants,'entertainments':entertainments,'tour_guide':tour_guide})
       else:
            #check if the posted keyword is country
            country = request.POST['city']
            # search in countries
            co = Countries.objects.filter(name__contains = country)
            hotels = ""
            restaurants = ""
            entertainments = ""
            tour_guide = ""
            if co.count() >0:
                for ii in co:
                    #search for cities in that country
                    id_country = Cities.objects.filter(country = ii.id) 
                    if id_country.count()>0:
                        for ci in id_country:
                             # here we save all results in same hotels, restaurants, entertainments, tour_guide by using chain library to concatenate QuerySet
                             hotels = chain(hotels,SubCategories.objects.filter(city_id = ci.id,cat=9,active =1))
                             restaurants = chain(restaurants,SubCategories.objects.filter(city_id = ci.id,cat=10,active =1))
                             entertainments = chain(entertainments,SubCategories.objects.filter(city_id = ci.id,cat=12,active =1))
                             tour_guide = chain(tour_guide,SubCategories.objects.filter(city_id = ci.id,cat=13,active =1))
                    return render(request,'result.html',{'hotels':hotels,'restaurants':restaurants,'entertainments':entertainments,'tour_guide':tour_guide})
            return render(request,'home.html')
    else:
        return render(request,'home.html')

# this action is to check login Credential
@csrf_exempt
def singin(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                check = Users.objects.filter(username=form.cleaned_data['username']).filter( password = form.cleaned_data['password']).filter(active = 1)
                if not check:
                    request.session['username'] = 'nothing'
                    messages.info(request, 'Your username or password are wrong!')
                    return render(request,'login/log.html')
                else:
                    request.session['username'] = form.cleaned_data['username']
                    for i in check:
                        request.session['name'] = i.name
                    messages.info(request, 'Login successfully !')
                    return render(request,'index.html')
            except:
                pass
    else:
        form = UserForm()
    return render(request,'/login/log.html',{'form':form})
#add form of country
@csrf_exempt
def addcountry(request):
    if request.method == "POST":
        #paste everything of form inside CountryForm in form.py
        form = CountryForm(request.POST,request.FILES)
        if form.is_valid():
            try:
                # use Model countries to control all fields not included in the html form 
                country = Countries()
                country.active =  1
                country.created_by =  request.session['username']
                country.created_date =  now
                country.profile = form.cleaned_data['profile']
                country.name = form.cleaned_data['name']
                country.description = form.cleaned_data['description']
                country.save()
                return redirect('/countries/show')
            except:
                pass
    else:
        form = CountryForm()
    return render(request,'countries/add.html',{'form':form})

#add form of category
@csrf_exempt
def addcategory(request):
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # use Model Categories to control all fields not included in the html form 
                cat = Categories()
                cat.active =  1
                cat.created_by =  request.session['username']
                cat.created_date =  now
                cat.icon = form.cleaned_data['icon']
                cat.name = form.cleaned_data['name']
                cat.description = form.cleaned_data['description']
                cat.save()
                return redirect('/categories/show')
            except:
                pass
    else:
        form = CategoryForm()
    return render(request,'categories/add.html',{'form':form})
#add form of cities
@csrf_exempt
def addcity(request):
    #get all countries FK to use them in cities form select list
    count = Countries.objects.filter(active =1)
    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            try:
                # use Model Cities to control all fields not included in the html form 
                city = Cities()
                city.active =  1
                city.created_by =  request.session['username']
                city.created_date =  now
                city.country = form.cleaned_data['country']
                city.name = form.cleaned_data['name']
                city.description = form.cleaned_data['description']
                city.save()
                return redirect('/cities/show')
            except:
                pass
    else:
        form = CityForm()
    return render(request,'cities/add.html',{'form':form,'count':count})

#add form of users
@csrf_exempt
def adduser(request):
    #get all Roles FK to use them in Users form select list
    roles = Roles.objects.all()
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                # use Model Users to control all fields not included in the html form 
                u = Users()
                u.active =  1
                u.created_by =  request.session['username']
                u.created_date =  now
                u.role = form.cleaned_data['role']
                u.name = form.cleaned_data['name']
                u.email = form.cleaned_data['email']
                u.phone = form.cleaned_data['phone']
                u.username = form.cleaned_data['username']
                u.password = form.cleaned_data['password']
                u.save()
                return redirect('/users/show')
            except:
                pass
    else:
        form = UserForm()
    return render(request,'users/add.html',{'form':form,'roles':roles})
# add form of subCategories
@csrf_exempt
def addsubcat(request):
    #get all cities FK to use them in subcategoryies form select list
    cities = Cities.objects.filter(active =1)
    #get all categories FK to use them in subcategoryies form select list
    categories = Categories.objects.filter(active =1)
    if request.method == "POST":
        form = SubCatForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # use Model SubCategories to control all fields not included in the html form 
                sub = SubCategories()
                sub.active =  1
                sub.created_by =  request.session['username']
                sub.created_date =  now
                sub.sub_cat_image = form.cleaned_data['sub_cat_image']
                sub.city = form.cleaned_data['city']
                sub.cat = form.cleaned_data['cat']
                sub.name = form.cleaned_data['name']
                sub.phone = form.cleaned_data['phone']
                sub.website = form.cleaned_data['website']
                sub.direction = form.cleaned_data['direction']
                sub.description = form.cleaned_data['description']
                sub.save()
                return redirect('/sub_cat/show')
            except:
                pass
    else:
        form = SubCatForm()
    return render(request,'sub_cat/add.html',{'form':form,'cities':cities,'categories':categories})
# about view
def about(request):
    return render(request,'about.html')
# page view to get all data related to subcategory (hotel, restaurant, entertainment....)
def page(request, id):
    count = SubCategories.objects.get(id = id)
    return render(request,'page.html',{'count':count})
# edit view to edit country
def editcountry(request, id):
    count = Countries.objects.get(id = id)
    return render(request,'countries/edit.html',{'count':count})
# edit view to edit city
def editcity(request, id):
    count = Cities.objects.get(id = id)
    cc = Countries.objects.filter(active =1)
    return render(request,'cities/edit.html',{'count':count,'cc':cc})
# edit view to edit user
def edituser(request, id):
    count = Users.objects.get(id = id)
    roles = Roles.objects.all()
    return render(request,'users/edit.html',{'count':count,'roles':roles})
# edit view to edit subcategory
def editsubcat(request, id):
    count = SubCategories.objects.get(id = id)
    cities = Cities.objects.filter(active =1)
    categories = Categories.objects.filter(active =1)
    return render(request,'sub_cat/edit.html',{'count':count,'cities':cities,'categories':categories})
# edit view to edit category
def editcategory(request, id):
    count = Categories.objects.get(id = id)
    return render(request,'categories/edit.html',{'count':count})
# update controller to update country as action in the form
def updatecountry(request, id):
    count = Countries.objects.get(id = id)
   
    form = CountryForm(request.POST, request.FILES, instance=count)
    if form.is_valid():
        count.created_by = count.created_by
        count.created_date = count.created_date
        count.active = 1
        count.updated_by = request.session['username']
        count.updated_date = now
        count.profile = form.cleaned_data['profile']
        count.name = form.cleaned_data['name']
        count.description = form.cleaned_data['description']
        count.save()
        return redirect('/countries/show')
    return render(request,'countries/edit.html',{'count':count})
# update controller to update category as action in the form
def updatecategory(request, id):
    count = Categories.objects.get(id = id)
    form = CategoryForm(request.POST,request.FILES, instance=count)
    if form.is_valid():
        count.created_by = count.created_by
        count.created_date = count.created_date
        count.active = 1
        count.updated_by = request.session['username']
        count.updated_date = now
        count.icon = form.cleaned_data['icon']
        count.name = form.cleaned_data['name']
        count.description = form.cleaned_data['description']
        count.save()
        return redirect('/categories/show')
    return render(request,'categories/edit.html',{'count':count})
# update controller to update country as action in the form
def updatecity(request, id):
    count = Cities.objects.get(id = id)
    cc = Countries.objects.filter(active =1)
    form = CityForm(request.POST, instance=count)
    if form.is_valid():
        count.created_by = count.created_by
        count.created_date = count.created_date
        count.active = 1
        count.updated_by = request.session['username']
        count.updated_date = now
        count.country = form.cleaned_data['country']
        count.name = form.cleaned_data['name']
        count.description = form.cleaned_data['description']
        count.save()
        return redirect('/cities/show')
    return render(request,'cities/edit.html',{'count':count,'cc':cc})
# update controller to update user as action in the form
def updateuser(request, id):
    count = Users.objects.get(id = id)
    roles = Roles.objects.all()
    form = UserForm(request.POST, instance=count)
    if form.is_valid():
        count.created_by = count.created_by
        count.created_date = count.created_date
        count.active = 1
        count.updated_by = request.session['username']
        count.updated_date = now
        count.role = form.cleaned_data['role']
        count.name = form.cleaned_data['name']
        count.email = form.cleaned_data['email']
        count.phone = form.cleaned_data['phone']
        count.username = form.cleaned_data['username']
        count.password = form.cleaned_data['password']
        count.save()
        return redirect('/users/show')
    return render(request,'users/edit.html',{'count':count,'roles':roles})
# update controller to update subcategory as action in the form
def updatesubcat(request, id):
    count = SubCategories.objects.get(id = id)
    cities = Cities.objects.filter(active =1)
    categories = Categories.objects.filter(active =1)
    form = SubCatForm(request.POST,request.FILES, instance = count)
    if form.is_valid():
        count.created_by = count.created_by
        count.created_date = count.created_date
        count.active = 1
        count.updated_by = request.session['username']
        count.updated_date = now
        count.sub_cat_image = form.cleaned_data['sub_cat_image']
        count.city = form.cleaned_data['city']
        count.cat = form.cleaned_data['cat']
        count.name = form.cleaned_data['name']
        count.phone = form.cleaned_data['phone']
        count.website = form.cleaned_data['website']
        count.direction = form.cleaned_data['direction']
        count.description = form.cleaned_data['description']
        count.save()
        return redirect('/sub_cat/show')
    return render(request,'sub_cat/edit.html',{'count':count,'cities':cities,'categories':categories})

# delete action to delete country, city, category, subcategory and users, just update active field to 0 to hide the row to avoid related rows in other tables as FK, 
# hide row better than delete row to return to histroy when admin need that
def deletecountry(request, id):
    count = Countries.objects.get(id = id)
    count.created_by = count.created_by
    count.created_date = count.created_date
    count.updated_by = request.session['username']
    count.updated_date = now   
    count.active = 0
    count.save()
    return redirect('/countries/show')

def deletecity(request, id):
    count = Cities.objects.get(id = id)
    count.created_by = count.created_by
    count.created_date = count.created_date
    count.updated_by = request.session['username']
    count.updated_date = now   
    count.active = 0
    count.save()
    return redirect('/cities/show')

def deletecategory(request, id):
    count = Categories.objects.get(id = id)
    count.created_by = count.created_by
    count.created_date = count.created_date
    count.updated_by = request.session['username']
    count.updated_date = now   
    count.active = 0
    count.save()
    return redirect('/categories/show')

def deletesubcat(request, id):
    count = SubCategories.objects.get(id = id)
    count.created_by = count.created_by
    count.created_date = count.created_date
    count.updated_by = request.session['username']
    count.updated_date = now   
    count.active = 0
    count.save()
    return redirect('/sub_cat/show')

def deleteuser(request, id):
    count = Users.objects.get(id = id)
    count.created_by = count.created_by
    count.created_date = count.created_date
    count.updated_by = request.session['username']
    count.updated_date = now   
    count.active = 0
    count.save()
    return redirect('/users/show')

