# 基于测试框架的测试平台



## 技术栈

### 前端

- Node.js
- Vue2

使用vue-admin-template开源基础脚手架：https://github.com/PanJiaChen/vue-element-admin

### 后端

- Python3
- Django-ninja（官方文档：https://django-ninja.rest-framework.com）



## 部署

### 前端

- nginx

- 打包

  ```shell
  npm run build:prod
  ```

  

### 后端





## jwt

全称： json web token

用于前后端分离/微信小程序/app开发的用户认证

- 基于传统的token认证
  - 用户登录，服务端返回token，并将token保存在服务端，以后用户再来访问时，需要携带token，服务端获取token后，再去数据库中获取token进行校验
- jwt
  - 用户登录，服务端给用户返回一个token（服务端不保存），以后用户再来访问，需要携带token，服务端获取token后，再做token的校验
  - 优势：相较于传统的token相比，它无需在服务端保存token



## jwt实现过程

- 第一步：用户提交用户名和密码给服务端，如果登录成功，使用jwt创建一个token，并给用户返回
  - 注意：jwt生成的token是由三段字符串组成，并且用`.`连接起来
    - 第一段字符串：HEADER，内部包含算法/token类型，JSON转化成字符串，然后做base64url加密（加密，在加字符替换）
    - 第二段字符串：payload，自定义值，json转化成字符串，然后做base64url加密（加密，在加字符替换）
    - 第三段字符串：
      - 第一步：将上述第一段、二段密文拼接起来
      - 第二步：对上述前两端进行HS256加密 + 加盐
      - 第三步：对HS256加密后的密文在做base64url加密
- 第二步：用户在进行访问时，需要携带token，后端需要对token进行校验
  - 获取token
    - 第一步：对token进行切割
    - 第二步：对第二段进行base64url解密，并获取payload信息，检测token是否超时
    - 第三步：把第一、二段进行拼接再次HS256加密，密文进行比较，如果相等，则认证通过



## 应用

安装：`pip install pyjwt`