<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:output encoding="utf-8" method="html"></xsl:output>

	<xsl:template match="knajpa">
		<xsl:apply-templates select="item"/>
	</xsl:template>

	<xsl:template match="item">
		<div class="w-100 admin-options">
			<xsl:value-of select="@name"/> : <xsl:value-of select="." />
		</div>
	</xsl:template>

</xsl:stylesheet>