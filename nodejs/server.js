var http = require("http");
//var timer = require("Timers");

http.createServer(function(request, response){
    response.writeHead(200, {"content-Type":"text/plain"});
    response.end("hello world");
    }
).listen(2000)

var e = require("express")
console.dir(e)

console.log("run server");

<<<<<<< HEAD
=======
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
>>>>>>> 0bb5cf589bc17d3200827cc31ff68e3d91f6d31a
