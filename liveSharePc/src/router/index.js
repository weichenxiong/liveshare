import Vue from "vue"
import Router from "vue-router"

import Home from "../components/Home";
import Login from "../components/Login";
import Register from "../components/Register";
import SetPasswordByEmail from "../components/SetPasswordByEmail";
import SetPasswordByPhone from "../components/SetPasswordByPhone";
import FindPassword from "../components/FindPassword";
import QQCallBack from "../components/QQCallBack";
import Write from "../components/Write";
import Writed from "../components/Writed";
import Article from "../components/Article";
import Wallet from "../components/Wallet";
import Special from "../components/Special";


Vue.use(Router)

export default new Router({
  //设置路由模式为'history，去掉默认的
  mode: "history",
  routes:[
    // 路由列表


    {
      name:"Home",
      path: "/",
      component:Home,
    },

        {
      name:"Login",
      path: "/user/login",
      component:Login,
    },

    {
      name:"Register",
      path: "/user/register",
      component:Register,
    },

        {
      name:"FindPassword",
      path: "/find/password",
      component:FindPassword,
    },

    {
      name:"SetPasswordByPhone",
      path: "/user/set_password_by_phone",
      component:SetPasswordByPhone,
    },
    {
      name:"SetPasswordByEmail",
      path: "/user/set_password_by_email",
      component:SetPasswordByEmail,
    },

    {
      name: "QQCallBack",
      path: "/oauth_callback.html",
      component: QQCallBack,
    },

        {
      name: "Write",
      path: "/write",
      component: Write,
    },

    {
      name: "Writed",
      path: "/:id/writed",
      component: Writed,
    },

    {
       name:"Article",
       path:"/article/:id",
       component: Article,
     },

     {
      name: "Wallet",
      path: "/user/wallet",
      component: Wallet,
    },

         {
      name: "Special",
      path: "/special/special",
      component: Special,
    },
  ]

})
