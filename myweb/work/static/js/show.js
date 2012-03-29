$(".active").bind("click", function(event){
        var tag = $(this).find("a").text();
        if (tag == "个人信息") {
            var name = document.cookie;
            $.get("/user/show",  function(data){
                $("#show").html("<h1>" + data  + "</h1>");
                var b ;
            });
            
        }
        
})
