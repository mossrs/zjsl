<template>
  <div>


    <el-row >

      <el-input v-model="q" placeholder="请输入内容" class="searchwidth" ></el-input><el-button icon="el-icon-search" @click="getAdmins"></el-button>
      <!-- 新增用户组-->
      <el-button class="row_right"  type="success" @click="addAdmin();">新增管理员</el-button>
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
        align="center"
        label="用户名">
      </el-table-column>
      <el-table-column
        property="phone"
        align="center"
        label="手机号">
      </el-table-column>
      <el-table-column
        property="email"
        align="center"
        label="邮箱">
      </el-table-column>

      <el-table-column
        label="操作"
        width="130"
        align="center">
        <template slot-scope="scope">
          <el-button circle icon="el-icon-edit-outline" type="primary" title="编辑" size="small"
            @click="rowEdit(scope.$index, scope.row)"></el-button>
          <el-button circle icon="el-icon-delete" type="danger" title="删除" size="small"
            @click="rowDel(scope.$index, scope.row, $event);"></el-button>
        </template>
      </el-table-column>
    </el-table>
    <br/><br/>
    <!--分页-->
    <el-pagination
      @current-change="handleCurrentPage"
      :page-sizes="[10, 20, 30, 40]"
      :current-page= 1
      :page-size= 10
      :total="totalRecords"
      layout="total, sizes, prev, pager, next, jumper">
    </el-pagination>

    <!--新增用户-弹出层-->
    <el-dialog
      title="编辑窗口"
      :visible.sync="isShowEditDialog"
      width="700px"
      @close="dialogClose()">
      <el-form
        ref="formFileds"
        :model="formFileds"
        label-width="100px"
        :rules="rules"
        >
        <el-input type="hidden" v-model="formFileds.id"></el-input>
        <el-form-item label="用户名" prop="username">
          <el-input v-model="formFileds.username"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input type="password" v-model="formFileds.password"></el-input>
        </el-form-item>`
        <el-form-item label="手机" prop="phone">
          <el-input v-model="formFileds.phone"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="formFileds.email"></el-input>
        </el-form-item>

        <el-form-item label="用户组" prop="groups">
          <el-transfer v-model="formFileds.groups" :data="groups_data"></el-transfer>
        </el-form-item>
        <el-form-item label="权限" prop="user_permissions">
          <el-transfer v-model="formFileds.user_permissions" :data="per_data"></el-transfer>
        </el-form-item>


        <el-form-item>
          <el-button type="primary" @click="handleFlag=='handleAdd'?handleAdd():handleEdit(formFileds.id)" class="pull-right margin-l-25">确定</el-button>
          <el-button @click="isShowEditDialog = false;" class="pull-right">取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
  import Bus from '../common/bus';

  export default {
    name: "usergroup",
    data() {

      return {
        host:'http://101.35.247.14:8000',
        token:localStorage.token,
        username:localStorage.username,
        userid:localStorage.user_id,


        q:'',
        totalRecords:0,
        pagesize:10,

        groups_data:[],
        per_data:[],
        formFileds: {
          id:'',
          username:'',
          password:'',
          phone:'',
          email:'',
          groups:[],
          user_permissions:[]

        },
        rules: {
          username: [
            {required: true, message: '用户名不能为空', trigger: 'blur, change'}
          ],
          password: [
            {required: true, message: '密码不能为空', trigger: 'blur, change'}
          ],
          phone: [
            {required: true, message: '手机号不能为空', trigger: 'blur, change'}
          ],
          groups: [
            {required: true, message: '用户组不能为空', trigger: 'blur, change'}
          ],
          user_permissions: [
            {required: true, message: '权限不能为空', trigger: 'blur, change'}
          ]

        },
        tableData: [],
        isShowEditDialog: false,
        options:[],
        handleFlag:'handleAdd'
      }
    },
    methods: {
      getCookie:function(name){
          var value = '; ' + document.cookie
          var parts = value.split('; ' + name + '=')
          if (parts.length === 2) return parts.pop().split(';').shift()
        },
      getAdmins(){
        this.$axios.get(this.host +'/admins/?search '+this.q+'&page=1&pagesize=10',{
          headers:{
            'Authorization': 'JWT ' + this.token
          }
        }).then(response=>{
          this.tableData = response.data.lists;
          this.totalRecords = response.data.count;

        });
      },
      getAdminsPage(page=1){
        this.$axios.get(this.host +'/admins/?search= &page='+page+'&pagesize=10',{
          headers:{
            'Authorization': 'JWT ' + this.token
          }
        }).then(response=>{
          this.tableData = response.data.lists;
          this.totalRecords = response.data.count;
        });
      },
      getGroups(){
        this.$axios.get(this.host +'/groups/',{
          headers:{
            'Authorization': 'JWT ' + this.token
          }
        }).then(response=>{
          for(let item of response.data){
            this.groups_data.push({key:item.id,label:item.name});
          }
        });
      },
      getPermissions(){
        this.$axios.get(this.host +'/permissions/',{
          headers:{
            'Authorization': 'JWT ' + this.token
          }
        }).then(response=>{
          for(let item of response.data){
            this.per_data.push({key:item.id,label:item.name});
          }
        });
      },

      addAdmin(){
        // 显示新增用户组表单
        this.isShowEditDialog = true;
      },
      handleAdd(){
        delete this.formFileds['id']
        this.$axios.post(this.host +'/admins/',this.formFileds,{
          headers:{
                  'Authorization': 'JWT ' + this.token,
                  'X-CSRFToken': this.getCookie('csrftoken')
                }
        }).then(response=>{
          if(response.data.id){
            this.isShowEditDialog = false;
            this.$message.success('提交成功');
            this.getAdmins();

          }else{
            this.$message.error('提交失败');
          }
        }).catch(error=>{
          console.log(error.response);
        });
      },
      rowEdit(index, row) {
        this.handleFlag = 'handleEdit';

        this.setCurRowChecked(row);

        // 给编辑弹出层赋值
        // ***这里需要注意的是：因为加了排序 所以tableData的顺序和实际显示的行顺序不一样
        for (let key in this.formFileds) {

          this.formFileds[key] = row[key];
        }
        // 显示表单
        this.isShowEditDialog = true;
      },
      handleEdit(id){
        this.$refs.formFileds.validate(isValid=>{
          if(isValid){
              this.$axios.put(this.host + '/admins/'+id+'/',this.formFileds,{
                headers:{
                  'Authorization': 'JWT ' + this.token,
                  'X-CSRFToken': this.getCookie('csrftoken')
                }
              }).then(response=>{
                if(response.data.id){
                  this.$message.success('提交成功');
                  this.isShowEditDialog = false;
                  this.getAdmins();
                }else{
                  this.$message.error('提交失败')
                }

              }).catch(error=>{
                console.log(error.response);
              });


          }else{
            this.$message.error('表单校验失败')
          }
        });

      },
      handleCurrentPage(val){
        // 翻页功能  val:当前页码
        this.getAdminsPage(`${val}`);

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
        }).then(() => {

          this.$axios.delete(this.host +'/admins/'+row.id+'/',{
            headers:{
                  'Authorization': 'JWT ' + this.token,
                  'X-CSRFToken': this.getCookie('csrftoken')
                }
          }).then(response=>{
            this.$message.success('删除成功')
            this.getAdmins();
          }).catch(error=>{
            this.$message.error('删除失败')
          });

        }).catch(error=>{
          // 取消删除操作
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
      this.getAdmins();
      this.getPermissions();
      this.getGroups();
    },
    created() {

      Bus.$on('collapse', isCollapse => {

        this.collapse = isCollapse;
      });
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
