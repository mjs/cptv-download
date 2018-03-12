import pytest
from fixturetestapi import FixtureTestAPI


class TestUser:

     def test_can_create_new_user(self):
        testapi = FixtureTestAPI()

        print("If a new user 'bob' signs up", end='')
        bob = testapi.given_new_user(self, 'bob')

        print("Then 'bob' should able to log in")
        bob_login = testapi.login_as(bob.username)

        print('And bob should be able to see his details include user id. ')
        testapi.admin_user().get_user_details(testapi.admin_user())
        bob.get_user_details(bob)
        userdetails = bob.get_user_details(testapi.admin_user())

        print("Bob's user id is {}".format(userdetails))

    