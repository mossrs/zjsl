<template>
  <div>


    <el-row >

      <!-- 搜索用户信息-->
      <el-input v-model="q" placeholder="请输入内容" class="searchwidth"></el-input><el-button icon="el-icon-search" @click="getUsers();"></el-button>
      <!-- 新增用户信息-->
      <el-button class="row_right"  type="success" @click="addUser();">新增用户</el-button>
    </el-row>
    <br/>

    <!--表格内容-->
    <el-table
      ref="list"
      :data="tableData"
      style="width: 100%"
      border
      stripe
      highlight-current-row
      :default-sort="{prop: 'id', order: 'descending'}"
      @row-click="handleRowClick"
      @select-all="handleCheckedAllAndCheckedNone"
      @select="handleCheckedAllAndCheckedNone">
      <el-table-column
        type="selection"
        width="45"
        align="center">
      </el-table-column>
      <el-table-column
        property="id"
        label="序号"
        width="50">
      </el-table-column>

      <el-table-column
        property="username"
        label="用户名"
        width="180">
      </el-table-column>
      <el-table-column
        property="phone"
        label="手机号">
      </el-table-column>
      <el-table-column
        property="email"
        label="邮箱">
      </el-table-column>
      <el-table-column
        label="操作"
        width="130"
        align="center">
        <template slot-scope="scope">

          <el-button circle icon="el-icon-delete" type="danger" title="删除" size="small"
            @click="rowDel(scope.$index, scope.row, $event);"></el-button>
        </template>
      </el-table-column>
    </el-table>
    <br/><br/>
    <!--分页-->
    <el-pagination
      @current-change="handleCurrentPage"
      :page-sizes="[5, 10, 15, 20]"
      :current-page= 1
      :page-size= 5
      :total="totalRecords"
      layout="total, sizes, prev, pager, next, jumper">
    </el-pagination>

    <!--新增用户-弹出层-->
    <el-dialog
      title="新增"
      :visible.sync="isShowEditDialog"
      width="430px"
      @close="dialogClose()">
      <el-form
        ref="formFileds"
        :model="formFileds"
        label-width="80px"
        :rules="rules"
        >

        <el-form-item label="用户名" prop="username">
          <el-input v-model="formFileds.username"></el-input>
        </el-form-item>
        <el-form-item  label="密码" prop="password">
          <el-input type="password" v-model="formFileds.password"></el-input>
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="formFileds.phone" ></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="formFileds.email"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleAdd();"  class="pull-right margin-l-25">确定</el-button>
          <el-button @click="isShowEditDialog = false;" class="pull-right">取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
  export default {
    name: "UserMan",
    data() {

      return {
        host:'http://101.35.247.14:8000',
        token:localStorage.token,
        username:localStorage.username,
        userid:localStorage.user_id,


        q:'',
        totalRecords:0,

        formFileds: {
          username: '',
          phone: '',
          email: '',
          password:''

        },
        rules: {
          username: [
            {required: true, message: '用户名不能为空', trigger: 'blur, change'}
          ],
          phone: [
            {required: true, message: '手机号不能为空', trigger: 'blur, change'}
          ],
          password: [
            {required: true, message: '密码不能为空', trigger: 'blur, change'}
          ]
        },
        tableData: [],
        isShowEditDialog: false
      }
    },
    methods: {
      getCookie:function(name){
          var value = '; ' + document.cookie
          var parts = value.split('; ' + name + '=')
          if (parts.length === 2) return parts.pop().split(';').shift()
        },
      getUsers(){
        this.$axios.get(this.host +'/users/?search= '+ this.q + '&page=1&pagesize=5',{
          headers:{
            'Authorization': 'JWT ' + this.token
          }
        }).then(response=>{
          this.tableData = response.data.lists;
          this.totalRecords = response.data.count;
        }).catch(error=>{
          console.log(error.response);
        });
      },
      getUsersPage(page=1){
        this.$axios.get(this.host +'/users/?search= &page='+page+'&pagesize=5',{
          headers:{
            'Authorization': 'JWT ' + this.token
          }
        }).then(response=>{
          this.tableData = response.data.lists;
          this.totalRecords = response.data.count;
        }).catch(error=>{
          console.log(error.response);
        });
      },
      addUser(){
        // 显示新增用户表单
        this.isShowEditDialog = true;
      },
      handleAdd(){
        // 提交新增用户表单信息

        // 1. 表单校验
        this.$refs.formFileds.validate(isvalid=>{
          // 2. 校验成功
          if(isvalid){
            this.$axios.post(this.host +'/users/',this.formFileds,{
              headers:{
                'Authorization': 'JWT ' + this.token,
                'X-CSRFToken': this.getCookie('csrftoken')
              }
            }).then(response=>{
              if(response.data.id){
                 // 关闭对话框
                 this.isShowEditDialog = false;
                 // 提示信息
                 this.$message.success('提交成功')
              }else{
                this.$message.error('提交失败')
              }
              // 刷新用户列表
              this.getUsers();
            }).catch(error=>{
              console.log(error.response);
            })
          }else{// 3. 校验失败
            this.$message.error('表单校验失败')
          }

        })
      },
      handleCurrentPage(val){
        // 翻页功能  val:当前页码
        this.getUsersPage(`${val}`);

      },
      handleRowClick(row, event, column) {

        // 仅选中当前行
        this.setCurRowChecked(row);
      },
      handleCheckedAllAndCheckedNone(selection) {

        // 当前选中仅一行时操作-（当前表格行高亮）
        1 != selection.length && this.$refs.list.setCurrentRow();
      },
      dialogClose() {

        // 清空编辑表单
        this.$refs.formFileds.resetFields();

      },
      rowDel(index, row, event) {

        // 让当前删除按钮失焦
        event.target.blur();
        this.$confirm('确定要删除当前行吗？', '删除', {
          comfirmButtonText: '确定',
          cancelButtonText: '取消'
        }).then((response) => {
            this.$axios.delete(this.host + '/users/'+row.id+'/',{
              headers:{
                'Authorization': 'JWT ' + this.token,
                'X-CSRFToken': this.getCookie('csrftoken')
              }
            }).then(response=>{
              this.$message.success('删除成功');
              this.getUsers();
            })

          }).catch(error=>{
            console.log(error);
        });
      },
      // 选中当前行-当前行的复选框被勾选
      setCurRowChecked(row) {

        this.$refs.list.clearSelection();
        this.$refs.list.toggleRowSelection(row);
      }
    },
    mounted(){
      this.getUsers();
    }
  }
</script>

<style scoped lang="less">
.row_right{
  position:relative;
  left:5px;
  button:3px;
}


.el-form {
  padding: 0 10px;
}
.el-date-editor {
  width: 100% !important;
}

.searchwidth{
  width:1270px;
}
</style>
