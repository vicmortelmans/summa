<?xml version="1.0"?>
<xsl:stylesheet version="2.0" 
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xpath-default-namespace="http://www.w3.org/1999/xhtml">
  <xsl:output method="xml" indent="yes"/>
  <xsl:template match="/">
    <summa>
      <xsl:apply-templates select="collection('./kapitel_tidy?select=kapitel*.htm')/html"/>
    </summa>
  </xsl:template>
  <xsl:template match="p[span[@class='a2textf']]">
    <lemma>
      <xsl:variable name="html" select="ancestor::html"/>
      <xsl:variable name="liber" select="($html//span[@class='a3text'])[1]/text()"/>
      <xsl:variable name="liber-number">
        <xsl:choose>
          <xsl:when test="$liber='Prima Pars'">1</xsl:when>
          <xsl:when test="$liber='Prima Pars Secundae Partis'">2</xsl:when>
          <xsl:when test="$liber='Secunda Pars Secundae Partis'">3</xsl:when>
          <xsl:when test="$liber='Tertia Pars'">4</xsl:when>
        </xsl:choose>
      </xsl:variable>
      <xsl:variable name="quaestio" select="substring-after(($html//span[@class='a2text'])[1]/text(), 'Quaestio ')"/>
      <xsl:variable name="articulus" select="substring-after(($html//h1)[1]/text(), 'Articulus')"/>
      <xsl:variable name="reference" select="span[@class='a2textf']/text()"/>
      <xsl:variable name="type">
        <xsl:choose>
          <xsl:when test="contains($reference, 's. c.')">
            <xsl:value-of select="'sc'"/>
          </xsl:when>
          <xsl:when test="contains($reference, 'co.')">
            <xsl:value-of select="'co'"/>
          </xsl:when>
          <xsl:when test="contains($reference, 'pr.')">
            <xsl:value-of select="'pr'"/>
          </xsl:when>
          <xsl:when test="contains($reference, 'ad')"><!-- sometimes 'ad.', sometimes 'ad. arg.' -->
            <xsl:value-of select="'ad'"/>
          </xsl:when>
          <xsl:when test="contains($reference, 'arg.')">
            <xsl:value-of select="'arg'"/>
          </xsl:when>
          <xsl:otherwise>
            <xsl:value-of select="replace(tokenize($reference,' ')[last()-1],'.','')"/>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:variable>
      <xsl:variable name="last-item" select="tokenize($reference,' ')[last()]"/>
      <xsl:variable name="index">
        <xsl:choose>
          <xsl:when test="number($last-item)=number($last-item)"><!-- test if it's a number-->
            <xsl:value-of select="$last-item"/>
          </xsl:when>
          <xsl:otherwise>
            <xsl:value-of select="1"/>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:variable>
      <xsl:variable name="latin" select="normalize-space(string-join(span[@class='a2textf']/following-sibling::node()|following-sibling::p[not(span[@class='a2textf'])],' '))"/>
      <liber><xsl:value-of select="$liber-number"/></liber>
      <quaestio>
        <xsl:choose><!-- exception case for prooemium of book III (4), to be merged with first Quaestio -->
          <xsl:when test="normalize-space($reference) = 'IIIª pr.'">1</xsl:when>
          <xsl:otherwise>
            <xsl:value-of select="normalize-space($quaestio)"/>
          </xsl:otherwise>
        </xsl:choose>
      </quaestio>
      <articulus><xsl:value-of select="normalize-space($articulus)"/></articulus>
      <reference><xsl:value-of select="normalize-space($reference)"/></reference>
      <type><xsl:value-of select="normalize-space($type)"/></type>
      <index><xsl:value-of select="normalize-space($index)"/></index>
      <latin><xsl:value-of select="$latin"/></latin>
    </lemma>
  </xsl:template>
  <xsl:template match="@*|node()">
      <xsl:apply-templates select="@*|node()"/>
  </xsl:template>
</xsl:stylesheet>
