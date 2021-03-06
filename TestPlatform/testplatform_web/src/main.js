import Vue from 'vue'
import App from './App.vue'
import router from './router'
import VueI18n from 'vue-i18n';
import { messages } from './components/common/i18n';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import './assets/css/icon.css';
import "babel-polyfill";
import './assets/icons/index'
import './axios';

import contentmenu from 'v-contextmenu'

Vue.config.productionTip = false;
Vue.use(VueI18n);
Vue.use(ElementUI, {
  size: 'small'
});

// 开启contentmenu
Vue.use(contentmenu);

const i18n = new VueI18n({
  locale: 'zh',
  messages
});

new Vue({
  router,
  i18n,
  render: h => h(App)
}).$mount('#app')
