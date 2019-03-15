from steem import Steem
from uuid import uuid4
from time import sleep
import pytest
import os
import json

TEST_NODES = [os.environ.get("STEEM_TEST_NODE", None)]
WIF = os.environ.get("STEEM_TEST_WIF", None)


def test_evn_variables():
    assert TEST_NODES[0] is not None, "{} environment variable not set".format("STEEM_TEST_NODE")
    assert WIF is not None, "{} environment variable not set".format("STEEM_TEST_WIF")

def test_debug_has_hardfork():
    s = Steem(nodes = TEST_NODES, no_broadcast = False, keys = [WIF])
    ret = s.debug_has_hardfork(0)
    assert ret['has_hardfork'] == True, "Ret: {}".format(ret)

def test_debug_get_witness_schedule():
    s = Steem(nodes = TEST_NODES, no_broadcast = False, keys = [WIF])
    ret = s.debug_get_witness_schedule()
    print(ret)


def test_debug_get_hardfork_property_object():
    s = Steem(nodes = TEST_NODES, no_broadcast = False, keys = [WIF])
    ret = s.debug_get_hardfork_property_object()
    assert ret['last_hardfork'] == 0, "Ret: {}".format(ret)


def test_debug_get_json_schema():
    s = Steem(nodes = TEST_NODES, no_broadcast = False, keys = [WIF])
    ret = s.debug_get_json_schema()
    assert ret['schema'] == '', "Ret: {}".format(ret)


def test_debug_generate_blocks():
    s = Steem(nodes = TEST_NODES, no_broadcast = False, keys = [WIF])
    ret = s.debug_generate_blocks(WIF, 10, 0, 0, True)
    assert ret['blocks'] == 10, "Ret: {}".format(ret)


def test_debug_generate_blocks_until():
    s = Steem(nodes = TEST_NODES, no_broadcast = False, keys = [WIF])
    import datetime
    timestamp = (datetime.datetime.now() + datetime.timedelta(hours = 1)).replace(microsecond=0).isoformat()

    ret = s.debug_generate_blocks_until(WIF, timestamp, False)
    print(ret)


def test_debug_set_hardfork():
    s = Steem(nodes = TEST_NODES, no_broadcast = False, keys = [WIF])
    ret = s.debug_set_hardfork(22)
    assert len(ret) == 0, "Ret: {}".format(ret)

    ret = s.debug_generate_blocks(WIF, 5, 0, 0, True)
    assert ret['blocks'] == 5, "Ret: {}".format(ret)

    ret = s.debug_has_hardfork(22)
    assert ret['has_hardfork'] == True, "Ret: {}".format(ret)


def test_debug_pop_block():
    s = Steem(nodes = TEST_NODES, no_broadcast = False, keys = [WIF])
    ret = s.debug_pop_block()
    ret = ret.get("block", None)
    assert ret is not None


def test_debug_push_blocks():
    s = Steem(nodes = TEST_NODES, no_broadcast = False, keys = [WIF])
    file_name = "/tmp/blocks"
    ret = s.debug_push_blocks(file_name, 1000, skip_validate_invariants = False)
    print(ret)

if __name__ == "__main__":
    test_evn_variables()
    test_debug_has_hardfork()
    test_debug_get_hardfork_property_object()
    test_debug_get_witness_schedule()
    test_debug_get_json_schema()
    test_debug_generate_blocks()
    test_debug_set_hardfork()
    test_debug_generate_blocks()
    test_debug_pop_block()
    test_debug_generate_blocks_until()
