# PRD
There are 7 packages : 

1. **createBase** : there are some elements (.py) for create the Learning database. In fact we use package <Generation_de_la_base_d'apprentissage> for generating the Learning   database.
2. **database**: 
   1. the Database*.txt file are parts of the base.txt
   2. base.txt which has the whole data generated from the program: Generation_de_la_base_d'apprentissage(we merge all Database*.txt file)
   3. databaseC.csv has the data form for the seq2seq model with the Completion Time, we use this file for training.
3. **documents**: 
   1. all the test documents 
   2. Euqation.pdf: description of the model and the euqation.
   3. Soutenance Finale.pdf : the slides of the final presentation

4. **flowshop**: package for integration of the matheuristics
5. **Generation_de_la_base_d'apprentissage**: it has all the source code (C) of the gereration of Learning database. For using, it needs to lanch the Generation_de_la_base_d'apprentissage/CampagneGenBdDApprentissage/testexact1.exe.
6. **nn**: it has the code of construction of seq2seq model
   1. preprocess.py : the functions of preprocessing data
   2. Seq2seqnn.py : the model of the seq2seq model.

7. Pydoc : python doc genrated by sphinx.