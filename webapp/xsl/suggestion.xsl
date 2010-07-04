<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:output encoding="utf-8" method="html"></xsl:output>

	<xsl:variable name="filter">а</xsl:variable>

	<xsl:variable name="lover-case">абвгґдеєжзиіїйклмнопрстуфхцчшщьюяabcdefghijklmnopqrstuvwxyz</xsl:variable>
	<xsl:variable name="up-case">АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯABCDEFGHIJKLMNOPQRSTUVWXYZ</xsl:variable>

	<xsl:template match="suggestion">
		<xsl:if test="count(item [contains(translate(@value,$up-case,$lover-case) , $filter)])">
			<em class="br"></em>
			<em class="bl"></em>

			<em class="t"></em>
			<em class="b"></em>
			<em class="r"></em>

			<ul>
				<xsl:for-each select="item [contains(translate(@value,$up-case,$lover-case) , $filter)]">
					<xsl:sort order="descending" select="starts-with(translate(@value,$up-case,$lover-case) , $filter)" />
					<xsl:sort order="descending" select="contains(translate(@value,$up-case,$lover-case) , $filter)" />

					<xsl:if test="position() &lt;= 10">
						<li><xsl:value-of select="@value"/></li>
					</xsl:if>

				</xsl:for-each>
			</ul>
		</xsl:if>
	</xsl:template>
</xsl:stylesheet>