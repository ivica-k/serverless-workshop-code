from chalicelib.utils import chunk_list


def test_chunk_list():
    expected_value = [[1, 2], [3, 4], [5]]
    return_value = list(chunk_list([1, 2, 3, 4, 5], 2))

    assert expected_value == return_value