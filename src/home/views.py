from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from database.models.user import Customer, Manager, Cook, Salesperson, Deliverer
from database.models.restaurant import Restaurant
from database.models.address import CustomerAddress, RestaurantAddress, Address
from helper import parse_req_body, userTypeChecker
# from django.contrib import admin

# Create your views here.

def nexus(request):
    """
        This view will simply redirect the user to another
        url based on what usertype they are
    """
    user = request.user
    userIs = userTypeChecker(user)
    response = None
    try:
        if userIs(Manager):
            print('redirecting to manager-home')
            response = redirect('manager-home')
        elif userIs(Deliverer):
            print('redirecting to deliverer-home')
            response = redirect('deliverer-home')
        elif userIs(Cook):
            print('redirecting to cook-home')
            response = redirect('cook-home')
        elif userIs(Salesperson):
            print('redirecting to salesperson-home')
            response = redirect('salesperson-home')
        elif userIs(Customer):
            print('redirecting to customer-home')
            response = redirect('customer-home')
        else:
            print('user assumed to be site staff')
            response = redirect('/admin')
    except:
        if user.is_staff:
            print('user is site staff')
            response = redirect('/admin')
        print('anon user')
        print('redirecting to customer-home')
        response = redirect('customer-home')
    return response

def signup(request):
    """
    signup
    """
    states = [choice[1] for choice in Address.STATE_CHOICES]
    error = None

    if(request.method == "POST"):
        body = parse_req_body(request.body)

        addr_str_accept = []
        for string in [ body['staddr'], body['city'], body['state'], body['zipcode'] ]:
            word_acceptable = False
            for char in string:
                if char != ' ':
                   word_acceptable = True 
                   break
            addr_str_accept.append(word_acceptable)
        addr_acceptable = False in addr_str_accept
        addr_acceptable = not addr_acceptable
        rest_acceptable = False
        for char in body['restname']:
            if char != ' ':
                rest_acceptable = True 
                break

        if(body['usertype']=='cust'):
            if addr_acceptable:
                new_user = User.objects.create_user(body['usrname'], body['email'].replace('%', '@'), body['psw'])
                new_customer = Customer(user=new_user)
                new_customer.save()
                new_customer_address = CustomerAddress(
                    street_address = body['staddr'],
                    apt = body['apt'],
                    city = body['city'],
                    state = body['state'],
                    zip_code = int(body['zipcode']),
                    customer = new_customer
                )
                new_customer_address.save()
            else:
                error = 'must enter address'
                return render(request, 'home/signup.html', {'states': states, 'error': error})
        elif(body['usertype']=='mang'):
            if addr_acceptable and rest_acceptable:
                new_user = User.objects.create_user(body['usrname'], body['email'].replace('%', '@'), body['psw'])
                new_manager = Manager(user=new_user)
                new_manager.save()
                new_resturant = Restaurant(name=body['restname'], manager=new_manager)
                new_resturant.save()
                new_resturant_address = RestaurantAddress(
                    street_address = body['staddr'],
                    apt = body['apt'],
                    city = body
                    ['city'],
                    state = body['state'],
                    zip_code = body['zipcode'],
                    restaurant = new_resturant
                )
                new_resturant_address.save()
            else:
                error = 'must enter address and restaurant name'
                return render(request, 'home/signup.html', {'states': states, 'error': error})
        elif(body['usertype']=='cook'):
            new_user = User.objects.create_user(body['usrname'], body['email'].replace('%', '@'), body['psw'])
            new_staff = Cook(user=new_user)
            new_staff.save()
        elif(body['usertype']=='salespers'):
            new_user = User.objects.create_user(body['usrname'], body['email'].replace('%', '@'), body['psw'])
            new_staff = Salesperson(user=new_user)
            new_staff.save()
        elif(body['usertype']=='deliverer'):
            new_user = User.objects.create_user(body['usrname'], body['email'].replace('%', '@'), body['psw'])
            new_staff = Deliverer(user=new_user)
            new_staff.save()
        else:
            error = 'must pick a user type'
            return render(request, 'home/signup.html', {'states': states, 'error': error})
        response = redirect('home-nexus')
        return response
    else:
        return render(request, 'home/signup.html', {'states': states, 'error': error})

