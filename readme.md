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

## 8) Flag "edit_request_survey"
### Etapes pour trouver le flag
1. Accès à la page "?page=survey" qui présente un classement avec des votes de 1 à 10
2. Observation des paramètres de requête : sujet=2&valeur=X où X représente la valeur du vote
3. Modification de la valeur dans la requête pour dépasser la limite de 10 (par exemple : sujet=2&valeur=54)
4. Le serveur accepte la modification sans valider la plage de valeurs autorisée

### Description
Cette vulnérabilité résulte d'un manque de validation côté serveur des données envoyées par l'utilisateur. Le serveur fait confiance aux données reçues sans vérifier si elles respectent les règles métier définies (ici, la plage de valeurs 1-10 pour les votes).

### OWASP associés
1. OWASP A04:2021 - Insecure Design
2. OWASP A03:2021 - Injection
3. OWASP A05:2021 - Security Misconfiguration

### Comment s'en protéger
1. Implémenter une validation stricte des données côté serveur
2. Définir des limites claires pour les valeurs acceptables
3. Ne jamais faire confiance aux données envoyées par le client
4. Mettre en place des contrôles de validation dans la base de données (contraintes)
5. Journaliser les tentatives de manipulation des requêtes
6. Utiliser des listes blanches pour les valeurs autorisées


## 9) Flag "edit_request_upload"
### Etapes pour trouver le flag
1. Accès à la page d'upload qui n'accepte que les fichiers JPEG
2. Interception de la requête
3. Modification du Content-Type dans l'en-tête de la requête :
```http
Content-Type: image/jpeg
```
4. Possibilité d'uploader des fichiers malveillants (scripts PHP, shells, etc.) en contournant la restriction JPEG

### Description
Cette vulnérabilité exploite une validation insuffisante du type de fichier côté serveur. Le serveur se fie uniquement au Content-Type de la requête HTTP sans vérifier le contenu réel du fichier. Un attaquant peut ainsi télécharger des fichiers potentiellement dangereux (shells web, scripts malveillants, etc.) en faisant passer ces fichiers pour des images JPEG.

### OWASP associés
1. OWASP A01:2021 - Broken Access Control
2. OWASP A05:2021 - Security Misconfiguration
3. OWASP A03:2021 - Injection

### Comment s'en protéger
1. Vérifier le contenu réel du fichier (magic bytes) et pas seulement le Content-Type
2. Implémenter une double validation côté client ET serveur
3. Utiliser des bibliothèques dédiées pour la validation des fichiers
4. Renommer les fichiers uploadés de manière aléatoire
5. Stocker les fichiers en dehors de la racine web
6. Scanner les fichiers uploadés avec un antivirus
7. Limiter la taille maximale des fichiers
8. Restreindre les extensions de fichiers autorisées via une liste blanche


Cette faille peut mener à une compromission complète du serveur si elle est exploitée avec succès.

## 10) Flag "redirect_social_network"
### Etapes pour trouver le flag
1. Observation des liens de réseaux sociaux en bas de page du site
2. Ces liens utilisent une URL de redirection du type :
```
http://10.11.249.0/index.php?page=redirect&site=
```
3. En cliquant sur un réseau social (Facebook, Twitter, etc.), on peut voir que le site redirige sans validation
4. L'URL peut être modifiée pour rediriger vers n'importe quel site :
```
http://10.11.249.0/index.php?page=redirect&site=https://malicious-site.com
```

### Description
Cette vulnérabilité exploite les liens de réseaux sociaux du site qui utilisent un système de redirection non sécurisé. Au lieu de rediriger uniquement vers les réseaux sociaux légitimes, le système accepte n'importe quelle URL de destination, permettant potentiellement des redirections vers des sites malveillants.

### OWASP associés
1. OWASP A01:2021 - Broken Access Control
2. OWASP A04:2021 - Insecure Design

### Comment s'en protéger
1. Hardcoder les URLs des réseaux sociaux plutôt que d'utiliser un système de redirection
2. Si un système de redirection est nécessaire :
   - Utiliser une liste blanche des domaines de réseaux sociaux autorisés
   - Valider strictement l'URL de destination
3. Implémenter des contrôles de sécurité sur les redirections
4. Utiliser des liens directs vers les réseaux sociaux plutôt qu'un système de redirection intermédiaire

Cette faille est particulièrement problématique car les utilisateurs s'attendent à être redirigés vers des réseaux sociaux légitimes, augmentant leur confiance dans le lien et les rendant plus vulnérables aux attaques de phishing.

## 11) Flag "xss_data_url"
### Etapes pour trouver le flag
1. Accès à la page média avec le paramètre src : 
```
http://10.11.249.0/?page=media&src=nsa
```
2. Utilisation du protocole data: pour injecter du code JavaScript encodé en base64 :
https://owasp.org/www-community/attacks/xss/
```
http://10.11.249.0/?page=media&src=data:text/html;base64,PHNjcmlwdD5hbGVydCgndGVzdDMnKTwvc2NyaXB0Pg
```
3. Le code décodé correspond à :
```javascript
<script>alert('test3')</script>
```

### Description
Cette vulnérabilité exploite le protocole data: URL qui permet d'inclure des données directement dans l'URL. L'utilisation de l'encodage base64 est cruciale ici car elle permet de contourner le filtrage des caractères spéciaux. Sans encodage base64, les caractères comme `<`, `>`, `/` présents dans le code JavaScript seraient échappés ou filtrés par le navigateur, rendant l'attaque inefficace. Le base64 transforme notre payload en caractères alphanumériques sûrs qui seront correctement transmis, puis décodés et exécutés par le navigateur.

Par exemple :
1. Sans base64 (ne fonctionne pas) :
```
data:text/html,<script>alert('test')</script>
```

2. Avec base64 (fonctionne) :
```
data:text/html;base64,PHNjcmlwdD5hbGVydCgndGVzdDMnKTwvc2NyaXB0Pg
```

Le serveur ne valide pas correctement la source des médias et ne bloque pas l'utilisation du protocole data:, permettant ainsi l'injection et l'exécution de code JavaScript arbitraire.


### OWASP associés
1. OWASP A03:2021 - Injection
2. OWASP A05:2021 - Security Misconfiguration

### Comment s'en protéger
1. Valider strictement les sources de médias autorisées
2. Bloquer l'utilisation du protocole data:
3. Implémenter une Content Security Policy (CSP) stricte
4. Échapper correctement les données non fiables
5. Filtrer les URLs entrantes pour n'autoriser que les protocoles et sources légitimes
6. Utiliser des listes blanches pour les sources de médias autorisées

Cette vulnérabilité est particulièrement dangereuse car elle permet l'exécution de code JavaScript arbitraire dans le contexte de la page, pouvant mener à du vol de données, des redirections malveillantes, ou d'autres actions non autorisées.

## 12) Flag "referer_user_agent"
### Etapes pour trouver le flag
1. En inspectant le code source, on trouve des commentaires HTML cachés qui indiquent :
```html
<!--
You must come from : "https://www.nsa.gov/".
-->
```
et plus loin :
```html
<!--
	Let's use this browser : "ft_bornToSec". It will help you a lot.
-->
```

2. Pour obtenir le flag, il faut modifier :
- L'en-tête `Referer` pour faire croire qu'on vient de "https://www.nsa.gov/"
- L'en-tête `User-Agent` pour simuler le navigateur "ft_bornToSec"

### Description
Cette vulnérabilité repose sur une validation côté serveur basée uniquement sur les en-têtes HTTP qui sont facilement modifiables. Le serveur utilise les en-têtes `Referer` et `User-Agent` pour contrôler l'accès, ce qui est une mauvaise pratique car ces en-têtes peuvent être falsifiés.

### OWASP associés
1. OWASP A04:2021 - Insecure Design
2. OWASP A07:2021 - Identification and Authentication Failures
3. OWASP A05:2021 - Security Misconfiguration

### Comment s'en protéger
1. Ne jamais faire confiance aux en-têtes HTTP pour l'authentification ou le contrôle d'accès
2. Implémenter une authentification robuste basée sur des tokens ou des sessions
3. Ne pas stocker d'informations sensibles dans les commentaires HTML
4. Utiliser des mécanismes de sécurité côté serveur plutôt que de se fier aux informations envoyées par le client
5. Mettre en place une vérification d'origine plus sûre si nécessaire (ex: CORS bien configuré)
6. Implémenter une authentification forte basée sur des cookies de session sécurisés

Les en-têtes HTTP comme `Referer` et `User-Agent` sont facilement modifiables avec des outils comme curl, Burp Suite ou même des extensions de navigateur, ce qui rend ce type de protection inefficace.

## 13) Flag "robots_whatever_admin"
### Etapes pour trouver le flag
1. Découverte du fichier `robots.txt` à la racine du site :
```
http://10.11.249.0/robots.txt
```

2. Le fichier `robots.txt` révèle le dossier `/whatever`

3. Dans ce dossier, découverte du fichier `.htpasswd` :
```
http://10.11.249.4/whatever/htpasswd
```
qui contient des identifiants :
```
root:437394baff5aa33daa618be47b75cb49
```

4. Décryptage du hash MD5 via un service en ligne (md5decrypt.net) :
- Hash MD5 : 437394baff5aa33daa618be47b75cb49
- Texte en clair : qwerty123@

5. Utilisation des identifiants sur la page admin :
```
http://10.11.249.4/admin/
login: root
password: qwerty123@
```

### Description
Cette vulnérabilité combine plusieurs problèmes de sécurité :
- Exposition du fichier robots.txt révélant des chemins sensibles
- Accès public au fichier .htpasswd contenant des hashes de mots de passe
- Utilisation de MD5, un algorithme de hashage faible et facilement décryptable
- Mot de passe relativement simple malgré l'utilisation de caractères spéciaux

### OWASP associés
1. OWASP A01:2021 - Broken Access Control
2. OWASP A07:2021 - Identification and Authentication Failures
3. OWASP A05:2021 - Security Misconfiguration

### Comment s'en protéger
1. Ne pas exposer de fichiers sensibles comme .htpasswd
2. Utiliser des algorithmes de hashage forts (bcrypt, Argon2) au lieu de MD5
3. Stocker les fichiers d'authentification hors de la racine web
4. Configurer correctement les permissions des fichiers
5. Utiliser des mots de passe forts et complexes
6. Ne pas révéler de chemins sensibles dans robots.txt
7. Mettre en place une authentification à deux facteurs pour l'accès admin
8. Restreindre l'accès à l'interface d'administration par IP ou VPN

## 14) Flag "feedback"
### Etapes pour trouver le flag
http://10.11.249.0/?page=feedback
```
l e s i c t r p a
```
???