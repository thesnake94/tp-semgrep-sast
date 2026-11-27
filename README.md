# TP DevSecOps : Semgrep SAST

Depot pedagogique public avec un historique independant des exercices de secrets.

Les workflows Gitleaks, TruffleHog et Semgrep sont separes dans `.github/workflows/`.
Semgrep utilise `p/default` et `p/owasp-top-ten`, un Quality Gate `--error`
et publie un rapport SARIF dans GitHub Code scanning.

Le code volontairement vulnerable apparait dans une PR de demonstration puis est corrige.
Ce programme de TP ne doit pas etre deploye comme service public.

## Reponses aux questions d'analyse

### 1. Theorie des flux

La source est `request.args.get("id")`, dont la valeur non fiable est stockee dans
`user_id`. Le sink est `cursor.execute(query)`. Dans la version initiale,
l'interpolation de `user_id` dans la requete permet de modifier sa syntaxe SQL.
La correction utilise `cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))` :
le parametre est transmis comme donnee, distinctement du texte SQL. Ce mecanisme
n'est pas un nettoyage de chaine, mais une separation entre code et donnees.

### 2. Architecture CI/CD

Des workflows distincts permettent aux scanners de s'executer independamment,
avec leurs propres droits, declencheurs et resultats. Ils facilitent la maintenance,
le diagnostic et la relance d'un outil sans relancer les autres. Un unique fichier
peut aussi contenir des jobs paralleles ; la separation des fichiers n'est donc
pas indispensable au parallelisme, mais clarifie les responsabilites.

### 3. Gouvernance AppSec

`nosemgrep` masque une alerte sans corriger le programme. Une validation par un
Security Champion doit verifier le flux reel, les controles et le perimetre de
l'exception. Une revue reguliere evite qu'une modification du code rende une
ancienne exception dangereuse. Pour auditer les suppressions avec la version
utilisee ici :

```bash
semgrep scan --config p/default --config p/owasp-top-ten --disable-nosem --error
```

Dans ce TP, cet audit retrouve trois alertes de commande tandis que les alertes
SQL disparaissent apres parametrage. L'exception est pedagogique : elle ne
constitue pas une validation AppSec de production. Une regex de forme IPv4 est
completee par `IPv4Address`, puis l'adresse est reconvertie en forme canonique.
Un service reel doit aussi restreindre les destinations et authentifier les
administrateurs ; la route de demonstration n'est pas reservee aux administrateurs.
En production, preferer une liste d'arguments avec `subprocess.run`, sans shell.
