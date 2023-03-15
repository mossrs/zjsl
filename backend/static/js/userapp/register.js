let vue = new Vue({
   el:'#register',
   delimiters: ['${','}'],
   data:{
       // v-model
        username:'',
        password:'',
        smscode:'',
        imgcode:'',
        phone:'',

        // v-show
        error_username:false,
        error_password:false,
        error_phone:false,
        error_smscode:false,
        error_imgcode:false,

        // v-message
        error_username_msg:'请输入长度5-8的字符！',
        error_password_msg:'请输入长度3-8的字符！',
        error_phone_msg:'手机号输入有误！',
        error_smscode_msg:'验证码输入有误！',
        error_imgcode_msg:'验证码错误！',


       //图片验证码相关变量
       imgcode_url:'',
       uuid:'',

       //短信验证码相关变量
       smscode_btn:'获取短信验证码',
       send_flag:false,

       // 响应
       errormsg :''

   },mounted(){
       this.generate_imgcode();
    },
    methods:{
       send_smscode:function(){
           //发送短信验证码

           //1.判断短信验证码是否正在发送
           if(this.send_flag){
               return;
           }

           //2.修改发送状态
           this.send_flag = true;

           //3.校验用户输入的手机号和图片验证码
           this.check_phone();
           this.check_imgcode();
           if(this.error_phone||this.error_imgcode){
               this.send_flag = false;
               return;
           }

           //4.发送短信验证码
           var url = '/smscodes/'+this.phone+'/?imgcode='+this.imgcode+'&uuid='+this.uuid;
           axios.get(url,{
               responseType:'json'
           }).then(response=>{
               if(response.data.code=='200'){
                   let num = 60;
                   var i = setInterval(()=>{
                       if(num==1){
                           clearInterval(i);
                           this.smscode_btn = '获取短信验证码';
                           this.send_flag = false;
                       }else{
                           num -= 1;
                           this.smscode_btn = '倒计时：'+ num + '秒';
                       }
                   },1000,60)
               }else{// 4001 表示缺少必传参数
                   if(  response.data.data == '4001' || response.data.data == '4002' ||
                        response.data.data == '4003' || response.data.code == '4004' ||
                        response.data.code == '5001'){
                       this.error_smscode_msg = response.data.errormsg;
                       this.error_smscode = true;
                       // 4002 图片验证码已经过期
                   }

                   //重新生成图片验证码
                   this.generate_imgcode();
                   //重置发送状态
                   this.send_flag = false;
               }
           }).catch(error=>{
               console.log(error.response);
           });

       },
       check_smscode:function(){
           //短信验证码格式校验
           let reg = /^\d{6}$/;
           if(!reg.test(this.smscode)){
               this.error_smscode = true;
           }else{
               this.error_smscode = false;
           }
           // 短信验证码有效性校验
           if (!this.error_smscode){
               axios.get('/check_smscode/' + this.phone + '/?smscode=' + this.smscode,{
                   responseType: 'json'
               }).then(response=>{
                   let code = response.data.code;
                   if (code != 200){
                       this.error_smscode_msg = response.data.errormsg
                       this.error_smscode = true;
                   }else{
                       this.error_smscode = false;
                   }
               })
           }

       },

       check_imgcode:function(){

           //非空校验（用户输入的图片验证码值不能为空）
           if(!this.imgcode){
               this.error_imgcode_msg = '图片验证码不能为空！'
               this.error_imgcode = true;
           }else{
               this.error_imgcode = false;
           }
       },
       // 图片验证码展示功能
       generate_imgcode:function(){
           // 生成uuid
           this.uuid = generateUUID();
           // 生成请求地址
           this.imgcode_url = '/imgcodes/'+this.uuid;
       },
       // 校验用户名(只能输入5-8位字符)
        check_uname:function(){
            //1.格式校验
            let reg = /^[A-Za-z][A-Za-z0-9_]{4,7}$/;
            if(!reg.test(this.username)){
                this.error_username = true;
            }else{
                this.error_username = false;
            }

            //2.用户名是否重复注册校验
            if(!this.error_username){
                axios.get('/usernames/'+this.username+'/count/',{
                    responseType:'json'
                }).then(response=>{
                    if(response.data.count==1){
                        this.error_username_msg = '当前用户名已经注册';
                        this.error_username = true;
                    }else{
                        this.error_username = false;
                    }
                }).catch(error=>{
                    console.log(error.response);
                });
            }
        },
        // 校验密码
        check_pwd:function(){
            let reg = /^[A-Za-z0-9_]{3,8}$/;
            if(!reg.test(this.password)){
                this.error_password = true;
            }else{
                this.error_password = false;
            }
        },
        // 校验手机号
        check_phone:function(){
            // 1.格式校验
            let reg = /^1[35789]\d{9}$/;
            if(!reg.test(this.phone)){
                this.error_phone = true;
            }else{
                this.error_phone = false;
            }

            // 2.手机号是否重复注册校验
            if(!this.error_phone){
                axios.get('/phones/'+this.phone+'/count/',{
                    responseType:'json'
                }).then(response=>{
                    if(response.data.count==1){
                        this.error_phone_msg = '手机号已经被注册';
                        this.error_phone = true;
                    }else{
                        this.error_phone = false;
                    }
                }).catch(error=>{
                    console.log(error.response);
                });
            }
        },
        // 监听表单提交事件
        reg_sub:function(){
            this.check_uname();
            this.check_phone();
            this.check_pwd();

            if(this.error_username||this.error_phone||this.error_password){
                //阻止表单提交
                window.event.returnValue = false;
            }
        }

    }
});
