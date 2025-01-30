Application de prédiction de prime d'assurance utilisant un modèle de Machine Learning.

Installations nécessaires :

    Se placer dans le répertoire MyApp et créer l'environnement de développement :

        python -m venv .venv

    L'activer : 

        source .venv/bin/activate 

        
    Installer les dépendances du projet :
     
        pip install -r requirements.txt

        il peut être nécessaire d'intaller npm ou nodejs s'ils n sont pas reconnus (pour l'utilisation de tailwindcss)

    Créer la base de données : 

        python manage.py makemigrations
        python manage.py migrate

    Créer un super user : 

        python manage.py createsuperuser

        (nécessitera username, email, password)


Lancer le projet :

    dans un premier terminal (dossier MyApp) démarrer le serveur tailwind avec :
      
        python manage.py tailwind start

    dans un second terminal (dossier MyApp aussi) démarrer le serveur django avec :

        python manage.py runserver
