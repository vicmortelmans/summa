<?xml version="1.0"?>
<xsl:stylesheet version="2.0" 
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:f="http://functions">
  <xsl:output method="html" name="html" version="5.0" encoding="UTF-8" indent="yes" />
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

  <xsl:template match="quaestio">
    <xsl:variable name="file" select="f:file(.)"/>
    <xsl:result-document format="html" href="summa/{$file}">
<html lang="nl">
<head>
  <title>Quaestio <xsl:value-of select="@index"/> - Summa Theologiae</title>
  
  <!-- Meta info -->
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <meta name="HandheldFriendly" content="true" />
  <meta name="viewport" content="initial-scale=1.0, user-scalable=yes, width=device-width" />
  <meta name="apple-mobile-web-app-title" content="Summa Theologiae" />
  <meta property="og:title" content="{../@title} Quaestio {@index} - Summa Theologiae" />
  <meta property="og:description" content="Theologische Summa van den H. Thomas van Aquino, Latijnsche en Nederlandsche tekst uitgegeven door een groep Dominicanen" />
  <meta property="og:image" content="https://summa.gelovenleren.net/images/euclid/poster-closeup.jpg?v=1" />
  <meta name="twitter:card" content="summary_large_image" /><!-- TODO -->
  <meta name="twitter:title" content="Summa Theologiae" />
  <meta name="twitter:description" content="Theologische Summa van den H. Thomas van Aquino, Latijnsche en Nederlandsche tekst uitgegeven door een groep Dominicanen" />
  <meta name="twitter:image" content="https://summa.gelovenleren.net/images/euclid/poster-closeup.jpg?v=1" />

  <!-- Icons -->
  <link rel="icon" type="image/png" href="favicon-32x32.png" sizes="32x32" />
  <link rel="icon" type="image/png" href="favicon-16x16.png" sizes="16x16" />
  
  <!-- Styles -->
  <link href="https://use.typekit.net/voh3vfd.css" rel="stylesheet" type="text/css" />
  <link href="styles/summa.css" rel="stylesheet" type="text/css" />
  <link href="styles/shapes.css" rel="stylesheet" type="text/css" />
  
  <!-- Scripts -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js" type="text/javascript"></script>
  
  <script type="text/javascript" src="scripts/summa.js"></script>
  <script type="text/javascript" src="scripts/shapes.js"></script>
</head>
<body>

<header>
    <a href="{$file}#" id="nav-toggle"><i class="fal fa-bars"></i></a>
    <a href="index.html" id="logo">Summa Theologiae</a>
    <nav id="nav-primary">
        <ul>
            <li id="nav-home"><a href="index.html">Summa</a></li>
            <xsl:for-each select="../../liber/quaestio[1]">
              <xsl:variable name="file" select="f:file(.)"/>
              <li><a href="{$file}"><xsl:value-of select="../@title"/></a></li>
            </xsl:for-each>
            <li><a href="about.html">Over deze website</a></li>
        </ul>
    </nav>
    <a id="nav-secondary-toggle" href="{$file}#"><span id="nav-secondary-toggle-label">Quaestio</span> <i class="fal fa-angle-double-down"></i></a>
    <a id="nav-ternary-toggle" href="book1.html#"><span id="nav-ternary-toggle-label">Articulus</span> <i class="fal fa-angle-double-down"></i></a>
</header>
<main id="main">

<nav id="nav-secondary">
    <ul class="nav-secondary-list">
        <xsl:for-each select="../quaestio">
          <xsl:variable name="file" select="f:file(.)"/>
          <li>
              <a href="{$file}">
                  <xsl:choose>
                      <xsl:when test=".//nl[not(abest)]"><b>Quaestio <xsl:value-of select="@index"/><br/><xsl:value-of select="@title"/></b></xsl:when>
                      <xsl:otherwise>Quaestio <xsl:value-of select="@index"/><br/><xsl:value-of select="@title"/></xsl:otherwise>
                  </xsl:choose>
              </a>
          </li>
        </xsl:for-each>
    </ul>
</nav>

<nav id="nav-ternary">
    <ul class="nav-ternary-grid">
        <xsl:for-each select="articulus">
          <li>
            <a data-figure="figure-articulus{@index}" href="{$file}#articulus{@index}">
              <xsl:choose>
                <xsl:when test="not(@index='')">
                  <xsl:text>Articulus </xsl:text><xsl:value-of select="@index"/><br/><xsl:value-of select="@title"/>
                </xsl:when>
                <xsl:otherwise>Prooemium</xsl:otherwise>
              </xsl:choose>
            </a>
          </li>
        </xsl:for-each>
        <li></li>
    </ul>
</nav>

<xsl:for-each select="articulus">
<section class="figure-context" id="articulus{@index}">
    <div class="section-content">
        <div class="section-copy">
            <xsl:if test="position()=1">
              <h1>
                  <xsl:value-of select="../../@title"/><xsl:text>. </xsl:text>
                  <xsl:if test="not(../@index='')">Quaestio <xsl:value-of select="../@index"/>.<br/></xsl:if>
                  <xsl:if test="../@title"><xsl:value-of select="../@title"/>.</xsl:if>
              </h1>
              <xsl:if test="not(../../@index='') and not(../@title)">
                <p class="message">Deze Quaestio is niet beschikbaar in Nederlandse vertaling</p>
              </xsl:if>
            </xsl:if>

            <h2>
              <xsl:choose>
                <xsl:when test="@index=''">
                  <xsl:text>Prooemium</xsl:text>
                </xsl:when>
                <xsl:otherwise>
                  <xsl:text>Articulus </xsl:text><xsl:value-of select="@index"/>.<br/>
                  <xsl:value-of select="@title"/>
                </xsl:otherwise>
              </xsl:choose>
            </h2>
            
            <figure id="figure-articulus{@index}">
              <script type="text/javascript">document.write(newShape())</script>
            </figure>
            
            <xsl:if test="@title and lemma[1]/nl/abest">
              <p class="message">Dit artikel is beschikbaar in Nederlandse vertaling, maar die kan
                slechts gepubliceerd worden na correctie van de <a href="bronbestanden/{../@source-file}.txt">tekstherkenning</a> van de <a href="bronbestanden/{../@source-file}.pdf">ingescande PDF</a>. Wil je deze website
                helpen vervolledigen, neem dan contact op met <a href="mailto:info@gelovenleren.net">info@gelovenleren.net</a>!</p>
            </xsl:if>

            <xsl:for-each select="lemma">
              <p class="latin {type}"><xsl:value-of select="latin"/> (<xsl:value-of select="reference"/>)</p>
              <xsl:if test="normalize-space(nl) != ''">
                  <p class="nl {type}">
                    <xsl:if test="not(nl/abest) and (type='arg' or type='ad') and count(../lemma[type='arg']) &gt; 1">
                      <xsl:value-of select="index"/><xsl:text> &#x2014; </xsl:text>
                    </xsl:if>
                    <xsl:value-of select="nl"/>
                  </p>
              </xsl:if>
            </xsl:for-each>
        </div>
    </div>
</section>
</xsl:for-each>
</main>
<footer>
    <p>Website design based on a project from <a href="https://www.c82.net/">Nicholas Rougeux</a> &#160; &#160; bluntly adapted by <a href="http://www.gelovenleren.net/">Geloven Leren</a></p> &#160; &#160; <span id="longs">ſ &#x2192; s</span>
</footer>
</body>
</html>
    </xsl:result-document>
  </xsl:template>
  <xsl:template match="@*|node()">
    <xsl:apply-templates select="@*|node()"/>
  </xsl:template>
</xsl:stylesheet>
