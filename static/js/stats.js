document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('count-1-percentage').style.width = count_1_percentage + "%"
    document.getElementById('count-2-percentage').style.width = count_2_percentage + "%"
    document.getElementById('count-3-percentage').style.width = count_3_percentage + "%"
    document.getElementById('count-4-percentage').style.width = count_4_percentage + "%"
    document.getElementById('count-5-percentage').style.width = count_5_percentage + "%"
    document.getElementById('count-6-percentage').style.width = count_6_percentage + "%"
    document.getElementById('fail-count-percentage').style.width = fail_count_percentage + "%"
});


let total_count = document.getElementById('count-total').innerHTML
let count_1_percentage = document.getElementById('count-1').innerHTML / total_count * 100
let count_2_percentage = document.getElementById('count-2').innerHTML / total_count * 100
let count_3_percentage = document.getElementById('count-3').innerHTML / total_count * 100
let count_4_percentage = document.getElementById('count-4').innerHTML / total_count * 100
let count_5_percentage = document.getElementById('count-5').innerHTML / total_count * 100
let count_6_percentage = document.getElementById('count-6').innerHTML / total_count * 100
let fail_count_percentage = document.getElementById('count-fails').innerHTML / total_count * 100