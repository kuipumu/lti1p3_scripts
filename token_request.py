#!/usr/bin/env python3
"""LTI 1.3 Service Token Request."""
import json
import time
import uuid

import click
import jwt
import requests
from jwcrypto.jwk import JWK  # type: ignore

TITLE_STYLE = {'fg': 'green', 'bold': True}


@click.command()
@click.argument('platform')
def token_request(platform: str):
    """Request LTI 1.3 Service Token."""
    with open('platforms.json', encoding='utf-8') as file:
        platforms = json.load(file)

    platform = platforms.get(platform, {})

    if not platform:
        return

    client_id = platform['client_id']
    token_url = platform['token_url']
    scopes = platform.get(
        'scopes',
        [
            'https://purl.imsglobal.org/spec/lti-ags/scope/lineitem.readonly',
            'https://purl.imsglobal.org/spec/lti-ags/scope/result.readonly',
            'https://purl.imsglobal.org/spec/lti-ags/scope/score',
        ]
    )

    with open('id_rsa', encoding='utf-8') as file:
        private_key = file.read()

    with open('id_rsa.pub', encoding='utf-8') as file:
        public_key = file.read()

    jwk = JWK.from_pem(public_key.encode("utf-8"))
    jwt_payload = {
        'iss': client_id,
        'sub': client_id,
        'aud': token_url,
        'iat': int(time.time()) - 5,
        'exp': int(time.time()) + 60,
        'jti': 'lti-service-token-' + str(uuid.uuid4()),
    }
    jwt_token = jwt.encode(
        jwt_payload,
        private_key,
        algorithm='RS256',
        headers={'kid': jwk.get('kid')},
    )
    payload = {
        'grant_type': 'client_credentials',
        'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
        'client_assertion': jwt_token,
        'scope': ' '.join(list(map(str, scopes))),
    }
    response = requests.post(token_url, data=payload, timeout=60)

    click.secho('Client ID', **TITLE_STYLE)
    click.echo(client_id)
    click.secho('Token URL', **TITLE_STYLE)
    click.echo(token_url)
    click.secho('JWT Payload', **TITLE_STYLE)
    click.echo(jwt_payload)
    click.secho('Request Payload', **TITLE_STYLE)
    click.echo(payload)
    click.secho('Response Status', **TITLE_STYLE)
    click.echo(response.status_code)
    click.secho('Response Body', **TITLE_STYLE)
    click.echo(response.text)


if __name__ == '__main__':
    token_request()  # pylint: disable=no-value-for-parameter
