$(document).ready(function(){
    $('.modal').modal();
    $('.datepicker').datepicker();
    $('select').formSelect();
    $('.carousel').carousel();
});

var addButtons = document.getElementsByClassName('addbtn')

$(".addbtn").click(function(){
    $('.modal').modal('close');
});
