#!/usr/bin/env python3
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
