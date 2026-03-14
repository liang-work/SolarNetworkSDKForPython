# Solar Network Python SDK API 文档

## 概述

Solar Network Python SDK 提供了与 Solar Network API 交互的完整解决方案。本 SDK 包含认证、账户管理、内容操作等所有核心功能。

## 安装

```bash
pip install solar-network-sdk
```

## 快速开始

### 基本认证

```python
from solar_network_sdk import SolarNetworkClient, WebAuthClient

# 创建客户端
client = SolarNetworkClient()

# 获取认证客户端
web_auth = client.get_web_auth_client()

# 获取认证 URL
auth_url = web_auth.get_authentication_url()
print(f"请在浏览器中打开: {auth_url}")

# 等待用户认证
auth_result = web_auth.wait_for_auth()

if auth_result.status == "challenge":
    # 签名挑战
    signed_challenge = sign_challenge(auth_result.challenge)
    
    # 交换令牌
    token_result = web_auth.exchange_token(signed_challenge)
    
    if token_result.status == "success":
        # 设置令牌
        client.set_token(token_result.token)
        
        # 现在可以进行认证请求
        account = client.get_account()
        print(f"你好, {account.name}!")
```

## 核心类

### SolarNetworkClient

主客户端类，提供所有 API 操作。

#### 构造函数

```python
SolarNetworkClient(
    server_url: str = "https://api.solian.app",
    token: Optional[str] = None,
    timeout: int = 30
)
```

**参数:**
- `server_url`: Solar Network API 服务器 URL
- `token`: 可选的认证令牌
- `timeout`: 请求超时时间（秒）

#### 方法

##### 认证相关

- `get_web_auth_client() -> WebAuthClient`
  - 获取 Web 认证客户端实例

##### 账户管理

- `get_account() -> Account`
  - 获取当前账户信息
  
- `update_account(**kwargs) -> Account`
  - 更新账户信息
  
- `get_account_profile() -> AccountProfile`
  - 获取账户配置文件
  
- `update_account_profile(**kwargs) -> AccountProfile`
  - 更新账户配置文件
  
- `get_account_status() -> AccountStatus`
  - 获取账户状态
  
- `set_account_status(attitude: int, type: int = 0, label: str = "", symbol: Optional[str] = None, meta: Optional[Dict[str, Any]] = None) -> AccountStatus`
  - 设置账户状态
  
- `clear_account_status() -> None`
  - 清除账户状态

##### 活动操作

- `check_in() -> CheckInResult`
  - 执行每日签到
  
- `get_notable_days(start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[NotableDay]`
  - 获取显著日期
  
- `get_timeline_events(limit: int = 20, offset: int = 0, types: Optional[List[str]] = None) -> List[TimelineEvent]`
  - 获取时间线事件

##### 聊天操作

- `get_chat_rooms(limit: int = 20, offset: int = 0, types: Optional[List[int]] = None) -> List[ChatRoom]`
  - 获取聊天室列表
  
- `get_chat_messages(room_id: str, limit: int = 50, before: Optional[str] = None, after: Optional[str] = None) -> List[ChatMessage]`
  - 获取聊天室消息
  
- `send_chat_message(room_id: str, content: str, type: str = "text", nonce: Optional[str] = None, meta: Optional[Dict[str, Any]] = None) -> ChatMessage`
  - 发送聊天消息

##### 文件操作

- `get_file_pools() -> List[FilePool]`
  - 获取文件池列表
  
- `get_cloud_files(limit: int = 50, offset: int = 0, pool_id: Optional[str] = None) -> List[CloudFile]`
  - 获取云文件列表
  
- `upload_file(file_path: str, pool_id: Optional[str] = None, name: Optional[str] = None, description: Optional[str] = None) -> DriveTask`
  - 上传文件

##### 帖子操作

- `create_post(content: str, title: Optional[str] = None, visibility: int = 0, type: int = 0, attachments: Optional[List[str]] = None, tags: Optional[List[str]] = None, categories: Optional[List[str]] = None) -> Post`
  - 创建帖子
  
- `get_posts(limit: int = 20, offset: int = 0, types: Optional[List[int]] = None, visibility: Optional[List[int]] = None) -> List[Post]`
  - 获取帖子列表

##### 钱包操作

- `get_wallet() -> Wallet`
  - 获取钱包信息
  
- `get_wallet_pockets() -> List[WalletPocket]`
  - 获取钱包口袋
  
- `get_wallet_transactions(limit: int = 50, offset: int = 0, types: Optional[List[int]] = None) -> List[Transaction]`
  - 获取钱包交易

##### 工具方法

- `set_token(token: str) -> None`
  - 设置认证令牌
  
- `clear_token() -> None`
  - 清除认证令牌

### WebAuthClient

Web 认证客户端，用于与 Solar Network 桌面应用进行认证交互。

#### 构造函数

```python
WebAuthClient(
    base_url: str = "http://127.0.0.1",
    default_port: int = 40000,
    web_url: str = "https://app.solian.fr"
)
```

**参数:**
- `base_url`: 本地服务器基础 URL
- `default_port`: 默认连接端口
- `web_url`: Solar Network Web URL

#### 属性

- `port: int`
  - 获取/设置当前端口

#### 方法

##### URL 生成

- `get_authentication_url() -> str`
  - 获取认证 URL
  
- `get_protocol_challenge_url(app_slug: str, redirect_uri: str, state: Optional[str] = None) -> str`
  - 获取协议挑战 URL
  
- `get_protocol_exchange_url(signed_challenge: str, redirect_uri: str, secret_id: Optional[str] = None, state: Optional[str] = None) -> str`
  - 获取协议交换 URL

##### 认证流程

- `wait_for_auth(port: Optional[int] = None, app_name: str = "PythonApp") -> WebAuthResult`
  - 等待用户认证响应
  
- `exchange_token(signed_challenge: str, port: Optional[int] = None, device_info: Optional[Dict[str, Any]] = None, secret_id: Optional[str] = None) -> WebAuthResult`
  - 交换认证令牌
  
- `fetch_account_info(port: Optional[int] = None, token: str = "") -> Dict[str, Union[bool, Optional[Dict[str, Any]], Optional[str]]]`
  - 获取账户信息
  
- `authenticate(app_name: str = "PythonApp", sign_challenge: Optional[callable] = None) -> WebAuthResult`
  - 完整认证流程

## 数据模型

### Account

账户信息模型。

**字段:**
- `id: str` - 账户 ID
- `name: str` - 账户名称
- `email: str` - 邮箱地址
- `status: int` - 账户状态
- `created_at: datetime` - 创建时间

### AccountProfile

账户配置文件模型。

**字段:**
- `nick: str` - 昵称
- `birthday: Optional[datetime]` - 生日
- `gender: int` - 性别
- `bio: str` - 个人简介

### ChatRoom

聊天室模型。

**字段:**
- `id: str` - 聊天室 ID
- `name: str` - 聊天室名称
- `type: int` - 聊天室类型
- `is_public: bool` - 是否公开

### CloudFile

云文件模型。

**字段:**
- `id: str` - 文件 ID
- `name: str` - 文件名
- `size: int` - 文件大小
- `mime_type: str` - MIME 类型
- `url: str` - 文件 URL

### Post

帖子模型。

**字段:**
- `id: str` - 帖子 ID
- `title: str` - 帖子标题
- `content: str` - 帖子内容
- `visibility: int` - 可见性
- `created_at: datetime` - 创建时间

### Wallet

钱包模型。

**字段:**
- `id: str` - 钱包 ID
- `pockets: List[WalletPocket]` - 钱包口袋列表

### WalletPocket

钱包口袋模型。

**字段:**
- `currency: str` - 货币类型
- `amount: float` - 金额

## 错误处理

所有 API 方法都可能抛出异常。建议使用 try-catch 块进行错误处理：

```python
try:
    account = client.get_account()
    print(f"账户信息: {account.name}")
except Exception as e:
    print(f"获取账户信息失败: {e}")
```

## 分页

大多数列表方法都支持分页参数：

- `limit`: 返回项目数量
- `offset`: 偏移量
- `before/after`: 时间戳分页

示例：

```python
# 获取前 20 个项目
items = client.get_posts(limit=20, offset=0)

# 获取下一页
next_items = client.get_posts(limit=20, offset=20)
```

## 异步支持

分页控制器支持异步操作：

```python
from solar_network_sdk.pagination import AsyncPaginationController

async def fetch_data():
    controller = AsyncPaginationController(fetch_func)
    await controller.refresh()
    await controller.fetch_further()
```

## 最佳实践

1. **认证安全**: 始终使用安全的方式存储和传输认证令牌
2. **错误处理**: 为所有 API 调用添加适当的错误处理
3. **分页**: 处理大量数据时使用分页
4. **超时**: 根据需要调整请求超时时间
5. **类型检查**: 利用类型注解提高代码质量

## 贡献

欢迎贡献代码！请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详细信息。

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件。