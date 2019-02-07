<?xml version="1.0"?>
<xsl:stylesheet version="2.0" 
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="xml" indent="yes"/>
  <xsl:template match="/">
    <summa>
      <xsl:for-each-group select="summa/lemma" group-by="liber">
        <xsl:sort select="number(liber)"/>
        <liber>
          <xsl:attribute name="index" select="current-group()[1]/liber"/>
          <xsl:for-each-group select="current-group()" group-by="quaestio">
            <xsl:sort select="number(quaestio)"/>
            <quaestio>
              <xsl:attribute name="index" select="current-group()[1]/quaestio"/>
              <xsl:for-each-group select="current-group()" group-by="articulus">
                <xsl:sort select="number(articulus)"/>
                <articulus>
                  <xsl:attribute name="index" select="current-group()[1]/articulus"/>
                  <xsl:apply-templates select="current-group()"/>
                </articulus>
              </xsl:for-each-group>
            </quaestio>
          </xsl:for-each-group>
        </liber>
      </xsl:for-each-group>
    </summa>
  </xsl:template>
  <xsl:template match="@*|node()">
      <xsl:copy>
        <xsl:apply-templates select="@*|node()"/>
      </xsl:copy>
  </xsl:template>
</xsl:stylesheet>
