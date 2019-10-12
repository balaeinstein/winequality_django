from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics
# Create your views here.
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name'] 
        last_name = request.POST['last_name'] 
        username = request.POST['username'] 
        password1 = request.POST['password1'] 
        password2 = request.POST['password2'] 
        email = request.POST['email'] 

        if password1==password2 :
            if User.objects.filter(username=username).exists():
                messages.info(request,'username taken')
                return redirect('register')
            elif  User.objects.filter(email=username).exists(): 
                messages.info(request,'Email already exists') 
                return redirect('register')
            else :     
                user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)      
                user.save()
                return redirect('login')
        else:
            messages.info(request,'Password Mismatch') 
            return redirect('register')
        return redirect('/')           
    else:   
        return render(request,'register.html')

def login(request):
   if request.method == 'POST':
       username = request.POST['username'] 
       password = request.POST['password'] 

       user = auth.authenticate(username=username,password=password)

       if user is not None:
           auth.login(request ,user)
           return render(request,'winedata.html')
       else:
           messages.info(request,'invalid credentials')   
           return redirect('login')

   else:
       return render(request,'login.html')

def compute(request):
    if request.method == 'POST':
        alcohol = float(request.POST['alcohol']) 
        Malic_Acid = float(request.POST['Malic_Acid']) 
        ash = float(request.POST['ash']) 
        Alcalinity_of_ash = float(request.POST['Alcalinity_of_ash'])
        Magnesium = float(request.POST['Magnesium'])
        Total_phenols = float(request.POST['Total_phenols']) 
        Flavanoids = float(request.POST['Flavanoids']) 
        Nonflavanoid_phenols = float(request.POST['Nonflavanoid_phenols'])
        Proanthocyanins = float(request.POST['Proanthocyanins'])
        Color_intensity = float(request.POST['Color_intensity']) 
        Hue = float(request.POST['Hue']) 
        diluted_wines = float(request.POST['diluted_wines'])
        Proline = float(request.POST['Proline'])

        wine = datasets.load_wine()
        X = wine["data"]
        y = wine["target"]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,random_state=109)
        gnb = GaussianNB()
        gnb.fit(X_train, y_train)
        predicted= gnb.predict([[alcohol,Malic_Acid,ash,Alcalinity_of_ash,Magnesium,Total_phenols,Flavanoids,Nonflavanoid_phenols,Proanthocyanins,Color_intensity,Hue,diluted_wines,Proline]])
        y_pred = gnb.predict(X_test)
        print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
        return render(request,'result.html',{'predicted_class':predicted})
    else:
       return render(request,'winedata.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

