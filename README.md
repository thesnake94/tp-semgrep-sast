# TP DevSecOps : Semgrep SAST

Depot pedagogique public avec un historique independant des exercices de secrets.

Les workflows Gitleaks, TruffleHog et Semgrep sont separes dans `.github/workflows/`.
Semgrep utilise `p/default` et `p/owasp-top-ten`, un Quality Gate `--error`
et publie un rapport SARIF dans GitHub Code scanning.

Le code volontairement vulnerable apparait dans une PR de demonstration puis est corrige.
Ce programme de TP ne doit pas etre deploye comme service public.
