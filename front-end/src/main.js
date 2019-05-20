import Vue from "vue";
import App from "./App.vue";
import "@fortawesome/fontawesome-free";
import "vuetify/dist/vuetify.min.css";
import Vuetify from "vuetify";
import Lightbox from "vue-easy-lightbox";
import $ from "jquery";

global.$ = $;
global.jquery = $;
global.jQuery = $;
Vue.use(Lightbox);
Vue.use(Vuetify);
Vue.config.productionTip = false;
new Vue({
  render: h => h(App)
}).$mount("#app");
