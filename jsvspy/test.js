/*
	����this�Ĳ�ͬ����python�Ĳ�ͬ��test.py
	js�Ķ���this��window��pythonû���������, python �õ���global
*/
function create() {
	var result = new Array();
	for(var i = 0; i < 10; ++i)
	{
		result[i] = function(num) {
			return num;
		}(i);
	}
	return result;
};

var func = create();
for(var i = 0; i<func.length; i++)
{
	document.write(func[i]);
}    

var name = "test";
var handler = {
	name : "asdasd",
	test:function(){ 
		return function(){
			return this.name;
		};
	}
};
document.write(handler.test().apply(handler));
 