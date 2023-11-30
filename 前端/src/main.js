import Vue from 'vue'
import App from './App.vue'
import router from './router'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';


import configs from './configs'
Vue.prototype.$formRules = configs.formRules
Vue.prototype.$urls = configs.urls
import api from './request/api';
Vue.prototype.$api = api

Vue.config.productionTip = false
Vue.use(ElementUI);
export default new Vue({
  router,
  created() {
  },
  mounted() {
  },
  methods: {
  },
  render: h => h(App)
}).$mount('#app')
