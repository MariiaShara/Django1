'use strict';

window.onload = function() {
    $('.shopping_bag').on('change', 'input[type="number"]', function (event) {
        console.log(event.target);
        $.ajax({
            url: '/cart/change/' + event.target.name + '/quantity/' + event.target.value + '/',
            success: function (data) {
                console.log(data);
                $('.shopping_bag').html(data.result);
            }
        });
    })
}

