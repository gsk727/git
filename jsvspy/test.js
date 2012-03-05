/*
	查找this的不同，与python的不同见test.py
	js的顶端this是window而python没有这个东西, python 用的是global
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
 