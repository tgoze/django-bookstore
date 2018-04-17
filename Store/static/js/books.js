$(document).ready(function(){
    $('.modal').modal();
    $('.datepicker').datepicker();
    $('select').formSelect();
    $('.materialboxed').materialbox();
});

var addButtons = document.getElementsByClassName('addbtn')

$(".addbtn").click(function(){
    $('.modal').modal('close');
});
