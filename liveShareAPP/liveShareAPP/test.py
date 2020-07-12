import re
content = "生活趣事！生活趣事![people.jpeg](http://192.168.106.131:8888/group1/M00/00/00/wKhqg17ZBoeARsGeAABddQ7YSuQ2772545)"
print(content.find("(") - content.find("]"))
#先提取url
index1 = content.find("(")
index2 = content.find(")")
image_url = content[index1 + 1:index2]
print(image_url)

# 提取文章内容段进行拼接
content = content[0:index1] + content[index2 + 1:]
content1 = content.find("[")
content2 = content.find("]")
content_article = content[0:content1] + content[content2 + 1:]
print(content_article)