<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:output encoding="utf-8" method="html"></xsl:output>

	<xsl:template match="item">
		<div class='knajpaItem'>
			<h2>
				<a>
					<xsl:attribute name="href">
						/<xsl:value-of select="@id"/>
					</xsl:attribute>
					<xsl:value-of select="title"></xsl:value-of>
				</a>
			</h2>
			<article><xsl:copy-of select="description//*"/></article>
			<a>
				<xsl:attribute name="href">
					<xsl:value-of select="@id"/>
				</xsl:attribute>
				<xsl:value-of select="cut"></xsl:value-of>
			</a>
		</div>
	</xsl:template>

	<xsl:template match="article">
		<div class='knajpaItem'>
			<h2><xsl:value-of select="title" /></h2>
			<article>
				<xsl:copy-of select="description//*"/>
				<xsl:copy-of select="text//*"/>
			</article>
		</div>

		<xsl:apply-templates select="comments"></xsl:apply-templates>
	</xsl:template>

	<xsl:template match="comments">
		<div class="comments corners corners-10">
			Відгуки та коментарі
			<b>(<xsl:value-of select="count(//item)"/>)</b>
			<em class="tl"></em><em class="tr"></em><em class="bl"></em><em class="br"></em>
		</div>
		<ul class='comments'>
			<xsl:for-each select="item">
				<li>
					<div class="user-name">
						<xsl:value-of select="@autor"></xsl:value-of>
						<span  class="f-right">12:12 12.12/2012</span>
					</div>
					<xsl:value-of select="text()"></xsl:value-of>
					<xsl:apply-templates select="." mode="comment"></xsl:apply-templates>
				</li>
			</xsl:for-each>
		</ul>
	</xsl:template>

	<xsl:template match="item" mode="comment">
		<xsl:if test="item">
			<ul>
				<xsl:for-each select="item">
					<li>
						<div class="user-name">
							<xsl:value-of select="@autor"></xsl:value-of>
							<span class="f-right">12:12 12.12/2012</span>
						</div>
						<xsl:value-of select="text()"></xsl:value-of>
						<xsl:apply-templates select="." mode="comment"></xsl:apply-templates>
					</li>
				</xsl:for-each>
			</ul>
		</xsl:if>

	</xsl:template>

</xsl:stylesheet>