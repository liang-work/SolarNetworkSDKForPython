#!/usr/bin/env python3
"""
Solar Network Python SDK 使用示例

这个示例展示了如何使用 Solar Network Python SDK 进行基本操作。
"""

import asyncio
import os
from solar_network_sdk import SolarNetworkClient, WebAuthClient


def sign_challenge(challenge: str) -> str:
    """
    实现挑战签名逻辑。
    
    在实际应用中，你需要使用你的私钥对挑战进行签名。
    这里只是一个示例实现。
    
    Args:
        challenge: 需要签名的挑战字符串
        
    Returns:
        签名后的字符串
    """
    # TODO: 实现实际的签名逻辑
    # 例如使用 RSA、ECDSA 或其他签名算法
    print(f"需要对挑战进行签名: {challenge}")
    return f"signed_{challenge}"


async def main():
    """主函数，演示 SDK 的基本使用方法。"""
    
    print("=== Solar Network Python SDK 使用示例 ===\n")
    
    # 1. 创建客户端实例
    print("1. 创建 Solar Network 客户端...")
    client = SolarNetworkClient(
        server_url="https://api.solian.app",
        timeout=30
    )
    print("✓ 客户端创建成功\n")
    
    # 2. 获取 Web 认证客户端
    print("2. 获取 Web 认证客户端...")
    web_auth = client.get_web_auth_client(
        base_url="http://127.0.0.1",
        default_port=40000,
        web_url="https://app.solian.fr"
    )
    print("✓ Web 认证客户端获取成功\n")
    
    # 3. 获取认证 URL
    print("3. 获取认证 URL...")
    auth_url = web_auth.get_authentication_url()
    print(f"请在浏览器中打开以下 URL 进行认证:")
    print(f"   {auth_url}")
    print("认证完成后，程序将继续执行...\n")
    
    # 4. 等待用户认证
    print("4. 等待用户认证响应...")
    auth_result = web_auth.wait_for_auth(app_name="PythonSDKExample")
    
    if auth_result.status == "denied":
        print("❌ 用户拒绝了认证请求")
        return
    
    if auth_result.status != "challenge":
        print(f"❌ 认证失败: {auth_result.error}")
        return
    
    print("✓ 收到认证挑战\n")
    
    # 5. 签名挑战
    print("5. 签名认证挑战...")
    try:
        signed_challenge = sign_challenge(auth_result.challenge)
        print("✓ 挑战签名完成\n")
    except Exception as e:
        print(f"❌ 挑战签名失败: {e}")
        return
    
    # 6. 交换令牌
    print("6. 交换认证令牌...")
    token_result = web_auth.exchange_token(
        signed_challenge=signed_challenge,
        device_info={
            "platform": "Python",
            "version": "3.10",
            "app_name": "PythonSDKExample"
        }
    )
    
    if token_result.status != "success":
        print(f"❌ 令牌交换失败: {token_result.error}")
        return
    
    print("✓ 令牌交换成功\n")
    
    # 7. 设置认证令牌
    print("7. 设置认证令牌...")
    client.set_token(token_result.token)
    print("✓ 认证令牌设置成功\n")
    
    # 8. 获取账户信息
    print("8. 获取账户信息...")
    try:
        account = client.get_account()
        print(f"✓ 账户信息获取成功:")
        print(f"   ID: {account.id}")
        print(f"   名称: {account.name}")
        print(f"   邮箱: {account.email}")
        print(f"   状态: {account.status}")
        print()
    except Exception as e:
        print(f"❌ 获取账户信息失败: {e}")
        return
    
    # 9. 获取账户配置文件
    print("9. 获取账户配置文件...")
    try:
        profile = client.get_account_profile()
        print(f"✓ 账户配置文件获取成功:")
        print(f"   昵称: {profile.nick}")
        print(f"   生日: {profile.birthday}")
        print(f"   性别: {profile.gender}")
        print()
    except Exception as e:
        print(f"❌ 获取账户配置文件失败: {e}")
    
    # 10. 执行签到
    print("10. 执行每日签到...")
    try:
        checkin_result = client.check_in()
        print(f"✓ 签到成功:")
        print(f"   获得积分: {checkin_result.award}")
        print(f"   连续签到: {checkin_result.streak}")
        print()
    except Exception as e:
        print(f"❌ 签到失败: {e}")
        print()
    
    # 11. 获取聊天室
    print("11. 获取聊天室列表...")
    try:
        rooms = client.get_chat_rooms(limit=10)
        print(f"✓ 获取到 {len(rooms)} 个聊天室:")
        for room in rooms[:3]:  # 只显示前3个
            print(f"   - {room.name} (ID: {room.id})")
        if len(rooms) > 3:
            print(f"   ... 还有 {len(rooms) - 3} 个聊天室")
        print()
    except Exception as e:
        print(f"❌ 获取聊天室失败: {e}")
        print()
    
    # 12. 获取钱包信息
    print("12. 获取钱包信息...")
    try:
        wallet = client.get_wallet()
        print(f"✓ 钱包信息获取成功:")
        print(f"   钱包 ID: {wallet.id}")
        print()
        
        # 获取钱包口袋
        pockets = client.get_wallet_pockets()
        print(f"   钱包口袋 ({len(pockets)} 个):")
        for pocket in pockets:
            print(f"     - {pocket.currency}: {pocket.amount}")
        print()
        
    except Exception as e:
        print(f"❌ 获取钱包信息失败: {e}")
        print()
    
    # 13. 获取文件池
    print("13. 获取文件池...")
    try:
        pools = client.get_file_pools()
        print(f"✓ 获取到 {len(pools)} 个文件池:")
        for pool in pools:
            print(f"   - {pool.name} (ID: {pool.id})")
        print()
    except Exception as e:
        print(f"❌ 获取文件池失败: {e}")
        print()
    
    # 14. 获取帖子
    print("14. 获取帖子列表...")
    try:
        posts = client.get_posts(limit=5)
        print(f"✓ 获取到 {len(posts)} 个帖子:")
        for post in posts:
            print(f"   - {post.title or '无标题'} (ID: {post.id})")
        print()
    except Exception as e:
        print(f"❌ 获取帖子失败: {e}")
        print()
    
    print("=== 示例执行完成 ===")
    print("\n提示:")
    print("- 如果需要上传文件，请确保文件路径正确")
    print("- 如果需要发送消息，请确保有权限访问聊天室")
    print("- 更多 API 方法请参考 SDK 文档")


def create_simple_example():
    """创建一个简单的使用示例。"""
    
    print("创建简单示例文件...")
    
    simple_code = '''#!/usr/bin/env python3
"""
Solar Network Python SDK 简单使用示例
"""

from solar_network_sdk import SolarNetworkClient, WebAuthClient

def main():
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
        # 签名挑战（需要实现你的签名逻辑）
        signed_challenge = f"signed_{auth_result.challenge}"
        
        # 交换令牌
        token_result = web_auth.exchange_token(signed_challenge)
        
        if token_result.status == "success":
            # 设置令牌
            client.set_token(token_result.token)
            
            # 获取账户信息
            account = client.get_account()
            print(f"你好, {account.name}!")
            
            # 获取钱包
            wallet = client.get_wallet()
            print(f"钱包 ID: {wallet.id}")
        else:
            print(f"认证失败: {token_result.error}")
    else:
        print(f"认证被拒绝或失败")

if __name__ == "__main__":
    main()
'''
    
    with open("SN_sdk_py/simple_example.py", "w", encoding="utf-8") as f:
        f.write(simple_code)
    
    print("✓ 简单示例文件创建成功: simple_example.py")


if __name__ == "__main__":
    # 创建简单示例
    create_simple_example()
    
    # 运行完整示例
    asyncio.run(main())