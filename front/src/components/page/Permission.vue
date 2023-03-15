<template>
  <div>


    <el-row >

      <!-- 搜索权限信息-->
      <el-input v-model="q" placeholder="请输入内容" class="searchwidth" ></el-input><el-button icon="el-icon-search" @click="getPermissions"></el-button>
      <!-- 新增权限-->
      <el-button class="row_right"  type="success" @click="addPermission();">新增权限</el-button>
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
        property="name"
        label="权限名称">
      </el-table-column>
      <el-table-column
        property="codename"
        label="权限识别名">
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
      :page-size= 10
      :total="totalRecords"
      :current-page= 1
      layout="total, sizes, prev, pager, next, jumper">
    </el-pagination>

    <!--新增用户-弹出层-->
    <el-dialog
      title="编辑窗口"
      :visible.sync="isShowEditDialog"
      width="500px"
      @close="dialogClose()">
      <el-form
        ref="formFileds"
        :model="formFileds"
        label-width="100px"
        :rules="rules"
        >
        <el-input type="hidden" v-model="formFileds.id"></el-input>
        <el-form-item label="权限名称" prop="name">
          <el-input v-model="formFileds.name"></el-input>
        </el-form-item>
        <el-form-item label="权限识别名" prop="codename">
          <el-input v-model="formFileds.codename"></el-input>
        </el-form-item>
        <el-form-item label="权限类型" prop="content_type">
          <el-select v-model="formFileds.content_type" placeholder="请选择">
          <el-option
            v-for="item in options"
            :key="item.id"
            :label="item.name"
            :value="item.id">
          </el-option>
        </el-select>
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
    name: "permission",
    data() {

      return {
        host:'http://101.35.247.14:8000',
        token:localStorage.token,
        username:localStorage.username,
        userid:localStorage.user_id,

        q: '',
        search:'',
        totalRecords:0,
        pagesize:10,

        formFileds: {
          id:'',
          name:'',
          codename:'',
          content_type:''

        },
        rules: {
          name: [
            {required: true, message: '用户名不能为空', trigger: 'blur, change'}
          ],
          codename: [
            {required: true, message: '手机号不能为空', trigger: 'blur, change'}
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
      getPermissions(){
        this.$axios.get(this.host + '/permissions/?search= '+this.q+'&page=1&pagesize=10',{
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
      getPermissionsPage(page=1){
        this.$axios.get(this.host + '/permissions/?search= &page='+page+'&pagesize=10',{
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

      getContentType(){
        this.$axios.get(this.host + '/permissions/content_types/',{
          headers:{
            'Authorization': 'JWT ' + this.token
          }
        }).then(response=>{
          this.options = response.data;

        }).catch(error=>{
          console.log(error.response);
        });
      },
      addPermission(){
        this.isShowEditDialog = true;
      },
      handleAdd(){
        delete this.formFileds['id']  // 删除id 因为新增中自动添加

        this.$refs.formFileds.validate(isValid=>{
          if(isValid){
              this.$axios.post(this.host + '/permissions/',this.formFileds,{
                headers:{
                  'Authorization': 'JWT ' + this.token,
                  'X-CSRFToken': this.getCookie('csrftoken')
                }
              }).then(response=>{
                if(response.data.id){
                  this.$message.success('提交成功');
                  this.isShowEditDialog = false;
                  this.getPermissions();
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
              this.$axios.put(this.host + '/permissions/'+id+'/',this.formFileds,{
                headers:{
                  'Authorization': 'JWT ' + this.token,
                  'X-CSRFToken': this.getCookie('csrftoken')
                }
              }).then(response=>{
                if(response.data.id){
                  this.$message.success('提交成功');
                  this.isShowEditDialog = false;
                  this.getPermissions();
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
        this.getPermissionsPage(`${val}`);
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
          this.$axios.delete(this.host + '/permissions/'+row.id+'/',{
                headers:{
                  'Authorization': 'JWT ' + this.token,
                  'X-CSRFToken': this.getCookie('csrftoken')
                }
              }).then(response=>{
                  this.$message.success('删除成功');
                  this.getPermissions();

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
      this.getPermissions();
      this.getContentType();
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
