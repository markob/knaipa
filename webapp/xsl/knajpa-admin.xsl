<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

	<xsl:template match="knajpa">
		<div class="knajpa-info corners corners-10"><!-- For easy rendering -->
			<em class="bl"></em><em class="br"></em>

				<h2 class="corners corners-10">
					<xsl:attribute name="knajpa-id"><xsl:value-of select="@id"/></xsl:attribute>

					<div contenteditable="true" class="f-left">
						<xsl:attribute name="item-id"><xsl:value-of select="./item[1]/@item-id"/></xsl:attribute>
						<xsl:value-of select="./item[1]"/>
					</div>

					<span  contenteditable="true" class="f-left">
						<xsl:attribute name="item-id"><xsl:value-of select="./item[2]/@item-id"/></xsl:attribute>
						<xsl:value-of select="./item[2]"/>
					</span>
					<em class="tr"></em><em class="tl"></em>
				</h2>

				<xsl:apply-templates select="group"/>
		</div>
	</xsl:template>

	<xsl:template match="group">
		<h3 class="corners corners-10">
			<xsl:attribute name="group-id"><xsl:value-of select="@group-id"/></xsl:attribute>

			<xsl:value-of select="@name"/>
			<span class="bottom"></span> <!--Gradient bottom line-->
			<em class="tr"></em><em class="tl"></em>  <!--Corners-->
		</h3>
		<div class="description-block">
			<xsl:attribute name="group-id"><xsl:value-of select="@group-id"/></xsl:attribute>

			<xsl:apply-templates select="item"/>

			<div class="item new-item">
				<h4 contenteditable="true"><span>Новий пункт опису</span></h4>
				<div class="description">Опис</div>
				<em class="remove"></em>
			</div>

		</div>
	</xsl:template>

	<xsl:template match="item">
		<div class="item">
			<xsl:attribute name="item-id"><xsl:value-of select="@item-id"/></xsl:attribute>

			<h4><span><xsl:value-of select="@name"/></span></h4>
			<div class="description"><xsl:value-of select="."/></div>
		</div>
	</xsl:template>

</xsl:stylesheet>