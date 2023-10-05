# input-File
input_file_url = "in/et_in_file.csv"

# encoding
encoding = "utf8"

# Listen
emotionwords_url = "lists/words.csv"
negations_url = "lists/negation.csv"
modificator_url = "lists/modifikator.csv"
seperator = ";"

# ET = output-File , EC = input/output-File
outFile = "out/ETout_KEeKS_LS_EFB_09062023_605-647.csv"

# Spalten, die in der Auswertung untersucht werden
labels_to_look_through = ['Verständnisfrage', 'Frage 1', 'Nachfrage 1', 'Nachfrage 2', 'Nachfrage 3', 'Nachfrage 4']
labels_raising_problem = ['Verständnisfrage']


et_labels = {"emotion":"Emotion", 
             "reduction":"Reduction", 
             "intensifier":"Intensifier", 
             "negation":"Negation", 
             "problems": "Problems", 
             "coder": "Coder"}


#labels = ['Nennung 1']
#labels = ['Emotionswort']


# Fragt bei True bei Funden in der ersten Spalte immer nach. Wenn nicht gewünscht --> False
#firstIgnore = True
firstIgnore = True

# Optionen: "de" und "en"
language = "de"



#### E.C. ####

# Kodierer
coder = "JSB"

# Spalten, die mit angezeit werden sollen
#showLabels = ["ID subject", "vignette", "Bemerkung"]
#showLabels = ["ID_bl", "vignette", "Nennung 1", "Nennung 2", "Nennung 3", "Nennung 4", "Nennung 5"]
showLabels = ["CASE", "vignette"]
