var http = require("http");
//var timer = require("Timers");

http.createServer(function(request, response){
    response.writeHead(200, {"content-Type":"text/plain"});
    response.end("hello world");


}

).listen(2000)

console.log("server run");

console.dir(http)

var t = function (a){
    console.log(a);

};
setTimeout(t,
1000, "asdsad"
);

setTimeout(function(a) {
    console.log(a);
},
100, "asdsadaaa"
);
