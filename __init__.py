#import winrt.windows.ui.notifications as notifications
#import winrt.windows.data.xml.dom as dom
import enum
import sys

import winsdk.windows.ui.notifications as notifications
import winsdk.windows.data.xml.dom as dom
from winsdk.windows.foundation import IPropertyValue
from winsdk.windows.ui.notifications import ToastActivatedEventArgs, ToastDismissedEventArgs, ToastFailedEventArgs,ToastDismissalReason
#from winsdk.windows.foundation import DateTime
import time


#__all__=['通知','通知器','ToastDismissalReason']

class 通知消除原因(enum.IntEnum):
    #https://docs.microsoft.com/zh-cn/uwp/api/windows.ui.notifications.toastdismissalreason
    用户取消 = 0
    应用隐藏 = 1
    超时 = 2


def 转换时间戳为64位(t0:int)->int:
    t1=int(t0)
    if t1<=4294967296:
        return t1*10000000+116444736000000000
    else:
        return t1

#def 转换时间(t0:int)->DateTime:
#    return DateTime(转换时间戳为64位(t0))

def 转换xml(s:str)->dom.XmlDocument:
    xDoc=dom.XmlDocument()
    xDoc.load_xml(s)
    #不加background并且使用其他的application_id会导致toast消失
    #xDoc.first_child.owner_document.document_element.set_attribute('activationType','background')
    return xDoc

def 转换通知数据(values:dict,sequence_number:int):
    data=notifications.NotificationData()
    for i in values:
        data.values[i]=values[i]
    data.sequence_number=sequence_number
    return data


def 转换已激活回调(func):
    def f2(sender,event_args_d):
        event_args=ToastActivatedEventArgs._from(event_args_d)
        def 获取输入(input_id):
            IPropertyValue._from(event_args.user_input.lookup(input_id)).get_string()
        return func(event_args.arguments,获取输入)
    return f2


def 转换已消除回调(func):
    def f2(sender,event_args_d):
        event_args=ToastDismissedEventArgs._from(event_args_d)
        原因=通知消除原因(event_args.reason)
        return func(原因)
    return f2


class 通知:
    def __init__(s,xml,已激活回调=None,已消除回调=None,失败回调=None,过期时间=None,标签=None,组=None):
            
        s.通知=notifications.ToastNotification(转换xml(xml))
        if 已激活回调:
            s.添加已激活回调(已激活回调)
        if 已消除回调:
            s.添加已消除回调(已消除回调)
        if 失败回调:
            s.添加失败回调(失败回调)

        if 过期时间:
            s.设置过期时间(过期时间)
        

        if 标签:
            s.设置标签(标签)
        if 组:
            s.设置组(组)
    
    def 添加已激活回调(s,回调):
        s.通知.add_activated(转换已激活回调(回调))
        return s

    def 添加已消除回调(s,回调):
        s.通知.add_dismissed(转换已消除回调(回调))
        return s

    def 添加失败回调(s,回调):
        s.通知.add_failed(回调)
        return s

    def 设置过期时间(s,过期时间:int):
        #s.通知.expiration_time=转换时间(过期时间)
        return s
    
    def 设置标签(s,标签:str):
        s.通知.tag=标签
        return s
    
    def 设置组(s,组:str):
        s.通知.group=组
        return s

    def 设置数据(s,values:dict,sequence_number:int):
        s.通知.data=转换通知数据(values,sequence_number)
        return s




class 通知器:
    def __init__(s,application_id):
        s.application_id=application_id
        s.notifier=notifications.ToastNotificationManager.create_toast_notifier(application_id)
        s.history:notifications.ToastNotificationHistory=nManager.get_history()

    def 显示(s,通知_:通知):
        return s.notifier.show(通知_.通知)
        
    

    def 更新通知(s,values:dict,sequence_number:int,tag,group=None):
        data=转换通知数据(values,sequence_number)
        if group:
            return s.notifier.update(data,tag,group)
        else:
            return s.notifier.update(data,tag)

    def 清除通知(s):
        return s.history.clear(s.application_id)


application_id=sys.executable

#create notifier
nManager = notifications.ToastNotificationManager
'''
#notifier = nManager.create_toast_notifier("{FF5265E8-6DAB-4BD4-A52D-8999008A07C8}")
#notifier = nManager.create_toast_notifier(r"D:\1\toast\1.bat")
print(application_id)
#notifier = nManager.create_toast_notifier(application_id)
notifier = nManager.create_toast_notifier('程序名 applicationId')

#notifier = nManager.create_toast_notifier(r"C:\Program Files (x86)\Tencent\QQ\Bin\QQScLauncher.exe")
'''

history:notifications.ToastNotificationHistory=nManager.get_history()

def 清除通知():
    history.clear(application_id)


#define your notification as 
#print(nManager.OnActivated)

#nManager.OnActivated=callback
