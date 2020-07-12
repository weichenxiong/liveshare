from rest_framework import serializers
from .models import ArticleImage


#图片上传序列化器
class ArticleImageModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArticleImage
        fields = ['link']

    def create(self, validated_data):
        """保存数据"""

        link = validated_data.get("link") #接受client传回来的图片link
        instance = ArticleImage.objects.create(link=link)
        instance.group = str(instance.link).split('/')[0] # 保存到storage　的group中
        instance.save()
        return instance

from .models import ArticleCollection
class ArticleCollectionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleCollection
        fields = ["id", "name"]

    def validate(self, attrs):
        """验证数据"""
        name = attrs.get("name") #　获取文集名称
        user = self.context["request"].user
        try:
            ArticleCollection.objects.get(user=user, name=name)
            raise serializers.ValidationError("当前文集已创建！")
        except ArticleCollection.DoesNotExist:
            pass
        return attrs

    def create(self, validated_data):
        """创建文集"""
        name = validated_data.get("name") #　获取文集名称
        user = self.context["request"].user
        isinstance = ArticleCollection.objects.create(user=user, name=name)
        return isinstance



class ArticleCollectionDetailModelSerializer(serializers.ModelSerializer):
    """
    文集编辑序列化器
    """
    class Meta:
        model = ArticleCollection
        fields = ["id", "name"]

    def validate(self, attrs):
        id = self.context["view"].kwargs["pk"]
        name = attrs.get("name")
        user = self.context["request"].user
        try:
            ArticleCollection.objects.get(user=user, id=id)
        except ArticleCollection.DoesNotExist:
            raise serializers.ValidationError("当前文集无法修改！")

        try:
            ArticleCollection.objects.get(user=user, name=name)
            raise serializers.ValidationError("文集名称已存在，请更换名称！")
        except ArticleCollection.DoesNotExist:
            pass
        return attrs

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name")
        instance.save()
        return instance


from .models import Article
import re

class ArticleModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ["id", "title", "content", "collection", "save_id","article_image","is_public"]

    def validate(self, attrs):
        #获取内容,验证
        content = attrs.get("content")
        if len(content) > 0:
            #判断内容是否包含了恶意代码，防止客户端遭到跨站脚本攻击
            content = re.match("(<)(.*?script.*?)", "&lt;\\2&gt;", content)[0]
            #正则捕获模式，可以提取正则中的小括号里面的内容
            attrs["content"] = content

        return attrs

    def create(self, validated_data):
        isinstance = Article.objects.create(
            title=validated_data.get("title"),
            content = validated_data.get("content"),
            collection=validated_data.get("collection"),
            user=self.context["request"].user,

        )
        return isinstance


from .models import Special
class SpecialModelSerializer(serializers.ModelSerializer):
    post_status = serializers.BooleanField(read_only=True, help_text="文章的收录状态")
    class Meta:
        model = Special
        fields = ["id","name","image","article_count","follow_count","collect_count", "post_status"]


from users.models import User
class AuthorModelSerializer(serializers.ModelSerializer):
    """文章作者"""
    class Meta:
        model = User
        fields = "__all__" # 自己编写需要显示的字段即可

from .models import ArticleCollection
class CollectionInfoModelSerializer(serializers.ModelSerializer):
    """文集信息"""
    class Meta:
        model = ArticleCollection
        fields = "__all__" # 自己编写需要显示的字段即可

class ArticleInfoModelSerializer(serializers.ModelSerializer):
    user = AuthorModelSerializer()
    collection = CollectionInfoModelSerializer()
    class Meta:
        model = Article
        fields = [
            "title", "content", "user",
            "collection", "pub_date",
            "read_count", "like_count",
            "collect_count", "comment_count",
            "reward_count","article_image",
        ]

