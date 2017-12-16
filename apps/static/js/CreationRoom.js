var table;
var count = 1;

$(document).ready(function () {
    restaurant(1);
    $('[name = "selectButton"]').click(function()
    {
        document.getElementById('inputRname').value = $(this).attr('id');
    });
    $("#korean_food").click(function()
    {
        count = 1;
        restaurant(2);
        $('[name = "selectButton"]').click(function()
        {
            document.getElementById('inputRname').value = $(this).attr('id');
        });
    });
    $("#jokbo").click(function()
    {
        count = 2;
        restaurant(3);
        $('[name = "selectButton"]').click(function()
        {
            document.getElementById('inputRname').value = $(this).attr('id');
        });
    });
    $("#chinese_food").click(function()
    {
        count = 3;
        restaurant(4);
        $('[name = "selectButton"]').click(function()
        {
            document.getElementById('inputRname').value = $(this).attr('id');
        });
    });
    $("#night_food").click(function()
    {
        count = 4;
        restaurant(5);
        $('[name = "selectButton"]').click(function()
        {
            document.getElementById('inputRname').value = $(this).attr('id');
        });
    });
    $("#chicken").click(function()
    {
        count = 5;
        restaurant(6);
        $('[name = "selectButton"]').click(function()
        {
            document.getElementById('inputRname').value = $(this).attr('id');
        });
    });
    $("#flour_food").click(function()
    {
        count = 7;
        restaurant(7);
        $('[name = "selectButton"]').click(function()
        {
            document.getElementById('inputRname').value = $(this).attr('id');
        });
    });
    $("#andSoOn").click(function()
    {
        count = 8;
        restaurant(8);
        $('[name = "selectButton"]').click(function()
        {
            document.getElementById('inputRname').value = $(this).attr('id');
        });
    });
    $("#pizza").click(function()
    {
       count = 6;
       restaurant(6);
        $('[name = "selectButton"]').click(function()
        {
            document.getElementById('inputRname').value = $(this).attr('id');
        });
    });
});

function GoMain()
{
    location.href = "/";
}

function create_room()
{
    var title = $("#inputTitle").val();
    var password = $("#inputPassword").val();
    var rname = $("#inputRname").val();
    var number = $("#inputNumber").val();

    data = {'title':title, 'password':password, 'rname':rname, 'number':number};
    json_data = JSON.stringify(data);

    $.ajax
    ({
        type: 'PUT' ,
        headers:
            {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
        url: '/createroom',
        async: false,
        data: json_data,
        success: function(result){
            alert("새로운 방이 생성되었습니다");
            location.reload();
        },
        statusCode:{
            409:function(msg){
                alert(msg.responceText);
            },
            405:function(msg){
                alert(msg.responceText);
            },
            404:function(msg){
                alert(msg.responceText);
            }
        }
    });
}

function restaurant(num)
{
    $.ajax
   ({
      type: 'GET',
      headers:
      {
         'Accept': 'application/json',
         'Content-Type': 'application/json'
      },
      url: "/restaurant" + num,
      async: false,

      success: function(result){
          table=result.results;
          var i;
          var part_html="";
          all_html = "";
          for(i=0; i< table.length; i++ )
          {
              part_html+="<div id=\"restaurant-mold\">";
              part_html+="<div id=\"restaurant-title\"> <a href=\"#\" data-toggle=\"modal\" data-target=\"#" + table[i].phoneNumber + "\">" + table[i].title + "</a> </div>";
              part_html+="<div id=\"restaurant-info\"> <p>" + table[i].location + "</p>" + table[i].phoneNumber + "</div>";
              part_html+= "</div>";
              part_html+="<div class=\"modal\" id = \""+ table[i].phoneNumber +"\"> tabindex = \"-1\" role = \"dialog\">";
              part_html+="<div class = \"modal-content\" id = \"sizeOfModal\">";
              part_html+="<div class = \"modal-header\"><button type=\"button\" class=\"close\" data-dismiss=\"modal\">&times;</button><h4>" + table[i].title + " Menu</h4></div>";
              part_html+="<div class = \"modal-body\">";
              for (var j = 0; j < table[i].menulist.length; j++)
              {
                  part_html+="<p>"+table[i].menulist[j].food_name+ ":   " + table[i].menulist[j].food_price +"원<p>";
              }
              part_html+="</div>";
              part_html+="<div class=\"modal-footer\">";
              part_html+="<button type = \"button\" class = \"btn\" name = \"selectButton\" id = \"" + table[i].title + "\" data-dismiss=\"modal\"> 선택 </button>";
              part_html+=" <button type = \"button\" class=\"btn\" data-dismiss=\"modal\"> 나가기 </button></div></div></div>";
              part_html+="</div>";
          }
          all_html+=part_html;
          $("#restaurant-wrap").html(all_html);
      },
      statusCode:{
         409:function(msg){
            alert(msg.responseText);
         }
      }
   });
}