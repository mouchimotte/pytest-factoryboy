from __future__ import annotations

import factory

from pytest_factoryboy import register
from tests.compat import assert_outcomes


@register
class JSONPayloadFactory(factory.Factory):
    class Meta:
        model = dict

    name = "John Doe"


def test_fixture_name_as_expected(json_payload):
    """Test that the json_payload fixture is registered from the JSONPayloadFactory."""
    assert json_payload["name"] == "John Doe"


def test_fixture_name_cant_be_determined(testdir):
    """Test that an error is raised if the fixture name can't be determined."""
    testdir.makepyfile(
        """
        import factory
        from pytest_factoryboy import register

        @register
        class JSONPayloadF(factory.Factory):
            class Meta:
                model = dict

            name = "John Doe"

        """
    )
    res = testdir.runpytest()
    assert_outcomes(res, errors=1)
    res.stdout.fnmatch_lines("*JSONPayloadF *does not follow*naming convention*")


def test_invalid_factory_name_override(testdir):
    """Test that, although the factory name doesn't follow the naming convention, it can still be overridden."""
    testdir.makepyfile(
        """
        import factory
        from pytest_factoryboy import register

        @register(_name="payload")
        class JSONPayloadF(factory.Factory):
            class Meta:
                model = dict

            name = "John Doe"


        def test_payload(payload):
            assert payload["name"] == "John Doe"
        """
    )
    res = testdir.runpytest()
    assert_outcomes(res, passed=1)
