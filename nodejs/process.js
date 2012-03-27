var express = require("express");


var app = express.createServer();

process.nextTick(function(){
    console.log(":::::");
});


app.listen(3000);
process.nextTick(function(){
    console.log(":::::");
});

