<template>
    <div class="container new-collection">
      <Header></Header>
      <div class="row"><div class="col-xs-18 col-xs-offset-3 main">
        <h3>新建专题</h3>
        <table>
          <thead>
          <tr>
            <th class="setting-head"></th>
            <th></th>
          </tr>
          </thead>
          <tbody class="base">
          <tr>
            <td>
              <div class="avatar-collection"><img src="/static/image/logo.png"></div>
            </td>
            <td>
              <a rel="noreferrer" class="btn btn-hollow"><input unselectable="on" type="file" class="hide">上传专题封面</a>
            </td></tr>
          <tr>
            <td class="setting-title">名称</td>
            <td><input type="text" name="nick-name" placeholder="填写名称，不超过50字" v-model="special_name"></td>
          </tr>
          <tr>
            <td class="setting-title pull-left setting-input">描述</td>
            <td><textarea placeholder="填写描述" v-model="special_describe"></textarea></td>
          </tr>
          <tr class="add-manager">
            <td class="setting-title pull-left setting-input">其他管理员</td>
            <td>
              <div class="user-add">
                <input type="text" name="nick-name" placeholder="输入用户名" data-toggle="dropdown" v-model="manager_name">
                <ul class="dropdown-menu"></ul>
              </div>
            </td>
          </tr>
          <tr>
            <td class="setting-title setting-verticle">是否允许投稿</td>
            <td>
              <div class="col-xs-6">
                <input type="radio" name="push" value="True" v-model="checkKey">
                <span>允许</span>
              </div>
              <div class="col-xs-18">
                <input type="radio" name="push" value="False" v-model="checkKey">
                <span>不允许</span>
              </div>
            </td>
          </tr>
          <tr class="">
            <td class="setting-title setting-verticle">投稿是否需要审核</td>
            <td>
              <div class="col-xs-6"><input type="radio" name="verify" value="True" v-model="checkValue">
                <span>需要</span>
              </div>
              <div class="col-xs-18">
                <input type="radio" name="verify" value="False" v-model="checkValue">
                <span>不需要</span>
              </div>
            </td>
          </tr>
          </tbody>
        </table>
        <div class="btn btn-success follow create" @click.prevent="addSpecial">创建专题</div>
      </div>
      </div>
      <Footer></Footer>
    </div>
</template>
<script>
    import Header from "./common/Header";
    import Footer from "./common/Footer";
    export default {
        name: "Special",
        data(){
          return{
            img_url:"", // 图片路径
            special_name:"", // 专题内容
            special_describe:"", // 专题描述
            manager_name:"", // 管理员名称
            checkValue:"",
            checkKey:"",
          }
        },

      created() {
         this.token = this.get_login_user();
      },

      methods:{

          // 获取登录用户，登录了才能进行操作
          get_login_user(){
            return localStorage.user_token || sessionStorage.user_token;
                },

          // 添加专题
          addSpecial(){
              if (this.manager_name.length===0){
                this.$alert("对不起，请填写管理员名称！")
              }

              this.$axios.post(`${this.$settings.Host}/article/special/`,{
                img_url: this.img_url,
                special_name: this.special_name,
                special_describe: this.special_describe,
                manager_name: this.manager_name,
                checkKey: this.checkKey,
                checkValue: this.checkValue,
              },{
                headers:{
                    Authorization: "jwt " + this.token,
                  }
              }).then(response=>{
                this.$message.success("添加专题成功！");
                setTimeout(()=>{
                  this.$router.go(-1);
                }, 1000);
                this.$router.push(`/${article.id}/writed`);
              }).catch(error=>{
                this.$message.error("添加专题失败！");
              })


          },

        },

      components:{
          Header,
          Footer,
        },
    }

</script>

<style scoped>
.new-collection .main {
    margin-bottom: 60px;
}
.col-xs-offset-3 {
    margin-left: 40%;
}
.col-xs-18 {
    width: 100%;
}
.new-collection .main h3 {
    margin: 10px 0 20px;
    font-size: 21px;
    font-weight: 700;
    color: #333;
}
.avatar-collection img {
    width: 100px;
    height: 100px;
    border: 1px solid #ddd;
    border-radius: 10%;
}

img {
    vertical-align: middle;
}
.new-collection .main .btn-hollow {
    font-size: 14px;

}
.btn-hollow {
    border: 1px solid rgba(59,194,29,.7);
    color: #42c02e!important;
}
.btn-hollow {
    padding: 4px 12px;
    font-weight: 400;
    line-height: normal;
    border-radius: 40px;
    background: none;
}
.btn {
    display: inline-block;
    margin-bottom: 0;
    text-align: center;
    vertical-align: middle;
    touch-action: manipulation;
    cursor: pointer;
    white-space: nowrap;
    user-select: none;
}
a {
    text-decoration: none;
}
.new-collection .main .hide {
    position: absolute;
    display: block!important;
    width: 82px;
    opacity: 0;
}

.new-collection .main input {
    padding: 10px 15px;
    font-size: 15px;
    border: 1px solid #c8c8c8;
    border-radius: 4px;
    background-color: hsla(0,0%,71%,.1);
}

.new-collection .main td {
    padding: 16px 0;
    font-size: 15px;
}

td {
    display: table-cell;
    vertical-align: inherit;
}
table {
    border-collapse: collapse;
    border-spacing: 0;
}
.main input[name=nick-name] {
    width: 100%;
}

.new-collection .main input {
    padding: 10px 15px;
    font-size: 15px;
    border: 1px solid #c8c8c8;
    border-radius: 4px;
    background-color: hsla(0,0%,71%,.1);
}
.new-collection .main textarea {
    width: 100%;
    height: 100px;
    margin-bottom: 10px;
    padding: 10px 15px;
    font-size: 15px;
    border: 1px solid #c8c8c8;
    border-radius: 4px;
    background-color: hsla(0,0%,71%,.1);
    display: block;
    resize: none;
    outline-style: none;
}
textarea {
    line-height: inherit;
}

textarea {
    overflow: auto;
}
button, input, optgroup, select, textarea {
    color: inherit;
    font: inherit;
    margin: 0;
}
.col-xs-6 {
    width: 25%;
    float: left;
    position: relative;
    min-height: 1px;
    padding-left: 15px;
    padding-right: 15px;
}
.new-collection .main .create {
    margin: 20px 0 50px;
    border-radius: 20px;
}

.follow {
    border-color: #42c02e;
}
.follow{
    padding: 8px 22px;
    font-size: 16px;
    font-weight: 400;
    line-height: normal;
}
.btn-success {
    color: #fff;
    background-color: #42c02e;
}
.btn {
    display: inline-block;
    text-align: center;
    vertical-align: middle;
    touch-action: manipulation;
    cursor: pointer;
    background-image: none;
    border: 1px solid transparent;
    white-space: nowrap;
    user-select: none;
}
</style>
