
import Vue from 'vue'
import App from './App'
import router from './router/index'
import settings from "./settings";
import 'element-ui/lib/theme-chalk/index.css';
import "../static/css/reset.css"
import axios from 'axios'; // 从node_modules目录中导入包
import mavonEditor from 'mavon-editor'
import 'mavon-editor/dist/css/index.css'


// 注册mavon-editor组件
Vue.use(mavonEditor);
new Vue({
        'el': '#main'
    })
// 允许ajax发送请求时附带cookie
axios.defaults.withCredentials = false;

Vue.prototype.$axios = axios; // 把对象挂载vue中

Vue.config.productionTip = false;
Vue.prototype.$settings = settings;

//全局导入字体图标
import "../static/css/iconfont.css"
import "../static/css/iconfont.eot"

	// 注册mavon-editor组件

import ElementUI from 'element-ui'
Vue.use(ElementUI);

new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
