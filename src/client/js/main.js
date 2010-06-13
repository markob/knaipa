/**
 * @autor neformal (Ivankiv Mukhaylo)  neformal.lviv@gmail.com]
 *
 */

/**
 * Global object for Knajpa.
 */
$(function(){
	var Map = function (initObj){
		var _this = this;

		this.events = {};
		this.bind = function (ev,fn){
				var ev = ev.toLocaleLowerCase();
				ev = (ev.indexOf('on') != 0) ? 'on'+ev : ev;
				this.events[ev] ? this.events[ev].push(fn) : (this.events[ev]=[]).push(fn)
				return this;
			}
		this.trigger = function (ev){
				var ev = ev.toLocaleLowerCase();
				ev = (ev.indexOf('on') != 0) ? 'on'+ev : ev;
					for (var i=0; this.events[ev] && i<this.events[ev].length;i++)
						{this.events[ev][i](this)}
				return this;
			}
		this.unbind = function (ev,fn){
				var ev = ev.toLocaleLowerCase();
				ev = (ev.indexOf('on') != 0) ? 'on'+ev : ev;
				if (this.events[ev])
					for (var i=0; i < this.events[ev].length ;i++)
					if (this.events[ev][i].toString() === fn.toString()) { this.events[ev].splice(i,1); break;}
				return this;
			}

		var gMap = google.maps;
		this.map = {}
		this.markers ={};

		this.markerIcons ={
			'knajpa': new gMap.MarkerImage('css/img/map-i/knajpa.png'),
			1: new gMap.MarkerImage('css/img/map-i/1.png'),
			2: new gMap.MarkerImage('css/img/map-i/2.png'),
			3: new gMap.MarkerImage('css/img/map-i/3.png'),
			4: new gMap.MarkerImage('css/img/map-i/4.png'),
			5: new gMap.MarkerImage('css/img/map-i/5.png'),
			6: new gMap.MarkerImage('css/img/map-i/6.png'),
			7: new gMap.MarkerImage('css/img/map-i/7.png'),
			8: new gMap.MarkerImage('css/img/map-i/8.png'),
			9: new gMap.MarkerImage('css/img/map-i/9.png')
		}

		this.addMarker = function(ia,ja,icon){
			var latlng = new google.maps.LatLng(ia,ja);
			_this.markers[ia+'_'+ja] = new gMap.Marker({ map :_this.map, position: latlng});
			if (icon){_this.markers[ia+'_'+ja].setIcon(_this.markerIcons[icon]);}
			else {_this.markers[ia+'_'+ja].setIcon(_this.markerIcons['knajpa']);}
		}

		/**
		 *
		 * @param ia
		 * @param ja
		 */
		_this.showMarker = function (ia,ja,icon){
			var id = ia+'_'+ja;
			if (_this.markers[id]){
				if (icon)_this.markers[id].setIcon(_this.markerIcons[icon]);
				_this.markers[id].setVisible(true);
			}
			else {_this.addMarker(ia,ja,icon)}
		}

		this.hideAllMarkers = function(){
			for (var marker in _this.markers){ _this.markers[marker].setVisible(false);}
		}

		this.init = function(initObj){
			for (var tmp in initObj){ _thisp[tmp]=initObj.tmp;}
			//TODO: Move this in config part, or
			var latlng = new gMap.LatLng(49.835657,24.048901);
			_this.map = new gMap.Map(document.getElementById("map"), { zoom: 13, center: latlng, mapTypeId: google.maps.MapTypeId.ROADMAP});
		}
		this.init(initObj);
		return this
	}


	window.Knajpa = (function(){
		var _this = this;

		this.contentXML = {};

		this.getContent = function (par){$.address.value(par);};

		this.setContent = function (){
			function feelMap (markerNodes){
				_this.map.hideAllMarkers();

				if (markerNodes){
					markerNodes.each(function(infex){
						var infex = (infex+1)%9;
						_this.map.showMarker($(this).attr('ia'),$(this).attr('ja'),infex);
					});
				}
			}

			/**
			 * Feel data from xml documents.
			 * @param {Document} xml Document who contained some data, for example "Knajpa" articles.
			 */
			function feelData (xml){ //TODO test this in IE;
				_this.contentXML = xml;
				$('#textInfo').xslt(_this.contentXML,'xsl/content-template.xsl');
				feelMap($('item[type=address]',_this.contentXML));
			}

			//TODO: move to normal path
				//content/content-article-template.xml
				//content/content-list-template.xml

			if (/blank/gim.test(window.location)){}
			else if (/admin/gim.test(window.location)){ //TODO:Remove this temporary admin check
				$.ajax({
					type: "GET",
					url: "js/admin.js",
					dataType: "script"
				});
			}
			else if (/knajpa/gim.test(window.location)){
				$.ajax({ dataType: "xml", url: 'content/knajpa.xml', success: feelData});
			}
			else if ($.address.path() && $.address.path() != '/'){
				$.ajax({ dataType: "xml", url: 'article?cmd=get;id='+$.address.path().replace('/',''), success: feelData});}
			else { $.ajax({ dataType: "xml", url: 'article?cmd=list', success: feelData}); }
		}

		this.init = function(){

			// init corners
			$('img').wrap("<div class='img-wrapper corners corners-5 f-right'></div>");

			// Initialize functional of AJAX linking.
			$(document).bind('click',function(/*Event*/e){
				if (e.target.tagName == 'A' && e.button == 0 && !e.ctrlKey){
					_this.getContent(e.target.getAttribute('href').replace(/.*\//,''));
					return false;
				}
			});

			// Initialize handlers of address change.
			$.address.change(function(e){ _this.setContent()});

			_this.map = new Map()
			//TODO: remove "hard code"
			// Init Map
			// ll=49.835657,24.048901 ; spn=0.085475,0.222988 ; z=13; output=embed
			// var latlng = new google.maps.LatLng(49.835657,24.048901);
			//TODO: Temporary comment this init map;
			//_this.map = new google.maps.Map(document.getElementById("map"), { zoom: 13, center: latlng, mapTypeId: google.maps.MapTypeId.ROADMAP});
		};

		this.init();
		return this;
	})();

});