console.log('hello from static/js/home.js');

$('#testURL').submit(function(e) {
                    e.preventDefault();
                    var data = {};
                    var Form = this;
                    $.each(this.elements, function(i, v) {
                        var input = $(v);
                        data[input.attr("name")] = input.val();
                        console.log(data)
                        delete data["undefined"];
                    });
                    $.ajax({
                        type: 'POST',
                        url: '/indexpage',
                        dataType: 'json',
                        contentType: 'application/json; charset=utf-8',
                        data: JSON.stringify(data),
                        context: Form,
                        beforeSend: function(){
                        // Show image container
                        $("#loader").show();
                        $("#btnSubmit").attr("disabled", true);
                        },
                        success: function(callback) {
                            alert(callback.message);
                        },
                        error: function(callback) {
                            alert(callback.responseJSON.message);
                        },
                        complete:function(data){
                        // Hide image container
                        $("#loader").hide();
                        $("#btnSubmit").attr("disabled", false);
                        $('#inputID').val('');
                        window.location.reload();
                        }
                    });

                });

$(document).ready(function() {
    $.ajax({
        url: "/indexpage",
        dataType: 'json',
        method: 'GET',
        contentType: 'application/json; charset=utf-8',
        success: function(data){
            console.log(data.tasks)
            var htmlText = data.tasks.map(function(o){
                return `
                <div class="card">
                <h5> Base address(URL)  : <a href="${o[0]}">${o[0]}</a> </h5>
                <h5> Extraction Details    : ${o[1]}</h5>
                <h5> Last updated on    : ${o[2]}</h5>
                <h5> No of records found : ${o[3]}</h5>
                `;
                });
            $('#body').append(htmlText);

            var htmlTextURL = data.testtasks.map(function(t){
                return `
                <div class="card">
                <h5> Test URL  : <a href="${t[0]}">${t[0]}</a> </h5>
                <h5> No of Proxies Responded    : ${t[1]}</h5>
                <h5> Test date   : ${t[2]}</h5>
                `;
                });
            $('#bodytest').append(htmlTextURL);

            },
        error: function(d){
            alert("404 !");
            }
    });
});