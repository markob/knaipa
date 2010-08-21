/**
 * Created by IntelliJ IDEA.
 * User: neformal
 * Date: Jul 10, 2010
 * Time: 12:40:28 PM
 * To change this template use File | Settings | File Templates.
 */
	var separateInput = function (initObj){
		var _this = this;
		//Events Commander
			this.events = {};
			this.eventsOne = {};

			this.bind = function (ev,fn){
					var ev = ev.toLocaleLowerCase();
					ev = (ev.indexOf('on') != 0) ? 'on'+ev : ev;
					this.events[ev] ? this.events[ev].push(fn) : (this.events[ev]=[]).push(fn)
					return this;
				}
			this.trigger = function (ev,arg){
					var ev = ev.toLocaleLowerCase();
					ev = (ev.indexOf('on') != 0) ? 'on'+ev : ev;
					for (var i=0; this.events[ev] && i<this.events[ev].length;i++)
						{this.events[ev][i](this,arg)}
					for (var i=0; this.eventsOne[ev] && i<this.eventsOne[ev].length;i++)
						{this.eventsOne[ev][i](this,arg);}
					delete this.eventsOne[ev];

					return this;
				}
			this.unbind = function (ev,fn){
					var ev = ev.toLocaleLowerCase();
					ev = (ev.indexOf('on') != 0) ? 'on'+ev : ev;
					if (this.events[ev])
						for (var i=0; i < this.events[ev].length ;i++)
						if (this.events[ev][i].toString() === fn.toString()) { this.events[ev].splice(i,1); break;}

					if (this.eventsOne[ev])
						for (var i=0; i < this.eventsOne[ev].length ;i++)
						if (this.eventsOne[ev][i].toString() === fn.toString()) { this.eventsOne[ev].splice(i,1); break;}
					return this;
				}
			this.one = function (ev,fn){
				var ev = ev.toLocaleLowerCase();
				ev = (ev.indexOf('on') != 0) ? 'on'+ev : ev;
				this.eventsOne[ev] ? this.eventsOne[ev].push(fn) : (this.eventsOne[ev]=[]).push(fn)
				return this;
			}

		this.makeExtended = function (){
			_this.container.data('position','extended');
			// Animation test
			_this.container.animate({ top: 20, left:0});
		}

		this.makeCompact = function(){
			_this.container.data('position','compact');
			_this.container.animate({top: 0, left:225 });
			_this.container.parent().stop().animate({ height: 14});
		}

		_this.setPointer = function(el, offset){
			if (! _this.sel)_this.sel = window.getSelection();

			var range = document.createRange();
			range.setStart(el, offset);
			range.setEnd(el, offset);
			_this.sel.removeAllRanges();
			_this.sel.addRange(range);
		}

		this.separate = function (){
			if (_this.separator){
				var newElements = [];
				$(_this.selNode).text().replace (/[^;]+;?/gim,function(){
					var newSpan = $("<span>"+arguments[0]+"</span>").insertBefore(_this.selNode.parentNode);
					if (arguments[1] <= _this.selOffset && arguments[1]+arguments[0].length >= _this.selOffset){ _this.setPointer(newSpan[0].firstChild, _this.selOffset-arguments[1])}
					newElements.push(newSpan);
				})
				_this.trigger('separate',newElements);

				$(_this.selNode.parentNode).remove();

				_this.sel = window.getSelection();
				_this.selNode = _this.sel.anchorNode;
				_this.selOffset = _this.sel.anchorOffset;
			}
		}

		this.merge = function (){
			_this.selNode.parentNode.nextSibling.innerHTML = _this.selNode.nodeValue + _this.selNode.parentNode.nextSibling.firstChild.nodeValue;
			_this.setPointer(_this.selNode.parentNode.nextSibling.firstChild, _this.selOffset);
			_this.selNode.parentNode.parentNode.removeChild(_this.selNode.parentNode);
		}

		this.removeEmptyNodes = function(){
			if (_this.selNode && _this.selNode.parentNode.getAttribute('contenteditable') && _this.selNode.previousSibling){
				var selectedNode = _this.selNode.previousSibling.firstChild;
				_this.selNode.parentNode.removeChild(_this.selNode);
				_this.setPointer(selectedNode,selectedNode.nodeValue.length)
			} else if (_this.selNode && _this.selNode.parentNode.getAttribute('contenteditable') && _this.selNode.nextSibling && _this.selNode.nextSibling.tagName != 'BR'){
				var selectedNode=_this.selNode.nextSibling.firstChild;
				_this.selNode.parentNode.removeChild(_this.selNode);
				_this.setPointer(selectedNode,0);
			}
		}

		this.init = function (initObj){
			if (initObj) for (parametr in initObj) _this[parametr] = initObj[parametr]

			_this.container.wrapInner('<div style="float:left;" contenteditable="true"></div>');
			_this.editabelEl = _this.container.find('div:first'); 

			if (_this.separator){
				_this.container.addClass('separator');
			}

			_this.container
				.data('position','compact')
				.bind('click', function(){ _this.editabelEl.trigger('focus')})
				.bind('keydown',function(e){
						window.setTimeout(function(){
							if (_this.container.data('position') == 'compact' && (_this.editabelEl.height() > 20 || _this.container.width()-20 < _this.editabelEl.width())) {_this.makeExtended();}
							if (_this.container.data('position') == 'extended'){
								_this.container.parent().stop().animate({height:_this.container.height()+40})
								if (_this.editabelEl.width() < 230 && _this.editabelEl.height() < 20) { _this.makeCompact(); }
							}
						}, 10)
					})

			_this.editabelEl[0].onpaste = function (e){_this.container.data ('isPaste', true)};
			_this.editabelEl
				.bind('focus',function(e) {
						_this.sel = window.getSelection();
						_this.selNode = _this.sel.anchorNode;
						_this.selOffset = _this.sel.anchorOffset;

						if (_this.selNode.tagName && _this.editabelEl[0].childNodes.length){
							if (_this.editabelEl[0].lastChild.firstChild)
								_this.setPointer(_this.editabelEl[0].lastChild.firstChild,_this.editabelEl[0].lastChild.firstChild.nodeValue.length)
							else _this.setPointer(_this.editabelEl[0].firstChild,_this.editabelEl[0].firstChild.nodeValue.length)
						};
					})
				.bind('keydown',function(e){
						window.setTimeout(function(){
							// If content is pasted
							if (_this.container.data ('isPaste')){
								_this.editabelEl.html(_this.editabelEl.text());
								_this.sel = window.getSelection();
								_this.setPointer(_this.editabelEl[0].firstChild, 0);
								_this.container.data ('isPaste', false)
							}

							_this.sel = window.getSelection();
							_this.selNode = _this.sel.anchorNode;
							_this.selOffset = _this.sel.anchorOffset;

							// Remove empty nodes
							_this.removeEmptyNodes();

							// Wrap text node to span (When text node placed in <div contentEditable = true />)
							if (_this.selNode && _this.selNode.nodeType==3 && _this.selNode.parentNode == _this.editabelEl[0]){
								$(_this.selNode).wrap("<span></span>");
								_this.setPointer(_this.selNode, _this.selOffset);
							}

							// Separate node if present ";" symbol
							if (_this.selNode && _this.selNode.nodeType==3 && $(_this.selNode).text().trim().indexOf(';')> -1 && $(_this.selNode).text().trim().indexOf(';') < $(_this.selNode).text().trim().length-1 ){
								_this.separate();
							}
							// Merge nodes if symbol ";" does not exist
							if (_this.selNode && _this.selNode.nodeType==3 && _this.selNode.parentNode != $(_this.selNode.parentNode.parentNode).find('span::last')[0]  && $(_this.selNode).text().trim().indexOf(';') == -1){
								_this.merge();
							}

							if (_this.textContent && _this.textContent.trim() != _this.editabelEl.text().trim())
								_this.trigger('change', window.getSelection().anchorNode.parentNode)
							_this.textContent = _this.editabelEl.text();

						},10);

						if (e.keyCode == 13){ //Return
							document.execCommand('inserthtml',false,'<br>&nbsp;');
							_this.sel = window.getSelection();

							if (!_this.sel.isCollapsed) _this.sel.collapseToEnd();
							var r = _this.sel.getRangeAt(0);
							var offset = r.startOffset
							var offsetElement = r.startContainer;

							r.setStart(offsetElement,offset-1);
							r.setEnd(offsetElement,offset);

							document.execCommand('delete',false,false);
							_this.container.trigger('keydown');
							return false;
						}
					})
				.bind('focus',function(){_this.container.css({'z-index':99});})
				.bind('blur',function(){_this.container.css({'z-index':0});})
		}
		this.init(initObj);
	}