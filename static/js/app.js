var titel_counter = 0;
var des_counter = 0;
var Titletxt = "رزومه باز";
var Destxt = "رزومه آنلاین خود را در 10 دقیقه بسازید";
var title = document.querySelector(".header__title");
var des = document.querySelector(".header__description");

function typeHeaderTitle() {

    var text = title.innerHTML;
    title.innerHTML = text + Titletxt[titel_counter];
    titel_counter++;
    var time = setTimeout(typeHeaderTitle, 100);
    if (titel_counter >= Titletxt.length) {
        clearTimeout(time)
    }
}

function typeHeaderDes() {

    var text = des.innerHTML;
    des.innerHTML = text + Destxt[des_counter];
    des_counter++;
    var time = setTimeout(typeHeaderDes, 80);
    if (des_counter >= Destxt.length) {
        clearTimeout(time)
    }
}

window.addEventListener('load', typeHeaderTitle());
window.addEventListener('load', typeHeaderDes());

let icon = document.querySelector(".menu__icon");
let menu = document.querySelector(".nav__list");

icon.addEventListener("click", function () {
    if (icon.classList.contains("fa-bars")) {
        menu.style.left = 0;
        icon.classList = "fa fa-times menu__icon";
    } else {
        menu.style.left = "-250px";
        icon.classList = "fa fa-bars menu__icon";
    }
})


function showpass(elem) {
    var input = $(elem).parent().find("input");
    if (input.attr("type") == "password") {
        elem.innerHTML = '<i class="fa fa-eye c-blue"></i>'
        input.attr("type", "text")
    } else if (input.attr("type") == "text") {
        elem.innerHTML = '<i class="fa fa-eye-slash c-blue"></i>'
        input.attr("type", "password")
    }


}