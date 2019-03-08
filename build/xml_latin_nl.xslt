<?xml version="1.0"?>
<xsl:stylesheet version="2.0" 
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="xml" indent="yes"/>
  <xsl:variable name="all-nl" select="collection('./geloofsverdediging_xml?select=*.xml')/summa/lemma"/>
  <xsl:variable name="all-nl-titles" select="collection('./geloofsverdediging_titels_xml?select=*.xml')/summa/quaestio"/>
  <xsl:template match="lemma">
    <xsl:copy>
      <xsl:apply-templates/>
      <nl>
        <xsl:variable name="q" select="$all-nl[liber=current()/liber][quaestio=current()/quaestio]"/>
        <xsl:choose>
          <xsl:when test="type='pr'">
            <xsl:choose>
              <xsl:when test="not(liber)"><!-- prologue to the summa -->
                <xsl:message><xsl:value-of select="reference"/></xsl:message>
                <xsl:value-of select="$all-nl[not(liber)][not(quaestio)]/nl"/>
              </xsl:when>
              <xsl:when test="$q[type='pr']"><!-- prologue to the quaestio -->
                <xsl:message><xsl:value-of select="reference"/></xsl:message>
                <xsl:value-of select="$q[type='pr']/nl"/>
              </xsl:when>
              <xsl:otherwise>
                <abest/>
              </xsl:otherwise>
            </xsl:choose>
          </xsl:when>
          <xsl:otherwise>
            <xsl:choose>
              <xsl:when test="articulus">
                <!-- more than one articulus in quaestio -->
                <xsl:variable name="nl" select="$q[articulus=current()/articulus][type=current()/type][index=current()/index]"/>
                <xsl:choose>
                  <xsl:when test="$nl">
                    <xsl:message><xsl:value-of select="reference"/></xsl:message>
                    <xsl:value-of select="$nl/nl"/>
                  </xsl:when>
                  <xsl:otherwise>
                    <abest/>
                  </xsl:otherwise>
                </xsl:choose>
              </xsl:when>
              <xsl:otherwise>
                <!-- only one articulus in quaestio -->
                <xsl:variable name="nl" select="$q[type=current()/type][index=current()/index]/nl"/>
                <xsl:choose>
                  <xsl:when test="$nl">
                    <xsl:message><xsl:value-of select="reference"/></xsl:message>
                    <xsl:value-of select="$nl/nl"/>
                  </xsl:when>
                  <xsl:otherwise>
                    <abest/>
                  </xsl:otherwise>
                </xsl:choose>
              </xsl:otherwise>
            </xsl:choose>
          </xsl:otherwise>
        </xsl:choose>
      </nl>
    </xsl:copy>
  </xsl:template>
  <xsl:template match="summa/liber">
    <xsl:copy>
      <xsl:choose>
        <xsl:when test="@index='1'">
          <xsl:attribute name="title" select="'Prima pars'"/>
        </xsl:when>
        <xsl:when test="@index='2'">
          <xsl:attribute name="title" select="'Prima secundae'"/>
        </xsl:when>
        <xsl:when test="@index='3'">
          <xsl:attribute name="title" select="'Secunda secundae'"/>
        </xsl:when>
        <xsl:when test="@index='4'">
          <xsl:attribute name="title" select="'Tertia pars'"/>
        </xsl:when>
        <xsl:otherwise>
          <xsl:attribute name="title" select="'Prooemium'"/>
        </xsl:otherwise>
      </xsl:choose>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>
  <xsl:template match="summa/liber/quaestio">
    <xsl:copy>
      <xsl:variable name="liber" select="../@index"/>
      <xsl:variable name="title" select="$all-nl-titles[@liber=$liber][@index=current()/@index]/@title"/>
      <xsl:if test="$title">
        <xsl:variable name="source-file" select="base-uri($all-nl-titles[@liber=$liber][@index=current()/@index]/ancestor::summa)"/>
        <xsl:attribute name="title" select="$title"/>
        <xsl:attribute name="source-file" select="substring-before(tokenize($source-file,'/')[last()],'_toc')"/>
      </xsl:if>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>
  <xsl:template match="summa/liber/quaestio/articulus">
    <xsl:copy>
      <xsl:variable name="liber" select="../../@index"/>
      <xsl:variable name="quaestio" select="../@index"/>
      <xsl:variable name="title" select="$all-nl-titles[@liber=$liber][@index=$quaestio]/articulus[@index=current()/@index]/@title"/>
      <xsl:if test="$title">
        <xsl:attribute name="title" select="$title"/>
      </xsl:if>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>
  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>
</xsl:stylesheet>
 
