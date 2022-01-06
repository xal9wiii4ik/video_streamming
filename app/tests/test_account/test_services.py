from account.services_views import create_tokens, generate_access_token_from_refresh


class TestRefreshToken:
    """
    Test services which related to refresh token
    """

    def test_token_invalid(self) -> None:
        """
        Test case for refresh token invalid token
        """

        return_data, status_code = generate_access_token_from_refresh(refresh_token='123')
        assert status_code == 401
        assert return_data == {'error': 'Invalid token or token is expired'}

    def test_token_invalid_sub(self) -> None:
        """
        Test case for refresh token invalid token sub
        """

        tokens = create_tokens(data={'username': 'username', 'password': 'password'})
        return_data, status_code = generate_access_token_from_refresh(refresh_token=tokens['access_token'])
        assert status_code == 401
        assert return_data == {'error': 'Refresh token is expected'}

    def test_token_valid_data(self) -> None:
        """
        Test case for refresh token valid data
        """

        tokens = create_tokens(data={'username': 'username', 'password': 'password'})
        return_data, status_code = generate_access_token_from_refresh(refresh_token=tokens['refresh_token'])
        assert status_code == 200
