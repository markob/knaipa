<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:output encoding="utf-8" method="html"></xsl:output>

	<!--List-->
	<xsl:template match="request[@type = 'list']">
			<xsl:apply-templates select="knajpa|article" mode="list"/>
	</xsl:template>

	<xsl:template match="article" mode="list">

		<div class='articleItem'><hr/>
			<h2>
				<span class="index"><xsl:value-of select="position()"></xsl:value-of></span>
				<xsl:value-of select="title"/>
			</h2>
			<div class="img-wrapper corners corners-5 f-right">
				<img src="content/img/armenian-yard.png" class="f-right"/>
			</div>
			<article><xsl:copy-of select="description//*"/></article>
			<a href="#"><xsl:value-of select="cut"/></a>
		</div>

	</xsl:template>

	<xsl:template match="knajpa" mode="list">
		<div class='knajpaItem'><hr/>
			<h2><span class="index"><xsl:value-of select="position()"></xsl:value-of></span>Просто Кнайпа</h2>

			<div class="img-wrapper corners corners-5 f-right">
				<img src="content/img/man-on-stairs.png" class="f-right"/>
			</div>

			<div class="knajpa-info-wraper">
				<p>
					Нічний клюб<br/>
					8:00 - 22:00<br/>
					вулю Героїв Упаб 72<br/>
				</p>
				<p>
					Телефон: <br/>
					(032) 226-18-34<br/>
					моб.: 097 123-45-67
				</p>
				<p>
					Цінова категорія:<br/>
					будні 100-200 грн.<br/>
					свята 150 - 500 грн.<br/>
				</p>
				<p class="tags">
					<a>Wi-Fi</a><span class="separator"></span>
					<a>TB</a><span class="separator"></span>
					<a>Зал для курців</a><span class="separator"></span>
					<a>Стриптиз</a><span class="separator"></span>
					<a>Face control</a><span class="separator"></span>
					<a>Розважальні автомати</a>
				</p>
			</div>

		</div>
	</xsl:template>

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

	<!--Cooments for articles-->
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
	
	<!--Template for display information about knajpa -->
		<xsl:template match="knajpa">
			<div class="knajpa-info corners corners-10">
				<em class="bl"></em><em class="br"></em>

				<h2 class="corners corners-10">
					<xsl:value-of select="@name"/>
					<span><xsl:value-of select="@type"/></span>
					<em class="tr"></em><em class="tl"></em>
				</h2>
				<xsl:apply-templates select="group" mode="knajpa"></xsl:apply-templates>
			</div>
		</xsl:template>

			<xsl:template match="group" mode="knajpa">
				<h3>
					<xsl:if test="position()=1">
						<xsl:attribute name="class">corners corners-10</xsl:attribute>
						<em class="tl"></em><em class="tr"></em>
					</xsl:if>
					<xsl:value-of select="@name"/><span class="bottom"></span>
				</h3>
				<ul>
					<xsl:apply-templates select="item" mode="knajpa"></xsl:apply-templates>
				</ul>
			</xsl:template>

				<xsl:template match="item" mode="knajpa">
					<xsl:if test="not(@type)">
						<li>
							<h4><xsl:value-of select="@name"/></h4>
							<span class="description"><xsl:copy-of select="."/></span>
						</li>
					</xsl:if>

					<xsl:if test="@type = 'address'">
						<li>
							<h4><xsl:value-of select="@name"/></h4>
							<span class="description"><xsl:copy-of select="."/></span>
						</li>
					</xsl:if>

					<xsl:if test="@type = 'tags'">
						<li class="tags">
							<h4><xsl:value-of select="@name"/></h4>
							<span class="description corners">
								<em class="tl"></em><em class="tr"></em><em class="br"></em><em class="bl"></em>
								<xsl:copy-of select="."/>
							</span>
						</li>
					</xsl:if>

					<xsl:if test="@type = 'img'">
						<li class="long-description">
							<h4><xsl:value-of select="@name"/></h4>
							<span class="img-description">
								<xsl:for-each select="item">
									<div class="img-wrapper corners corners-5 f-right">
										<img>
											<xsl:attribute name="src"><xsl:value-of select="@src"/></xsl:attribute>
											<xsl:attribute name="alt"><xsl:value-of select="@alt"/></xsl:attribute>
										</img>
									</div>
								</xsl:for-each>
							</span>
						</li>
					</xsl:if>
				</xsl:template>

</xsl:stylesheet>