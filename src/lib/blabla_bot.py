import pycurl
import cStringIO
import json

#HOOK_URL="http://hook.dooray.com/services/1387695619080878080/1688914151759469773/AOPFTLJxT3KkHLE1mG710g"
HOOK_URL="http://hook.dooray.com/services/1387695619080878080/1707740231284618893/s6Fu8M-WQ3-XM32PMDT53w"
ICON_URL="http://t1.daumcdn.net/liveboard/bloter/90b9e7c6a5424637b44ff3dc0977ed2b.jpg"
BOT_NAME="Alertor"

response = cStringIO.StringIO()

def generate_post_data(msg):
    fmt = json.dumps({"botName":BOT_NAME, "botIconImage":ICON_URL, "text": msg})
    return fmt

def send_data(url, post_data):
    ret = False
    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.HTTPHEADER, ['Content-Type: application/json'])
    curl.setopt(pycurl.POSTFIELDS, post_data)
    curl.setopt(pycurl.WRITEFUNCTION, response.write)

    try:
        curl.perform()
        http_code = curl.getinfo(pycurl.HTTP_CODE)
        if http_code is 200:
            ret = True
    except:
        print "Error"

    curl.close()
    return ret
