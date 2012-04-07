$("#div1").bind("click", function(){
    $(this).removeClass().addClass("desktop_show_prepare2");
    var that = $(this);
    
    setTimeout(function(){
        that.addClass("desktop_show_animation2");
    }, 100);
});

$("#div2").bind("click", function(){
    alert("div2");
});

$("#div3").bind("click", function(){
    alert("div3");
});
