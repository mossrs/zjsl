let vue = new Vue({
    el:'#login',
    delimiters:['${','}'],
    data:{
        // v-model
        username:'',
        password:'',


        // v-message
        error_username_msg:'用户名输入有误！',
        error_password_msg:'密码输入有误！',

        // v-show
        error_username:false,
        error_password:false,

        // qq相关变量
        qq_url:'',

    },
    mounted(){
      // 页面元素加载完成后自动调用执行当前函数
        this.get_qq_url();
    },
    methods:{
        get_qq_url:function () {
            //获取QQ扫码登录链接地址
            axios.get('/qq/login/',{
                responseType:'json'
            }).then(response=>{
                if(response.data.code=='200'){
                    this.qq_url = response.data.login_url;
                }
            }).catch(error=>{
                console.log(error.response);
            });
        }
    }
});

