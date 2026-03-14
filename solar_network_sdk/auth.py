"""
Authentication module for Solar Network Python SDK.

This module provides the WebAuthClient class for authenticating
with the Solar Network desktop app via local HTTP server.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Dict, Any, Union
import requests
from .models import AppToken, GeoIpLocation, AuthFactor, AccountConnection


@dataclass
class WebAuthResult:
    """Authentication result."""
    status: str
    challenge: Optional[str] = None
    token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    refresh_expires_in: Optional[int] = None
    error: Optional[str] = None


class WebAuthStatus:
    """Authentication status constants."""
    CHALLENGE = "challenge"
    SUCCESS = "success"
    ERROR = "error"
    DENIED = "denied"


class WebAuthClient:
    """Web Authentication Client for Solar Network.
    
    Connects to the Solar Network desktop app's local authentication server
    to perform secure authentication without requiring users to re-enter credentials.
    """
    
    def __init__(
        self,
        base_url: str = "http://127.0.0.1",
        default_port: int = 40000,
        web_url: str = "https://app.solian.fr"
    ):
        """Initialize the WebAuthClient.
        
        Args:
            base_url: The local server base URL (default: 'http://127.0.0.1')
            default_port: The default port to connect to (default: 40000)
            web_url: The Solar Network web URL for auth redirects (default: 'https://app.solian.fr')
        """
        self.base_url = base_url
        self.default_port = default_port
        self.web_url = web_url
        self._port = default_port

    @property
    def port(self) -> int:
        """Get the current port."""
        return self._port

    @port.setter
    def port(self, value: int) -> None:
        """Set the current port."""
        self._port = value

    def get_authentication_url(self) -> str:
        """Get the authentication URL to open in a browser.
        
        This URL redirects the user to the Solar Network web app for additional
        authentication if needed.
        
        Returns:
            The authentication URL
        """
        return f"{self.web_url}/auth/web?port={self._port}"

    def get_protocol_challenge_url(
        self,
        app_slug: str,
        redirect_uri: str,
        state: Optional[str] = None
    ) -> str:
        """Get the protocol challenge URL for native app authentication.
        
        Args:
            app_slug: The application slug
            redirect_uri: The redirect URI
            state: Optional state parameter
            
        Returns:
            The protocol challenge URL
        """
        params = {
            'app': app_slug,
            'redirect_uri': redirect_uri,
        }
        if state:
            params['state'] = state
        
        return f"solian://auth/web?{self._dict_to_query_string(params)}"

    def get_protocol_exchange_url(
        self,
        signed_challenge: str,
        redirect_uri: str,
        secret_id: Optional[str] = None,
        state: Optional[str] = None
    ) -> str:
        """Get the protocol exchange URL for native app authentication.
        
        Args:
            signed_challenge: The signed challenge
            redirect_uri: The redirect URI
            secret_id: Optional secret ID
            state: Optional state parameter
            
        Returns:
            The protocol exchange URL
        """
        params = {
            'signed_challenge': signed_challenge,
            'redirect_uri': redirect_uri,
        }
        if secret_id:
            params['secret_id'] = secret_id
        if state:
            params['state'] = state
        
        return f"solian://auth/web?{self._dict_to_query_string(params)}"

    def wait_for_auth(self, port: Optional[int] = None, app_name: str = "PythonApp") -> WebAuthResult:
        """Wait for user to respond to authentication request.
        
        This method opens a long-polling connection to the local Solar Network app.
        It will wait until the user either allows or denies the authentication request.
        
        Args:
            port: The port of the local server (defaults to instance port)
            app_name: The name of your application
            
        Returns:
            The authentication result
        """
        port = port or self._port
        url = f"{self.base_url}:{port}/alive?app={app_name}"

        try:
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                status = data.get('status')
                
                if status == WebAuthStatus.DENIED:
                    return WebAuthResult(status=WebAuthStatus.DENIED)
                
                if status == WebAuthStatus.CHALLENGE and 'challenge' in data:
                    return WebAuthResult(
                        status=WebAuthStatus.CHALLENGE,
                        challenge=data['challenge']
                    )
                
                return WebAuthResult(
                    status=WebAuthStatus.ERROR,
                    error=data.get('error', 'Unknown response from server')
                )
            
            return WebAuthResult(
                status=WebAuthStatus.ERROR,
                error=f"HTTP {response.status_code}: {response.reason}"
            )
            
        except requests.RequestException as e:
            return WebAuthResult(
                status=WebAuthStatus.ERROR,
                error=str(e)
            )

    def exchange_token(
        self,
        signed_challenge: str,
        port: Optional[int] = None,
        device_info: Optional[Dict[str, Any]] = None,
        secret_id: Optional[str] = None
    ) -> WebAuthResult:
        """Exchange a signed challenge for an authentication token.
        
        After the user allows authentication and you've signed the challenge,
        call this method to exchange it for a session token.
        
        Args:
            signed_challenge: The signed challenge returned from waitForAuth
            port: The port of the local server (defaults to instance port)
            device_info: Optional device information
            secret_id: Optional APP_CONNECT secret ID
            
        Returns:
            The token result
        """
        port = port or self._port
        url = f"{self.base_url}:{port}/exchange"
        
        payload = {'signed_challenge': signed_challenge}
        if device_info:
            payload['device_info'] = device_info
        if secret_id:
            payload['secret_id'] = secret_id

        try:
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'token' in data:
                    return WebAuthResult(
                        status=WebAuthStatus.SUCCESS,
                        token=data['token'],
                        refresh_token=data.get('refresh_token'),
                        expires_in=data.get('expires_in'),
                        refresh_expires_in=data.get('refresh_expires_in')
                    )
                
                return WebAuthResult(
                    status=WebAuthStatus.ERROR,
                    error='No token in response'
                )
            
            error_data = response.json()
            return WebAuthResult(
                status=WebAuthStatus.ERROR,
                error=error_data.get('error', f"HTTP {response.status_code}: {response.reason}")
            )
            
        except requests.RequestException as e:
            return WebAuthResult(
                status=WebAuthStatus.ERROR,
                error=str(e)
            )

    def fetch_account_info(
        self,
        port: Optional[int] = None,
        token: str = ""
    ) -> Dict[str, Union[bool, Optional[Dict[str, Any]], Optional[str]]]:
        """Fetch account information using an auth token.
        
        This endpoint proxies through the local Solar Network app to fetch
        the authenticated user's account info.
        
        Args:
            port: The port of the local server (defaults to instance port)
            token: The authentication token
            
        Returns:
            The account info response
        """
        port = port or self._port
        url = f"{self.base_url}:{port}/me"

        try:
            response = requests.get(url, headers={'Authorization': f'Bearer {token}'}, timeout=30)
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'data': response.json()
                }
            
            error_data = response.json()
            return {
                'success': False,
                'error': error_data.get('error', f"HTTP {response.status_code}: {response.reason}")
            }
            
        except requests.RequestException as e:
            return {
                'success': False,
                'error': str(e)
            }

    def authenticate(
        self,
        app_name: str = "PythonApp",
        sign_challenge: Optional[callable] = None
    ) -> WebAuthResult:
        """Full authentication flow helper.
        
        This convenience method combines waitForAuth, challenge signing (via callback),
        and exchangeToken into a single call.
        
        Args:
            app_name: The name of your application
            sign_challenge: Callback to sign the challenge - implement your signing logic here
            
        Returns:
            The token result
        """
        # Step 1: Wait for user to respond
        auth_result = self.wait_for_auth(app_name=app_name)

        if auth_result.status != WebAuthStatus.CHALLENGE:
            return auth_result

        # Step 2: Sign the challenge
        if not sign_challenge:
            return WebAuthResult(
                status=WebAuthStatus.ERROR,
                error="No sign_challenge callback provided"
            )

        try:
            signed_challenge = sign_challenge(auth_result.challenge)
        except Exception as e:
            return WebAuthResult(
                status=WebAuthStatus.ERROR,
                error=f"Failed to sign challenge: {str(e)}"
            )

        # Step 3: Exchange for token
        return self.exchange_token(signed_challenge)

    def _dict_to_query_string(self, params: Dict[str, Any]) -> str:
        """Convert a dictionary to a query string."""
        return '&'.join([f"{k}={v}" for k, v in params.items()])