/**
 * @autor neformal (Ivankiv Mukhaylo)  neformal.lviv@gmail.com]
 *
 */

String.prototype.trim = function (){ return this.replace(/^\s*(\S+(\s+\S+)*)\s*$/gim,"$1");}

var eventCommander = function(){
	var events = {};
	var eventsOne = {};

	this.bind = function (ev,fn){
			var ev = ev.toLocaleLowerCase();
			ev = (ev.indexOf('on') != 0) ? 'on'+ev : ev;
			events[ev] ? events[ev].push(fn) : (events[ev]=[]).push(fn)
			return this;
		}

	this.one = function (ev,fn){
		var ev = ev.toLocaleLowerCase();
		ev = (ev.indexOf('on') != 0) ? 'on'+ev : ev;
		eventsOne[ev] ? eventsOne[ev].push(fn) : (eventsOne[ev]=[]).push(fn)
		return this;
	}

	this.trigger = function (ev,arg){
			var ev = ev.toLocaleLowerCase();
			ev = (ev.indexOf('on') != 0) ? 'on'+ev : ev;
			for (var i=0; events[ev] && i<events[ev].length;i++) {events[ev][i](this,arg)}
			for (var i=0; eventsOne[ev] && i<eventsOne[ev].length;i++) {eventsOne[ev][i](this,arg);}
			delete eventsOne[ev];

			return this;
		}

	this.unbind = function (ev,fn){
			var ev = ev.toLocaleLowerCase();
			ev = (ev.indexOf('on') != 0) ? 'on'+ev : ev;
			if (events[ev])
				for (var i=0; i < events[ev].length ;i++)
				if (events[ev][i].toString() === fn.toString()) {events[ev].splice(i,1); break;}

			if (eventsOne[ev])
				for (var i=0; i < eventsOne[ev].length ;i++)
				if (eventsOne[ev][i].toString() === fn.toString()) {eventsOne[ev].splice(i,1); break;}

			return this;
		}
}

/**
 * Global object for Knajpa.
 */
$(function(){
	var Map = function (initObj){
		var _this = this;
		var geocoder = new google.maps.Geocoder();

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

		/**
		 * You can use both of two methods initializing markers
		 *    1. parameter initializing
		 *
		 *       @param ia
		 *       @param ja
		 *       @param  {String} icon item from {@link Map.markerIcons} object
		 *
		 *    2. object initializing
		 *       @param  {
		 *         ia: {Integer},
		 *         ja: {Integer},
		 *         icon: {String},
		 *         draggable: {Boolean}
		 *       }
		 * @return {String} marker id
		 */
		this.addMarker = function(){
			var initObj = {
				icon: 'knajpa',
				draggable: false
			};

			if (arguments[0] instanceof Object){
				for (var par in arguments[0]){initObj[par] = arguments[0][par];}
			}else{
				initObj.ia = arguments[0];
				initObj.ja = arguments[1];
				if (arguments[2]) initObj.icon = arguments[2];
			}

			var latlng = new google.maps.LatLng(initObj.ia,initObj.ja);

			if (!_this.markers[initObj.ia+'_'+initObj.ja]){
				_this.markers[initObj.ia+'_'+initObj.ja] = new gMap.Marker({ map :_this.map, position: latlng, draggable:initObj.draggable});
				_this.markers[initObj.ia+'_'+initObj.ja].setIcon(_this.markerIcons[initObj.icon]);
			} else {
				_this.updateMarker(initObj.ia+'_'+initObj.ja,latlng)
			}
			return initObj.ia+'_'+initObj.ja ;
		}

		this.updateMarker = function (id, newLatLng){
			var newId = newLatLng.lat()+'_'+newLatLng.lng()
			if (!_this.markers[newId]){
				_this.markers[id].setPosition(newLatLng);
				_this.markers[newId] = _this.markers[id];
				delete _this.markers[id];
			}
			return newId;
		}

		this.identifyMarker = function(initObj){
			geocoder.geocode({address: initObj.address, language:'ua'},
				function (responce,status){
					if (status == 'OK'){
						initObj.success(responce,status);
					}else {
						initObj.decline(responce,status);
					}
				})
			return _this;
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
		this.hideMarker = function(marker){
			_this.markers[marker].setVisible(false);
		}
		this.removeMarker = function(marker){
			_this.hideMarker(marker);
			delete (_this.markers[marker]);
//			console.log(_this.markers);
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
			else if ($.address.path() && $.address.path().indexOf('query')+1){
				$.ajax({
					dataType: "xml",
					url: 'search?'+$.address.path().replace('/',''),
					success:function(xml){feelData(xml)},
					error: function(xml){feelData(xml)}
				});
			}
			else if ($.address.path() && $.address.path() != '/'){
				$.ajax({ dataType: "xml", url: 'article?cmd=get;id='+$.address.path().replace('/',''), success: feelData});}
			else { $.ajax({ dataType: "xml", url: 'article?cmd=list', success: feelData}); }
		}

		this.init = function(){
			eventCommander.apply(this);

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
	
	var Search = (function (){
		_this = this;
		this.init = function(){
			$("#search a").bind('click',function(e){
				$(this).attr('href','#query='+$("#search input").attr('value'));
				e.stopPropagation();
			})
		}
		this.init();
		return this
	})();
});