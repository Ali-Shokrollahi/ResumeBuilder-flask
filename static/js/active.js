$(function () {
    var CurrentUrl = document.URL;
    var CurrentUrlEnd = CurrentUrl.split('/').filter(Boolean).pop();

    $(".dashboard__item a").each(function () {
        var ThisUrl = $(this).attr('href');
        var ThisUrlEnd = ThisUrl.split('/').filter(Boolean).pop();
        if (ThisUrlEnd == CurrentUrlEnd)
            $(this).parent().addClass('active')
    });
});

function dis(elem) {

    if (elem.readOnly) {

        elem.readOnly = false
    } else {
        elem.readOnly = true
    }
}


function add_job(elem) {
    var adddiv = document.querySelector(".add-job")
    if ( elem.firstChild.className=="fa fa-plus"){
        adddiv.classList.add("d-block")
        elem.firstChild.className="fa fa-minus"
    }
    else {
        adddiv.classList.remove("d-block")
        elem.firstChild.className="fa fa-plus"
    }


}


function showpic(elem){

    $(elem).parent().find("#file").trigger("click")
}