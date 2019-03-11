from steem import Steem
from uuid import uuid4
from time import sleep
import pytest
import os

TEST_NODES = [os.environ.get("STEEM_TEST_NODE", None)]
WIF = os.environ.get("STEEM_TEST_WIF", None)
ACCOUNT = os.environ.get("STEEM_TEST_ACCOUNT", None)
SUBJECT = str(uuid4())

@pytest.mark.serial
def test_evn_variables():
    assert TEST_NODES[0] is not None, "{} environment variable not set".format("STEEM_TEST_NODE")
    assert WIF is not None, "{} environment variable not set".format("STEEM_TEST_WIF")
    assert ACCOUNT is not None, "{} environment variable not set".format("STEEM_TEST_ACCOUNT")

@pytest.mark.serial
def test_create_proposal():
    print("test_create_proposal")
    s = Steem(nodes = TEST_NODES, no_broadcast = False, keys = [WIF])
    
    import datetime
    now = datetime.datetime.now()

    start_date = now + datetime.timedelta(days = 1)
    end_date = start_date + datetime.timedelta(days = 2)

    start_date = start_date.replace(microsecond=0).isoformat()
    end_date = end_date.replace(microsecond=0).isoformat()

    ret = s.commit.create_proposal(
      ACCOUNT, 
      "treasury", 
      start_date, 
      end_date,
      "16.000 TBD",
      SUBJECT,
      "mypermlink"
    )

    assert ret["operations"][0][1]["creator"] == ACCOUNT
    assert ret["operations"][0][1]["receiver"] == "treasury"
    assert ret["operations"][0][1]["start_date"] == start_date
    assert ret["operations"][0][1]["end_date"] == end_date
    assert ret["operations"][0][1]["daily_pay"] == "16.000 TBD"
    assert ret["operations"][0][1]["subject"] == SUBJECT
    assert ret["operations"][0][1]["url"] == "mypermlink"
    sleep(6)

@pytest.mark.serial
def test_list_proposals():
    print("test_list_proposals")
    s = Steem(nodes = TEST_NODES, no_broadcast = False, keys = [WIF])
    # list inactive proposals, our proposal shoud be here
    proposals = s.list_proposals(ACCOUNT, "by_creator", "direction_ascending", 1000, 0)
    found = None
    for proposal in proposals:
        if proposal["subject"] == SUBJECT:
            found = proposal
    
    assert found is not None
    
    # list active proposals, our proposal shouldnt be here
    proposals = s.list_proposals(ACCOUNT, "by_creator", "direction_ascending", 1000, 1)
    found = None
    for proposal in proposals:
        if proposal["subject"] == SUBJECT:
            found = proposal
    
    assert found is None

    # list all proposals, our proposal should be here
    proposals = s.list_proposals(ACCOUNT, "by_creator", "direction_ascending", 1000, -1)

    found = None
    for proposal in proposals:
        if proposal["subject"] == SUBJECT:
            found = proposal
    
    assert found is not None

@pytest.mark.serial
def test_find_proposals():
    print("test_find_proposals")
    s = Steem(nodes = TEST_NODES, no_broadcast = False, keys = [WIF])
    # first we will find our special proposal and get its id
    proposals = s.list_proposals(ACCOUNT, "by_creator", "direction_ascending", 1000, -1)

    found = None
    for proposal in proposals:
        if proposal["subject"] == SUBJECT:
            found = proposal
    
    assert found is not None
    proposal_id = int(found["id"])

    ret = s.find_proposals([proposal_id])
    assert ret[0]["subject"] == found["subject"]

@pytest.mark.serial
def test_vote_proposal():
    print("test_vote_proposal")
    s = Steem(nodes = TEST_NODES, no_broadcast = False, keys = [WIF])
    # first we will find our special proposal and get its id
    proposals = s.list_proposals(ACCOUNT, "by_creator", "direction_ascending", 1000, -1)

    found = None
    for proposal in proposals:
        if proposal["subject"] == SUBJECT:
            found = proposal
    
    assert found is not None
    proposal_id = int(found["id"])

    # now lets vote
    ret = s.commit.update_proposal_votes(ACCOUNT, [proposal_id], True)
    assert ret["operations"][0][1]["voter"] == ACCOUNT
    assert ret["operations"][0][1]["proposal_ids"][0] == proposal_id
    assert ret["operations"][0][1]["approve"] == True
    sleep(6)

@pytest.mark.serial
def test_list_voter_proposals():
    print("test_list_voter_proposals")
    s = Steem(nodes = TEST_NODES, no_broadcast = False, keys = [WIF])
    proposals = s.list_voter_proposals(ACCOUNT, "by_creator", "direction_ascending", 1000, -1)

    found = None
    for proposal in proposals:
        if proposal["subject"] == SUBJECT:
            found = proposal
    
    assert found is not None

@pytest.mark.serial
def test_remove_proposal():
    print("test_remove_proposal")
    s = Steem(nodes = TEST_NODES, no_broadcast = False, keys = [WIF])
    # first we will find our special proposal and get its id
    proposals = s.list_proposals(ACCOUNT, "by_creator", "direction_ascending", 1000, -1)

    found = None
    for proposal in proposals:
        if proposal["subject"] == SUBJECT:
            found = proposal
    
    assert found is not None
    proposal_id = int(found["id"])

    # remove proposal
    s.commit.remove_proposal(ACCOUNT, [proposal_id])

    # try to find our special proposal
    proposals = s.list_proposals(ACCOUNT, "by_creator", "direction_ascending", 1000, -1)

    found = None
    for proposal in proposals:
        if proposal["subject"] == SUBJECT:
          found = proposal
    
    assert found is None


if __name__ == '__main__':
    test_create_proposal()
    # wait approx 2 blocks
    test_list_proposals()
    test_find_proposals()
    test_vote_proposal()
    # wait approx 2 blocks
    test_remove_proposal()
