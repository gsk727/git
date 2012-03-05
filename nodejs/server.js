var http = require("http")
http.createServer(function(request, response){
    response.writeHead(200, {"content-Type":"text/plain"});
    response.end("hello world");
    }
).listen(2000)

var e = require("express")
console.dir(e)

console.log("run server");

