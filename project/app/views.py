from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import*
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from .forms import*
from datetime import datetime
import string
import random
import razorpay
# from django.http import HttpResponse

# Create your views here.

# ================ registration function ================
def registerdata(request):
    print(request.method)
    name=request.POST.get('name')
    email=request.POST.get('email')
    print(email)
    number=request.POST.get('number')
    password=request.POST.get('password')
    con_password=request.POST.get('con_password')
    data=RegistrationModel.objects.filter(Email=email)
    if name=="" or email=="" or number=="" or password=="":
        msg="Please fill all data field"
        return render(request, 'register.html', {'key':msg,'data1':name,'data2':email,'data3':number})     
    else:
        if data:
            msg="User aleary Exist"
            Context={
                 'key':msg
            }
            return render(request, 'register.html', Context)
        else:
            
            if password==con_password:
                global otp
                lis=string.ascii_letters + string.digits
                otp= ''.join(random.choice(lis) for _ in range(4))
                subject = 'New Customer User Account'
                message =  f'TRENDGENIX Registration Email Verification OTP is {otp}. Please verify this OTP.'
                email_from = email
                recipient_list = [email]
                sentmail=send_mail(subject, message, email_from, recipient_list)
                print(sentmail)
                if sentmail:
                    OTP1=otp
                    request.session['regist_customer_info']={
                        'Name':name,
                        'Email':email,
                        'Number':number,
                        'Password':password
                    }
                    otp_email=reversed(email[-1:-15:-1])
                    result=''
                    for i in otp_email:
                        result+=i
                    print(result) 
                    Context={
                       'reg_otp': OTP1,
                       'otp_sending_mail':result
                    }
                    return render(request, 'register.html',Context)   
                else:
                    msg="Password and Confirm Password Not Match"
                    Context={'key':msg,
                            'data1':name,
                            'data2':email,
                            'data3':number
                            }
                    return render(request, 'register.html',Context )
            else:
                msg="Enter Correct email"
                return render(request, 'register.html', {'key': msg})
            
def signup(request):
    first=request.POST.get('first')  
    second=request.POST.get('second')  
    third=request.POST.get('third')  
    fourth=request.POST.get('fourth')
    customer_info=request.session.get('regist_customer_info')
    print(customer_info)
    if otp==first+second+third+fourth:
        RegistrationModel.objects.create(
            Name=customer_info['Name'],
            Email=customer_info['Email'],
            Number=customer_info['Number'],
            Password=customer_info['Password']
        )
        subject = 'New Customer User Account'
        message = 'A New Customer register On Our Website'+customer_info['Name']+'  '+customer_info['Email']+'  '+customer_info['Number']+'  '+customer_info['Password']
        email_from = customer_info['Email']
        recipient_list = ['indrajeetyadu36@gmail.com']
        send_mail(subject, message, email_from, recipient_list)
        msg="Registration Successfully Done"
        del request.session['regist_customer_info']
        return render(request, 'login.html', {'key': msg})
    else:
        msg="Enter Correct OTP"
        return render(request, 'register.html', {'reg_otp': otp, 'key':msg})



# ============= login function =====================
   
def logindata(request):
    email=request.POST.get('email')
    password=request.POST.get('password')
    login_type=request.POST.get('login_type')
    # print(login_type)
    username=RegistrationModel.objects.filter(Email=email)
    if login_type=='none':
        msg="Choose your login Type"
        return render(request, 'login.html', {'key1': msg})
    elif login_type =='customer':
        if username:
            data=RegistrationModel.objects.get(Email=email)
            print("*********************************************")
            
            Password= data.Password
            if Password==password:
                msg="Welcome To "+data.Name
                request.session['User_id'] = data.id
                User_id=request.session.get('User_id')
                user_info=get_object_or_404(RegistrationModel, id=User_id)
                print('user_info-->',user_info)
                Context={
                         'key1': msg, 
                         'user_name':user_info, 
                         'media_url':settings.MEDIA_URL
                        }
                return render(request, 'index.html',Context )
            else:
                msg="Enter Password is Wrong Please Enter Correct Password"
                return render(request, 'login.html', {'key1': msg})
        else:
            msg="Userid doesnot exist Please create Account"
            return render(request, 'register.html', {'key1': msg})
    elif login_type =="admin":
        if username:
            data=RegistrationModel.objects.get(Email=email)
            print(data.Name)
            print(data)
            Password= data.Password
            if Password==password:
                request.session['Admin_id'] = data.id 

                Admin_id=request.session.get('Admin_id')
                admin_info=get_object_or_404(RegistrationModel, id=Admin_id)
                msg="Welcome To "+data.Name
                Context={
                    'media_url': settings.MEDIA_URL,
                    'key1': msg, 
                    'admin_user':admin_info 
                }
                return render(request, 'dashboard.html',Context )
            else:
                msg="Enter Password is Wrong Please Enter Correct Password"
                return render(request, 'login.html', {'key1': msg})
        else:
            msg="Userid doesnot exist Please create Account"
            return render(request, 'register.html', {'key1': msg})
        
# ============================== logout ===================================
def logout(request):
    del request.session['User_id']
    return render(request, 'index.html')

def Adminlogout(request):
    del request.session['Admin_id']
    return render(request, 'index.html')


def forgetpass(request):
    return render(request, 'forgetpass.html')

def setfogetpass1(request):
    email=request.POST.get('email')
    print(email)
    ckeck_account=get_object_or_404(RegistrationModel, Email=email)
    print(ckeck_account)
    global forget_otp
    if ckeck_account:
        lis=string.ascii_letters + string.digits
        otp= ''.join(random.choice(lis) for _ in range(4))
        subject = 'New Customer User Account'
        message =  f'TRENDGENIX forget Password creating new password Email Verification OTP is {otp}. Please verify this OTP.'
        email_from = email
        recipient_list = [email]
        sentmail=send_mail(subject, message, email_from, recipient_list)
        print(sentmail)
        forget_otp=otp
        if sentmail:
            otp_email=reversed(email[-1:-15:-1])
            result=''
            for i in otp_email:
                result+=i
            request.session['forg_user_info']={
                'Name':ckeck_account.Name,
                'Email':ckeck_account.Email,
                'Password':ckeck_account.Password
            }
            print(result) 
            Context={
                'fotget_otp':forget_otp,
                'sending_email':result
            }
        return render(request, 'forgetpass.html', Context)
    else:
        msg= email+' '+'Account does not exist, Please Enter correct Email'
        return render(request, 'forgetpass.html', {'key':msg})

def otpforgpass(request):
    first=request.POST.get('first')  
    second=request.POST.get('second')  
    third=request.POST.get('third')  
    fourth=request.POST.get('fourth')
    if forget_otp==first+second+third+fourth:
        msg="forget change password form"
        return render(request,'forgetpass.html',{'forg_user_info':msg})

def setforget_password(request):
    forget_userinfo=request.session['forg_user_info']
    newpassword = request.POST.get('newpassword')
    conpassword = request.POST.get('conpassword')
    if newpassword==conpassword:
        regist_data=get_object_or_404(RegistrationModel, Email=forget_userinfo['Email'])
        regist_data.Password=newpassword
        regist_data.save(update_fields=['Password'])
        msg='Password successfully Changed'
        return render(request, 'login.html', {'key':msg})
    else:
        msg='Newpassword and Confirm Password does not match'
        return render(request, 'forgetpass.html', {'forg_user_info':msg})







#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@---- User Dashboard -----@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#====================== Starting user Dashboard (Navigation) =======================

def index(request):
    try:
        User_id=request.session.get('User_id')
        user_info=get_object_or_404(RegistrationModel, id=User_id)
        addcart = request.session.get('addtocart')
        try:
            cart_no=len(addcart)
        except:
            cart_no=0
        Context={
            'user_name':user_info,
            'addcartno': cart_no,
            'media_url': settings.MEDIA_URL,
        }
        return render(request, 'index.html',Context )
    except:
        return render(request, 'index.html')

def about(request):
    try:
        User_id=request.session.get('User_id')
        user_info=get_object_or_404(RegistrationModel, id=User_id)
        addcart = request.session.get('addtocart')
        try:
            cart_no=len(addcart)
        except:
            cart_no=0
        Context={
            'user_name':user_info,
            'addcartno': cart_no,
            'media_url': settings.MEDIA_URL,
        }           
        return render(request, 'about.html', Context)
    except:
        return render(request, 'about.html')

def contact(request):
    try:
        User_id=request.session.get('User_id')
        user_info=get_object_or_404(RegistrationModel, id=User_id)
        addcart = request.session.get('addtocart')
        try:
            cart_no=len(addcart)
        except:
            cart_no=0
        Context={
            'user_name':user_info,
            'addcartno': cart_no,
            'media_url': settings.MEDIA_URL,
        }
        return render(request, 'contact.html', Context)
    except:
        return render(request, 'contact.html')

def register(request):
    return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')

def product(request):
    try:
        User_id=request.session.get('User_id')
        user_info=get_object_or_404(RegistrationModel, id=User_id)
        addcart = request.session.get('addtocart')
        try:
            cart_no=len(addcart)
        except:
            cart_no=0
        Context={
            'user_name':user_info,
            'addcartno': cart_no,
            'media_url': settings.MEDIA_URL,
        }
        return render(request, 'product.html', Context)
    except:
        return render(request, 'product.html')

# ----------------- starting Product page navigation -------------------------
def men(request):
    data=Productmodel.objects.filter(Prod_Name="Men")
    print(data.values()) 
    try:
        User_id=request.session.get('User_id')
        user_info=get_object_or_404(RegistrationModel, id=User_id)
        addcart = request.session.get('addtocart')
        try:
            cart_no=len(addcart)
        except:
            cart_no=0
        Context={
            'prop':data,
            'media_url': settings.MEDIA_URL,
            'user_name':user_info,
            'addcartno': cart_no,
        }
        return render(request, 'men.html',Context)
    except:
        Context={
            'prop':data,
            'media_url': settings.MEDIA_URL
        }
        return render(request,'men.html',Context )


def women(request):
    data=Productmodel.objects.filter(Prod_Name="Women")
    print(data.values())
    try:
        User_id=request.session.get('User_id')
        user_info=get_object_or_404(RegistrationModel, id=User_id)
        addcart = request.session.get('addtocart')
        try:
            cart_no=len(addcart)
        except:
            cart_no=0
        Context={
        'prop':data,
        'media_url': settings.MEDIA_URL,
        'user_name':user_info,
        'addcartno': cart_no,
    }
        return render(request, 'women.html', Context)
    except:
        Context={
        'prop':data,
        'media_url': settings.MEDIA_URL
    }
        return render(request, 'women.html',Context)

def girl(request):
    data=Productmodel.objects.filter(Prod_Name="Girl")
    # print(data.values())
    try:
        User_id=request.session.get('User_id')
        user_info=get_object_or_404(RegistrationModel, id=User_id)
        addcart = request.session.get('addtocart')
        try:
            cart_no=len(addcart)
        except:
            cart_no=0
        Context={
        'prop':data,
        'media_url': settings.MEDIA_URL,
        'user_name':user_info,
        'addcartno': cart_no,
    }
        return render(request, 'girl.html', Context )
    except:
        Context={
            'prop':data,
            'media_url': settings.MEDIA_URL
        }
        return render(request, 'girl.html', Context)
    
# ====================== Starting User Dashboard (Add to Cart) =============================================
#  =---------------------- Starting Cart add Button -----------------------------------------------
def addtocart(request, pk):
    # user_info=request.session.get('user_info')
    email = request.POST.get('email')
    prod_name = request.POST.get('prod_name')
    if email:
        data = RegistrationModel.objects.get(Email=email)
        addtocart = request.session.get('addtocart', [])
        addcart = request.session.get('addtocart')
        print(addcart)
        if pk not in [item['id'] for item in addtocart]:
            add_cartdata = {
                'id': pk,
                'Quantity': 1
            }
            addtocart.append(add_cartdata)
        request.session['addtocart'] = addtocart
        try:
            cart_no=len(addcart)
        except:
            cart_no=0
        user_info=data
        if prod_name == 'Men':
            prod_data1 = Productmodel.objects.filter(Prod_Name='Men')
            Context={
                'user_name': user_info, 
                'prop': prod_data1, 
                'addcartno': cart_no, 
                'media_url': settings.MEDIA_URL
            }
            return render(request, 'men.html', Context)
        elif prod_name == 'Women':
            prod_data1 = Productmodel.objects.filter(Prod_Name='Women')
            Context={
                'user_name': user_info, 
                'prop': prod_data1, 
                'addcartno': cart_no, 
                'media_url': settings.MEDIA_URL
            }
            return render(request, 'women.html', Context)
        elif prod_name == 'Kids':
            prod_data1 = Productmodel.objects.filter(Prod_Name='Kids')
            Context={
                'user_name': user_info, 
                'prop': prod_data1, 
                'addcartno': cart_no,
                'media_url': settings.MEDIA_URL
            }
            return render(request, 'girl.html', Context)
    else:
        return redirect('login')
# --------------------------------------------------------------------
def increment(request):
    User_id = request.session.get('User_id')
    user_info = get_object_or_404(RegistrationModel, id=User_id)
    addcart = request.session.get('addtocart', [])
    print(addcart)
    try:
        cart_no=len(addcart)
    except:
        cart_no=0
    prod_id = int(request.POST.get('incr'))
    total_MRP = 0
    total_amount = 0
    tax = 0
    shippingcharge = 40
    Quantity = 0
    pro_data = []

    for item in addcart:
        print('==============================')
        print(prod_id)
        print(type(prod_id))
        print(item['id'])
        print(type(item['id']))
        if prod_id == item['id']:
            print('==============================')
            pquantity=item['Quantity']
            # print(type(pquantity))
            pquantity=pquantity+1
            item['Quantity']=pquantity
            # print(item['Quantity'])
            print('==============================')

            break  
    request.session['addtocart'] = addcart
    addcart = request.session.get('addtocart', [])
    try:
        cart_no=len(addcart)
    except:
        cart_no=0
    for item in addcart:
        pro_value = Productmodel.objects.get(id=item['id'])
        print(item['Quantity'])
        pro_quantitydata = {
            'pro_value': pro_value,
            'Quantity': item['Quantity']
        }
        pro_data.append(pro_quantitydata)
        
        total_amount += pro_value.Prod_Price * item['Quantity']
        total_MRP += pro_value.Prod_MRP * item['Quantity']
        Quantity += item['Quantity']

    tax = int(round((total_amount * 12) / 100, 0))
    
    discount = total_MRP - total_amount
    Total_pay_amount = total_amount + shippingcharge + tax

    billamount = {
        'total_amount': total_amount,
        'total_MRP': total_MRP,
        'discount': discount,
        'tax': tax,
        'shippingcharge': shippingcharge,
        'Total_pay_amount': Total_pay_amount,
        'Quantity': Quantity
    }
    Context = {
        'user_name': user_info,
        'addcartno': cart_no,
        'prod_data': pro_data,
        'media_url': settings.MEDIA_URL,
        'amount': billamount
    }
    return render(request, 'addtocart.html', Context)

def decrement(request):
    User_id = request.session.get('User_id')
    user_info = get_object_or_404(RegistrationModel, id=User_id)
    addcart = request.session.get('addtocart', [])
    print(addcart)
    try:
        cart_no=len(addcart)
    except:
        cart_no=0
    prod_id = int(request.POST.get('decr'))
    total_MRP = 0
    total_amount = 0
    tax = 0
    shippingcharge = 40
    Quantity = 0
    pro_data = []

    for item in addcart:
        print('==============================')
        print(prod_id)
        print(type(prod_id))
        print(item['id'])
        print(type(item['id']))
        if prod_id == item['id']:
            # print('==============================')
            pquantity=item['Quantity']
            # print(type(pquantity))
            if pquantity>1:
                pquantity=pquantity-1
            item['Quantity']=pquantity
            # print(item['Quantity'])
            # print('==============================')
            break

    request.session['addtocart'] = addcart
    addcart = request.session.get('addtocart', [])
    try:
        cart_no=len(addcart)
    except:
        cart_no=0
    for item in addcart:
        pro_value = Productmodel.objects.get(id=item['id'])
        print(item['Quantity'])
        pro_quantitydata = {
            'pro_value': pro_value,
            'Quantity': item['Quantity']
        }
        pro_data.append(pro_quantitydata)
        
        total_amount += pro_value.Prod_Price * item['Quantity']
        total_MRP += pro_value.Prod_MRP * item['Quantity']
        Quantity += item['Quantity']

    tax = int(round((total_amount * 12) / 100, 0))
    
    discount = total_MRP - total_amount
    Total_pay_amount = total_amount + shippingcharge + tax

    billamount = {
        'total_amount': total_amount,
        'total_MRP': total_MRP,
        'discount': discount,
        'tax': tax,
        'shippingcharge': shippingcharge,
        'Total_pay_amount': Total_pay_amount,
        'Quantity': Quantity
    }
    Context = {
        'user_name': user_info,
        'addcartno': cart_no,
        'prod_data': pro_data,
        'media_url': settings.MEDIA_URL,
        'amount': billamount
    }
    return render(request, 'addtocart.html', Context)


def removeadd_cart(request, pk):
    User_id = request.session.get('User_id')
    user_info = get_object_or_404(RegistrationModel, id=User_id)
    addcart = request.session.get('addtocart', [])
    print(addcart)
    total_MRP = 0
    total_amount = 0
    tax = 0
    shippingcharge = 40
    Quantity = 0
    pro_data = []

    for i in range(len(addcart)):
        print('==============================')
        print(pk)
        print(type(pk))
        print(addcart[i]['id'])
        print(type(addcart[i]['id']))
        if pk == addcart[i]['id']:
            # print('==============================')
            del addcart[i]
            # print('==============================')
            break

    request.session['addtocart'] = addcart
    addcart = request.session.get('addtocart', [])
    try:
        cart_no=len(addcart)
    except:
        cart_no=0
    for item in addcart:
        pro_value = Productmodel.objects.get(id=item['id'])
        print(item['Quantity'])
        pro_quantitydata = {
            'pro_value': pro_value,
            'Quantity': item['Quantity']
        }
        pro_data.append(pro_quantitydata)
        
        total_amount += pro_value.Prod_Price * item['Quantity']
        total_MRP += pro_value.Prod_MRP * item['Quantity']
        Quantity += item['Quantity']

    tax = int(round((total_amount * 12) / 100, 0))
    
    discount = total_MRP - total_amount
    Total_pay_amount = total_amount + shippingcharge + tax

    billamount = {
        'total_amount': total_amount,
        'total_MRP': total_MRP,
        'discount': discount,
        'tax': tax,
        'shippingcharge': shippingcharge,
        'Total_pay_amount': Total_pay_amount,
        'Quantity': Quantity
    }
    Context = {
        'user_name': user_info,
        'addcartno': cart_no,
        'prod_data': pro_data,
        'media_url': settings.MEDIA_URL,
        'amount': billamount
    }
    return render(request, 'addtocart.html', Context)


    
# ---------------------- ENDing Cart add Button -----------------------------------------------

def cartpage(request):
    # email = request.POST.get('email')
    # data = RegistrationModel.objects.get(Email=email)
    User_id=request.session.get('User_id')
    user_info=get_object_or_404(RegistrationModel, id=User_id)
    try:
        addcart = request.session.get('addtocart')
        print(addcart,'----------------------1--')

        try:
            cart_no=len(addcart)
        except:
            cart_no=0

        addcart_data = request.session.get('addtocart', [])
        print(addcart_data,'============================  2  ======')
        total_MRP = 0
        total_amount = 0
        tax = 0
        shippingcharge = 40
        Quantity=0
        pro_data = []

        for item in addcart_data:
            print(item)
            pro_value = get_object_or_404(Productmodel, id=item['id'])
            print(pro_value,'-------------------- 3 ----')
            pro_quantitydata = {
                'pro_value': pro_value,
                'Quantity': item['Quantity']
            }
            print(pro_value,'-----------------  04-------')
            pro_data.append(pro_quantitydata)
            print(pro_quantitydata)
            total_amount += pro_value.Prod_Price * item['Quantity']
            total_MRP += pro_value.Prod_MRP * item['Quantity']
            tax += int(round((total_amount * 12) / 100,0))
            Quantity += item['Quantity']
            print(pro_value,'-----------------  05-------')
              
            print(pro_value,'-----------------  06-------')
                
        discount = total_MRP - total_amount
        print(discount,'================ 6.2 ==================')    
        Total_pay_amount = total_amount + shippingcharge + tax
        print(Total_pay_amount,'================ 6.5 ==================')
        billamount = {
                'total_amount': total_amount,
                'total_MRP': total_MRP,
                'discount': discount,
                'tax': tax,
                'shippingcharge': shippingcharge,
                'Total_pay_amount': Total_pay_amount,
                'Quantity':Quantity     
        }
        print(billamount,'============================ 7 ===')
    
        Context={
            'user_name': user_info,
            'addcartno': cart_no, 
            'prod_data': pro_data, 
            'media_url': settings.MEDIA_URL, 
            'amount': billamount
        }
        print(Context,'------------- 8  -')
        return render(request, 'addtocart.html', Context)
    except:
        return render(request, 'login.html')


# ====================== Ending User Dashboard (Add to Cart) =============================================
 
# ======================== Starting user profile Function ==========================================

def editpro(request):
    email=request.POST.get('email')
    Account_type=request.POST.get('accounttype')
    if Account_type=='admin_profile':
        Admin_id=request.session.get('Admin_id')
        admin_info=get_object_or_404(RegistrationModel, id=Admin_id)
        Context={
            'admin_user':admin_info,
            'profileform':Registrationform,
            'media_url': settings.MEDIA_URL, 
        }
        return render(request, 'editprofile.html', Context)
    elif Account_type=='user_profile':
        User_id=request.session.get('User_id')
        user_info=get_object_or_404(RegistrationModel, id=User_id)
        addcart = request.session.get('addtocart')
        try:
            cart_no=len(addcart)
        except:
            cart_no=0
        Context={
            'user_name': user_info,
            'addcartno': cart_no,
            'profileform':Registrationform,
            'media_url': settings.MEDIA_URL, 
        }
        return render(request, 'editprofile.html', Context)
    
# -------------- image updating -------------------
def updatepro_img(request):
    profile_img=request.FILES.get('Profile')
    print(profile_img)
    pro_image=request.POST.get('Profile')
    Account_type=request.POST.get('accounttype')
    print(Account_type)
    if Account_type =='user_profile':
        User_id=request.session.get('User_id')
        user_info=get_object_or_404(RegistrationModel, id=User_id)
        addcart = request.session.get('addtocart')
        try:
            cart_no=len(addcart)
        except:
            cart_no=0
        regist= RegistrationModel.objects.get(Email=user_info.Email)
        print(regist)
        regist.Profile=profile_img
        regist.save(update_fields=['Profile'])
        data=get_object_or_404(RegistrationModel, Email=user_info.Email)
        Context={
            'user_name' : user_info,
            'addcartno': cart_no,
            'media_url': settings.MEDIA_URL,
            'profileform':Registrationform
        }
        return render(request, 'editprofile.html', Context)
    if Account_type =='admin_profile':
        Admin_id=request.session.get('Admin_id')
        admin_info=get_object_or_404(RegistrationModel, id=Admin_id)
        # regist=get_object_or_404(RegistrationModel, Email=admin_info.Email)
        regist=RegistrationModel.objects.get(Email=admin_info.Email)
        print(regist)
        regist.Profile = pro_image
        regist.save(update_fields=['Profile'])
        registdata=get_object_or_404(RegistrationModel, Email=admin_info.Email)
        print(registdata)
        Context={
            'user_name' : registdata,
            'addcartno': cart_no,
            'media_url': settings.MEDIA_URL,
            'profileform':Registrationform
        }
        return render(request, 'editprofile.html',Context )

def userprofile(request):
    User_id=request.session.get('User_id')
    User_info=get_object_or_404(RegistrationModel, id=User_id)
    addcart = request.session.get('addtocart')
    try:
        cart_no=len(addcart)
    except:
        cart_no=0
    username=request.POST.get('username')
    Fname=request.POST.get('Fname')
    address=request.POST.get('address')
    about=request.POST.get('about')
    email=request.POST.get('email')
    number=request.POST.get('number')
    birthday=request.POST.get('birthday')

    User_info.About=about
    User_info.Username=username
    User_info.Name=Fname
    User_info.Address=address
    User_info.Email=email
    User_info.Number=number
    User_info.Birthday=birthday
    User_info.save(update_fields=['About','Username','Name','Email','Number','Birthday', 'Address'])
    user_info=get_object_or_404(RegistrationModel, id=User_id)
    Context={
        'user_name' : user_info,
        'addcartno': cart_no,
        'media_url': settings.MEDIA_URL, 
    }
    return render(request, 'editprofile.html',Context)

# --------------------------------------------

def changepass(request):
    try:
        Admin_id=request.session.get('Admin_id')
        admin_info=get_object_or_404(RegistrationModel, id=Admin_id)
        Context={
            'admin_user':user_info,
            'media_url': settings.MEDIA_URL
        }
        return render(request, 'changepass.html', Context)
    except:
        User_id=request.session.get('User_id')
        user_info=get_object_or_404(RegistrationModel, id=User_id)
        addcart = request.session.get('addtocart')
        try:
            cart_no=len(addcart)
        except:
            cart_no=0
        Context={
            'user_name':user_info,
            'addcartno': cart_no,
            'media_url': settings.MEDIA_URL,
        }
        return render(request, 'changepass.html', Context)


def passwordchange(request):
    if request.method=='POST':
        email=request.POST.get('email')
        print(email)
        login_type=request.POST.get('login_type')
        newpassword=request.POST.get('newpassword')
        conpassword=request.POST.get('conpassword')
        register = get_object_or_404(RegistrationModel, Email=email)
    try:
        if newpassword == conpassword:
            print(register)
            register.Password = newpassword
            register.save(update_fields=['Password'])

            msg="Password successfully Changed"
            User_id=request.session.get('User_id')
            user_info=get_object_or_404(RegistrationModel, id=User_id)
            addcart = request.session.get('addtocart')
            cart_no=len(addcart)
            Context={
                'key':msg,
                'user_name':user_info,
                'addcartno': cart_no,
                'media_url': settings.MEDIA_URL, 
            }    
            return render(request, 'index.html',Context)
    except:

        if newpassword == conpassword:
            register.Password = newpassword
            register.save(update_fields=['Password'])
            request.session['Password']=newpassword
            msg="Password successfully Changed"

        Admin_id=request.session.get('Admin_id')
        admin_info=get_object_or_404(RegistrationModel, id=Admin_id)
        Context={
            'key':msg,
            'admin_user':admin_info,
             'media_url': settings.MEDIA_URL
        }
        return render(request, 'dashboard.html', Context)    

    
#========================= Endinging user profile Function ==========================================
#========================= ENDing user Dashboard (Navigation) ========================================

# ============ Show Product Data ================
def showmenproductdata(request):
    data=Productmodel.objects.filter(Prod_Name="women")
    # print(data.values())
    return render(request,'men.html',{'prop':data,'media_url': settings.MEDIA_URL} )
# ======== Contact page Customer query ====================================
def customerquery(request):
    User_id=request.session.get('User_id')
    user_info=get_object_or_404(RegistrationModel, id=User_id)
    addcart = request.session.get('addtocart')
    try:
        cart_no=len(addcart)
    except:
        cart_no=0
    # ----------------------------------------------
    name=request.POST.get('name')
    email=request.POST.get('email')
    urlpath=request.POST.get('urlpath')
    query=request.POST.get('query')
    subject = email+' '+'Query'
    message = query
    email_from = email
    recipient_list = ['indrajeetyadu36@gmail.com']
    send_mail(subject, message, email_from, recipient_list)
    msg='Your Query is successfully submited, Thank for Your suggestion'
    Context={
        'key':msg,
        'user_name':user_info,
        'addcartno': cart_no,
        'media_url': settings.MEDIA_URL
    }
    return render(request, 'contact.html', Context)

# =================== Startinging User Dashboard (Razorpay payment integrations) ================================

def checkout(request):
    User_id=request.session.get('User_id')
    user_info=get_object_or_404(RegistrationModel, id=User_id)
    addcart = request.session.get('addtocart')
    try:
        cart_no=len(addcart)
    except:
        cart_no=0
    # ------------------------------------------
    amount=int(request.POST.get('amount'))*100
    # print(amount)
    email=request.POST.get('email')
    # print(email)
    # userdata=RegistrationModel.objects.get(Email=email)
    global Payableamount 
    client = razorpay.Client(auth =("rzp_test_8jTLUV3aVex82Q" , "n3PL7ZbSgnKSWJeA1s9ndhaO"))
    data = { "amount": amount, "currency": "INR", "receipt": "order_rcptid_11" }
    # print(data)
    payment = client.order.create(data=data)
    print("Payment ----->",payment)
    Payableamount=payment

    print(payment['id'])
    PaymentdataModel.objects.create(
        Email=email,
        Amount=payment['amount'],
        Amount_paid=payment['amount_paid'],
        Amount_due=payment['amount_due'],
        Currency=payment['currency'],
        Receipt =payment['receipt'],
        Status=payment['status'],
        Attempts=payment['attempts'],
        Notes=payment['notes'],
        Created_at=payment['created_at'], 
        Order_id=payment['id']
    )
    addcart_data = request.session.get('addtocart', [])
    # print(addcartround(_data)
    total_MRP = 0
    total_amount = 0
    tax = 0
    shippingcharge = 40
    Quantity=0
    pro_data = []

    for item in addcart_data:
        # print(item)
        pro_value = Productmodel.objects.get(id=item['id'])
        # print(pro_value)
        pro_quantitydata = {
            'pro_value': pro_value,
            'Quantity': item['Quantity']
        }
        pro_data.append(pro_quantitydata)
        # print(pro_quantitydata)
        total_amount += pro_value.Prod_Price * item['Quantity']
        total_MRP += pro_value.Prod_MRP * item['Quantity']
        tax += int(round((total_amount * 12) / 100,2))
        Quantity += item['Quantity']

    discount = total_MRP - total_amount
    Total_pay_amount = total_amount + shippingcharge + tax
    
    billamount = {
        'total_amount': total_amount,
        'total_MRP': total_MRP,
        'discount': discount,
        'tax': tax,
        'shippingcharge': shippingcharge,
        'Total_pay_amount': Total_pay_amount,
        'Quantity':Quantity
    }
    cart_length = len(addcart_data)
    Context={
        'user_name': user_info,
        'addcartno': cart_no, 
        'pay_data':data, 
        'media_url': settings.MEDIA_URL,
        'payment':payment,
        'amount': billamount,
        'prod_data': pro_data,
        'length':cart_length,
        'makepay':True
    }
    # print(payment)
    return render(request, 'addtocart.html', Context)
#  -------------------- MakePayment -----------------------------------
@csrf_exempt
def making_payment(request):
    User_id=request.session.get('User_id')
    user_info=get_object_or_404(RegistrationModel, id=User_id)
    addcart = request.session.get('addtocart')
    cart_no=len(addcart)
    # --------------------------------------------
    # print(request.POST)
    razorpay_payment_id = request.POST.get('razorpay_payment_id')
    print('razorpay_payment_id-------->',razorpay_payment_id)
    razorpay_order_id = request.POST.get('razorpay_order_id')
    email = request.POST.get('email')
    print(razorpay_order_id)
    razorpay_signature = request.POST.get('razorpay_signature')
    print('razorpay_signature-------->',razorpay_signature)
    # payment_data= get_object_or_404(PaymentdataModel, Order_id=razorpay_order_id)
    payment_data=PaymentdataModel.objects.get(Order_id=razorpay_order_id)
    print(payment_data)

    payment_data.Payment_Id = razorpay_payment_id
    payment_data.Signature = razorpay_signature
    payment_data.save(update_fields=['Payment_Id','Signature'])

    payment_data=PaymentdataModel.objects.get(Order_id=razorpay_order_id)
    if addtocart in request.session['addtocart']:
        del request.session['addtocart']
    print(user_info)
    Context={
        'user_name': user_info,
        'addcartno': cart_no,
        'media_url': settings.MEDIA_URL,
        'payment_data':payment_data,
    }
    return render(request, 'paymentdone.html', Context)

# ------------------------- Product Payment function ----------------------------

def buyproduct(request):
    User_id=request.session.get('User_id')
    user_info=get_object_or_404(RegistrationModel, id=User_id)
    addcart = request.session.get('addtocart')
    cart_no=len(addcart)
    # ------------------------------------------
    amount=int(request.POST.get('amount'))*100
    print(amount)
    email=request.POST.get('email')
    pid=request.POST.get('pid')
    # print(email)
    userdata=RegistrationModel.objects.get(Email=email)
    global Payableamount 
    # amount in paisa
    client = razorpay.Client(auth =("rzp_test_8jTLUV3aVex82Q" , "n3PL7ZbSgnKSWJeA1s9ndhaO"))
    # amount = int(amount * 100)
    data = { "amount": amount, "currency": "INR", "receipt": "order_rcptid_11" }
    # print(data)
    payment = client.order.create(data=data)
    print("Payment ----->",payment)
    Payableamount=payment


    print(payment['id'])
    PaymentdataModel.objects.create(
        Email=email,
        Amount=payment['amount'],
        Amount_paid=payment['amount_paid'],
        Amount_due=payment['amount_due'],
        Currency=payment['currency'],
        Receipt =payment['receipt'],
        Status=payment['status'],
        Attempts=payment['attempts'],
        Notes=payment['notes'],
        Created_at=payment['created_at'], 
        Order_id=payment['id']
    )
    addcart_data = request.session.get('addtocart', [])
    # print(addcartround(_data)
    total_MRP = 0
    total_amount = 0
    tax = 0
    shippingcharge = 40
    Quantity=0
    pro_data = []

    for item in addcart_data:
        # print(item)
        pro_value = Productmodel.objects.get(id=item['id'])
        # print(pro_value)
        pro_quantitydata = {
            'pro_value': pro_value,
            'Quantity': item['Quantity']
        }
        pro_data.append(pro_quantitydata)
        # print(pro_quantitydata)
        total_amount += pro_value.Prod_Price * item['Quantity']
        total_MRP += pro_value.Prod_MRP * item['Quantity']
        tax += int(round((total_amount * 12) / 100,2))
        Quantity += item['Quantity']

    discount = total_MRP - total_amount
    Total_pay_amount = total_amount + shippingcharge + tax
    
    billamount = {
        'total_amount': total_amount,
        'total_MRP': total_MRP,
        'discount': discount,
        'tax': tax,
        'shippingcharge': shippingcharge,
        'Total_pay_amount': Total_pay_amount,
        'Quantity':Quantity
    }
    cart_length = len(addcart_data)
    Context={
        'user_name': user_info,
        'addcartno': cart_no, 
        'pay_data':data, 
        'media_url': settings.MEDIA_URL,
        'payment':payment,
        'amount': billamount,
        'prod_data': pro_data,
        'length':cart_length,
        'buyproduct':pid,
    }
    # print(payment)
    return render(request, 'addtocart.html', Context)
#  -------------------- MakePayment -----------------------------------
@csrf_exempt
def buyproduct_payment(request):
    User_id=request.session.get('User_id')
    user_info=get_object_or_404(RegistrationModel, id=User_id)
    addcart = request.session.get('addtocart')
    cart_no=len(addcart)
    # --------------------------------------------
    pid = request.POST.get('pid')
    print('product id ------->', pid)
    # print(request.POST)
    razorpay_payment_id = request.POST.get('razorpay_payment_id')
    print('razorpay_payment_id------>',razorpay_payment_id)
    razorpay_order_id = request.POST.get('razorpay_order_id')
    print('razorpay_payment_id------>',razorpay_payment_id)
    # print(razorpay_order_id)
    razorpay_signature = request.POST.get('razorpay_signature')
    print('razorpay_payment_id------>',razorpay_payment_id)

    # payment_data= get_object_or_404(PaymentdataModel, Order_id=razorpay_order_id)
    payment_data=PaymentdataModel.objects.get(Order_id=razorpay_order_id)
    # print(payment_data)

    payment_data.Payment_Id = razorpay_payment_id
    payment_data.Signature = razorpay_signature
    # Save the updated payment data
    payment_data.save(update_fields=['Payment_Id', 'Signature'])
    for i in range(len(addtocart)):
        if pid==addtocart[i]['id']:
            del addtocart[i]

    request.session['addtocart'] = addcart

    addcart_data = request.session.get('addtocart', [])
    # print(addcartround(_data)
    total_MRP = 0
    total_amount = 0
    tax = 0
    shippingcharge = 40
    Quantity=0
    pro_data = []

    for item in addcart_data:
        # print(item)
        pro_value = Productmodel.objects.get(id=item['id'])
        # print(pro_value)
        pro_quantitydata = {
            'pro_value': pro_value,
            'Quantity': item['Quantity']
        }
        pro_data.append(pro_quantitydata)
        # print(pro_quantitydata)
        total_amount += pro_value.Prod_Price * item['Quantity']
        total_MRP += pro_value.Prod_MRP * item['Quantity']
        tax += int(round((total_amount * 12) / 100,2))
        Quantity += item['Quantity']

    discount = total_MRP - total_amount
    Total_pay_amount = total_amount + shippingcharge + tax
    
    billamount = {
        'total_amount': total_amount,
        'total_MRP': total_MRP,
        'discount': discount,
        'tax': tax,
        'shippingcharge': shippingcharge,
        'Total_pay_amount': Total_pay_amount,
        'Quantity':Quantity
    }
    cart_length = len(addcart_data)
    Context={
        'user_name': user_info,
        'addcartno': cart_no, 
        'media_url': settings.MEDIA_URL,
        'amount': billamount,
        'prod_data': pro_data,
        'length':cart_length
    }
    return render(request, 'paymentdone.html', Context)

# ====================== Ending User Dashboard (Razorpay payment integrations) ======================================

















# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  Admin Dashboard Views Function @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    #===================Starting Admin dashboard (Navigation)============================

def dashbordindex(request):
    Admin_id=request.session.get('Admin_id')
    admin_info=get_object_or_404(RegistrationModel, id=Admin_id)
    customer_data=RegistrationModel.objects.all()
    print(customer_data)
    Context={
        'media_url': settings.MEDIA_URL,
        'admin_user':admin_info,
        'customer':customer_data
    }
    return render(request, 'dashboardindex.html', Context) 
# ------------------------ register data CRUD -----------------------
def editregistdata(request, pk):
    data=RegistrationModel.objects.get(id=pk)
    
    Admin_id=request.session.get('Admin_id')
    admin_info=get_object_or_404(RegistrationModel, id=Admin_id)
    customer_data=RegistrationModel.objects.all()
    print(customer_data)
    Context={
        'media_url': settings.MEDIA_URL,
        'admin_user':admin_info,
        'customer':customer_data,
        'registform':Registrationform,
        'editdata':data
    }
    return render(request, 'dashboardindex.html', Context)

def deletregistdata(request, pk):
    data=RegistrationModel.objects.get(id=pk)
    data.delete()
    Admin_id=request.session.get('Admin_id')
    admin_info=get_object_or_404(RegistrationModel, id=Admin_id)
    customer_data=RegistrationModel.objects.all()
    print(customer_data)
    Context={
        'media_url': settings.MEDIA_URL,
        'admin_user':admin_info,
        'customer':customer_data
    }
    return render(request, 'dashboardindex.html', Context)



def updateeditregistdata(request):
    print(request.FILES)
    print(request.POST)


    data=RegistrationModel.objects.get(Email=request.POST['email'])
    data.Profile=request.FILES.get('profile')
    data.Name=request.POST['name']
    data.Username=request.POST['username']
    data.Email=request.POST['email']
    data.Address=request.POST['address']
    data.Number=request.POST['number']
    data.Password=request.POST['password']
    data.Birthday=request.POST['birthday']
    data.About=request.POST['about']
    data.save()
    Admin_id=request.session.get('Admin_id')
    admin_info=get_object_or_404(RegistrationModel, id=Admin_id)
    customer_data=RegistrationModel.objects.all()
    print(customer_data)
    Context={
        'media_url': settings.MEDIA_URL,
        'admin_user':admin_info,
        'customer':customer_data,
        'key':'Data Suceesfully Updated'
    }
    return render(request, 'dashboardindex.html', Context)


# =============== completed Registrationt data CRUD =====================
# =============== Starting Product data CRUD ===========================

def productdata(request):
    Admin_id=request.session.get('Admin_id')
    admin_info=get_object_or_404(RegistrationModel, id=Admin_id)
    data=Productmodel.objects.all()
    Context={
        'admin_user':admin_info,    
        'prod_form':Productmodelform,
        'media_url': settings.MEDIA_URL,
        'prop':data
    }
    
    return render(request, 'productdata.html',Context )
# -------------- product dtat CRUD -------------------------
def editproductdata(request, pk):
    data=Productmodel.objects.get(id=pk)
    
    Admin_id=request.session.get('Admin_id')
    admin_info=get_object_or_404(RegistrationModel, id=Admin_id)
    product_data=Productmodel.objects.all()
    print(product_data)
    Context={
        'media_url': settings.MEDIA_URL,
        'admin_user':admin_info,
        'prop':product_data,
        'Productdataform':Productmodelform,
        'editdata':data
    }
    return render(request, 'productdata.html', Context)

def deletproductdata(request, pk):
    print(pk)
    data=Productmodel.objects.get(id=pk)
    data.delete()
    Admin_id=request.session.get('Admin_id')
    admin_info=get_object_or_404(RegistrationModel, id=Admin_id)
    product_data=Productmodel.objects.all()
    print(product_data)
    Context={
        'media_url': settings.MEDIA_URL,
        'admin_user':admin_info,
        'prop':product_data,
        'key':'Data Successfully Deleted'
    }
    return render(request, 'productdata.html', Context)



def updateditproductdata(request):
    print(request.FILES)
    print(request.POST)
    data=Productmodel.objects.get(id=request.POST['id'])
    data.Profile=request.FILES.get('profile')
    data.Name=request.POST['name']
    data.Username=request.POST['username']
    data.Email=request.POST['email']
    data.Address=request.POST['address']
    data.Number=request.POST['number']
    data.Password=request.POST['password']
    data.Birthday=request.POST['birthday']
    data.About=request.POST['about']
    data.save()
    Admin_id=request.session.get('Admin_id')
    admin_info=get_object_or_404(RegistrationModel, id=Admin_id)
    product_data=Productmodel.objects.all()
    # print(product_data)
    Context={
        'media_url': settings.MEDIA_URL,
        'admin_user':admin_info,
        'customer':product_data,
        'key':'Data Suceesfully Updated'
    }
    return render(request, 'productdata.html', Context)

def addproductdata(request):
    Admin_id=request.session.get('Admin_id')
    admin_info=get_object_or_404(RegistrationModel, id=Admin_id)
    product_data=Productmodel.objects.all()
    # print(product_data)
    Context={
        'media_url': settings.MEDIA_URL,
        'admin_user':admin_info,
        'customer':product_data,
        'Productdataform':Productmodelform,
        'Addnewproduct':'add new Product',
        
    }
    return render(request, 'productdata.html', Context)

# =============== Ending Product data CRUD ===========================


def userdata(request):
    Admin_id=request.session.get('Admin_id')
    admin_info=get_object_or_404(RegistrationModel, id=Admin_id)
    Context={
        'media_url': settings.MEDIA_URL,
        'admin_user':admin_info
    }
    return render(request, 'userdata.html', Context)

def result(request):
    Admin_id=request.session.get('Admin_id')
    admin_info=get_object_or_404(RegistrationModel, id=Admin_id)
    Context={
        'media_url': settings.MEDIA_URL,
        'admin_user':admin_info
    }
    return render(request, 'result.html', {'admin_user':admin_info})

def product_entry(request):
    Admin_id=request.session.get('Admin_id')
    admin_info=get_object_or_404(RegistrationModel, id=Admin_id)
    if request.method == "POST":
        # print(request.POST)
        # print(request.FILES)
        serialno=request.POST.get('Serial_no')
        serialmodel=Productmodel.objects.filter(Serial_no=serialno)
        if serialmodel:
            msg = "This data already exist "
            Context={
                    'media_url': settings.MEDIA_URL,
                    'admin_user':admin_info,
                    'msg': msg,
                }
            return render(request, 'productform.html', Context)
        else:
            form = Productmodelform(request.POST, request.FILES)
        # print(form)
            if form.is_valid():
                form.save()
                msg = "Data submitted successfully"
                return redirect('productdata')
            else:
                msg = "There is some error, please try again"
                Context={
                    'media_url': settings.MEDIA_URL,
                    'admin_user':admin_info,
                    'msg': msg,
                }
                return render(request, 'productform.html', Context)
    else:
        form = Productmodelform()
        Context={
        'media_url': settings.MEDIA_URL,
        'admin_user':admin_info
        }
        return render(request, 'productform.html', Context)
    
    
#======================= ENDing Admin dashboard (Navigation) =================================
    
# ====================== Starting admin Dashboard (Todo task CRUD) ============================  
def  todoform(request):
    Admin_id=request.session.get('Admin_id')
    admin_info=get_object_or_404(RegistrationModel, id=Admin_id)
    msg="open task form"
    return render(request, 'dashboard.html',{'admin_user':admin_info, 'show':msg} )

def todotask(request):
    # print(request.POST)
    title = request.POST.get('title')
    task = request.POST.get('task')
    email = request.POST.get('email')

    Admin_id=request.session.get('Admin_id')
    admin_info=get_object_or_404(RegistrationModel, id=Admin_id)
    
    taskcheck=Todolist.objects.filter(Title=title)
    if taskcheck:
        msg="This Tutle task Already Saved"  
        return render(request, 'dashboard.html', {'key1': msg, 'admin_user':admin_info})   
    else:
        Todolist.objects.create(
            Title=title,
            Task=task,
            Email=email
        )
        msg="Your Task is Saved"
        return render(request, 'dashboard.html', {'key1': msg, 'admin_user':admin_info})


# def search(request):
#     date=request.POST.get('date')
#     print(date)
#     email=request.POST.get('email')
#     print(email)
#     data=RegistrationModel.objects.get(Email=email)
#     taskdata=Todolist.objects.filter(Date=date) and Todolist.objects.filter(Email=email) 
#     # if taskdata:
#     #     return render(request, 'dashboard.html', {'user_name':data, 'tododata':taskdata})
#     # else:
#     #     msg="data not found"
#     #     return render(request, 'dashboard.html', { 'key1':msg, 'user_name':data})
#     return render(request, 'dashboard.html')


def showdata1(request, pk):
    
    Admin_id=request.session.get('Admin_id')
    admin_info=get_object_or_404(RegistrationModel, id=Admin_id)
    taskdata=Todolist.objects.filter(Email=admin_info.Email)
    return render(request, 'dashboard.html', {'admin_user':admin_info, 'tododate':taskdata})

def showdata2(request):
    email=request.POST.get('email')
    # print(email)
    data=RegistrationModel.objects.get(Email=email)
    # print(data)
    taskdata=Todolist.objects.filter(Email=email)
    # print(taskdata)
    # print(taskdata.values())
    return render(request, 'dashboard.html', {'admin_user':data, 'tododate':taskdata})


def edittodo(request, pk):
    # print(pk)
    data1=Todolist.objects.get(id=pk)
    email=data1.Email
    taskdata=Todolist.objects.filter(Email=email)
    data=RegistrationModel.objects.get(Email=email)
    return render(request, 'dashboard.html', {'admin_user':data, 'tododate':taskdata, 'taskobject':data1})

def delettodo(request, pk):
    # print(pk)
    data=Todolist.objects.get(id=pk)
    email=data.Email
    data.delete()
    taskdata=Todolist.objects.filter(Email=email)
    data=RegistrationModel.objects.get(Email=email)
    msg="Data deleted successfully"
    return render(request, 'dashboard.html', {'admin_user':data, 'tododate':taskdata, 'key1':msg})

def updatedata(request):
    Todotask=Todolist.objects.get(id=request.POST.get('id'))
    email=Todotask.Email
    Todotask.id=request.POST.get('id')
    Todotask.Title=request.POST.get('title')
    Todotask.Task=request.POST.get('task')
    Todotask.Date = datetime.now()
    Todotask.Email=request.POST.get('email')
    Todotask.save()
    taskdata=Todolist.objects.filter(Email=email)
    data=RegistrationModel.objects.get(Email=email)
    msg="Data update Successfully"
    return render(request, 'dashboard.html', {'admin_user':data, 'tododate':taskdata, 'key1':msg })

# ========================= ENDing admin Dashboard (Todo task CRUD) =======================================

# ========================= Starting Admin Dashboard (Product CRUD) ========================================

def product_show1(request):
    Admin_id=request.session.get('Admin_id')
    admin_info=get_object_or_404(RegistrationModel, id=Admin_id)
    pro_data1=Productmodel.objects.all()
    print(pro_data1.values())
    Context={
        'admin_user':admin_info, 
        'prop':pro_data1, 
        'media_url': settings.MEDIA_URL
    }
    return render(request, 'productdata.html', Context)

# ================ ENDing Admin Dashboard (Product CRUD) ======================
# ===============@@@@@$     Admin Panel        $@@@@===========================




#=================== User Dashboard login after Navition =============
# def home(request):
#     return render(request, 'index.html', {'user_name':user_info})

# def about1(request):
#     print(request.POST)
#     email=request.POST.get('email')
#     data=RegistrationModel.objects.get(Email=email)
#     return render(request, 'about.html', {'user_name':user_info})

# def contact1(request):
#     print(request.POST)
#     email=request.POST.get('email')
#     data=RegistrationModel.objects.get(Email=email)
#     return render(request, 'contact.html', {'user_name':user_info})

# def product1(request):
#     print(request.POST)
#     email=request.POST.get('email')
#     data=RegistrationModel.objects.get(Email=email)
#     return render(request, 'product.html', {'user_name':user_info})

# def men1(request):
#     print(request.POST)
#     email=request.POST.get('email')
#     data=RegistrationModel.objects.get(Email=email)
#     data1=Productmodel.objects.filter(Prod_Name="Men")
#     print(data)
#     Context={
#         'user_name':user_info, 
#         'prop':data1,
#         'media_url': settings.MEDIA_URL
#     }
#     return render(request, 'men.html',Context )

# def women1(request):
#     print(request.POST)
#     email=request.POST.get('email')
#     data=RegistrationModel.objects.get(Email=email)
#     return render(request, 'women.html', {'user_name':user_info})

# def girl1(request):
#     print(request.POST)
#     email=request.POST.get('email')
#     data=RegistrationModel.objects.get(Email=email)
#     return render(request, 'girl.html', {'user_name':user_info})