# Guide Developement

##  Telechargement du projet

Nous pouvons télécharger le projet en github ： https://github.com/AlafateABULIMITI/PRD

Nous utilisons la commande  $git\  clone​$  pour télécharger le projet dans un dossier local.

## Libraires 

1. Ici, nous utilisons beaucoup de libraires, voici une liste:

   $numpy$ 

   $$pandas​$$

   $$matplotlib​$$

   $$keras​$$

   $$tensorflow​$$

   $$recurentshop$$

   $$seq2seq$$

2. Pour installer les libraires suivantes, nous utilisons l’outil pip. Voici les commandes d'installation pour chaque libraire.

   $$ numpy : pip\  install\  numpy$$

   $$pandas: pip \ install \ pandas$$

   $$matplotlib: pip \ install \ matplotlib$$

   $$keras: pip \ install \ keras$$

   

   $$tensorflow: pip \ install \ tensorflow$$

   

   $$recurentshop : $$

   ```
   git clone https://www.github.com/farizrahman4u/recurrentshop.git
   cd recurrentshop
   python setup.py install
   ```

   $$seq2seq: sudo\  pip \ install\  git+https://github.com/farizrahman4u/seq2seq.git$$

   

   **Important :** pour utiliser ce modele dans notre projet, il faut modifier le source code dans le fichier python3.6/site-packages/seq2seq/cell.py.

   ​	line 45 et 105 à 

   ```python
   y = Activation('softmax')(W2(h))
   ```

   **Note**：Bien entendu, le plus simple consiste à exécuter le code dans le Pycharm, ce qui présente les avantages suivants:

   1. Vous pouvez vérifier le processus en cours d'exécution du code
   2. Observer l'effet d'entraînement
   3. Facile à utiliser

   

   

   

   

   

    

