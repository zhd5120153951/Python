// 处理函数--原始的
function bindEmailCaptchaClick() {
    $("#captcha-btn").click(function (event) {
        // this: 代表当前按钮的 jQuery 对象
        var $this = $(this);
        // 阻止默认的事件
        event.preventDefault();

        var email = $("input[name='email']").val();
        $.ajax({
            url: "/auth/captcha/email?email=" + email,
            method: "GET",
            success: function (result) {
                var code = result['code'];
                if (code == 200) {
                    var countdown = 60;
                    // 开始倒计时之前，取消按钮的点击事件
                    $this.off("click");
                    var timer = setInterval(function () {
                        $this.text(countdown);
                        countdown -= 1;
                        // 倒计时结束时执行
                        if (countdown <= 0) {
                            // 清除定时器
                            clearInterval(timer);
                            // 按钮文本恢复原样
                            $this.text("获取验证码");
                            // 重新绑定点击事件
                            bindEmailCaptchaClick();
                        }
                    }, 1000);
                    $("#success-message").text("邮箱验证码发送成功!").show();
                    setTimeout(function () {
                        $("#success-message").hide(); // 3秒后隐藏消息
                    }, 3000);
                } else {
                    alert(result['message']);
                }
            },
            error: function (error) {
                console.log(error);
            }
        });
    });
}
//处理函数自己重写的
function bindEmailCaptchaClick_myself() {
    // bindEmailCaptchaClick();
    $("#captcha-btn").click(function (event) {
        //代表当前按钮的jQuery对象
        var $this = $(this);
        //阻止默认的事件发生,获取验证码--注册按钮都可以触发,但是只允许注册触发
        //前端获取数据
        event.preventDefault();

        var email = $("input[name='email']").val();//获取input标签输入的QQ邮箱
        // alert(email);
        //传导后端处理
        $.ajax({
            // 前缀可不写:http://127.0.0.1:5000
            url: "captcha/email?email=" + email,
            method: "GET",
            success: function (result) {
                // console.log(result);
                var code = result['code'];
                if (code == 200) {
                    var countdown = 10;
                    $this.off("click");//没到60秒,不可以再次点击获取验证码
                    var timer = setInterval(function () {
                        $this.text(countdown);
                        countdown -= 1;
                        if (countdown <= 0) {
                            clearInterval(timer);//清除定时器
                            $this.text("获取验证码");//60秒到了,重置文字
                            bindEmailCaptchaClick_myself();//重新绑定点击事件
                        }
                    }, 1000);
                }
            },
            fail: function (error) {
                console.log(error);
            }

        })
    })
}


// 整个网页加载完成后再执行---有些js在HTML前面,而触发事件的按钮在后面--此时就加载完再触发
$(function () {
    bindEmailCaptchaClick_myself();
});
