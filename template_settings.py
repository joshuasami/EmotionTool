# input-File
file = "in/finalTest.csv"

# Listen
nonwordsUrl = "lists/nonwords.csv"
negationsUrl = "lists/negation.csv"
modifikatorUrl = "lists/modifikator.csv"

# ET = output-File , EC = input/output-File
outFile = "out/testout.csv"

# Spalten, die in der Auswettung untersucht werden
labels = ['Verständnisfrage', 'Frage 1', 'Nachfrage 1', 'Nachfrage 2', 'Nachfrage 3', 'Nachfrage 4']

# Fragt bei True bei Funden in der ersten Spalte immer nach. Wenn nicht gewünscht --> False
firstIgnore = True

# Optionen: "de" und "en"
language = "en"


#### E.C. ####

# Kodierer
coder = "JSB"

# Spalten, die mit angezeit werden sollen
showLabels = ["vignette", "Bemerkung", "gender"]
