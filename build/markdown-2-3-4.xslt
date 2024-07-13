<?xml version="1.0"?>
<xsl:stylesheet version="2.0" 
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="text" encoding="UTF-8"/>
  <xsl:strip-space elements="*" />
  <xsl:template match="/">
    <xsl:result-document method="text" href="markdown/Aquino_Summa-2-3-4.md">
      <xsl:text>---&#10;</xsl:text>
      <xsl:text>title: | &#10; | SUMMA THEOLOGIÆ&#10; | Prima Secundæ - Secunda Secundæ - Tertia Pars&#10;</xsl:text>
      <xsl:text>author: Thomas van Aquino&#10;</xsl:text>
      <xsl:text>lang: nl&#10;</xsl:text>
      <xsl:text>classoption:&#10;</xsl:text>
      <xsl:text>- twocolumn&#10;</xsl:text>
      <xsl:text>geometry: twoside, paperheight=297mm, paperwidth=210mm, top=19.05mm, bottom=19.05mm, left=22.225mm, right=19.05mm&#10;</xsl:text>
      <xsl:text>toc: false&#10;</xsl:text>
      <xsl:text>header-includes: |&#10;</xsl:text>
      <xsl:text>    \usepackage{fancyhdr}&#10;</xsl:text>
      <xsl:text>    \pagestyle{fancy}&#10;</xsl:text>
      <xsl:text>    \fancyhead[CO,CE]{\leftmark}&#10;</xsl:text>
      <xsl:text>    \fancyfoot[CE,CO]{\thepage}&#10;</xsl:text>
      <xsl:text>    \fancyhead[LO,LE,RO,RE]{}&#10;</xsl:text>
      <xsl:text>    \fancyfoot[LO,LE,RO,RE]{}&#10;</xsl:text>
      <xsl:text>...&#10;</xsl:text>
      <xsl:text>&#10;</xsl:text>
      <xsl:call-template name="ls"/>
      <xsl:text># Proœmium {.unlisted .unnumbered}&#10;</xsl:text>
      <xsl:text>&#10;</xsl:text>
      <xsl:apply-templates select="summa/liber[@title = 'Proœmium']//lemma"/>
      <xsl:apply-templates select="summa/liber[@title and number(@index) &gt; 1]"/>
      <xsl:text>\clearpage&#10;</xsl:text>
      <xsl:text>\tableofcontents&#10;</xsl:text>
      <xsl:text>&#10;</xsl:text>
    </xsl:result-document>
  </xsl:template>  
  <xsl:template name="ls">
    <xsl:text># Lectori Salutem {.unlisted .unnumbered}&#10;</xsl:text>
    <xsl:text>&#10;</xsl:text>
    <xsl:text>Dit boek is een gedeeltelijke heruitgave van de Nederlandse vertaling van de Summa Theologiae, die omstreeks 1933 werd gemaakt door een groep Dominicanen. Deze uitgave is een vrijetijdsproject van een klein aantal vrijwilligers. De originele vertaling besloeg niet de ganse Summa en deze heruitgave is ook op haar beurt onvolledig. Deze uitgave voldoet geenszins aan de kwaliteitsvoorwaarden die een lezer normaliter van boekuitgaven mag verwachten en wordt aangeboden aan de kostprijs van het drukwerk. De meest actuele status van de teksten kan worden geraadpleegd op de website https://summa.gelovenleren.net.&#10;</xsl:text>
    <xsl:text>&#10;</xsl:text>
    <xsl:text>A.M.D.G.&#10;</xsl:text>
    <xsl:text>&#10;</xsl:text>
    <xsl:value-of select="format-date(current-date(), '[D01]/[M01]/[Y0001]')"/>
    <xsl:text>&#10;</xsl:text>
    <xsl:text>&#10;</xsl:text>
  </xsl:template>
  <xsl:template match="liber[@title]">
    <xsl:message>Processing liber <xsl:value-of select="@title"/></xsl:message>
    <xsl:text># </xsl:text><xsl:value-of select="@title"/><xsl:text>&#10;</xsl:text>
    <xsl:text>&#10;</xsl:text>
    <xsl:apply-templates select="quaestio[articulus/@title][not(articulus/lemma/nl/abest)]"/>    
  </xsl:template>
  <xsl:template match="quaestio">
    <!--xsl:text># </xsl:text><xsl:value-of select="substring-before(articulus[@index = '']/lemma[contains(reference, 'q.')]/reference,' pr')"/><xsl:text> </xsl:text><xsl:value-of select="@title"/><xsl:text>&#10;</xsl:text-->
    <xsl:text>## Quaestio </xsl:text><xsl:value-of select="@index"/><xsl:text> </xsl:text><xsl:value-of select="@title"/><xsl:text>&#10;</xsl:text>
    <xsl:text>&#10;</xsl:text>
    <xsl:apply-templates select="articulus[@index = '']"/>    
    <xsl:if test="not(articulus[@index = ''])">
      <xsl:message>WARNING: no pr. for q. <xsl:value-of select="@index"/> in <xsl:value-of select="../@title"/></xsl:message>
    </xsl:if>
    <xsl:apply-templates select="articulus[@title]"/>    
  </xsl:template>
  <xsl:template match="articulus[@title]">
    <!--xsl:text>## </xsl:text><xsl:value-of select="substring-before(../articulus[@index = '']/lemma[contains(reference, 'q.')]/reference,' pr')"/><xsl:text> a. </xsl:text><xsl:value-of select="@index"/><xsl:text> </xsl:text><xsl:value-of select="@title"/><xsl:text>&#10;</xsl:text-->
    <xsl:text>### Articulus </xsl:text><xsl:value-of select="@index"/><xsl:text> </xsl:text><xsl:value-of select="@title"/><xsl:text>&#10;</xsl:text>
    <xsl:text>&#10;</xsl:text>
    <xsl:apply-templates select="lemma"/>
  </xsl:template>
  <xsl:template match="articulus[@index = '']">
    <xsl:apply-templates select="lemma"/>
  </xsl:template>
  <xsl:template match="lemma">
    <xsl:value-of select="nl"/><xsl:text> (</xsl:text><xsl:value-of select="reference"/><xsl:text>)&#10;</xsl:text>
    <xsl:text>&#10;</xsl:text>
  </xsl:template>
</xsl:stylesheet>

