<?xml version="1.0"?>
<xsl:stylesheet version="2.0" 
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:f="http://functions">
  <xsl:output method="text" encoding="UTF-8"/>
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
    <xsl:apply-templates select="summa/liber/quaestio[articulus[@title][not(lemma/nl/abest)]]"/>
  </xsl:template>

  <xsl:template match="quaestio">
    <xsl:text>https://summa.gelovenleren.net/</xsl:text><xsl:value-of select="f:file(.)"/><xsl:text>&#10;</xsl:text>
  </xsl:template>

</xsl:stylesheet>
