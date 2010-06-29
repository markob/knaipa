/**
 * @author neformal [neformal.lviv@gmail.com].
 * 19 лют 2010 1:34:12
 */

var suggestions = function (initObj){
	var _this = this;
	this.container = $('#suggestions');
	this.suggestElement = $('#suggestion-test')[0]?
								$('#suggestion-test'):
								$('<div class="suggestion"></div>')
	this.data = {};
	this.dataURL = 'content/knajpa-suggestion.xml';
	this.dataFilter = {};
	/**
	 * URL of data filter
	 */
	this.dataFilterURL = 'xsl/suggestion.xsl';

	/**
	 * Contains suggestion "empty result" string.
	 *  Need for compare empty result 
	 */
	this.emptySuggestion = '';
	/**
	 * Contains the initial data input
	 */
	this.bufer = "";

	this.styleModifier = {
		width:0,
		top: 0,
		left:1
	}

	this.selected = false;

	var specialKeys = {
		13: 'Enter',
		27: 'Escape',
		38: 'Up',
		40: 'Down'
	}
	/**
	 * Events
	 *  	select - When user select some item.
	 *  	show - When showed suggestions
	 *  	hide - When hided suggestions
	 */
	this.events={};
	/**
	 *
	 * @param {String} ev Event name can use without "on" "onSelect" == "onselect" == "select"
	 * @param {Function} fn
	 */
	this.bind = function (ev,fn){
		var ev = ev.toLocaleLowerCase();
		ev = (ev.indexOf('on') != 0) ? 'on'+ev : ev;
		_this.events[ev] ? _this.events[ev].push(fn) : (_this.events[ev]=[]).push(fn)
		return _this;
	}

	this.trigger = function (ev){
		var ev = ev.toLocaleLowerCase();
		ev = (ev.indexOf('on') != 0) ? 'on'+ev : ev;
		for (var i=0; _this.events[ev] && i<_this.events[ev].length;i++){_this.events[ev][i](_this)}
		return _this;
	}

	/**
	 *
	 * @param {Event} e
	 */
	this.keyEvents = function(e){
		e.stopPropagation();

		//Enter;
		if (e.keyCode == 13) {_this.setSuggestion();}

		//Escape;
		if (e.keyCode == 27) {
			_this.hide();
			_this.container.attr('value',_this.bufer);
		}

		//Up;
		else if (e.keyCode == 38) {
			if (!_this.showed) {_this.searchAndRender (_this.container.attr('value')); return}
			if (!_this.getActiveElement()) {
				_this.setActiveElement($(_this.suggestElement).find('li:last'));
			}
			else {
				if (!_this.getActiveElement().prev()[0]){ _this.clearActiveElement();}
				else{_this.setActiveElement(_this.getActiveElement().prev());}
			}
		}

 		//Down;
		else if (e.keyCode == 40) {
			if (!_this.showed) {_this.searchAndRender (_this.container.attr('value')); return}

			if (!_this.getActiveElement()) {_this.setActiveElement($(_this.suggestElement).find('li:first'));}
			else {
				if (!_this.getActiveElement().next()[0]){ _this.clearActiveElement();}
				else{ _this.setActiveElement(_this.getActiveElement().next());}
			}
		}

	};

	this.searchInit = function(e){
		if (e.keyCode in specialKeys) { return;}
		_this.searchAndRender (_this.container.attr('value'));
		_this.bufer = _this.container.attr('value');
	}

	/**
	 *
	 * @param {Event} e
	 */
	this.hide = function(e){
		_this.showed = false;
		_this.suggestElement
				.css ('display','none')
				.unbind('mousedown',_this.setSuggestion)
		_this.trigger("hide");
	}

	/**
	 * Show suggestion popup.
	 * @param {Event} e
	 */
	this.show = function (e){
		_this.showed = true;
		_this.suggestElement
				.css ({
					left: _this.container.offset().left +_this.styleModifier.left + 'px',
					top: _this.container.offset().top + _this.styleModifier.top + 'px',
					width: _this.container.width() + _this.styleModifier.width + 'px',
					display: 'block'
				})
				.bind('mousedown',_this.setSuggestion)
		_this.trigger("show");
	};

	/**
	 * Generate and insert data to {@link this.suggestElement}
	 */
	this.searchAndRender = function(query){
		(_this.dataFilter.getElementsByTagName('xsl:variable')[0] || _this.dataFilter.getElementsByTagName('variable')[0])
			.firstChild.nodeValue = query.toLowerCase();
		_this.suggestElement
				.xslt (_this.data, _this.dataFilter, function (suggestElement){
					if (suggestElement.html() == ""){_this.hide(); return}
					else {
						suggestElement
								.find ('li')
								.each (function(){this.innerHTML = this.innerHTML.replace((new RegExp('('+query+')','i')),'<b>$1</b>');}); // To highlight search query.
						_this.show()
						_this.selected = false;
					}
				}) // Make transformation

	}

	/**
	 * @param {Element} el
	 */
	this.setActiveElement = function(el){
		if (_this.selected) _this.selected.removeClass('active');
		_this.selected = $(el);
		_this.selected.addClass('active');
		_this.container.attr('value',_this.selected.text());
	}

	this.clearActiveElement = function(){
		if (_this.selected) _this.selected.removeClass('active');
		_this.selected = false;
		_this.container.attr('value', _this.bufer)
	}

	this.getActiveElement = function(){return _this.selected}

	/**
	 *
	 * @param {Event} e
	 */
	this.setSuggestion = function (e){
		if (e) {_this.setActiveElement(e.target)}
		if (_this.getActiveElement()) _this.container.attr('value', _this.getActiveElement().text());
		_this.bufer = _this.container.attr('value');
		_this.container.trigger('blur').trigger('focus'); //Need for reset some specific behavior of input control. (Escape button for example)
		_this.trigger('select');
	}

	this.init = function(){
		for (var tmp in initObj){_this[tmp]=initObj[tmp];}

		$.ajax({
			url: _this.dataURL,
			dataType: "xml",
			success : function (data){_this.data = data; },
			error: function (XMLHttpRequest, textStatus, errorThrown){
					alert(XMLHttpRequest.status);
					alert(XMLHttpRequest.responseText);
				}
		});

		$.ajax({url: _this.dataFilterURL,  dataType: "xml", success : function (data){_this.dataFilter = data;}})

		$(document.body).append(_this.suggestElement);

		_this.container
			.bind('keydown',_this.keyEvents)
			.bind('keyup', _this.searchInit)
//			.bind('focus',_this.show)
			.bind('blur',_this.hide);
	
		_this.bufer = _this.container.attr('value');
	};
	this.init();
};