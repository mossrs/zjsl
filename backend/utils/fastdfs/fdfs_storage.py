from django.conf import settings
from django.core.files.storage import Storage


class FastDFSStorage(Storage):
    """
        自定义文件存储系统 修改存储的方案
    """

    def __init__(self, fdfs_base_url=None):
        # 得到一个url前缀
        self.fdfs_base_url = fdfs_base_url or settings.FDFS_BASE_URL

    def url(self, name):
        """
            参数 图片在数据库中的相对地址
            返回name所指的文件绝对url
        """
        return self.fdfs_base_url + name
