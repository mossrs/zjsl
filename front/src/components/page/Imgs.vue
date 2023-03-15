<template>
  <div>

    <el-row >
      <!-- 搜索图片信息-->
      <el-input v-model="q" placeholder="请输入内容" class="searchwidth" ></el-input><el-button icon="el-icon-search" @click="getArticleImgs"></el-button>
      <!-- 新增图片信息-->
      <el-button class="row_right"  type="success" @click="addArticleImg();">新增首页图片</el-button>
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
        width="100"
        align="center">
      </el-table-column>
      <el-table-column
        property="id"
        label="序号"
        width="200">
      </el-table-column>

      <el-table-column
        property="article"
        label="诗路编号"
        width="200">
      </el-table-column>

      <el-table-column
        property="image"
        align="center"
        width="512.5"
        height="200"
        label="图片">
        <template slot-scope="scope" >

            <el-image
              ref="imgH"
              style="width: 300px;height:200px;"
              :src="scope.row.image"
              fit="contain">
            </el-image>

        </template>

      </el-table-column>

      <el-table-column
        label="操作"
        width="450"
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
      @current-change="handleCurrentChange"
      :current-page="currentPage"
      :page-sizes="[10, 20, 30, 40]"
      :page-size="pagesize"
      :total="totalRecords"
      layout="total, sizes, prev, pager, next, jumper">
    </el-pagination>

    <!--发布文章-弹出层-->
    <el-dialog
      title="编辑窗口"
      :visible.sync="isShowEditDialog"
      width="1000px"
      @close="dialogClose()">
      <el-form
        ref="formFileds"
        :model="formFileds"
        label-width="80px"
        :rules="rules"
        >

        <el-input type="hidden" v-model="formFileds.id"></el-input>

        <el-form-item label="诗路编号" prop="article">
          <el-select v-model="formFileds.article" placeholder="请选择">
          <el-option
            v-for="item in options"
            :key="item.id"
            :label="item.title"
            :value="item.id">
          </el-option>
        </el-select>
        </el-form-item>
        <el-form-item  label="诗路图片" prop="image">
          <template>
            <el-upload
            ref="uploadRef"
            class="upload-demo"
            action="1"
            :http-request="httprequest"
            accept=".png,.jpeg,.jpg"
            :before-upload="beforeUploadHandle">
            <el-button size="small" type="primary">点击上传</el-button>
            <div slot="tip" class="el-upload__tip">只能上传jpg/png文件</div>
          </el-upload>

          </template>
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
  // object-fit
  import objectFitImages from 'object-fit-images'


  export default {
    name: "Imgs",
    data() {

      return {
        host:'http://101.35.247.14:8000',
        token:localStorage.token,
        username:localStorage.username,
        userid:localStorage.user_id,


        currentPage:1,
        totalRecords:0,
        pagesize:10,

        fileList:[],
        uploadUrl:'http://127.0.0.1/article_imgs/',
        multipleFlag:false,

        formFileds: {
          id:'',
          article: '',
          image:''
        },
        fd:'',//向服务器进行传递的参数（带有图片formdata）
        options:[],
        q: '',
        rules: {
          article: [
            {required: true, message: '标题不能为空', trigger: 'blur, change'}
          ]

        },
        tableData: [],
        isShowEditDialog: false,
        handleFlag:'handleAdd',
        param:'',
        timer:''
      }
    },
    methods: {
      getCookie:function(name){
          var value = '; ' + document.cookie
          var parts = value.split('; ' + name + '=')
          if (parts.length === 2) return parts.pop().split(';').shift()
      },
      getArticleImgs(){
        this.$axios.get(this.host +'/article_imgs/?search= '+ this.q +'&page=1&pagesize=10',{
          headers:{
            'Authorization': 'JWT ' + this.token
          }
        }).then(response=>{
          this.tableData = response.data.lists;
          this.totalRecords = response.data.count;
        });
      },
      getArticleImgsPage(page=1){
        this.$axios.get(this.host +'/article_imgs/?search= &page='+page+'&pagesize=10',{
          headers:{
            'Authorization': 'JWT ' + this.token
          }
        }).then(response=>{
          this.tableData = response.data.lists;
          this.totalRecords = response.data.count;
        });
      },
      getArticleID(){
        this.$axios.get(this.host +'/articles/',{
          headers:{
            'Authorization': 'JWT ' + this.token
          }
        }).then(response=>{
          this.options = response.data;


        });
      },
      handleCurrentChange(currentPage){
        this.getArticleImgsPage(currentPage);
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
  　　 beforeUploadHandle(file) {

        this.param = new FormData();
        this.param.append('file', file, file.name);

        return false;
      },
      httprequest() {
        //覆盖默认的上传行为

      },
      addArticleImg() {

        this.isShowEditDialog = true;
        this.handleFlag = 'handleAdd';
        // 避免 'resetFields' of undefined 问题
        this.$nextTick(()=>{
            // 重置表单
            this.$refs.formFileds.resetFields();
            var ulEle = document.getElementsByClassName('el-upload-list el-upload-list--text')[0];

            ulEle.innerHTML = '';
        })

      },
      handleAdd() {
        var article = this.formFileds.article;
        this.param.append('article',article);

        this.$axios.post(this.host + '/article_imgs/',this.param,{
            headers: {
              'X-CSRFToken': this.getCookie('csrftoken'),
              'Authorization': 'JWT ' + this.token,
              'Content-Type': 'multipart/form-data'
            }
          }).then(response=>{
            console.log(response.data);
            // 获取文件上传后显示文件名列表
            var ulEle = document.getElementsByClassName('el-upload-list el-upload-list--text')[0];

            ulEle.innerHTML += '<li>'+response.data.filename +'</li>';

            this.isShowEditDialog = false;
            this.getArticleImgs();

            this.handleSuccess(response.data);


          }).catch(error=>{
            console.log(error.data);
          });
      },
      rowEdit(index, row) {
        this.handleFlag = 'handleEdit';

        console.log(this.handleFlag);

        this.setCurRowChecked(row);

        // 给编辑弹出层赋值
        // ***这里需要注意的是：因为加了排序 所以tableData的顺序和实际显示的行顺序不一样
        for (let key in this.formFileds) {

          this.formFileds[key] = row[key];
        }
        this.isShowEditDialog = true;
      },
      handleEdit(id){
        // 处理编辑数据操作
        this.$refs.formFileds.validate(isVaild=>{
          if(isVaild){
              this.param.append('article',this.formFileds.article);
              this.$axios.put(this.host +'/article_imgs/'+id+'/',this.param,{
                headers: {
                  'X-CSRFToken': this.getCookie('csrftoken'),
                  'Authorization': 'JWT ' + this.token,
                  'Content-Type': 'multipart/form-data'
                }
              }).then(response=>{
                if(response.data.filename){
                  this.$message.success('编辑成功');
                  this.isShowEditDialog = false;
                }else{
                  this.$message.error('编辑失败')
                }
                this.getArticleImgs();
              }).catch(error=>{
                console.log(error.response);
              });



          }else{
            this.$message.error('表单校验失败');
          }
        });


      },
      rowDel(index, row, event) {

        // 让当前删除按钮失焦
        event.target.blur();

        this.$confirm('确定要删除当前行吗？', '删除', {
          comfirmButtonText: '确定',
          cancelButtonText: '取消'
        }).then(() => {
          // 调用后端接口完成删除操作
          this.$axios.delete(this.host + '/article_imgs/'+row.id+'/',{
            headers:{
              'X-CSRFToken': this.getCookie('csrftoken'),
              'Authorization': 'JWT ' + this.token
            }
          }).then(response=>{
            this.$message.success('删除成功')
            this.getArticleImgs();
          }).catch(error=>{
            this.$message.error('删除失败')
          });



        }).catch(error=>{

        });
      },
      // 选中当前行-当前行的复选框被勾选
      setCurRowChecked(row) {

        this.$refs.list.clearSelection();
        this.$refs.list.toggleRowSelection(row);
      }
    },
    mounted(){
      //获取所有图片信息
      this.getArticleImgs();
      this.getArticleID();
    }
    }
</script>

<style >
img{
	width:100%;
	height:100%;
}


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
  width:1200px;
}



.fill { object-fit: fill; }
.contain { object-fit: contain; }
.cover { object-fit: cover; }
.none { object-fit: none; }
.scale-down { object-fit: scale-down; }

</style>
