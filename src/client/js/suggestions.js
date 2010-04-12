/**
 * @author neformal [neformal.lviv@gmail.com].
 * 19 лют 2010 1:34:12
 */

var suggestions = function (initObj){
	var _this = this;
	this.container = $('#suggestions');
	this.suggestElement = $('#suggestion-test')[0]?$('#suggestion-test'):$('<ul id="suggestion-test"></ul>')
	this.data = {};
	this.dataURL = 'content/knajpa-suggestion.xml';
	this.dataFilter = {};
	this.dataFilterURL = 'xsl/suggestion.xsl';

	this.selected = false;

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
		if (e.keyCode == 13) {_this.setSuggestion();} //enter;

		else if (e.keyCode == 38) { //up;
			_this.setActivElement(_this.getActivElement().prev()[0]||_this.suggestElement.find('li:last'));
		}

		else if (e.keyCode == 40) { //down;
			_this.setActivElement(_this.getActivElement().next()[0]||_this.suggestElement.find('li:first'));
		}
		else _this.showSuggestions(e)
	};

	/**
	 *
	 * @param {Event} e
	 */
	this.hideSuggestion = function(e){
		_this.suggestElement
				.css ('display','none');
		_this.suggestElement
				.unbind('mousedown',_this.setSuggestion)
	}

	/**
	 *
	 * @param {Event} e
	 */
	this.showSuggestions = function (e){
		function closure (){
			_this.dataFilter.getElementsByTagName('xsl:variable')[0].firstChild.nodeValue = e.target.value.toLowerCase();
			_this.suggestElement
					.css ('display','block')
					.xslt (_this.data, _this.dataFilter)
					.find ('li')
					.each (function(){this.innerHTML = this.innerHTML.replace((new RegExp('('+e.target.value+')','i')),'<b>$1</b>');});

			_this.setActivElement($(_this.suggestElement).find('li')[0]);
		}
		window.setTimeout(closure,10);

		_this.suggestElement
				.css ({
					left: _this.container.offset().left + 'px',
					top: _this.container.offset().top + 'px',
					width: _this.container.width() + 'px'
				})
				.bind('mousedown',_this.setSuggestion)
	};

	/**
	 *
	 * @param {Element} el
	 */
	this.setActivElement = function(el){
		if (_this.selected) _this.selected.removeClass('active');
		_this.selected = $(el)
		_this.selected.addClass('active');
	}

	this.getActivElement = function(){return _this.selected}

	/**
	 *
	 * @param {Event} e
	 */
	this.setSuggestion = function (e){
		if (e) {_this.setActivElement(e.target)}
		_this.container.attr('value', _this.getActivElement().text());
		_this.trigger('select');
		_this.hideSuggestion();
	}

	this.init = function(){
		for (var tmp in initObj){_this[tmp]=initObj[tmp];}

		$.ajax({url: _this.dataURL, success : function (data){_this.data = data;}});
		$.ajax({url: _this.dataFilterURL, success : function (data){_this.dataFilter = data;}})

		$(document.body).append(_this.suggestElement);

		_this.container
			.bind('keydown',_this.keyEvents)
			.bind('focus',_this.showSuggestions)
			.bind('blur',_this.hideSuggestion);
	};
	this.init();
};