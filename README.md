# sirene_server.exe

## Description
`sirene_server.exe` est un projet Python qui permet de récupérer des données SIREN, de les traiter via des recherches Pappers et LinkedIn, et de les envoyer à une feuille de calcul Google Sheets.

## Structure du projet
sirene_server/ ├── config/ │ ├── .env │ └── service_account.json ├── data/ │ └── final_results.csv ├── scripts/ │ ├── run.sh │ └── setup.sh ├── src/ │ ├── fetch_siren.py │ ├── linkedin_search.py │ ├── main.py │ ├── pappers_search.py │ └── to_gsheet.py ├── tests/ │ └── test_main.py ├── .gitignore └── README.md

## Prérequis
- Python 3.x
- pip
- Google Chrome

## Installation
1. Clonez le dépôt :
    ```sh
    git clone https://github.com/votre-utilisateur/sirene_server.exe.git
    cd sirene_server.exe
    ```

2. Installez les dépendances :
    ```sh
    pip install -r requirements.txt
    ```

3. Configurez les variables d'environnement :
    - Créez un fichier `.env` dans le dossier [config](http://_vscodecontentref_/2) avec le contenu suivant :
        ```properties
        SPREADSHEET_ID=your_google_spreadsheet_id_here
        EMAIL=your_email_here
        PASSWORD=your_password_here
        SIREN_API=your_siren_api_key_here
        ```
    - Placez le document `service_account.json` dans le dossier `config`.

4. Exécutez le script de configuration :
    ```sh
    bash scripts/setup.sh
    ```

## Utilisation
Pour exécuter le script principal :
```sh
python src/main.py
```

## Tests
Pour exécuter les tests unitaires :
```sh
python -m unittest discover -s tests
```

## Contribuer
Les contributions sont les bienvenues ! Veuillez soumettre une pull request ou ouvrir une issue pour discuter des changements que vous souhaitez apporter.

## Licence
Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.
