$(function(){
    room_Line();
    total_price();
    user_recommend();
});

function deleteMyCookie()
{
    var expireDate = new Date();
    var cookieName="pr_session";
    expireDate.setDate( expireDate.getDate() - 1 );
    document.cookie = cookieName + "= " + "; expires=" + expireDate.toGMTString() + "; path=/";
    location.reload()
}

function makeANewRoom()
{
    location.href=("/creation");
}

function room_Line(){
    $.ajax
   ({
      type: 'GET',
      headers:
      {
         'Accept': 'application/json',
         'Content-Type': 'application/json'
      },
      url: "/roomList",
      async: false,

      success: function(result){
          table=result.results;
          all_html="<div id=\"padding_border\"></div>";
          var i;
          var part_html="";
          part_html+="<div id=\"pr\"> <div id = \"pr_line1\">";
          part_html+="<div id=\"pr_contents\">" + "방ID" + "</div>";
          part_html+="<div id=\"nick_id_date\">" + "방 제목" + "</div></div>";
          part_html+="<div id = \"pr_line2\"><div id=\"pr_nickname\"><b>" + "방장 이름"+"</b></div>";
          part_html+="<div id=\"pr_id\">" + "음식점 이름" +"</div>";
          part_html+="<div id=\"pr_date\">"+ "생성시간"+"</div>";
          part_html+="</div></div>";
          for(i=0; i< table.length; i++ )
          {
              part_html+="<a href=\"/room/" + table[i].room_id + "\">";
              part_html+="<div id=\"pr\"><div id = \"pr_line1\">";
              part_html+="<div id=\"pr_contents\">" + table[i].room_id + "</div>";
              part_html+="<div id=\"nick_id_date\">" + table[i].room_title + "</div></div>";
              part_html+="<div id =\"pr_line2\"><div id=\"pr_nickname\"><b>" + table[i].user_name+"</b></div>";
              part_html+="<div id=\"pr_id\">" + table[i].restaurant_name +"</div>";
              part_html+="<div id=\"pr_date\">"+ table[i].created+"</div>";
              part_html+="</div></div></a>";
          }
          all_html+=part_html;
          $("#time-line").html(all_html);
      },
      statusCode:{
         409:function(msg){
            alert(msg.responseText);
         }
      }
   });
}

function total_price(){
    $.ajax
   ({
      type: 'GET',
      headers:
      {
         'Accept': 'application/json',
         'Content-Type': 'application/json'
      },
      url: "/showTotal",
      async: false,

      success: function(result){
          table=result.results;
          table2 = result.results2;
          var part_html= "";
          var all_html="<div id=\"pay-money\">줄 돈</div>";
          for(i=0; i< table.length; i++ )
          {
              part_html+="<div id=\"total-price\">";
              part_html+= table[i].giver + " -> " + table[i].taker + " : " + table[i].price + "원";
              part_html+="</div>";
          }
          part_html+="<div id = \"payed-money\">받을 돈</div>";
          for(j=0;j<table2.length;j++)
          {
              part_html+="<div id=\"total-price\">";
              part_html+= table2[j].giver + " -> " + table2[j].taker + " : " + table2[j].price + "원";
              part_html+="</div>";
          }
          all_html+=part_html;
          $("#search_user_wrap").html(all_html);
      },
      statusCode:{
         409:function(msg){
            alert(msg.responseText);
         }
      }
   });
}

function user_recommend(){
    $.ajax
   ({
      type: 'GET',
      headers:
      {
         'Accept': 'application/json',
         'Content-Type': 'application/json'
      },
      url: "/recommend",
      async: false,

      success: function(result){
          table=result.results;
          var all_html = "<div id = \"recommend-menu\">추천메뉴</div>";
          for(i=0;i<table.length;i++)
          {
              all_html+="<div id = \"recommend-menu-list\">";
              all_html+=table[i].restaurant_name + " / " + table[i].food_name + " / " + table[i].food_price + "원";
              all_html+="</div>";
          }
          if(table.length === 0)
          {
              all_html+="<div id = \"recommend-menu-list\">아직 추천메뉴가 생성되지 않았습니다";
              all_html+="</div>";
          }
          $("#user-recommend-wrap").html(all_html);
      },
      statusCode:{
         409:function(msg){
            alert(msg.responseText);
         }
      }
   });
}