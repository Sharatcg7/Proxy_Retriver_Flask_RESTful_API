console.log('hello from static/js/proxylist.js');

$(window).on("load resize ", function() {
  var scrollWidth = $('.tbl-content').width() - $('.tbl-content table').width();
  $('.tbl-header').css({'padding-right':scrollWidth});
}).resize();

$(document).ready(function() {
    $.ajax({
        url: "/proxiestest",
        dataType: 'json',
        method: 'GET',
        success: function(data){
            var dataTable = $("#viewTable").DataTable();
            dataTable.clear().draw();
            $.each(data.tasks, function(index, value){
                dataTable.row.add([value[0],value[1],value[2], value[3], value[4], value[5] ]).draw();
            });
            },
        error: function(callback){
            alert(callback);
            }
    });
});

var modal = document.getElementById('id01');
$('#addproxytoDB').submit(function(e) {
                    e.preventDefault();
                    console.log('inside addproxytoDB block')
                    var data = {};
                    var Form = this;
                    $.each(this.elements, function(i, v) {
                        var input = $(v);
                        data[input.attr("name")] = input.val();
                        delete data["undefined"];
                    });
                    console.log(data)
                    $.ajax({
                        type: 'POST',
                        url: '/proxiestest',
                        dataType: 'json',
                        contentType: 'application/json; charset=utf-8',
                        data: JSON.stringify(data),
                        context: Form,
                        beforeSend: function(){
                        // Show image container
                        $("#btnSubmit").attr("disabled", true);
                        },
                        success: function(callback) {
                            alert(callback.message);
                        },
                        error: function(callback) {
                            alert(callback.message);
                        },
                        complete:function(data){
                        // Hide image container
                        $("#btnSubmit").attr("disabled", false);
                        $('#inputID1').val('');
                        $('#inputID2').val('');
                        modal.style.display = "none";
                        window.location.reload();
                        }
                    });
        });

var modal1 = document.getElementById('id02');
$('#updateproxytoDB').submit(function(e) {
                    e.preventDefault();
                    console.log('inside updateproxytoDB block')
                    var data = {};
                    var Form = this;
                    $.each(this.elements, function(i, v) {
                        var input = $(v);
                        data[input.attr("name")] = input.val();
                        delete data["undefined"];
                    });
                    console.log(data)
                    $.ajax({
                        type: 'PUT',
                        url: '/proxiestest',
                        dataType: 'json',
                        contentType: 'application/json; charset=utf-8',
                        data: JSON.stringify(data),
                        context: Form,
                        beforeSend: function(){
                        $("#updatebtnSubmit").attr("disabled", true);
                        },
                        success: function(callback) {
                            console.log(callback)
                            alert(callback.message);
                        },
                        error: function(callback) {
                            alert(callback.responseJSON.message);
                        },
                        complete:function(data){
                        $("#updatebtnSubmit").attr("disabled", false);
                        $('#inputID1').val('');
                        $('#inputID2').val('');
                        $('#inputID3').val('');
                        modal1.style.display = "none";
                        window.location.reload();
                        }
                    });
        });


function deleteFunction() {
   if (confirm("Are You Sure To Delete List?") == true) {
        /*logical to delete query*/
         var id = 1
         console.log(id)
         $.ajax({
                  type: 'DELETE',
                  url: '/proxiestest',
                  data: JSON.stringify(id),
                  beforeSend: function(){
                      // Show image container
                      $("#btnSubmit").attr("disabled", true);
                   },
                   success: function(callback) {
                       alert("Deleted Successfully");
                       window.location.reload();
                   },
                   error: function() {
                        alert("error code 404!");
                   }
            });
    } else {
        return false;
    }
}