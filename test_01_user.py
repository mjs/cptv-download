import pytest
from fixturetestapi import FixtureTestAPI


class TestUser:

     def test_can_create_new_user(self):
        testapi = FixtureTestAPI()

        print("If a new user 'bob' signs up", end='')
        bob = testapi.given_new_user(self, 'bob')

        print("Then 'bob' should able to log in")
        bob_login = testapi.logon_as(bob.username)

        # bob = api.given_new_user(self, 'bob')


    