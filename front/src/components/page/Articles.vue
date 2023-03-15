<template>
  <div>


    <el-row>

      <!-- 搜索文章信息-->
      <el-input v-model="q" placeholder="请输入内容" class="searchwidth"></el-input>
      <el-button icon="el-icon-search" @click="getArticles"></el-button>
      <!-- 新增文章信息-->
      <el-button class="row_right" type="success" @click="addArtcile();">新增诗路景点</el-button>
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
        property="title"
        label="标题"
        width="450">
      </el-table-column>
      <el-table-column
        property="starcount"
        label="点赞量">
      </el-table-column>
      <el-table-column
        property="commentcount"
        label="评论量">
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
      :page-sizes="[2, 4, 6, 8]"
      :current-page=1
      :page-size=2
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

        <el-form-item label="标题" prop="title">
          <el-input v-model="formFileds.title"></el-input>
        </el-form-item>
        <el-form-item label="正文" prop="content">
          <quill-editor v-model="formFileds.content"></quill-editor>
        </el-form-item>
        <el-form-item label="点赞量" prop="starcount">
          <el-input v-model="formFileds.starcount"></el-input>
        </el-form-item>
        <el-form-item label="评论量" prop="commentcount">
          <el-input v-model="formFileds.commentcount"></el-input>
        </el-form-item>
        <el-form-item label="景点类别" prop="category">
          <el-select v-model="formFileds.category" placeholder="请选择">
            <el-option
              v-for="item in options"
              :key="item.id"
              :label="item.name"
              :value="item.id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="诗路类别" prop="channel">
          <el-select v-model="formFileds.channel" placeholder="请选择">
            <el-option
              v-for="item in channels"
              :key="item.id"
              :label="item.name"
              :value="item.id">
            </el-option>
          </el-select>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" class="pull-right margin-l-25"
                     @click="handleFlag=='handleAdd'?handleAdd():handleEdit(formFileds.id)">确定
          </el-button>
          <el-button @click="isShowEditDialog = false;" class="pull-right">取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: "Articles",
  data() {

    return {
      host: 'http://101.35.247.14:8000',
      token: localStorage.token,
      username: localStorage.username,
      userid: localStorage.user_id,

      totalRecords: 0,

      formFileds: {
        id: '',
        title: '',
        content: '',
        starcount: '0',
        commentcount: '0',
        category: '',
        channel: '',
      },

      options: [],
      channels: [],
      q: '',
      rules: {
        title: [
          {required: true, message: '标题不能为空', trigger: 'blur, change'}
        ],
        content: [
          {required: true, message: '正文不能为空', trigger: 'blur, change'}
        ],

      },
      tableData: [],
      isShowEditDialog: false,
      handleFlag: 'handleAdd'
    }
  },
  methods: {
    getCookie: function (name) {
      var value = '; ' + document.cookie
      var parts = value.split('; ' + name + '=')
      if (parts.length === 2) return parts.pop().split(';').shift()
    },

    getArticles() {
      //搜索所有文章信息
      this.$axios.get(this.host + '/articles/?search= ' + this.q + '&page=1&pagesize=2', {
        headers: {
          'Authorization': 'JWT ' + this.token
        }
      }).then(response => {
        this.tableData = response.data.lists;
        this.totalRecords = response.data.count;
      }).catch(error => {
        console.log(error.response);
      })
    },
    getArticlesPage(page = 1) {
      //分页数据
      this.$axios.get(this.host + '/articles/?search= &page=' + page + '&pagesize=2', {
        headers: {
          'Authorization': 'JWT ' + this.token
        }
      }).then(response => {
        this.tableData = response.data.lists;
        this.totalRecords = response.data.count;
      }).catch(error => {
        console.log(error.response);
      })
    },
    getCategories() {
      // 查询所有的类别信息
      this.$axios.get(this.host + '/mg_admin/categories/', {
        headers: {
          'Authorization': 'JWT ' + this.token
        }
      }).then(response => {
        this.options = response.data;
      }).catch(error => {
        console.log(error.response);
      })
    },
    getChannels() {
      // 查询所有的类别信息
      this.$axios.get(this.host + '/mg_admin/channels/', {
        headers: {
          'Authorization': 'JWT ' + this.token
        }
      }).then(response => {
        this.channels = response.data;
      }).catch(error => {
        console.log(error.response);
      })
    },

    addArtcile() {
      // 显示表单
      this.isShowEditDialog = true;
    },
    handleAdd() {
      // 新增文章表单处理
      this.$refs.formFileds.validate(isValid => {
        if (isValid) {
          this.$axios.post(this.host + '/articles/', this.formFileds, {
            headers: {
              'Authorization': 'JWT ' + this.token,
              'X-CSRFToken': this.getCookie('csrftoken')
            }
          }).then(response => {
            if (response.data.id) {
              this.isShowEditDialog = false;
              this.$message.success('提交成功');
            } else {
              this.$message.error('提交失败');
            }

            this.getArticles();
          }).catch(error => {
            console.log(error.response);
          })
        } else {
          this.$message.error('表单校验失败');
        }
      });
    },
    handleCurrentPage(val) {
      // 翻页功能  val:当前页码
      this.getArticlesPage(`${val}`);

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
    handleEdit(id) {
      // 编辑文章表单处理
      this.$refs.formFileds.validate(isValid => {
        if (isValid) {
          this.$axios.put(this.host + '/articles/' + id + '/', this.formFileds, {
            headers: {
              'Authorization': 'JWT ' + this.token,
              'X-CSRFToken': this.getCookie('csrftoken')
            }
          }).then(response => {
            if (response.data.id) {
              this.isShowEditDialog = false;
              this.$message.success('提交成功');
            } else {
              this.$message.error('提交失败');
            }

            this.getArticles();
          }).catch(error => {
            console.log(error.response);
          })
        } else {
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
      }).then((resp) => {
        // 调用后端接口执行删除操作
        this.$axios.delete(this.host + '/articles/' + row.id + '/', {
          headers: {
            'Authorization': 'JWT ' + this.token,
            'X-CSRFToken': this.getCookie('csrftoken')
          }
        }).then(response => {
          this.$message.success('删除成功');
          this.getArticles();
        })

      }).catch(error => {
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
  mounted() {
    this.getArticles();
    this.getCategories();
    this.getChannels();
  }
}
</script>

<style scoped lang="less">
.row_right {
  position: relative;
  left: 5px;
  button: 3px;
}


.el-form {
  padding: 0 10px;
}

.el-date-editor {
  width: 100% !important;
}

.searchwidth {
  width: 1200px;
}
</style>
