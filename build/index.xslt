<?xml version="1.0"?>
<xsl:stylesheet version="2.0" 
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:f="http://functions">
  <xsl:output method="xml" encoding="UTF-8" indent="yes" />
  <xsl:function name="f:file">
    <xsl:param name="quaestio"/>
    <xsl:choose>
      <xsl:when test="$quaestio/@index=''">
        <xsl:value-of select="concat('liber-',$quaestio/../@index,'.html')"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="concat('liber-',$quaestio/../@index,'-quaestio-',format-number($quaestio/@index,'000'),'.html')"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:function>

  <xsl:template match="/">
    <summa>
      <xsl:apply-templates select="summa/liber/quaestio/articulus[@title][not(lemma/nl/abest)]"/>
    </summa>
  </xsl:template>

  <xsl:template match="articulus">
    <articulus>
      <title><xsl:value-of select="@title"/></title>
      <url>https://summa.gelovenleren.net/<xsl:value-of select="f:file(..)"/>#articulus<xsl:value-of select="@index"/></url>
      <image>https://summa.gelovenleren.net/images/eclid/book<xsl:value-of select="lemma[1]/liber"/>.png</image>
    </articulus>
  </xsl:template>

</xsl:stylesheet>
