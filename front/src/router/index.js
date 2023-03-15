import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router);

export default new Router({
  // mode: "history",
  routes: [
    {
      path: '/',
      redirect: '/index'
    },
    {
      path: '/',
      component: () => import('../components/common/Base.vue'),
      meta: {
        title: '公共部分'
      },
      children: [
        {
          path: '/index',
          component: () => import('../components/page/Home.vue'),
          meta: {
            title: '系统首页'
          }
        },
        {
          path: '/chart-simple',
          component: () => import('../components/page/EChartsSimple.vue'),
          meta: {
            title: '简单图表'
          }
        },
        {
          path: '/chart-complex',
          component: () => import('../components/page/EChartsComplex.vue'),
          meta: {
            title: '复杂图表'
          }
        },
        {
          path: '/tab',
          component: () => import('../components/page/Tab.vue'),
          meta: {
            title: 'tab选项卡'
          }
        },
        {
          path: '/table',
          component: () => import('../components/page/Table.vue'),
          meta: {
            title: '表格'
          }
        },
        {
          path: '/mg_user',
          component: () => import('../components/page/UserMangement.vue'),
          meta: {
            title: '用户管理'
          }
        },
        {
          path: '/mg_articles',
          component: () => import('../components/page/Articles.vue'),
          meta: {
            title: '景点管理'
          }
        },
        {
          path: '/mg_imgs',
          component: () => import('../components/page/Imgs.vue'),
          meta: {
            title: '图片管理'
          }
        },
        {
          path: '/order',
          component: () => import('../components/page/Order.vue'),
          meta: {
            title: '支付管理'
          }
        },
        {
          path: '/permission',
          component: () => import('../components/page/Permission.vue'),
          meta: {
            title: '权限管理'
          }
        },
        {
          path: '/user_group',
          component: () => import('../components/page/UserGroup.vue'),
          meta: {
            title: '用户组管理'
          }
        },
        {
          path: '/admin',
          component: () => import('../components/page/Admin.vue'),
          meta: {
            title: '管理员管理'
          }
        }
      ]
    },
    {
      path: '/login',
      component: () => import('../components/page/Login.vue')
    },
    {
      path: '/error',
      component: () => import('../components/page/Error.vue')
    },
    {
      path: '/404',
      component: () => import('../components/page/404.vue')
    }
  ]
})
