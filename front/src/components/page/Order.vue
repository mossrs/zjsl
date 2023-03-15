<template>
  <div>

    <el-row>
      <!-- 搜索订单信息-->
      <el-input v-model="q" placeholder="请输入内容" class="searchwidth" ></el-input><el-button icon="el-icon-search" @click="getOrders"></el-button>
    </el-row>
    <br>
    <!--表格内容-->
    <el-table
      ref="list"
      :data="tableData"
      style="width: 100%"

      stripe
      highlight-current-row
      :default-sort="{prop: 'create_time', order: 'descending'}"
      @row-click="handleRowClick"
      @select-all="handleCheckedAllAndCheckedNone"
      @select="handleCheckedAllAndCheckedNone">
      <el-table-column
        type="selection"
        width="100"
        align="center">
      </el-table-column>
      <el-table-column
        type="index"
        label="序号"
        width="100">
      </el-table-column>

      <el-table-column
        property="order_id"
        label="支付编号"
        width="450">
      </el-table-column>
      <el-table-column
        property="create_time"
        label="支付日期"
        width="450"
        sortable>
        <template slot-scope="scope">
          <span style="margin-left: 5px">{{scope.row.create_time}}</span>
        </template>
      </el-table-column>

      <el-table-column
        label="操作"
        width="365"
        align="center">
        <template slot-scope="scope">
          <el-button type="primary" icon="el-icon-edit" circle title="详情" size="small"
            @click="rowDetail(scope.$index, scope.row)"></el-button>
          <el-button circle icon="el-icon-edit-outline" type="primary" title="编辑" size="small"
            @click="rowEdit(scope.$index, scope.row)"></el-button>
          <el-button circle icon="el-icon-delete" type="danger" title="删除" size="small"
            @click="rowDel(scope.$index, scope.row, $event);"></el-button>
        </template>
      </el-table-column>
    </el-table>

    <br/>

    <!--分页-->
    <el-pagination
      @current-change="handleCurrentPage"
      :page-sizes="[3, 6, 9, 12]"
      :current-page= 1
      :page-size= 3
      :total="totalRecords"
      layout="total, sizes, prev, pager, next, jumper">
    </el-pagination>

    <h3 style="color:gray;">支付详情：</h3>
    <br/>

    <!--订单详情表格-->
    <el-table
      ref="list"
      :data="tableDetail"
      :border="showFlag"
      style="width: 100%;">
      <el-table-column
        property="order_id"
        label="支付编号"
        width="150"
        align="center">
        <template slot-scope="scope">
          <span>{{scope.row.order_id}}</span>
        </template>
      </el-table-column>

      <el-table-column
        property="create_time"
        label="支付时间"
        width="180">
        <template slot-scope="scope">
          <span >{{scope.row.create_time}}</span>
        </template>
      </el-table-column>
      <el-table-column
        property="user"
        label="用户编号"
        width="80">
      </el-table-column>
      <el-table-column
        property="total_amount"
        label="鲜花数量">
      </el-table-column>
      <el-table-column
        property="total_amount"
        label="支付金额">
      </el-table-column>
      <el-table-column
        property="pay_method"
        label="支付方式">
      </el-table-column>
      <el-table-column
        property="status"
        label="支付状态"
        width="200">
        <template slot-scope="scope">
          <el-input-number size="small" v-model="scope.row.status" :min="1" :max="3" ></el-input-number>

          <el-button round @click="updateStatus(scope.row.order_id,scope.row.status)">修改状态</el-button>
        </template>
      </el-table-column>
      <el-table-column
        property="article"
        label="诗路编号">
      </el-table-column>

    </el-table>

    <!--编辑-弹出层-->
    <el-dialog
      title="编辑"
      :visible.sync="isShowEditDialog"
      width="430px"
      @close="dialogClose">
      <el-form
        ref="editForm"
        :model="formFileds"
        label-width="55px"

        :rules="rules">
        <el-form-item label="日期">
          <el-date-picker v-model="formFileds.date" value-format="yyyy-MM-dd" :editable="false" :clearable="false"></el-date-picker>
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input v-model="formFileds.name"></el-input>
        </el-form-item>
        <el-form-item label="地址" prop="address">
          <el-input v-model="formFileds.address"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleEdit(formFileds.id)" class="pull-right margin-l-25">确定</el-button>
          <el-button @click="isShowEditDialog = false;" class="pull-right">取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>

  import Bus from '../common/bus';

  export default {
    name: "Order",
    data() {
      return {
        host:'http://101.35.247.14:8000',
        token:localStorage.token,
        username:localStorage.username,
        userid:localStorage.user_id,

        formFileds: {
          orderid: '',
          create_time: '',
          id: ''
        },
        q: '',
        totalRecords:0,
        rules: {
          name: [
            {required: true, message: '姓名不能为空', trigger: 'blur, change'}
          ],
          address: [
            {required: true, message: '地址不能为空', trigger: 'blur, change'}
          ]
        },
        tableData: [],
        isShowEditDialog: false,
        tableDetail:[],
        showFlag:false,
      }
    },
    methods: {
      getCookie:function(name){
          var value = '; ' + document.cookie
          var parts = value.split('; ' + name + '=')
          if (parts.length === 2) return parts.pop().split(';').shift()
        },
      getOrders(){
        //获取所有订单数据
        this.$axios.get(this.host + '/orders/?search= '+this.q+'&page=1&pagesize=3',{
          headers:{
            'Authorization': 'JWT ' + this.token
          }
        }).then(response=>{
          this.tableData = response.data.lists;
          this.totalRecords = response.data.count;
        }).catch(error=>{
          console.log(error)
        });
      },
      getOrdersPage(page=1){
        //获取所有订单数据
        this.$axios.get(this.host + '/orders/?search= &page='+page+'&pagesize=3',{
          headers:{
            'Authorization': 'JWT ' + this.token
          }
        }).then(response=>{
          this.tableData = response.data.lists;
          this.totalRecords = response.data.count;
        }).catch(error=>{
          console.log(error);
        });
      },
      updateStatus(orderid,status){
          this.$axios.put(this.host + '/orders/'+orderid+'/status/',{'status':status},{
            headers:{
                'Authorization': 'JWT ' + this.token,
                'X-CSRFToken': this.getCookie('csrftoken')
              }
          }).then(response=>{
            this.tableDetail['status'] = response.data.status;
            this.$message.success('修改成功')
          }).catch(error=>{
            this.$message.error('修改失败')
          })
      },
      handleCurrentPage(val){
        // 翻页功能  val:当前页码
        this.getOrdersPage(`${val}`);
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
        this.$refs.editForm.resetFields();
      },
      rowDetail(index,row){
        this.setCurRowChecked(row);
        this.tableDetail = [];
        this.tableDetail.push(row);
      },
      rowEdit(index, row) {

        this.setCurRowChecked(row);

        // 给编辑弹出层赋值
        // ***这里需要注意的是：因为加了排序 所以tableData的顺序和实际显示的行顺序不一样
        for (let key in this.formFileds) {

          this.formFileds[key] = row[key];
        }
        this.isShowEditDialog = true;
      },
      handleEdit(id) {

        this.$refs.editForm.validate(isValid => {

          if (!isValid) return;

          // 保存编辑后的数据
          Object.assign(this.tableData[id], this.formFileds);
          this.isShowEditDialog = false;

          // 考虑到可能编辑了日期-需要重新排序
          // ***注意：手动排序传参和表格的default-sort属性格式不太一样
          this.$refs.list.sort('date', 'descending');

          this.$message.success('编辑成功');
        });
      },
      rowDel(index, row, event) {
        // 让当前删除按钮失焦
        event.target.blur();
        this.$confirm('确定要删除当前行吗？', '删除', {
          comfirmButtonText: '确定',
          cancelButtonText: '取消'
        }).then((resp) => {
            this.$axios.delete(this.host + '/orders/'+row.order_id+'/',{
              headers:{
                'Authorization': 'JWT ' + this.token,
                'X-CSRFToken': this.getCookie('csrftoken')
              }
            }).then(response=>{
              this.$message.success('删除成功');
              this.getOrders();
            }).catch(error=>{
              console.log(error);
            })
        });
      },
      // 选中当前行-当前行的复选框被勾选
      setCurRowChecked(row) {
        this.$refs.list.clearSelection();
        this.$refs.list.toggleRowSelection(row);
      }
    },
    mounted(){
      this.getOrders();
    }
  }
</script>

<style scoped lang="less">
.el-form {
  padding: 0 10px;
}
.el-date-editor {
  width: 100% !important;
}

/* 卡片样式*/
 .text {
    font-size: 14px;
  }

  .item {
    padding: 18px 0;
  }

  .box-card {
    width: 660px;
  }
.searchwidth{
  width:1400px;
}

  /* 卡片样式*/
</style>
