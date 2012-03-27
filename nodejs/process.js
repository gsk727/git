/* 下面是一些路由例子，以及与之相匹配的关联路径：
"/user/:id"
/user/12

"/users/:id?"
/users/5
/users

"/files/*"
/files/jquery.js
/files/javascripts/jquery.js

"/file/*.*"
/files/jquery.js
/files/javascripts/jquery.js

"/user/:id/:operation?"
/user/1
/user/1/edit

"/products.:format"
/products.json
/products.xml

"/products.:format?"
/products.json
/products.xml
/products

"/user/:id.:format?"
/user/12
/user/12.json
*/

var express = require("express");
var app = express.createServer();

process.nextTick(function(){
    console.log(":::::");
});


app.listen(3000);
process.nextTick(function(){
    console.log(":::::");
});


// 好像与位置有关 
app.get("/user/:id", function(req, res, next){
    b = "1111111";
    next();

})

app.get("/user/:id?", function(req, res){
    console.log(b);
    res.send(b + "1111");
    res.end();
});

