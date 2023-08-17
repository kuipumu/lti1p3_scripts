#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LTI 1.3 Service Token Request.

This script will request an service token to an LTI platform.

Example:
    To use this script first create platform.json file with a platform configuration
    (See platforms.example.json for an example config.).

    To request a token run the script followed by the platform config name:
    $ python token_request.py platform_config_id

Attributes:
    ENCODING (str): File encoding format.
    DEFAULT_SCOPES (list): Default service scopes.

Notes:
    https://www.imsglobal.org/spec/security/v1p0/#using-json-web-tokens-with-oauth-2-0-client-credentials-grant
"""
import json
import time
import uuid
from argparse import ArgumentParser
from urllib import parse
from urllib.request import Request, urlopen

import jwt
from jwcrypto.jwk import JWK  # type: ignore

ENCODING = 'utf-8'
DEFAULT_SCOPES = [
    'https://purl.imsglobal.org/spec/lti-ags/scope/lineitem',
    'https://purl.imsglobal.org/spec/lti-ags/scope/result.readonly',
    'https://purl.imsglobal.org/spec/lti-ags/scope/score',
]


def get_jwt_payload(client_id: str, token_url: str, expiration: int) -> dict:
    """Get JWT payload.

    Args:
        client_id: Platform client ID.
        token_url: Service token URL.
        expiration: Expiration time in minutes.

    Returns:
        JWT payload dictionary.
    """
    return {
        'iss': client_id,
        'sub': client_id,
        'aud': token_url,
        'iat': int(time.time()) - 5,
        'exp': int(time.time()) + expiration,
        'jti': 'lti-service-token-' + str(uuid.uuid4()),
    }


def get_jwt_token(jwt_payload: dict, private_key: str, jwk: JWK) -> str:
    """Get JWT token.

    Args:
        jwt_payload: JWT payload dictionary.
        private_key: Private KEY pem string.
        jwk: JWK object.

    Returns:
        Encoded JWT token.
    """
    return jwt.encode(
        jwt_payload,
        private_key,
        algorithm='RS256',
        headers={'kid': jwk.get('kid')},
    )


def get_request_payload(jwt_token: dict, scopes: dict) -> dict:
    """Get request payload.

    Args:
        jwt_token: Encoded JWT token.
        scopes: Service token request scopes.

    Returns:
        Service token request payload dictionary.
    """
    return {
        'grant_type': 'client_credentials',
        'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
        'client_assertion': jwt_token,
        'scope': ' '.join(list(map(str, scopes))),
    }


def main():
    """Script main function."""
    # Parse CLI arguments.
    parser = ArgumentParser(description='Request access token from LTI platform.')
    parser.add_argument('platform_name', type=str, help='Platform configuration name.')
    parser.add_argument('--timeout', '-t', type=int, default=15, help='Request timeout.')
    parser.add_argument('--expiration', '-e', type=int, default=60, help='Token expiration.')
    args = parser.parse_args()
    # Get platform configurations.
    with open('platforms.json', 'r', encoding=ENCODING) as file:
        platform_cfgs = json.load(file)
    # Get platform configuration .
    platform_cfg = platform_cfgs[args.platform_name]
    token_url = platform_cfg['token_url']
    # Get public key content.
    with open(platform_cfg['public_key'], 'r', encoding=ENCODING) as file:
        public_key = file.read()
    # Get private key content.
    with open(platform_cfg['private_key'], 'r', encoding=ENCODING) as file:
        private_key = file.read()
    # Get JWK from PEM public key.
    jwk = JWK.from_pem(public_key.encode(ENCODING))
    # Set JWT payload.
    jwt_payload = get_jwt_payload(platform_cfg['client_id'], token_url, args.expiration)
    print('JWT Payload:', jwt_payload)
    # Get request payload.
    jwt_token = get_jwt_token(jwt_payload, private_key, jwk)
    request_payload = get_request_payload(jwt_token, platform_cfg.get('scopes', DEFAULT_SCOPES))
    print('Request Payload:', request_payload)
    # Send service token request and print results.
    with urlopen(
        Request(token_url, data=parse.urlencode(request_payload).encode()),
        timeout=args.timeout,
    ) as response:
        print('Response Body:', response.read().decode(ENCODING))
        print('Response Status:', response.status)


if __name__ == '__main__':
    main()
