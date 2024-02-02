//扩展静态方法,$ajax()
// $.extend()
// 扩展静态乘员方法, $('div').html()
// $.fn.extend()

// $.max = function () {
//     console.log('max');
// }
$.extend({
    max: function (a, b) {
        return a > b ? a : b;
    },
    min: function (a, b) {
        return a > b ? b : a;
    }
})

    ; (function ($) {
        $.fn.extend({
            func1: function () {
                console.log('func1');
            },
            func2: function () {
                console.log('func2');
            },
            //修改css样式
            changeStyle: function (options) {
                // console.log('this', this);
                $(this).css({ color: 'red' });
            }
        })
    })(jQuery);