$(function () {
    showingMenu();
    roomMember();
});

setInterval(function(){
    roomMember();
}, 7000);

function UserReady()
{
    $.ajax
    ({
        type: 'POST',
        headers:
        {
           'Accept': 'application/json',
           'Content-Type': 'application/json'
        },
        url: '/orderReady',
        async: false,

        success: function(result){
            ready = result.results;
            if(ready)
            {
                alert("주문 준비가 취소되었습니다");
            }
            else
            {
                alert("주문이 준비되었습니다");
            }
        },
        statusCode:{
            404:function(msg){
                alert(msg.responseText);
            },
            400:function(msg){
                alert(msg.responseText);
            }
		}
    });
}

function RoomOut()
{
    $.ajax
   ({
      type: 'GET',
      headers:
      {
         'Accept': 'application/json',
         'Content-Type': 'application/json'
      },
      url: "/roomOut",
      async: false,

      success: function(result){
        alert("방에서 나갔습니다");
        var expireDate = new Date();
        var cookieName="room_session";
        expireDate.setDate( expireDate.getDate() - 1 );
        document.cookie = cookieName + "= " + "; expires=" + expireDate.toGMTString() + "; path=/";
        location.href=("/");
      },
      statusCode:{
         409:function(msg){
            alert(msg.responseText);
         }
      }
   });
}

function showingMenu()
{
    $.ajax
   ({
      type: 'GET',
      headers:
      {
         'Accept': 'application/json',
         'Content-Type': 'application/json'
      },
      url: "/select",
      async: false,

      success: function(result){
          table=result.results;
          all_html="";
          var i;
          var part_html="";
          part_html+="<form>";
          for(i=0; i< table.length; i++ )
          {
              part_html+="<div id=\"select-menu\"> <input type=\"checkbox\" name = \"menu_info\" value = \"menu\"";
              part_html+= "id = \""+ table[i].food_name + "\">" + table[i].food_name + ":   " + table[i].food_price + "원";
              part_html+="</div>";
          }
          part_html+="</form>";
          all_html+=part_html;

          uinfo = result.results2;
          var html2 = "";
          if(!uinfo[0])
          {
              html2+="<button class = \"btn btn-xs btn-search\" id = \"host-order\" onclick = \"finalDecision()\"> 최종주문결정 </button>";
              html2+="<button class= \"btn btn-xs btn-search\" id = \"host-select-pay\" data-toggle= \"modal\" data-target = \"#who_pay\"> 결제자결정 </button>";
              html2+="<div class = \"modal fade\" id = \"who_pay\" role = \"dialog\">";
              html2+="<div class = \"modal-dialog\"> <form id = \"selectMenu\">";
              html2+="<div class = \"modal-content\"> <div class = \"modal-header\"> <button type = \"button\" class = \"close\" data-dismiss= \"modal\">&times;</button>";
              html2+="<h4 class = \"modal-title\">결제자 선택</h4></div><div class = \"modal-body\" id = \"modal-payer\">";
              html2+="</div><div class = \"modal-footer\"><input type = \"button\" onclick=\"select_payer()\" class = \"btn btn-success\"";
              html2+="data-dismiss=\"modal\" name=\"btn\" value=\"선택완료\"/></div></div></form></div></div>"
          }
          else
          {
              html2+="<div id = \"uinfo\">참가자: ";
              html2+=uinfo+"</div>";
          }

          $("#modal-plus").html(all_html);
          $("#host-menu-wrap").html(html2);
      },
      statusCode:{
         409:function(msg){
            alert(msg.responseText);
         }
      }
   });
}

function finalDecision()
{
    var numberOfPerson = document.getElementById("inwon").innerHTML;
    json_data=JSON.stringify(numberOfPerson);

    $.ajax
   ({
      type: 'PUT',
      headers:
      {
         'Accept': 'application/json',
         'Content-Type': 'application/json'
      },
      url: '/finalOrder',
      async: false,
      data: json_data,
      success: function(result){
         alert("최종 주문에 성공했습니다");
          location.reload();
      },
      statusCode:{
         409:function(msg){
            alert(msg.responseText);
         }
      }
   });
}

function select_payer()
{
    payer = document.getElementsByName("payer_info");
    var csum = 0;
    for(var i = 0; i < payer.length; i++) {
        if (payer[i].checked) {
            csum = 1;
            var data = {'user_id': payer[i].id};
        }
    }
    json_data = JSON.stringify(data);
    $.ajax
   ({
      type: 'PUT',
      headers:
      {
         'Accept': 'application/json',
         'Content-Type': 'application/json'
      },
      url: '/getPayer',
      async: false,
      data: json_data,
      success: function(result){
          if(csum)
          {
              alert("결제자가 설정되었습니다.");
          }
          else
          {
              alert("결제자가 설정되어있지 않습니다");
          }
      },
      statusCode:{
         409:function(msg){
            alert(msg.responseText);
         }
      }
   });
 }


function orderComplete()
{
    food = document.getElementsByName("menu_info");
    var data = new Array();
    var realFoodNum = 0;
    for(var i = 1; i <= food.length; ++i){
        if(food[i-1].checked)
        {
            realFoodNum = realFoodNum +1;
            data[realFoodNum] = food[i-1].id;
        }
    }
    data[0] = realFoodNum;
    json_data=JSON.stringify(data);

    $.ajax
   ({
      type: 'PUT',
      headers:
      {
         'Accept': 'application/json',
         'Content-Type': 'application/json'
      },
      url: '/order',
      async: false,
      data: json_data,
      success: function(result){
         alert("주문 목록이 추가되었습니다");
         roomMember();
          location.reload();
      },
      statusCode:{
         409:function(msg){
            alert(msg.responseText);
         }
      }
   });
}

function roomMember()
{
    $.ajax
   ({
      type: 'GET',
      headers:
      {
         'Accept': 'application/json',
         'Content-Type': 'application/json'
      },
      url: "/roomMember",
      async: false,

      success: function(result){
          table=result.results;
          uinfo = result.results2;
          var all_html= "";
          var i;
          var part_html="";
          var part2="";
          document.getElementById("inwon").innerHTML = table.length;
          for(i=0; i< table.length; i++ )
          {
              part_html += "<div id = \"personal-menu\">";
              part_html+="<div id=\"participant\">" + table[i].user_name + "</div>";
              for(var j = 0; j< table[i].user_choice.length; j++)
              {
                part_html+="<div id = \"user-choice-menu\">";
                  part_html+="<div id = \"user-choice-menu-name\">";
                  part_html +=table[i].user_choice[j].food_name;
                  part_html +="</div>";
                  part_html += "<div id = \"user-choice-menu-price\">";
                  part_html += table[i].user_choice[j].food_price;
                  part_html += " 원</div>";
                  part_html += "</div>";
              }
              if(table[i].user_ready === 1)
              {
                  part_html+="<div id = \"personal-ready\">준비완료</div>";
              }
              part_html += "</div>";
              part2+="<div id = \"pay-person\">";
              part2+= table[i].user_name + " : " + table[i].user_pay + " 원";
              part2+="</div>";
          }
          all_html+=part_html;

          var part3 = "";
          for(var k = 0; k<uinfo.length; k++) {
                  part3 += "<div id = \"select-payer\"> <input type=\"radio\" name=\"payer_info\" value=\"menu\" id=\""+ uinfo[k].user_id + "\">";
                  part3 += uinfo[k].user_name + "</div>";
              }

          $("#contents-personal").html(all_html);
          $("#common-menu-select").html(part2);
          $("#modal-payer").html(part3);
      },
      statusCode:{
         409:function(msg){
            alert(msg.responseText);
         }
      }
   });
}
