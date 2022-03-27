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
2. copy it to build/geloofsverdediging
3. add it to git
4. edit build/summa/about.html to mark the chapter as published
5. in the build folder: 
  a. ant clean
  b. ant
  c. ant deploy
  Note: the xml_latin.xslt stylesheet seems to freeze when using Saxon PE from 2015
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
