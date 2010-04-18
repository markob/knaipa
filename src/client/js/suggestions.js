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
	this.dataFilterURL = 'xsl/suggestion.xsl';

	this.styleModifier = {
		width:0,
		top: 0,
		left:1
	}

	this.selected = false;

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
		if (e.keyCode == 27) {_this.hide();}

		//Up;
		else if (e.keyCode == 38) {_this.setActivElement(_this.getActivElement().prev()[0]||_this.suggestElement.find('li:last'));}

 		//Down;
		else if (e.keyCode == 40) { _this.setActivElement(_this.getActivElement().next()[0]||_this.suggestElement.find('li:first'));}

		else {
			if (!_this.showed) _this.show(e)
			_this.pasteData();
		}
	};

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
	 * Generate and insert data to {@link suggestElement}
	 */
	this.pasteData = function(){
		function closure (){
			_this.dataFilter.getElementsByTagName('xsl:variable')[0].firstChild.nodeValue = _this.container.attr('value').toLowerCase();
			_this.suggestElement
					.xslt (_this.data, _this.dataFilter) // Make transformation
					.find ('li')
					.each (function(){this.innerHTML = this.innerHTML.replace((new RegExp('('+_this.container.attr('value')+')','i')),'<b>$1</b>');}); // To highlight search query.

			_this.setActivElement($(_this.suggestElement).find('li')[0]);
		}
		window.setTimeout(closure,10); //Wait for event data
	}

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
		_this.hide();
	}

	this.init = function(){
		for (var tmp in initObj){_this[tmp]=initObj[tmp];}

		$.ajax({url: _this.dataURL, success : function (data){_this.data = data;}});
		$.ajax({url: _this.dataFilterURL, success : function (data){_this.dataFilter = data;}})

		$(document.body).append(_this.suggestElement);

		_this.container
			.bind('keydown',_this.keyEvents)
			.bind('focus',_this.show)
			.bind('blur',_this.hide);
	};
	this.init();
};