<?xml version="1.0"?>
<xsl:stylesheet version="2.0" 
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="text" encoding="UTF-8"/>
  <xsl:strip-space elements="*" />
  <xsl:template match="liber">
    <xsl:result-document method="text" href="markdown/Aquino_Summa_{@index}.md">
      <xsl:text>---&#10;</xsl:text>
      <xsl:text>title: SUMMA THEOLOGIAE - </xsl:text><xsl:value-of select="@title"/><xsl:text>&#10;</xsl:text>
      <xsl:text>author: Thomas van Aquino&#10;</xsl:text>
      <xsl:text>lang: nl&#10;</xsl:text>
      <xsl:text>classoption:&#10;</xsl:text>
      <xsl:text>- twocolumn&#10;</xsl:text>
      <xsl:text>geometry: top=2cm, bottom=2cm, left=2cm, right=2cm&#10;</xsl:text>
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
      <xsl:apply-templates select="../liber[@title = 'Proœmium']//lemma"/>
      <xsl:apply-templates select="quaestio[not(articulus/lemma/nl/abest)]"/>
      <xsl:text>\clearpage&#10;</xsl:text>
      <xsl:text>\tableofcontents&#10;</xsl:text>
      <xsl:text>&#10;</xsl:text>
    </xsl:result-document>
  </xsl:template>  
  <xsl:template match="quaestio">
    <!--xsl:text># </xsl:text><xsl:value-of select="substring-before(articulus[@index = '']/lemma[contains(reference, 'q.')]/reference,' pr')"/><xsl:text> </xsl:text><xsl:value-of select="@title"/><xsl:text>&#10;</xsl:text-->
    <xsl:text># Quaestio </xsl:text><xsl:value-of select="@index"/><xsl:text> </xsl:text><xsl:value-of select="@title"/><xsl:text>&#10;</xsl:text>
    <xsl:text>&#10;</xsl:text>
    <xsl:apply-templates select="articulus[@index = '']"/>    
    <xsl:if test="not(articulus[@index = ''])">
      <xsl:message>WARNING: no pr. for q. <xsl:value-of select="@index"/> in <xsl:value-of select="../@title"/></xsl:message>
    </xsl:if>
    <xsl:apply-templates select="articulus[@title]"/>    
  </xsl:template>
  <xsl:template match="articulus[@title]">
    <!--xsl:text>## </xsl:text><xsl:value-of select="substring-before(../articulus[@index = '']/lemma[contains(reference, 'q.')]/reference,' pr')"/><xsl:text> a. </xsl:text><xsl:value-of select="@index"/><xsl:text> </xsl:text><xsl:value-of select="@title"/><xsl:text>&#10;</xsl:text-->
    <xsl:text>## Articulus </xsl:text><xsl:value-of select="@index"/><xsl:text> </xsl:text><xsl:value-of select="@title"/><xsl:text>&#10;</xsl:text>
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

