from django.shortcuts import render, redirect
# get_user_model récupère le modèle utilisateur CustomUser défini dans models.py
from django.contrib.auth import get_user_model, login, logout, authenticate  

#récupère le modèle et donc AUTH_USER_MODEL dans settings.py
user = get_user_model()    

def signup(request):
    if request.method == 'POST':
        #si la requete est de type post on récupère les informations du formulaire
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password != password2:
            #si les mots de passe ne correspondent pas on renvoie une erreur
            return render(request, 'accounts/signup.html', {'error': 'Les mots de passe ne correspondent pas'})
        else:
            #si les mots de passe correspondent on vérifie si l'utilisateur existe déjà
            try:
                user.objects.get(username=username)
                #si l'utilisateur existe déjà on renvoie une erreur
                return render(request, 'accounts/signup.html', {'error': 'Cet utilisateur existe déjà'})
            #si l'utilisateur n'existe pas
            except user.DoesNotExist:
                #création du nouvel utilisateur
                new_user = user.objects.create_user(username=username, password=password)
                #connexion de l'utilisateur au site
                login(request, new_user)
                #redirection vers page d'accueil
                return redirect('index')
    #si la requete est de type get on revient au formulaire d'inscription
    return render(request, 'accounts/signup.html')

def logout_user(request):
    #déconnexion de l'utilisateur
    logout(request)
    #redirection vers page d'accueil
    return redirect('index')

def login_user(request):
    if request.method == 'POST':
        #récupération des informations du formulaire
        username = request.POST.get('username')
        password = request.POST.get('password')
        #vérification de l'existence de l'utilisateur
        user = authenticate(username=username, password=password)
        #si l'utilisateur existe
        if user:
            login(request, user)
            #redirection vers page d'accueil
            return redirect('index')
        else:
            #si l'utilisateur n'existe pas on renvoie une erreur
            return render(request, 'accounts/login.html', {'error': 'Utilisateur ou mot de passe incorrect'})
    #si la requete est de type get on revient au formulaire de connexion
    return render(request, 'accounts/login.html')