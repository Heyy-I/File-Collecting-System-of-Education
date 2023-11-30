import Vue from 'vue'
import VueRouter from 'vue-router'
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'auth',
    component: ()=> import('../views/Auth/Auth.vue')
  },
  {
    path: '/home',
    name: 'home',
    // redirect: '/myspace',
    component: () => import('../views/Home/Home.vue'),
    children: [
      { path: '/myspace', component: () => import('../views/Auth/myspace.vue') },

      { path: '/Teacher_myclass', component: () => import('../views/Teacher/myclass.vue') },


      { path: '/Collector_classes', component: () => import('../views/Collector/classes.vue') },
      { path: '/Collector_collections', name:'Collector_collections', component: () => import('../views/Collector/collections.vue'), props: true},
    
      
      { path: '/Student_classes', component: () => import('../views/Student/classes.vue') },
      { path: '/Student_collections', component: () => import('../views/Student/collections.vue') },
      { path: '/Student_upload', name:'Student_upload', component: () => import('../views/Student/upload.vue'), props: true},
      
      
      { path: '/Admin_user_manage', name: 'Admin_user_manage', component: () => import('../views/Admin/user.vue') },
      { path: '/Admin_activate_teacher', name:'Admin_activate_teacher', component: () => import('../views/Admin/activate.vue')},
    ]
  },
]


const router = new VueRouter({
  routes
})

router.beforeEach((to, from, next) => {
	if (to.path == '/') {
		return next();
  } else {
    if (localStorage.getItem('token')) {
      return next();
    }
    else {
      return next("/");
    }
	}
})
export default router
