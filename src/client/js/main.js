/**
 * @autor neformal (Ivankiv Mukhaylo)  neformal.lviv@gmail.com]
 *
 */

/**
 * Global object for Knajpa.
 */
$(function(){
	window.Knajpa = (function(){
		var _this = this;

		this.map={};
		this.markers ={};
		this.contentXML = {};

		this.getContent = function (par){$.address.value(par);};
		this.setContent = function (){
			function feelMap (markers){

				for (var tmp in _this.markers){ _this.markers[tmp].setVisible(false);}
				if (markers){
					markers.each(function(){
						var latlng = new google.maps.LatLng($(this).attr('ia') ,$(this).attr('ja'))
						var id = this.parentNode.getAttribute('id');
						if (_this.markers[id]) _this.markers[id].setVisible(true);
						else {_this.markers[id] = new google.maps.Marker({ map :_this.map, position: latlng});}
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
				feelMap($('marker',_this.contentXML));
			}
			if (/admin/gim.test(window.location)){ //TODO:Remove this temporary admin check
				$.ajax({
					type: "GET",
					url: "js/admin.js",
					dataType: "script"
				});
			}
			//TODO: move to normal path
//				content/content-article-template.xml
//				content/content-list-template.xml

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

			//TODO: remove "hard code"
			// Init Map
			// ll=49.835657,24.048901 ; spn=0.085475,0.222988 ; z=13; output=embed
			var latlng = new google.maps.LatLng(49.835657,24.048901);
			_this.map = new google.maps.Map(document.getElementById("map"), { zoom: 13, center: latlng, mapTypeId: google.maps.MapTypeId.ROADMAP});
		};

		this.init();
		return this;
	})();


	var knajpaMap = (function (initObj){
		var _this = this;

		/**
		 * Events
		 *    select - when user select some item.
		 */
		this.events={};
		/**
		 *
		 * @param {String} ev Event name can use without "on" "onSelect" == "onselect" == "select"
		 * @param {Function} fn
		 */
		this.bind = function (ev,fn){
			ev = ev.toLocaleLowerCase();
			ev = (ev.indexOf('on') != 0) ? 'on'+ev : ev;
			_this.events[ev] ? _this.events[ev].push(fn) : (_this.events[ev]=[]).push(fn)
			return _this;
		}

		this.trigger = function (ev){
			ev = ev.toLocaleLowerCase();
			ev = (ev.indexOf('on') != 0) ? 'on'+ev : ev;
			for (var i=0; _this.events[ev] && i<_this.events[ev].length;i++){_this.events[ev][i](_this)}
			return _this;
		}

		this.map = {};
		this.markers ={};

		this.addMarker = function(){
			
		}

		this.hideMarkers = function(){
			for (var tmp in _this.markers){ _this.markers[tmp].setVisible(false);}
		}

		this.init = function(initObj){
			for (var tmp in initObj){ _thisp[tmp]=initObj.tmp;}

			var latlng = new google.maps.LatLng(49.835657,24.048901);
			_this.map = new google.maps.Map(document.getElementById("map"), { zoom: 13, center: latlng, mapTypeId: google.maps.MapTypeId.ROADMAP});
		}
		this.init(initObj);
		return this
	})()

});