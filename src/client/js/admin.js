/**
 * @autor neformal (Ivankiv Mukhaylo)  neformal.lviv@gmail.com]
 *
 */

Knajpa.admin = new function(){
	var _this = this;
	_this.data={};

	this.init = function (){
		_this.dataForm = $('#knajpa-admin-form');
		_this.dataForm.bind('submit',function(){
			//test

			_this.data.cmd = 'post' ;
			_this.data.knaipa = Math.random() ;
			_this.data.title = _this.dataForm[0]['knajpa-title'].value;
			_this.data.description = _this.dataForm[0]['knajpa-description'].value;
			_this.data.text = _this.dataForm[0]['knajpa-article'].value;
			_this.data.cut = _this.dataForm[0]['knajpa-cut'].value;

//			for (var i=0; i< this.length ; i++)
//				if (this[i].name) _this.data[this[i].name] = this[i].value;

//			_this.data.markerIa='21';
//			_this.data.markerJa= '22';
			

			$.ajax({
				type: "POST",
				data: _this.data,
				url: 'article',
				success: function(msg){alert(msg);}
			});

			return false;
		})
	}
	this.init();
};