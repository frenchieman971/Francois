# RECAP — DJ FRANCOIS DE ST FRANCOIS (état au 08/10/2026)

## État
- Page en ligne : https://frenchieman971.github.io/Francois/
- Dépôt GitHub public : `frenchieman971/Francois`, branche `main`, GitHub Pages (source : main / root).
- Dernier commit poussé : `b69590d` (nom, téléphone, logo, 2 nouveaux catalogues, QR au nouveau nom).
- Dossier local = dépôt git. Suivis : `index.html`, `logo-dj.png`, 9 PDF `catalogue_*.pdf`, `QR/`, `.gitignore`.
- Non suivi : ce `RECAP.md`, et les 2 scripts copiés dans `QR/` (voir ci-dessous).

## Page
- Titre et en-tête : DJ FRANCOIS DE ST FRANCOIS.
- Bandeau hero : téléphone 0690 51 57 81, en lien cliquable `tel:+590690515781`. Demandé explicitement par le DJ pour cette page.
- Logo : `logo-dj.png`, version nettoyée (numéro retiré, fond transparent). L'original avec le numéro reste hors dépôt.
- 9 catalogues :
  - Catalogue complet : `catalogue_fr_all.pdf`
  - Français, Anglais, Espagnol, Allemand, Italien, Néerlandais : `catalogue_fr_<langue>.pdf`
  - Zouk : `catalogue_zouk_entier.pdf`
  - Top 50 & populaire : `catalogue_top50_populaire.pdf`
- Mise en page en grille : 2 colonnes sur smartphone (largeur ≤ 600 px), plusieurs colonnes sur ordinateur.

## QR
- URL encodée : https://frenchieman971.github.io/Francois/
- Carte A5 imprimable : `QR/carte-qr-francois-dj-disco-A5.pdf` et `.png`.
- QR carré : `QR/qr-francois-dj-disco.png`.
- Anciens QR simples, sans thème : `qr-francois-dj.png` et `.svg` à la racine.
- Scripts : `QR/build_disco_qr.py` (génère les cartes, nom en dur dans le script) et `QR/build_logo.py` (nettoie le logo). Relancer `build_disco_qr.py` après tout changement de nom.

## Pièges
- Sur ce Mac (clavier AZERTY), `cmd+a` envoyé par computer-use ferme GitHub Desktop (c'est `cmd+q`). Pour sélectionner un champ : clic, puis `shift+home`, puis coller.
- Après un commit en CLI, GitHub Desktop peut afficher des changements fantômes. Cliquer « Fetch origin » pour rafraîchir. Ne jamais cliquer « Commit » sur des fichiers déjà commités.
- Pas d'identifiants git en CLI : le push passe par GitHub Desktop (bouton « Push origin »).
- GitHub Pages met 1 à 3 minutes à se mettre à jour après un push.
- GitHub Pages gratuit exige un dépôt public : les PDF Karafun sont donc publics.

## Points à valider
- Droits : les catalogues sont des PDF Karafun, publiés en public.
- Historique git : les anciens commits (ex. `822611f`) contiennent encore le nom KARAFUN et les anciens noms de fichiers. Les réécrire demande un force-push, non fait.
- Anciens liens `karafuncatalog_*.pdf` : 404.
- QR non testé au téléphone (aucun lecteur sur le Mac).

## À faire
- Scanner la carte A5 avec un téléphone avant impression.
- Imprimer la carte A5.
- Commiter ce RECAP et les scripts si tu veux qu'ils soient versionnés (dépôt public).
