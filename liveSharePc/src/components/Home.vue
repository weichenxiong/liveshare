<template>
  <div id="home">
    <Header></Header>
    <div class="container">
      <div class="row">
        <div class="main">
          <!-- Banner -->
          <div class="banner">
            <el-carousel height="272px" indicator-position="none" :interval="2000">
              <el-carousel-item v-for="item in 4" :key="item">
                <h3 class="small">{{ item }}</h3>
              </el-carousel-item>
            </el-carousel>
          </div>
          <div id="list-container">
            <!-- 文章列表模块 -->
            <ul class="note-list">
<!--              <li class="">-->
<!--                <div class="content">-->
<!--                  <a class="title" target="_blank" href="">常做此运动，让你性福加倍</a>-->
<!--                  <p class="abstract">运动，是人类在发展过程中有意识地对自己身体素质的培养的各种活动 运动的方式多种多样 不仅仅是我们常知的跑步，球类，游泳等 今天就为大家介绍一种男...</p>-->
<!--                  <div class="meta">-->
<!--                    <span class="jsd-meta">-->
<!--                      <img src="/static/image/paid1.svg" alt=""> 4.8-->
<!--                    </span>-->
<!--                    <a class="nickname" target="_blank" href="">上班族也健身</a>-->
<!--                    <a target="_blank" href="">-->
<!--                      <img src="/static/image/comment.svg" alt=""> 4-->
<!--                    </a>-->
<!--                    <span><img src="/static/image/like.svg" alt=""> 31</span>-->
<!--                  </div>-->
<!--                </div>-->
<!--              </li>-->
              <li :class="check_img(article.content)?'have-img':''" v-for="article in article_list">
                <a class="wrap-img" href="" target="_blank" v-if="check_img(article.content)">
                  <img class="img-blur-done" :src="check_img(article.content)" />
                </a>
                <div class="content">
                  <router-link class="title" target="_blank" :to="`/article/${article.id}`">{{article.title}}</router-link>
                  <p class="abstract"　v-html="subtext(article.content,120)">
                  </p>
                  <div class="meta">
                    <a class="nickname" target="_blank" href="">{{article.user.nickname}}</a>
                    <a target="_blank" href="">
                      <img src="/static/image/comment.svg" alt=""> {{article.comment_count}}
                    </a>
                    <span><img src="/static/image/like.svg" alt=""> {{article.like_count}}</span>
                    <span v-if="article.reward_count>0"><img src="/static/image/shang.svg" alt=""> {{article.reward_count}}</span>
                  </div>
                </div>
              </li>
            </ul>
            <!-- 文章列表模块 -->
          </div>
        <a @click="get_next_article" class="load-more" v-if="new_article_list">阅读更多</a></div>
        <div class="aside">
          <!-- 推荐作者 -->
          <div class="recommended-author-wrap">
            <!---->
            <div class="recommended-authors">
              <div class="title">
                <span>推荐作者</span>
                <a class="page-change"><img class="icon-change" src="/static/image/exchange-rate.svg" alt="">换一批</a>
              </div>
              <ul class="list">
                <li>
                  <a href="" target="_blank" class="avatar">
                    <img src="/static/image/avatar.webp" />
                  </a>
                  <a class="follow" state="0"><img src="/static/image/follow.svg" alt="" />关注</a>
                  <a href="" target="_blank" class="name">董克平日记</a>
                  <p>写了807.1k字 · 2.5k喜欢</p>
                </li>
                <li>
                  <a href="" target="_blank" class="avatar">
                    <img src="/static/image/avatar.webp" />
                  </a>
                  <a class="follow" state="0"><img src="/static/image/follow.svg" alt="" />关注</a>
                  <a href="" target="_blank" class="name">董克平日记</a>
                  <p>写了807.1k字 · 2.5k喜欢</p>
                </li>

              </ul>
              <a href="" target="_blank" class="find-more">查看全部 ></a>
              <!---->
            </div>
          </div>
        </div>
      </div>
    </div>
    <Footer></Footer>
  </div>
</template>
<script>
  import Header from "./common/Header";
  import Footer from "./common/Footer";
  export default {
      name:"Home",
      data(){
          return {
            get_article_url:"",
            new_article_list:"",
            is_send_get_article_request:false, // 函数节流，判断当前ajax是否执行过程中
            token:{},
            article_list:[
              {
                "user":{

                }
              }
            ]
          }
      },
      created(){
        this.token = this.get_login_user();
        this.get_article_url = `${this.$settings.Host}/home/article/`;
        this.get_article_list()
      },
      methods:{
          subtext(content,len=100){
            // 如果文章开头有图片，则过滤图片
            if(content){
              while (content.search("<img") != -1){
                content = content.replace(/<img.*?src="(.*?)".*?>/,"")
              }
              return content.split("").slice(0,len).join("")+'...';
            }
            return "";
          },
          check_img(content){
            if(content){
              let ret = content.match(/<img.*?src="(.*?)".*?>/)
              if(ret){
                return ret[1];
              }
            }

            return false;

          },
          get_login_user(){
            // 获取登录用户
            return localStorage.user_token || sessionStorage.user_token;
          },
          get_article_list(){

            // 判断当前ajax是否正在执行
            if(this.is_send_get_article_request){
              this.$message.error("点击过于频繁！");
              return false;
            }

            this.is_send_get_article_request = true;

            // 获取推送文章
            let headers = {};
            if(this.token){
              headers = {
                Authorization:"jwt " +this.token,
              }
            }
            this.$axios.get(this.get_article_url,{
              headers
            }).then(response=>{
              if(!this.new_article_list){
                this.article_list = response.data.results;
              }else{
                this.article_list = this.article_list.concat(response.data.results);
              }
              this.article_count = response.data.count;
              this.new_article_list = response.data.next;

              // 开启再次执行ajax的状态
              this.is_send_get_article_request = false;
            }).catch(eror=>{
              this.$message.error("获取推送文章失败！");
            });
          },
          get_next_article(){
            this.get_article_url = this.new_article_list;
            this.get_article_list();
          }
      },
      components:{
        Header,
        Footer,
      }
  }
</script>

<style scoped>
.container{
    width: 960px;
    margin-right: auto;
    margin-left: auto;
    padding-left: 15px;
    padding-right: 15px;
    box-sizing: border-box;
}
.container:after, .container:before {
    content: " ";
    display: table;
}
.row {
    margin-left: -15px;
    margin-right: -15px;
}
.row:after, .row:before {
    content: " ";
    display: table;
}
.main {
    padding-top: 30px;
    padding-right: 0;
    position: relative;
    min-height: 1px;
    padding-left: 15px;
    width: 66.66667%;
    float: left;
    box-sizing: border-box;
}
.main .banner{
    width: 640px;
    height: 272px;
}
.note-list {
    margin: 0;
    padding: 0;
    list-style: none;
}
.note-list li {
    position: relative;
    width: 100%;
    margin: 0 0 15px;
    padding: 15px 2px 20px 0;
    border-bottom: 1px solid #f0f0f0;
    word-wrap: break-word;
    line-height: 20px;
}
.note-list li.have-img {
    min-height: 140px;
}
.note-list .have-img .wrap-img {
    position: absolute;
    top: 50%;
    margin-top: -60px;
    right: 0;
    width: 150px;
    height: 100px;
}
.note-list .have-img .wrap-img img {
    width: 100%;
    height: 100%;
    border-radius: 4px;
    border: 1px solid #f0f0f0;
    vertical-align: middle;
}
.main .note-list .have-img .content {
    padding-right: 165px;
    box-sizing: border-box;
}
.note-list .title {
    margin: -7px 0 4px;
    display: inherit;
    font-size: 18px;
    font-weight: 700;
    line-height: 1.5;
    color: #333;
}
.note-list .title:hover{
    text-decoration: underline;
}
.note-list .abstract {
    margin: 0 0 8px;
    font-size: 13px;
    line-height: 24px;
    color: #999;
}
.note-list .meta {
    padding-right: 0!important;
    font-size: 12px;
    font-weight: 400;
    line-height: 20px;
}
.note-list .meta span {
    margin-right: 10px;
    color: #b4b4b4;
}

.jsd-meta {
    color: #ea6f5a!important;
}
.note-list .meta a, .note-list .meta a:hover {
    transition: .1s ease-in;
}
.note-list .meta a {
    margin-right: 10px;
    color: #b4b4b4;
}
.note-list .meta img{
    width: 15px;
    vertical-align: middle;
}

.main .load-more {
    width: 100%;
    border-radius: 20px;
    background-color: #a5a5a5;
    margin: 30px auto 60px;
    padding: 10px 15px;
    text-align: center;
    font-size: 15px;
    color: #fff;
    display: block;
    line-height: 1.42857;
    box-sizing: border-box;
}
.main .load-more:hover {
    background-color: #9b9b9b;
}
.aside {
    padding: 30px 0 0;
    margin-left: 4.16667%;
    width: 29.16667%;
    float: left;
    position: relative;
    min-height: 1px;
    box-sizing: border-box;
}
.recommended-authors {
    margin-bottom: 20px;
    padding-top: 0;
    font-size: 13px;
    text-align: center;
}
.recommended-authors .title {
    text-align: left;
}
.recommended-authors .title span {
    font-size: 14px;
    color: #969696;
}
.recommended-authors .title .page-change {
    float: right;
    display: inline-block;
    font-size: 16px;
    color: #969696;
}
.icon-change{
    width: 16px;
    vertical-align: middle;
}
.recommended-authors .list {
    margin: 0 0 20px;
    text-align: left;
    list-style: none;
}
.recommended-authors .list li {
    margin-top: 15px;
    line-height: 20px;
}
.recommended-authors .list .avatar {
    float: left;
    width: 48px;
    height: 48px;
    margin-right: 10px;
}

.avatar {
    width: 24px;
    height: 24px;
    display: block;
    cursor: pointer;
}
.avatar img {
    width: 100%;
    height: 100%;
    border: 1px solid #ddd;
    border-radius: 50%;
}
.follow{
    font-size: 14px;
    color: #42c02e;
    border-color: #42c02e;
    font-weight: 400;
    line-height: normal;
}
.follow img{
    width: 14px;
}
.recommended-authors .list .follow, .recommended-authors .list .follow-cancel, .recommended-authors .list .follow-each, .recommended-authors .list .following {
    float: right;
    margin-top: 5px;
    padding: 0;
    font-size: 13px;
    color: #42c02e;
    box-sizing: border-box;
}
.recommended-authors .list .name {
    padding-top: 5px;
    margin-right: 60px;
    font-size: 14px;
    display: block;
    box-sizing: border-box;
}
.recommended-authors .list p {
    font-size: 12px;
    color: #969696;
    margin: 0 0 10px;
    box-sizing: border-box;
}
.recommended-authors .find-more {
    position: absolute;
    padding: 7px 7px 7px 12px;
    left: 0;
    width: 100%;
    font-size: 13px;
    color: #787878;
    background-color: #f7f7f7;
    border: 1px solid #dcdcdc;
    border-radius: 4px;
}
.row:after {
    clear: both;
}
.el-carousel__item h3 {
    color: #475669;
    font-size: 14px;
    opacity: 0.75;
    line-height: 150px;
    margin: 0;
}

.el-carousel__item:nth-child(2n) {
    background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n+1) {
    background-color: #d3dce6;
}
</style>
