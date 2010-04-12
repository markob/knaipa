/**
 * @autor neformal (Ivankiv Mukhaylo)  neformal.lviv@gmail.com]
 *
 */

/**
 * Global object for Knajpa.
 */
$(document).ready(function(){
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

		this.init = function() {

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
});

var suggestions = function (initObj){
	var _this = this;
	this.container = $('#suggestions');
	this.data = 'For,each,language,the,client,library,provides,tools,and,an,abstraction,layer,letting,you,construct,' +
				'queries,and,use,response,data,without,having,to,create,HTTP,requests,or,process,HTTP,responses,by,' +
				'hand,Each,client,library,provides,classes,that,correspond,to,the,elements,and,data,types,that,the,API,' +
				'uses,Each,client,library,also,provides,extensions,for,specific,Google,services,that,have,Data,APIs'.split(',');
	/**
	 *
	 * @param {Event} e
	 */
	this.showSuggestions = function (e){
		console.log(e.target.value);
	};

	this.init = function(){
		for (var tmp in initObj){_this[tmp]=initObj[tmp];}
		_this.container.bind('keyup',_this.showSuggestions);
	};
	this.init();
};
