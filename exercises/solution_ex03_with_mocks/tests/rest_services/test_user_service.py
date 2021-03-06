"""
Unit tests for UserServiceRest

See http://docs.pylonsproject.org/projects/pyramid/en/1.3-branch/narr/pyramid_testing.html
"""

__author__ = 'Mike Woinoski (mike@articulatedesign.us.com)'

from unittest import TestCase, main
from unittest.mock import Mock, ANY
from nose.tools import raises
import sqlite3

from pyramid import testing as pyramid_testing
from pyramid.httpexceptions import HTTPNotFound, HTTPInternalServerError

from ticketmanor.models.person import Person
from ticketmanor.rest_services.user_service import UserServiceRest
from ticketmanor.models.persistence import PersistenceError


class UserServiceRestTest(TestCase):
    """Unit tests for Pyramid view callable UserServiceRest"""

    def setUp(self):
        # Set up for Pyramid web application framework.
        request = pyramid_testing.DummyRequest()
        self.config = pyramid_testing.setUp(request=request)
        self.config.include('pyramid_chameleon')

    def tearDown(self):
        pyramid_testing.tearDown()

    def test_get_success(self):
        request = pyramid_testing.DummyRequest()
        request.db_session = None
        request.matchdict['email'] = 'benf@gmail.com'

        # TODO: note that we pass Mock as the DAO class to the
        # UserServiceRest constructor.
        # (no code change required)
        user_service = UserServiceRest(None, request, dao=Mock)

        person = Person(id=123)

        # TODO: note how we access the DAO from the UserServiceRest instance
        # after the Mock DAO has been set. Here, we program the Mock so that
        # its get() method returns a reference to the Person created above.
        # (no code change required)
        user_service._dao.get.return_value = person

        result = user_service.get_user()

        self.assertEqual(result, person)

    def test_get_not_found(self):
        request = pyramid_testing.DummyRequest()
        request.db_session = None
        request.matchdict['email'] = 'nobody@gmail.com'

        # TODO: pass Mock as the DAO class to the UserServiceRest
        # constructor.
        user_service = UserServiceRest(None, request, dao=Mock)

        # TODO: configure the mock so that a call to its get() method has
        # the side effect of raising a PersistenceError
        user_service._dao.get.side_effect = PersistenceError()

        # TODO: assert that an HTTPNotFound exception is raised when you call
        # the user_service's get_user() method.
        with self.assertRaises(HTTPNotFound):
            user_service.get_user()

        # assert_called_with() verifies that the mock DAO's add() method was
        # called once. ANY can be used as a placeholder so the mock doesn't
        # test the argument values.
        user_service._dao.add.assert_called_once(ANY, ANY)

    def test_get_unhandled_exception(self):
        request = pyramid_testing.DummyRequest()
        request.db_session = None
        request.matchdict['email'] = 'nobody@gmail.com'

        # TODO: pass Mock as the DAO class to the UserServiceRest
        # constructor.
        user_service = UserServiceRest(None, request, dao=Mock)

        # TODO: program the mock DAO's get() method to have a side effect of
        # raising a ValueError.
        user_service._dao.get = Mock(side_effect=ValueError())

        # TODO: assert that a ValueError is raised when you call
        # the user_service's get_user() method.
        with self.assertRaises(ValueError):
            user_service.get_user()

    # TODO: use the @nose.tools.raises decorator to verify that this test
    # raises an HTTPNotFound exception.
    @raises(HTTPNotFound)
    def test_get_not_found_with_decorator(self):
        request = pyramid_testing.DummyRequest()
        request.db_session = None
        request.matchdict['email'] = 'nobody@gmail.com'
        user_service = UserServiceRest(None, request, dao=Mock)

        # TODO: note that we program the mock DAO's get() method to raise
        # a PersistenceError
        # (no code change required)
        user_service._dao.get = Mock(side_effect=PersistenceError())

        # TODO: call the user_service get_user() method.
        user_service.get_user()

    def test_add_user_success(self):
        request = pyramid_testing.DummyRequest()
        request.db_session = None
        request.json_body = {"id": "1", "first_name": "Ben",
                             "last_name": "Franklin", "email": "benf@gmail.com"}
        user_service = UserServiceRest(None, request, dao=Mock)

        response = user_service.add_user()

        self.assertEqual(201, response.status_int)

    def test_add_user_db_exception(self):
        request = pyramid_testing.DummyRequest()
        request.db_session = None
        request.json_body = {"id": "1", "first_name": "Ben",
                             "last_name": "Franklin", "email": "benf@gmail.com"}
        user_service = UserServiceRest(None, request, dao=Mock)

        # TODO: note the mock DAO's add() method will raise a DatabaseError.
        # (no code change required)
        user_service._dao.add = Mock(side_effect=sqlite3.DatabaseError())

        # TODO: assert that an HTTPInternalServerError is raised when you call
        # the user_service's add_user() method, and that the exception's
        # message includes the string 'Could not add'
        with self.assertRaisesRegex(HTTPInternalServerError, r'Could not add'):
            user_service.add_user()

        # Assert that the mock DAO's add() method was called once, with
        # any two arguments.
        user_service._dao.add.assert_called_once(ANY, ANY)

    def test_update_user_success(self):
        request = pyramid_testing.DummyRequest()
        request.db_session = None
        request.json_body = {"id": "1", "first_name": "Ben",
                             "last_name": "Franklin", "email": "benf@gmail.com"}
        user_service = UserServiceRest(None, request, dao=Mock)

        response = user_service.update_user()

        self.assertEqual(202, response.status_int)

    def test_update_user_not_found(self):
        request = pyramid_testing.DummyRequest()
        request.db_session = None
        request.json_body = {"id": "1", "first_name": "Ben",
                             "last_name": "Franklin", "email": "benf@gmail.com"}
        user_service = UserServiceRest(None, request, dao=Mock)
        user_service._dao.update = Mock(side_effect=PersistenceError())

        with self.assertRaises(HTTPNotFound):
            user_service.update_user()

    def test_delete_user_success(self):
        request = pyramid_testing.DummyRequest()
        request.db_session = None
        request.matchdict['email'] = 'benf@gmail.com'
        user_service = UserServiceRest(None, request, dao=Mock)

        response = user_service.delete_user()

        self.assertEqual(204, response.status_int)

    def test_delete_user_not_found(self):
        request = pyramid_testing.DummyRequest()
        request.db_session = None
        request.matchdict['email'] = 'nobody@gmail.com'
        user_service = UserServiceRest(None, request, dao=Mock)
        user_service._dao.delete = Mock(side_effect=PersistenceError())

        with self.assertRaises(HTTPNotFound):
            user_service.delete_user()

if __name__ == '__main__':
    main()
