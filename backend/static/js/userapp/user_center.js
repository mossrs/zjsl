let vue = new Vue({
    el:'#user_center',
    delimiters:['${','}'],
    data:{
        // v-model
        email:'',
        // 当前登录用户的id
        userid:userid,

        error_email:false,
        error_email_msg:'保存邮箱失败！',

    },
    methods:{
        save_email:function () {
            //给当前登录用户绑定邮箱
            axios.post('/emails/',{
                'email':this.email,
                'userid':this.userid
            },{
                headers:
                    {
                       'X-CSRFToken': getCookie('csrftoken')
                    }//解决axios.post跨域访问
            }).then(response=>{
                if(response.data.code == '200'){
                    //刷新页面
                    location.reload();
                    this.error_email = false;
                }else{
                    this.error_email = true;
                    this.error_email_msg = response.data.errormsg;
                }
            }).catch(error=>{
                console.log(error.response);
            })
        }
    }
});

