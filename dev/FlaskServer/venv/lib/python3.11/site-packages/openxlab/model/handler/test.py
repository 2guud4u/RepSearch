from openxlab.model.handler.model_inference import inference
from openxlab.model.handler.model_inference import Inference
from openxlab.model import create
import openxlab
# method1
openxlab.login(ak="vegl9yn4xwd0nqz5rrwm", sk="x8an3z7ad9o0vw4don3g1jebvy6vggbeok2pekrq", re_login=True)
infer = Inference("meijiawen1/inference-image-classfication")
# infer.inference(['./demo_text_ocr.jpg'], var1='1', var2='2', var3=3)
result = infer.inference(['./demo_text_ocr.jpg'])
result.tojson()
# print(result)
# print(result.predictions)
# print(result.visualization)
# print(result.tojson())
# print(result.save_base64_images())
# method2
# inference("mmocr/SVTR", ['./demo_text_ocr.jpg'], var1='1', var2='2', var3=3)
# openxlab.login(ak="zbp7y9yer7ywrzv90jwe", sk="v4owjbd1e9qedvnybaoap8oegpr68akyzwxbmrgo", re_login=True)
# inference("demooooooo/CLIP", ['./demo_text_ocr.jpg'])

# import openxlab
#
# openxlab.login(ak='vegl9yn4xwd0nqz5rrwm', sk='x8an3z7ad9o0vw4don3g1jebvy6vggbeok2pekrq', re_login=True)
# download_metafile_template()

create('dongxiaozhuang/didigo')