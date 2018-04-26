$(document).ready(function(){
    $('.modal').modal();
    $('.datepicker').datepicker();
    $('select').formSelect();
    $('.carousel').carousel();
    $('input#input_text, textarea#textarea2').characterCounter();
});

var addButtons = document.getElementsByClassName('addbtn')

$(".addbtn").click(function(){
    $('.modal').modal('close');
});
