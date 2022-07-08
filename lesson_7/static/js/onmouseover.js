function changeBackgroundColorOver(day) {
    let cal_day = document.querySelector('#day-' + day);
    cal_day.style.backgroundColor = '#ffe0c269';
}

function changeBackgroundColorOut(day) {
    let cal_day = document.querySelector('#day-' + day);
    cal_day.style.backgroundColor = '#ebebeb';
}

function changeBackgroundColorOutToday(day) {
    let cal_day = document.querySelector('#day-' + day);
    cal_day.style.backgroundColor = '#8effdd';
}

function changeBackgroundColorOutMarked(day) {
    let cal_day = document.querySelector('#day-' + day);
    cal_day.style.backgroundColor = '#ffe0c269';
}

function changeBackgroundColorOutMarkedEvent(day) {
    let cal_day = document.querySelector('#day-' + day);
    cal_day.style.backgroundColor = '#ffa04169';
}
