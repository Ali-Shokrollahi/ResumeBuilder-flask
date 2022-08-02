$(document).ready(function () {
    $('.form2').submit(function (e) {
        var url = "/addExperience"; // send the form data here.
        $.ajax({
            type: "POST",
            url: url,
            data: $('.form2').serialize(), // serializes the form's elements.

        })

            .done(function (data) {
                markup = "<tr>" + "<td class='col-6 col-sm-2'>" + data.obj.title + "</td>" +
                    "<td class='col-6 col-sm-2'>" + data.obj.company + "</td>" +
                    "<td class='d-none d-sm-block col-sm-8'>" + data.obj.description.substring(0,50)+"..."+ "</td>" +

                    "</tr>"
                // "<td class=\"col-6 col-sm-2\"> data.obj.title </td>" +
                // "<td class=\"col-6 col-sm-2\"> data.obj.company </td>" +
                // "<td class=\"col-6 col-sm-2\"> data.obj.description </td>" +
                // "</tr>"

                tableBody = $(".content-box__table tbody")
                tableBody.append(markup)
                Swal.fire({

                    title: data.flash.text,
                    confirmButtonText:" متوجه شدم"

                })
            });
        e.preventDefault(); // block the traditional submission of the form.
    });

    // Inject our CSRF token into our AJAX request.
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", "{{ form2.csrf_token._value() }}")
            }
        }
    })
});