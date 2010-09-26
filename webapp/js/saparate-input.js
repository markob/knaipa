/**
 * Created by IntelliJ IDEA.
 * User: neformal
 * Date: Jul 10, 2010
 * Time: 12:40:28 PM
 * To change this template use File | Settings | File Templates.
 */

	var editableArea = function (){
		var _this = this;

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

		this.getCursorPosition = function(){
			var pos = $(_this.insertElement('<em/>'))
			var result = {top:pos.offset().top, left:pos.offset().left}
			pos.remove();
			return result;
		}

		/**
		 *
		 * @param el {String} HTML code of element
		 * @return inserted node
		 */
		this.insertElement = function(el){
			var sel = window.getSelection();
			var selNode = _this.sel.anchorNode;
			var selOffset = _this.sel.anchorOffset;

			var newContent = ($(selNode).text().slice(0, selOffset)||'&nbsp;')+el+'<em id="insertedTemporaryElement"></em>'+($(selNode).text().slice(selOffset)||'&nbsp;');

			$(selNode).replaceWith(newContent);
			selNode = $('#insertedTemporaryElement')[0].previousSibling;
			$('#insertedTemporaryElement').remove();

			var range = document.createRange();
			range.setStart(selNode.nextSibling, 0);
			range.setEnd(selNode.nextSibling, 0);
			window.getSelection().removeAllRanges();
			window.getSelection().addRange(range);

			return selNode;
		}

		this.init =

	}

	var separateInput = function (initObj){
		var _this = this;

		this.setPointer = function(el, offset){
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
			eventCommander.apply(_this);
			editableArea.apply(_this);

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
							_this.insertElement('<br/>');
							_this.container.trigger('keydown');
							return false;
						}
					})
				.bind('focus',function(){_this.container.css({'z-index':99});})
				.bind('blur',function(){_this.container.css({'z-index':0});})
		}
		this.init(initObj);
	}