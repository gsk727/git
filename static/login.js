// 学习的目的
function CLogin() {
	this.toString = function() {
		return "Login";
	};
	
	this.checkUser = function() 
	{
		//alert(Login);
		if ($("#user_id").val().length == 0)
		{
			var s = new String("123");
			s.test="test";
			alert(s.test);
			alert("输入用户名");
		}
	}
	
}
/*

var Login = {
	
	toString:function()
	{
		return "Login";
	},
	
	
	checkUser:function()
	{
		//alert(Login);
		if ($("#user_id").val().length == 0)
		{
			var s = new String("123");
			s.test="test";
			alert(s.test);
			alert("输入用户名");
		}
	}

}*/
var Login = new CLogin();