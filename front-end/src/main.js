import Vue from "vue";
import App from "./App.vue";
import $ from "jquery";

Vue.config.productionTip = false;
$(document).ready(() => {});
new Vue({
  render: h => h(App)
}).$mount("#app");
