from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class MySocialAdapter(DefaultSocialAccountAdapter):

    def pre_social_login(self, request, sociallogin):
        emails = sociallogin.email_addresses
        clean_emails = [e for e in emails if 'noreply.github.com' not in e.email]

        if clean_emails:
            sociallogin.email_addresses = clean_emails
            sociallogin.email_addresses[0].primary = True
            sociallogin.email_addresses[0].verified = True

        extra_data = sociallogin.account.extra_data
        user = sociallogin.user

        if sociallogin.account.provider == 'github':
            github_username = extra_data.get('login')
            if github_username:
                user.first_name = github_username

        elif sociallogin.account.provider == 'google':
            user.first_name = extra_data.get('given_name', '')
            user.last_name = extra_data.get('family_name', '')

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        return user