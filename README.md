# Text Conversion Guide
To convert xml in "xml" directory to txt files in "raw_txt" directory:

```
python xml_to_txt.py
```
I then removed the text before the first chapter for every txt and the index from each txt in the "raw_txt" folder

To convert raw txt files in "raw_txt" directory to processed txt files in "txt directory". This fixes various symbols:

```
python txt_clean.py
```
To convert txts in "txt" directory to sentence separted txts in "sentence" directory:

```
python txt_sentence.py
```