from urllib import parse

import requests
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialApp
from allauth.utils import valid_email_or_none
from django.contrib import messages
from django.shortcuts import redirect

from test_app.models import User

PROVIDER_NAME_DICT = {
    'FACEBOOK': '페이스북',
    'KAKAO': '카카오',
    'NAVER': '네이버'
}


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        """
        이 메소드가 호출되기까지의 과정은 대략적으로 다음과 같다.

        1. 인증 코드를 이용하여 액세스 토큰을 요청하는 API를 호출한다.
        2. 받아온 엑세스 토큰을 이용하여 SocialToken 인스턴스를 생성한다.
        3. 액세스 토큰을 이용하여 소셜 계정의 정보를 조회하는 API를 호출한다.
        4. 받아온 소셜 계정의 정보를 가지고 SocialAccount 인스턴스를 생성한다.
        5. 비어 있는 User 인스턴스를 생성하여 SocialAccount 인스턴스에 연결한다.
        6. 이 메소드를 호출하여 User 인스턴스의 필드 값들을 채워준다.

        인자로 전달받는 sociallogin 인스턴스의 account 필드는 SocialAccount 인스턴스를 가리킨다.
        따라서 sociallogin.account 인스턴스로부터 소셜 계정의 정보를 참조할 수 있다.
        """

        # 자동 회원가입으로 생성될 유저
        user = sociallogin.user

        # 소셜 서비스 이름 (페이스북, 카카오, 네이버)
        provider_name = sociallogin.account.provider.upper()

        # 엑세스 토큰으로 소셜 서비스 서버에게 API를 요청하여 받아온 소셜 계정의 정보 (= API 응답 데이터)
        social_account_data = sociallogin.account.extra_data

        # 페이스북 로그인
        if provider_name == 'FACEBOOK':
            email = valid_email_or_none(social_account_data.get('email'))
            name = social_account_data.get('name')

        # 카카오 로그인
        elif provider_name == 'KAKAO':
            email = valid_email_or_none(social_account_data['kakao_account'].get('email'))
            name = social_account_data.get('properties', {}).get('nickname')

        # 네이버 로그인
        else:
            email = valid_email_or_none(social_account_data.get('email'))
            name = social_account_data.get('name')

        # 유저 인스턴스의 이메일/이름 필드 값 설정
        user.email = email
        user.name = name

        return user

    def pre_social_login(self, request, sociallogin):
        # 소셜 회원가입을 이미 한 경우 (= SocialAccount 인스턴스가 데이터베이스에 이미 존재하는 경우)
        if sociallogin.is_existing:
            return

        # 자동으로 회원가입될 유저 (= 아직 데이터베이스에 저장되지 않은 유저 인스턴스)
        user = sociallogin.user

        # 이름/이메일이 올바르게 제공되지 않은 경우 (= 사용자가 동의를 하지 않았거나, 실제로 값이 없는 경우)
        if not (user.email and user.name):
            # 엑세스 토큰
            access_token = sociallogin.token.token

            # 소셜 서비스 이름 (페이스북, 카카오, 네이버)
            provider_name = sociallogin.account.provider.upper()

            # 페이스북 연결 끊기 (= 페이스북 서버에 저장되어 있는, 해당 페이스북 계정과 오픈갤러리 사이의 연결 정보를 삭제하는 것)
            if provider_name == 'FACEBOOK':
                requests.delete('https://graph.facebook.com/{}/permissions'.format(sociallogin.account.uid), params={
                    'access_token': access_token
                })

            # 카카오 연결 끊기 (= 카카오 서버에 저장되어 있는, 해당 카카오 계정과 오픈갤러리 사이의 연결 정보를 삭제하는 것)
            elif provider_name == 'KAKAO':
                requests.post('https://kapi.kakao.com/v1/user/unlink', headers={
                    'Authorization': 'Bearer {}'.format(access_token)
                })

            # 네이버 연결 끊기 (= 네이버 서버에 저장되어 있는, 해당 네이버 계정과 오픈갤러리 사이의 연결 정보를 삭제하는 것)
            else:
                naver = SocialApp.objects.get(provider='naver')
                requests.post('https://nid.naver.com/oauth2.0/token', data={
                    'grant_type': 'delete',
                    'client_id': naver.client_id,
                    'client_secret': naver.secret,
                    'access_token': parse.quote(access_token),
                    'service_provider': 'NAVER'
                })

            # 로그인 페이지로 리다이렉트
            messages.error(request, '이름 및 이메일 정보를 모두 올바르게 제공해 주셔야 {} 로그인이 가능합니다.'.format(
                PROVIDER_NAME_DICT[provider_name]
            ))
            raise ImmediateHttpResponse(redirect('login'))

        # 동일한 이메일로 가입된 유저가 있는 경우, 로그인 페이지로 리다이렉트
        user = User.objects.filter(email=user.email).first()
        if user:
            social_account = user.socialaccount_set.first()

            # 소셜 계정으로 회원가입된 유저
            if social_account:
                provider_name = social_account.provider.upper()  # 소셜 서비스 이름 (페이스북, 카카오, 네이버)
                messages.error(request, '이미 {} 계정으로 가입되어 있는 이메일입니다.'.format(
                    PROVIDER_NAME_DICT[provider_name]
                ))
                raise ImmediateHttpResponse(redirect('login'))

            # 이메일로 회원가입된 유저
            else:
                messages.error(request, '이미 가입되어 있는 이메일입니다.')
                raise ImmediateHttpResponse(redirect('login'))
