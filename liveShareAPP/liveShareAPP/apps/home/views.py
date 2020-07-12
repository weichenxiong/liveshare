"""
--code--: utf-8
__ author__: wcx
date:2020-07-07
version:1.0
"""

from django.shortcuts import render
from rest_framework.generics import ListAPIView
from article.models import Article
from .serializers import ArticleListModelSerializer
from .paginations import HomeArticlePageNumberPagination
from tablestore import *
from django.conf import settings
from users.models import User
from datetime import datetime
from liveShareAPP.utils.ItemCF import ItemCF

class ArticleListAPIView(ListAPIView):
    # queryset = Article.objects.all()
    serializer_class = ArticleListModelSerializer
    pagination_class = HomeArticlePageNumberPagination
    @property
    def client(self):
        return OTSClient(settings.OTS_ENDPOINT, settings.OTS_ID, settings.OTS_SECRET, settings.OTS_INSTANCE)

    def get_queryset(self):
        week_timestamp = datetime.now().timestamp() - 7 * 86400
        week_date = datetime.fromtimestamp(week_timestamp) # 获取一周前的时间对象
        queryset = Article.objects.filter(pub_date__gte=week_date).exclude(pub_date=None,).order_by("-reward_count","-comment_count","-like_count","-id")
        print("queryset:",queryset)
        # 记录本次给用户推送文章的记录
        user = self.request.user
        if isinstance(user, User):
            queryset1 = []
            #查询当前用户关注的作者是否有新的推送[查询同步库]
            #先到未读池中提取当前访问用户上一次服务Feed的最大主键
            start_sequence_id = self.get_start_sequence_id(user.id)
            #然后根据主键到同步库中查看数据
            message_id_list = self.get_feed_message(user.id,start_sequence_id)
            if len(message_id_list) >= 10:#同步库中有数据
                queryset = queryset.filter(id__in=message_id_list)
                limit_num = 0
            else:
                #基于物品进行协同过滤推荐文章
                message_id_list = self.get_message_by_itemCF(user.id)
                if len(message_id_list) > 0:
                    queryset1 = queryset.filter(id__in=message_id_list)
                    queryset1 = list(queryset1)
            #判断tablestore中是否曾经推送过当前文章给用户
            queryset2 = self.check_user_message_log(user,queryset)
            queryset2 = list(queryset2)
            queryset = queryset1 + queryset2
            queryset = list(set(queryset))[:10]
            if len(queryset)>0:
                article_id_list = []
                for item in queryset:
                    article_id_list.append(item.id)
                self.push_log(user.id, article_id_list)
        return queryset

    def get_user_read_history(self,user_id):
        """查询用户近１个月的浏览历史记录"""
        table_name = "user_message_log_table"
        #范围查询的起始主键
        inclusive_start_primary_key = [
            ("user_id",user_id),
            ("message_id",INF_MIN)
        ]
        #范围查询的结束主键
        exclusive_end_primary_key = [
            ("user_id",user_id),
            ("message_id",INF_MAX)
        ]
        #查询所有列
        columns_to_get = [] #表示返回所有列
        # 设置多条件
        cond = CompositeColumnCondition(LogicalOperator.AND)  # 逻辑条件
        # 多条件下的子条件
        cond.add_sub_condition(SingleColumnCondition("is_push", True, ComparatorType.EQUAL))  # 比较运算符:　等于
        cond.add_sub_condition(SingleColumnCondition("is_read", True, ComparatorType.EQUAL))  # 比较运算符:　等于

        consumed, next_start_primary_key, row_list, next_token = self.client.get_range(
            table_name,  # 操作表明
            Direction.FORWARD,  # 范围的方向，字符串格式，取值包括'FORWARD'和'BACKWARD'。
            inclusive_start_primary_key, exclusive_end_primary_key,  # 取值范围
            columns_to_get,  # 返回字段列
            column_filter=cond,  # 条件
            max_version=1  # 返回版本数量
        )
        data = []
        if len(row_list) == 0:
            return data
        for row in row_list:
            data.append(row.primary_key[1][1])
        return data

    def get_user_by_message_id(self,message_id):
        """根据文章id获取用户列表"""
        table_name = "user_message_log_table"
        # 范围查询的起始主键
        inclusive_start_primary_key = [
            ('user_id', INF_MIN),
            ('message_id', message_id)
        ]
        # 范围查询的结束主键
        exclusive_end_primary_key = [
            ('user_id', INF_MAX),
            ('message_id', message_id)
        ]
        # 查询所有列
        columns_to_get = []  # 表示返回所有列
        # 设置多条件
        cond = CompositeColumnCondition(LogicalOperator.AND)  # 逻辑条件
        # 多条件下的子条件
        cond.add_sub_condition(SingleColumnCondition("is_push", True, ComparatorType.EQUAL))  # 比较运算符:　等于
        cond.add_sub_condition(SingleColumnCondition("is_read", True, ComparatorType.EQUAL))  # 比较运算符:　等于
        consumed, next_start_primary_key, row_list, next_token = self.client.get_range(
            table_name,  # 操作表明
            Direction.FORWARD,  # 范围的方向，字符串格式，取值包括'FORWARD'和'BACKWARD'。
            inclusive_start_primary_key, exclusive_end_primary_key,  # 取值范围
            columns_to_get,  # 返回字段列
            column_filter=cond,  # 条件
            max_version=1  # 返回版本数量
        )
        data = set()
        if len(row_list) == 0:
            return list(data)
        for row in row_list:
            data.add(row.primary_key[0][1])
        return list(data)

    def find_user_by_history(self,message_list):
        """根据阅读文章列表的记录查询出阅读这些文章的用户"""
        users = []
        for message_id in message_list:
            users += self.get_user_by_message_id(message_id)
        users = list(set(users))
        return users

    def find_message_by_user(self,users):
        allUserItemsStartList = []#用户和文章之间的矩阵关系
        messages = [] #文章列表
        users_message = [] #所有用户读取过的文章列表
        for user_id in users:
            ret = self.get_user_read_history(user_id)
            messages += ret
            users_message.append(ret)
        messages = list(set(messages))
        for item_user_message in users_message:
            message_list = []
            for msg in messages:
                message_list.append( 1 if(msg in item_user_message) else 0)
            allUserItemsStartList.append(message_list)
        return allUserItemsStartList

    def get_message_by_itemCF(self,user_id):
        """基于物品的协同过滤获取Feed内容"""
        current_user_history_list = self.get_user_read_history(user_id)
        if len(current_user_history_list) == 0:
            return []
        #根据浏览历史记录查到曾经浏览过的文章的所有用户
        users = self.find_user_by_history(current_user_history_list)
        if len(users) == 0:
            return []
        #用户和物品的关系［点赞，赞赏，阅读，收藏］，文章id列表
        allUserItemsStarList,messages = self.find_message_by_user(users)
        if len(allUserItemsStarList) <1 or len(messages) < 1:
            return []

        cf = ItemCF(users,messages,allUserItemsStarList)
        return cf.calrecommendMoive(user_id)

    def get_feed_message(self,user_id,start_sequence_id):
        """获取同步库中的数据"""
        table_name = "user_message_table"
        # 范围查询的起始主键
        inclusive_start_primary_key = [
            ('user_id', user_id),
            ('sequence_id', start_sequence_id),
            ('sender_id', INF_MIN),
            ('message_id', INF_MIN)
        ]
        # 范围查询的结束主键
        exclusive_end_primary_key = [
            ('user_id', user_id),
            ('sequence_id', INF_MAX),
            ('sender_id', INF_MAX),
            ('message_id', INF_MAX),
        ]
        columns_to_get = []  # 表示返回所有列
        limit = 10
        consumed, next_start_primary_key, row_list, next_token = self.client.get_range(
            table_name,  # 操作表明
            Direction.FORWARD,  # 范围的方向，字符串格式，取值包括'FORWARD'和'BACKWARD'。
            inclusive_start_primary_key, exclusive_end_primary_key,  # 取值范围
            columns_to_get,  # 返回字段列
            limit,  # 结果数量
            max_version=1  # 返回版本数量
        )
        message_id_list = []
        for item in row_list:
            message_id_list.append(item.primary_key[3][1])
        # 下一次读取同步库的开始主键
        try:
            self.set_start_sequence_id(user_id, start_sequence_id, next_start_primary_key[1][1])
        except:
            pass
        return message_id_list

    def set_start_sequence_id(self, user_id,old_start_sequence_id, next_start_primary_key):
        table_name = "user_message_session_table"
        try:
            primary_key = [('user_id', user_id), ('last_sequence_id', old_start_sequence_id)]
            row = Row(primary_key)
            consumed, return_row = self.client.delete_row(table_name,row,None)
        except:
            pass
        primary_key = [('user_id', user_id), ('last_sequence_id', next_start_primary_key)]
        attribute_columns = []
        row = Row(primary_key,attribute_columns)
        consumed,return_row = self.client.put_row(table_name,row)
        # print(return_row)
        return return_row

    def get_start_sequence_id(self,user_id):
        """获取最后读取的Feed流id"""
        table_name = "user_message_session_table"
        #范围查询的起始主键
        inclusive_start_primary_key = [
            ('user_id', user_id),
            ('last_sequence_id', INF_MIN)
        ]
        # 范围查询的结束主键
        exclusive_end_primary_key = [
            ('user_id', user_id),
            ('last_sequence_id', INF_MAX)
        ]
        columns_to_get = []#表示返回所有列
        limit = 1
        consumed, next_start_primary_key, row_list, next_token = self.client.get_range(
            table_name,  # 操作表明
            Direction.FORWARD,  # 范围的方向，字符串格式，取值包括'FORWARD'和'BACKWARD'。
            inclusive_start_primary_key, exclusive_end_primary_key,  # 取值范围
            columns_to_get,  # 返回字段列
            limit,  # 结果数量
            # column_filter=cond, # 条件
            max_version=1  # 返回版本数量
        )
        if len(row_list) < 1:
            #之前没有读取过推送内容
            return INF_MIN
        else:
            return row_list[0].primary_key[1][1]

    def check_user_message_log(self, user, queryset):
        """判断系统是否曾经推送过文章给用户"""
        columns_to_get = []
        rows_to_get = []
        for article in queryset:
            primary_key = [('user_id', user.id), ('message_id', article.id)]
            rows_to_get.append(primary_key)
        request = BatchGetRowRequest()
        table_name = "user_message_log_table"

        cond = CompositeColumnCondition(LogicalOperator.OR)
        cond.add_sub_condition(SingleColumnCondition("is_read", True, ComparatorType.EQUAL))
        cond.add_sub_condition(SingleColumnCondition("is_like", True, ComparatorType.EQUAL))

        request.add(TableInBatchGetRowItem(table_name, rows_to_get, columns_to_get,column_filter=cond, max_version=1))
        result = self.client.batch_get_row(request)
        table_result = result.get_result_by_table(table_name)
        # print("table_result:",table_result)
        push_id_list = []
        for item in table_result:
            if item.row is not None:
                push_id_list.append(item.row.primary_key[1][1])
        return queryset.exclude(id__in=push_id_list)

    def push_log(self, user_id, article_id_list):
        """推送文章给用户的记录"""
        table_name = "user_message_log_table"
        put_row_items = []
        for i in article_id_list:
            # 主键列
            primary_key = [
                ('user_id', user_id),  # 用户ID
                ("message_id", i),  # 文章ID
            ]
            attribute_columns = [('is_push', True), ('is_read', False), ('is_like', False), ('is_reward',False), ('is_comment',False)]
            row = Row(primary_key, attribute_columns)
            condition = Condition(RowExistenceExpectation.IGNORE)
            item = PutRowItem(row, condition)
            put_row_items.append(item)

        request = BatchWriteRowRequest()
        request.add(TableInBatchWriteRowItem(table_name, put_row_items))
        result = self.client.batch_write_row(request)
        return result.is_all_succeed()