#general library
#import OCR library
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
from gtts import gTTS
import time,sys,uuid,requests,base64,hashlib,json,time,cv2,os,csv
from playsound import playsound
from imp import reload
reload(sys)

YOUDAO_URL = 'https://openapi.youdao.com/ocrapi'
APP_KEY = 'xxx'
APP_SECRET = 'xxx'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
i=0
filter1=''
audiono=i
knowledgebase=[]

def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]

def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()

def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)

cap=cv2.VideoCapture(1)
#default video cam source is 0, back is 1
fourcc=cv2.VideoWriter_fourcc(*'XVID')
out1=cv2.VideoWriter('/Users/ender/Dropbox/Python/Learning/Python Practice/OpenCV/resource/output.avi',fourcc,20.0,(640,480))

def talkfunction():
    job=gTTS(text=filter1[:100],lang='zh-tw',slow=False,tld='com')
    job.save("/Users/ender/OneDrive/Desktop/Python/0.mp3")
    playsound("/Users/ender/OneDrive/Desktop/Python/0.mp3")
    os.remove("/Users/ender/OneDrive/Desktop/Python/0.mp3")
    # job.save("/Users/ender/OneDrive/Desktop/Python/"+str(audiono)+".mp3")
    # playsound("/Users/ender/OneDrive/Desktop/Python/"+str(audiono)+".mp3")
    # os.remove("/Users/ender/OneDrive/Desktop/Python/"+str(audiono)+".mp3")
while(cap.isOpened()):
#check if cam is accessible
    ret,frame=cap.read()
    if ret==True:
        out1.write(frame)
        cv2.imshow('frame',frame)
        cv2.imwrite('a.jpg',frame)
        f = open(r'a.jpg', 'rb')  # 二进制方式打开图文件
        q = base64.b64encode(f.read()).decode('utf-8')  # 读取文件内容，转换为base64编码
        f.close()
        if q:
            data = {}
            data['detectType'] = '10012'
            data['imageType'] = '1'
            data['langType'] = 'zh-CHS'
            data['img'] = q
            data['docType'] = 'json'
            data['signType'] = 'v3'
            curtime = str(int(time.time()))
            data['curtime'] = curtime
            salt = str(uuid.uuid1())
            signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
            sign = encrypt(signStr)
            data['appKey'] = APP_KEY
            data['salt'] = salt
            data['sign'] = sign
            response = do_request(data)
            rawdata=response.content
            if cv2.waitKey(1)&0xFF==ord('a'):
            #use key A to capture when the live camera has a clear visual
                raw = json.loads(rawdata)
            #detect if the line has real value, if there is no value, we can not run gtts code
                if raw["Result"]["regions"]:
                    print('detected:..')
                    if raw["Result"]["regions"][0]["lines"]:
                        fullline=raw["Result"]["regions"][0]["lines"]
                        #print(type(fullline))
                        for x in range(0,len(fullline)):
                            filter1=raw["Result"]["regions"][0]["lines"][x]['text']
                            print(filter1)
                            #print(len(filter1))
                            #print(type(filter1))
                            talkfunction()
                            knowledgebase.extend(filter1)
                            print('stand by...')
                            with open('/Users/ender/Dropbox/Python/Test/readsmart/KnowledgeBase/cv.csv', 'a', newline = '', encoding = 'utf-8') as file:
                                writer = csv.writer(file)
                                writer.writerow(filter1)
                        StoreDecision=input('do you want to keep?')
                        if StoreDecision=='Y':
                            print(knowledgebase)
        elif cv2.waitKey(1)&0xFF==ord('q'):
            #exit keyboard code using Q
            break
cap.release()
out1.release()
cv2.destroyAllWindows()
#remember to release resources1
