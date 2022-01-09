import pytest

from hello_asyncio import say_hello


@pytest.mark.parametrize("name", ["Robert Paulson", "Seven of Nine", "x Æ a-12"])
@pytest.mark.asyncio
async def test_say_hello(name):
    """
    Asynchronous test for say_hello

    Args:
        name (str): A name to test
    """
    await say_hello(name)
