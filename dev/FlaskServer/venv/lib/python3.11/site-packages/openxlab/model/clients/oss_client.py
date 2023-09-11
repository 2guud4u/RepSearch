import oss2
import os
import sys
from openxlab.model.common.constants import oss_bucket_domain


class OssClient(object):
    def __init__(self, endpoint, access_key_id, access_key_secret, security_token, bucket_name):
        self.bucket = self.bucket(endpoint, access_key_id, access_key_secret, security_token, bucket_name)

    @staticmethod
    def bucket(endpoint, access_key_id, access_key_secret, security_token, bucket_name):
        auth = oss2.StsAuth(access_key_id, access_key_secret, security_token)
        bucket = oss2.Bucket(auth, endpoint, bucket_name)
        return bucket

    def upload_to_oss(self, local_file_path, object_key, callback, callback_var):
        headers = {'Host': oss_bucket_domain, 'x-oss-callback': callback, 'x-oss-callback-var': callback_var}
        self.bucket.put_object_from_file(object_key, local_file_path, headers, progress_callback=percentage)


# consumed_bytes表示已上传的数据量。
# total_bytes表示待上传的总数据量。当无法确定待上传的数据长度时，total_bytes的值为None。
def percentage(consumed_bytes, total_bytes):
    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        print(f'{consumed_bytes}/{total_bytes} |  {rate}% has been uploaded!')
        sys.stdout.flush()
