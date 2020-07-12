
#liveshare

import xadmin
from xadmin import views


class BaseSetting(object):
    '''
    xadmin的基本设置
    '''
    enable_themes = True # 开启主题切换功能
    use_bootswatch = True

xadmin.site.register(views.BaseAdminView, BaseSetting)


class GlobalSettings(object):
    """
    xadmin的全局配置
    """
    site_title = "liveShare" # 设置站点标题
    site_footer = "分享生活,分析人生"
    site_style = "accordion" #　设置折叠菜单

xadmin.site.register(views.CommAdminView, GlobalSettings)