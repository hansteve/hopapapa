#! /usr/bin/env python
# coding=utf-8

from src.common.wangyi.ServerAPI import ServerAPI

AppKey = 'd79963a97679ed3ba57e94f46585a13d';
AppSecret = '38e52a6c968d';
##p = ServerAPI(AppKey,AppSecret);
p = ServerAPI(AppKey, AppSecret, UseSSLLib=True);

##创建云信Id
##print( p.createUserId('hzchensheng1234') ) ;
##更新云信Id
print(p.updateUserId('user1'));
##更新并获取新token
##print( p.updateUserToken('user1') ) ;
##封禁云信ID
##print( p.blockUserId('user1') ) ;
##解禁云信ID
##print( p.unblockUserId('user1') ) ;
##更新用户名片
##print( p.updateUinfo('user1') ) ;
## 获取用户名片
##print( p.getUinfos( ['user1','user2'] ) ) ;
## 好友关系-加好友
##print( p.addFriend('user1','user2','1','请求的话') );
## 好友关系-更新好友关系
##print( p.updateFriend('user1','user2','备注') );
## 好友关系-获取好友关系
##print( p.getFriend('user1') );
## 好友关系-删除好友信息
##print( p.deleteFriend('user1','user2') );
## 好友关系-设置黑名单
##print( p.specializeFriend('user1','user2','1','0') );
## 好友关系-查看黑名单
##print( p.listBlackFriend('user1') );
##消息功能-发送普通消息
##print( p.sendMsg('user1','0','user2','0',dict({'msg':'hello'}),dict({"push":'false',"roam":'true',"history":'true',"sendersync":'true', "route":'false'}) ) );
##消息功能-发送自定义系统消息
##print( p.sendAttachMsg('user1','0','user2','helloworld') );
##消息功能-文件上传
##print( p.uploadMsg(base64.b64encode('gwettwgsgssgs323f'),'0') );
##消息功能-文件上传（multipart方式）
##print( p.uploadMultiMsg( base64.b64encode('gwettwgsgssgs323f') ) );

##群组功能（高级群）-创建群
##print( p.createGroup('groupname','user1',['user1','user2'],'','','invite','0','0','') );
##群组功能（高级群）-拉人入群
##print( p.addIntoGroup('432510','user1',['user1','user2'],'0','请您入伙') );
##群组功能（高级群）-踢人出群
##print( p.kickFromGroup('432510','user1','user2' ) );
##群组功能（高级群）-踢人出群
##print( p.removeGroup('432510','user1' ) );
##群组功能（高级群）-更新群资料
##print( p.updateGroup('432520','user1','groupname') );
##群组功能（高级群）-群信息与成员列表查询
##print( p.queryGroup(['432520'] ) );
##群组功能（高级群）-移交群主
##print( p.changeGroupOwner('432510','user1','user1','2' ) );
##群组功能（高级群）-任命管理员
##print( p.addGroupManager('432510','user1',['user2'] ) );
##群组功能（高级群）-移除管理员
##print( p.removeGroupManager('432510','user1',['user2'] ) );
##群组功能（高级群）-获取某用户所加入的群信息
##print( p.joinTeams('user1') );
##群组功能（高级群）-修改群昵称
##print( p.updateGroupNick('432510','user1','user1','xxx' ) );

##历史记录-单聊
##print( p.querySessionMsg('user1','user2',int(time.time()*1000-2000000),int(time.time()*1000),'100','2' ) );
##历史记录-群聊
##print( p.queryGroupMsg('432520','user1',int(time.time()*1000-2000000),int(time.time()*1000),'100','2' ) );

##发送短信验证码
##print( p.sendSmsCode('phonenum1','') );
##校验验证码
##print( p.verifycode('phonenum1','验证码') );
##发送模板短信
##print( p.sendSMSTemplate('templateid',['phonenum1'] ) );
##查询模板短信发送状态
##print( p.querySMSStatus('templateid') );

##发起单人专线电话
##print( p.startcall('user1','phonenum1','phonenum2',60) );
##发起专线会议电话
##print( p.startconf('user1','phonenum1',['phonenum2','phonenum3'],60) );
##查询单通专线电话或会议的详情
##print( p.queryCallsBySession('user1','0') );
