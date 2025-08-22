docs
  The final target of the build/build.xml script, containing the website, published on GitHub Pages

build
  Environment for building the website, see build/build.xml for explanation of all it's subdirs.
  IMPORTANT to know:
    - build/summa/bronbestanden contains the text files and PDF files that are visible on the website;
      the text files are 'state of the art' and that can be edited for new publication 
    - build/geloofsverdediging is where a text file is put after editing

split_languages
flow
source
target
  Environment for preprocessing the raw text files
  

How to publish a new chapter:

1. clean up the txt file in build/summa/bronbestanden
  - set list to show line ends
  - aspell -l nl -c Aquino_Summa_12.txt
2. copy it to build/geloofsverdediging
3. add it to git
4. edit build/summa/about.html to mark the chapter as published
5. in the build folder: 
  a. ant clean
  b. touch xml_latin_tree/xml_latin_tree.xml
  b. ant [builds website in build/summa]
  c. ant deploy [copies website to docs]
  d. ant deploy-pdf [copies pdfs to docs/pdf]
  Note: the xml_latin.xslt stylesheet seems to freeze when using Saxon PE from 2015
  Note: a build error was caused by a txt file containing a BOM (check with file command), which can be removed by running dos2unix command
  Note: build/build.xml was using Saxon9PE (/home/vic/Programs/jar/saxon9pe.jar -> saxon9pe_2020.jar), but suddenly a license expiration error shows up, and it looks like SaxonHE is working as well (/home/vic/Programs/jar/saxon9he.jar)
6. in the root folder:
  a. git status (check if any new files in docs/ need adding)
  a. git commit -am "Added Quaestiones xx to yy"
  b. git push origin master
7. synchronize the cached index at Alledaags:
  https://sync-dot-catecheserooster.appspot.com/init?key=summa

Corrections:
2. '/ den '
3. '/[Zz]oo '
4. '/onzen '
5. '/ezen '
6. '/[Dd]ien '
7. '/[Zz]óó
8. '/welken '
9. '/zoo,'

How to fix PDF that doesn't work in mupdf:
gs -o Aquino_Summa_21a_gs.pdf -sDEVICE=pdfwrite -dPDFSETTINGS=/prepress Aquino_Summa_21a.pdf 

