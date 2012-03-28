var checkMap={
    "stuff":checkStuff,
	"base":checkBase,
	"task":checkTask,	
    "airline":checkAir,
    "device": checkDevice,
    "content":checkContent,
};

function checkContent(frmName){
    return true;
}
function checkAir(frmName){
    return true;
};

function checkDevice(frmName){
    return true;
};

$("#addBtnOK").bind("click", function(){
	var cType=$("#checkType").val();
	cFun = checkMap[cType];
	if (!cFun("#frmAdd"))
		return;
	var objs = $("#frmAdd input[type!=hidden]");
	var p = {};

	for(var i=0; i < objs.length; ++i)
	{
	   p[objs.eq(i).attr("id")] = objs.eq(i).val();
	}

    var sel = $("#frmAdd select option:selected");
    p[sel.parent().attr("id")] = sel.val(); 
    url = $("#frmAdd").attr("action");
    $.ajax({
        type: "POST",
        url: url,
        data: p, 
        dataType: "json",
        success: function(data, textStatus){
            alert(data.message);
        }
    });

});


function handle_addStuff(data, textstatus){
    m = data.message;
}

$("#frmUpdate #base").bind("GETBASEOK", function(event, selName, index){
	$(selName+" option:nth-child("+(index+1)+ ")").attr("selected", true);
    g_cur_base = null;
});


function getBaseNames(callback, url, params, selName) {
        $.ajax({
           type: "GET",
           url: url,
           data: params, 
           dataType: "json",
           success: function(data, textStatus){
           			callback(data, textStatus, selName);
           		}
        });
};

function addBaseToSel(data, textStatus, selName) {
      var d = $(selName);
	  $(selName).empty();
      var dType=$("#checkType").val();

      for(var i = 0; i < data.message.length; ++i) {
      	if (typeof g_cur_base != "undefined" && g_cur_base == data.message[i])
      	     $("<option selected=true>"+data.message[i]+"</option>").appendTo(selName);
      	else if(typeof g_cur_airline!="undefined" && g_cur_airline==data.message[i])
      	     $("<option selected=true>"+data.message[i]+"</option>").appendTo(selName);
      	else{
      	     $("<option>"+data.message[i]+"</option>").appendTo(selName);
      	}
      }
      // $(selName).trigger("GETBASEOK", selName, index)
};

$("#addTab").bind("click", function(){
	 var cType=$("#checkType").val();
	
	 switch(cType){
        case 'base':
            break;
        case 'device':
            getBaseNames(addBaseToSel, url="/airline/", {dType:"json"}, "#frmAdd #airline");
        default:
            getBaseNames(addBaseToSel, "/base/", {dataType:"json"}, "#frmAdd #base")
	 };
});

$("#myTable tbody tr").bind("click", function(){
    		g_cur_index = $(this).index();
});

$("#updateTab").bind("click", function(){
	if (typeof g_cur_index == "undefined")
		return ""

	var rObject = $("#myTable tr:nth-child("+(g_cur_index+1)+")");
    var inputID, baseIndex;
    for (var i =0;i < $("#frmUpdate input[type!='hidden'], #frmUpdate select").length; ++i){  
        inputID = $("#frmUpdate input:[type!='hidden'],#frmUpdate select").eq(i).attr("id");
        if (inputID == "base") { baseIndex = i; continue; }
		$("#frmUpdate #"+inputID).attr("value", $.trim(rObject.children("td:eq("+i+")").text()));
    }
    
	g_cur_base = $.trim(rObject.children("td:eq("+baseIndex+")").text());
	if($("#checktype").val() == "device")
	  g_cur_airline =  $("#myTable tr:nth-child("+(g_cur_index+1)+")").children("td:eq("+i+")").text();

    var cType=$("#checkType").val();
    switch(cType){
        case 'base':
            break;
        case 'device':
            getBaseNames(addBaseToSel, url="/airline/", {dType:"json"}, "#frmUpdate #airline");
        default:
            getBaseNames(addBaseToSel, "/base/", {dataType:"json"}, "#frmUpdate #base")
    };
});


/*
   frmName:update一个,add一个
*/
function checkTask(frmName) {
	var start = $.trim($(frmName+" #start").val());
	var end = $.trim($(frmName+" #end").val());
	if (start.length==0 || end.length==0){
		alert("没有制定时间");
		return false;
	}
	return true;	
}

function checkBase(frmName){
	var name = $.trim($(frmName+" #name").val());
    if(name.length==0)
        return alert("名字不能空");
    return true;
};

function checkStuff(frmName){
	var name =  $.trim($(frmName+" #name").val());
    var role = $.trim($(frmName+" #role").val());
    var begin = $.trim($(frmName+" #begin").val());
    var end = $.trim($(frmName+" #end").val());
    var email = $.trim($(frmName+" #email").val());

    if (email.length == 0)
        return alert("email 不能空");
    else if (name.length== 0)
        return alert("名字不能空");
    else if (begin.length == 0)
        return alert("入职日期不能空");

	return true;
};

$("#updateBtnOK").bind("click", function(){	
	var cType=$("#checkType").val();
	cFun = checkMap[cType];
	if (!cFun("#frmUpdate"))
		return 
	$("#frmUpdate").submit();
});
