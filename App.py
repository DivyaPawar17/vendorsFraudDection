from django.shortcuts import render,redirect,HttpResponse
from .models import regmod
from .models import orgreg
import pickle
from django.contrib import messages
from django.template import loader



def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method=="POST":
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        pancard=request.POST['pancard']
        email=request.POST['email']
        password=request.POST['password']
        orgreg(first_name=first_name,last_name=last_name,pancard=pancard,email=email,password=password).save()
    return render(request,'orgreg.html')

def login(request):
    if request.method == 'POST':
        try:
            details=orgreg.objects.get(email=request.POST['email'], password=request.POST['password'])
            print("email= ",details)
            request.session['email']= details.email
            return render(request,'log.html')  
        except orgreg.DoesNotExist as e:
            messages.success(request, 'email or password Invalid')    
    return render(request, 'orglog.html')  



# Load the trained model from the pickle file
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

def predictor(request):
    if request.method == 'POST':
        # Get the form data
        product_name = int(request.POST['product_name'])
        product_quantity= int(request.POST['product_quantity'])
        rate = int(request.POST['rate'])
    
      
        # Make a predictionS
        prediction = model.predict([[product_name,product_quantity,rate]])

        # Check if the prediction is 1 or not
        if prediction == 1:
            result = 'Fraud is Not detected'
        else:
            result = 'Fraud is detected'

        # Render the result page with the prediction output
        return render(request, 'result.html', {'result': result})

    # Render the form page if the request method is GET
    return render(request, 'main.html')


def log(request):
    if request.method == 'POST':
        try:
            details=regmod.objects.get(product_name=request.POST['product_name'], product_quantity=request.POST['product_quantity'], rate=request.POST['rate'],product_name1=request.POST['product_name1'], product_quantity1=request.POST['product_quantity1'], rate1=request.POST['rate1'],product_name2=request.POST['product_name2'], product_quantity2=request.POST['product_quantity2'], rate2=request.POST['rate2'],product_name3=request.POST['product_name3'], product_quantity3=request.POST['product_quantity3'], rate3=request.POST['rate3'],product_name4=request.POST['product_name4'], product_quantity4=request.POST['product_quantity4'], rate4=request.POST['rate4'],product_name5=request.POST['product_name5'], product_quantity5=request.POST['product_quantity5'], rate5=request.POST['rate5'])
            # print("email= ",details)
            # request.session['email']= details.email
            print("product_name= ",details)
            request.session['product_name']= details.product_name
            return render(request,'result.html')  
        except regmod.DoesNotExist as e:
            messages.success(request, 'Your entries are filled')   
            # messages.success(request, 'email or password Invalid') 
            return render(request,'result1.html')
    return render(request, 'log.html') 
