$(document).ready(function () {
    $('.form').submit(function (e) {
        var url = "/dashboard/education"; // send the form data here.
        $.ajax({
            type: "POST",
            url: url,
            data: $('.form').serialize(), // serializes the form's elements.

        })

            .done(function (data) {
                Swal.fire({

                    title: data.flash.text,
                    confirmButtonText: '<a href="/dashboard/education" style="color: white">متوجه شدم</a>'

                })
            });
        e.preventDefault(); // block the traditional submission of the form.
    });

    // Inject our CSRF token into our AJAX request.
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", "{{ form.csrf_token._value() }}")
            }
        }
    })
});