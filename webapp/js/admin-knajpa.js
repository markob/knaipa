var adminKnajpa= function (initObj){
	var _this = this;
	var initSuccess=false;

	//Initialization parameters part;

	this.knajpa = false;
	this.activeDescription = false;
	this.activeHovered = false;

	// Methods part
	/**
	 *
	 * @param element jQuery element
	 */
	this.hoverElement = function (element){
		if (_this.activeHovered) _this.activeHovered.removeClass('hover')
		_this.activeHovered = element;
		_this.activeHovered.addClass ('hover');
	};
	/**
	 *
	 * @param element jQuery element
	 */
	this.setActiveDescription = function (element){
		if (_this.activeDescription) _this.activeDescription.removeClass('active').removeClass('hover');
		_this.activeDescription = element;
		_this.activeDescription.addClass ('active');

		_this.activeHovered = false;
	}

	this.init = function (initObj){
		eventCommander.apply(this);

		if (initObj)
			for (parametr in initObj) _this[parametr] = initObj[parametr];

		if (!initSuccess){
			//Init navigation
			$(document).bind('keydown',function (e){
				if (e.keyCode == 40 || e.keyCode == 38){ // 40 = Down ; 38 = Up
					var moderator = e.keyCode == 40 ? 'next' : 'prev'
					var el = {};
					if (_this.activeHovered) el = _this.activeHovered[moderator]();
					else if (_this.activeDescription) el = _this.activeDescription[moderator]();

					if (el[0] == _this.activeDescription[0]) el = el[moderator]();

					if (!el[0] && e.keyCode == 40) el = _this.container.find('li:not(".active"):first')
					if (!el[0] && e.keyCode == 38) el = _this.container.find('li:not(".active"):last')

					_this.hoverElement(el);

					return false;
				}

				if (e.keyCode == 13){ // Enter
					if (_this.activeHovered){_this.setActiveDescription(_this.activeHovered)}
					return false;
				}
			});
			_this.container.find('li:not(.active)')
				.live("click",function(){ _this.setActiveDescription($(this));})
				.live('mouseenter',function (){_this.hoverElement($(this))})

			if (adminKnajpa.elements) adminKnajpa.push(_this);
			else adminKnajpa.elements = [_this];
		}

		initSuccess = true;
	}
	this.init(initObj);
}
