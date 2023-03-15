<template>
  <el-aside width="auto" height="auto">
    <el-menu :collapse="isCollapse" :default-active="onRoutes" background-color="#232323" text-color="#ccc" active-text-color="#ddd" unique-opened router>
      <template v-for="item in items">
        <template v-if="item.subItems">
          <el-submenu :index="item.path">
            <template slot="title">
              <i :class="item.icon"></i>
              <span slot="title">{{item.title}}</span>
            </template>
            <el-menu-item v-for="(subItem, i) in item.subItems" :index="subItem.path" :key="i">
              {{subItem.title}}
            </el-menu-item>
          </el-submenu>
        </template>
        <template v-else>
          <el-menu-item :index="item.path">
            <i :class="item.icon"></i>
            <span slot="title">{{item.title}}</span>
          </el-menu-item>
        </template>
      </template>
    </el-menu>
  </el-aside>
</template>

<script>
  import Bus from "./bus";
  export default {
    name: "Sidebar",
    data() {
      return {
        isCollapse: false,
        items: [
          {
            title: '首页',
            path: '/index'
          },
          {
            title: '用户管理',
            path: '/mg_user'
          },
          {
            title: '诗路管理',
            path:'',
            subItems: [
              {
                title: '景点管理',
                path: '/mg_articles'
              },
              {
                title: '图片管理',
                path: '/mg_imgs'
              }
            ]
          },
          {
            title: '支付管理',
            path: '/order'
          },
          {
            title: '系统管理',
            path: '',
            subItems: [
              {
                title: '权限管理',
                path: '/permission'
              },
              {
                title: '用户组管理',
                path: '/user_group'
              },
              {
                title: '管理员管理',
                path: '/admin'
              }
            ]
          }

        ]
      }
    },
    computed: {
      onRoutes() {

        return this.$route.fullPath;
      }
    },
    created() {

      // 通过 event bus进行组件间的通信 来折叠和展开侧边栏
      Bus.$on('collapse', isCollapse => {

        this.isCollapse = isCollapse;
      });
    }
  }
</script>

<style scoped lang="less">
  .el-menu {
    height: 100%;
    border: none;
    &:not(.el-menu--collapse) {
      width: 200px;
    }
  }
  .el-menu-item.is-active {
    border-left: 3px solid @mainColor;
    background-color: #171717 !important;
  }
</style>
