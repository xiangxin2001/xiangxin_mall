from fdfs_client.client import Fdfs_client

client = Fdfs_client(r"D:/html/xiangxin_mall/utils/fastdfs/client.conf")

ret = client.upload_by_filename('D:/html/xiangxin_mall/static/images/logo.png')
print(ret)