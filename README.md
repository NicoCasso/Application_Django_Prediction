Application de prédiction de prime d'assurance utilisant un modèle de Machine Learning.

Installations nécessaires :

1. Se placer dans le répertoire MyApp et créer l'environnement de développement :

        python -m venv .venv

2. L'activer : 

        source .venv/bin/activate 

3. Installer les dépendances du projet :
     
        pip install -r requirements.txt

    il peut être nécessaire d'installer npm ou nodejs s'ils ne sont pas reconnus (pour l'utilisation de tailwindcss)
        
4. Initialiser tailwindcss :
    
        python manage.py tailwind init
        python manage.py tailwind install

5. Collecter les fichiers via whitenoise :
        
        python manage.py collectstatic
    
6. Créer la base de données : 

        python manage.py makemigrations
        python manage.py migrate

7. Créer un super user : 

        python manage.py createsuperuser

    (nécessitera username, email, password)


Lancer le projet :

1. dans un premier terminal (dossier MyApp) démarrer le serveur tailwind avec :

        python manage.py tailwind start

2. dans un second terminal (dossier MyApp aussi) démarrer le serveur django avec :

        python manage.py runserver

3. (Optionnel) Ouvrir un explorateur web à l'adresse : 

        127.0.0.1:8000/admin

    se connecter avec les information du super user et créer un utilisateur "normal"

4. Accéder à l'application via ce nouvel utilisateur

        127.0.0.1:8000/home
