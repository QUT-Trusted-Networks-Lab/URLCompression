# URLCompression
## About
This project implements the compression algorithm outlined in the paper "Efficient URL and URI Compression". Programs are provided allowing the generation of custom dictionaries as well as compressing URIs. 
## Getting Started
### Dependencies
This project was written using python 3.9.0 and requires python version 3.5 or up to run
The following libraries are required in order to use this program
* Dahuffman
  ```
  pip install dahuffman
  ```
* Pandas
  ```
  pip install pandas
  ```
* SpaCy
  ```
  pip install spacy
  ```
* BrotliCFFI
  ```
  pip install brotlicffi
  ```
* All required libraries can be install using the requirements.txt file
  ```
  pip install -r requirements.txt
  ```
  
  ## Usage
  Generate necessary dictionaries by passing a .txt or .tsv file of URIs to GenerateDicts.py as follows
  ```
  python GenerateDicts.py URLs.tsv
  python GenerateDicts.py URLs.txt
  ```
  Compress a .txt or .tsv file of URLs by passing it to Compress.py as follows
  ```
  python Compress.py URL_List.txt
  python Compress.py URL_List.tsv
  ```
  ### Example Usage
  ```
  $ python GenerateDicts.py 1mil.tsv
  $ python Compress.py 1mil.tsv
  
  Compressed to: 53.06%
  Size before compression: 
  Size before compression: 71523952 bytes
  Size after compression : 37950091 bytes
  Compressed in:  39.6310552  Seconds
  ```
  
  
  ## Contact
  Felix Savins - Felix.Savins@Connect.qut.edu.au
  
  
  
