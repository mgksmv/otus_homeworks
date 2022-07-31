function ajaxCall(navigation) {
    let date = $(`#${navigation}-month`).val()
    $.ajax({
        type: 'GET',
        url: `/courses/schedule-calendar-nav/?${date}`,
        beforeSend: function () {
            $('#calendar').hide()
            $('.ajax-loader').show()
        },
        success: function (response) {
            $('#calendar').show().html(response.data)
            $('#prev-month').val(response.prev_month)
            $('#next-month').val(response.next_month)
            $('.ajax-loader').hide()
        },
    });
    return false
}

$(document).ready(function () {
    $('#prev-month').on('click', function () {
        ajaxCall('prev')
    })
    $('#next-month').on('click', function () {
        ajaxCall('next')
    })
    $('#current-month').on('click', function () {
        ajaxCall('current')
    })
})
