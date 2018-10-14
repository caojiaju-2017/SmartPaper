var code = "";
var orgsign= "1e2c68303ebd11e880d3989096c1d848";
window.onload=function()
{
};

$(document).ready(function(e) {

});

$.extend({

    GetQueryString:function (name)
    {
         var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
         var r = window.location.search.substr(1).match(reg);
         if(r!=null)return  unescape(r[2]); return null;
    },

});