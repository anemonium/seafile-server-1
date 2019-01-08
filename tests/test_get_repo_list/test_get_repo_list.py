import pytest
from seaserv import seafile_api as api
from tests.config import USER

attr_to_assert = ['id', 'name', 'version', 'last_modify', 'size',
                  'last_modifier', 'head_cmmt_id', 'repo_id', 'repo_name',
                  'last_modified', 'encrypted', 'is_virtual', 'origin_repo_id',
                  'origin_repo_name', 'origin_path', 'store_id' ,'share_type',
                  'permission', 'user', 'group_id']

def assert_by_attr_name (repo, attr):
    if (attr == 'id'):
        assert repo.id == getattr(repo, attr)
    elif (attr == 'name'):
        assert repo.name == getattr(repo, attr)
    elif (attr == 'size'):
        assert repo.size == getattr(repo, attr)
    elif (attr == 'last_modifier'):
        assert repo.last_modifier == getattr(repo, attr)
    elif (attr == 'head_cmmt_id'):
        assert repo.head_cmmt_id == getattr(repo, attr)
    elif (attr == 'repo_id'):
        assert repo.id == getattr(repo, attr)
    elif (attr == 'repo_name'):
        assert repo.name == getattr(repo, attr)
    elif (attr == 'last_modified'):
        assert repo.last_modified == getattr(repo, attr)
    elif (attr == 'encrypted'):
        assert repo.encrypted == getattr(repo, attr)
    elif (attr == 'is_virtual'):
        assert repo.is_virtual == getattr(repo, attr)
    elif (attr == 'origin_repo_id'):
        assert repo.origin_repo_id == getattr(repo, attr)
    elif (attr == 'origin_repo_name'):
        assert repo.origin_repo_name == getattr(repo, attr)
    elif (attr == 'origin_path'):
        assert repo.origin_path == getattr(repo, attr)
    elif (attr == 'store_id'):
        assert repo.store_id == getattr(repo, attr)
    elif (attr == 'share_type'):
        assert repo.share_type == getattr(repo, attr)
    elif (attr == 'permission'):
        assert repo.permission == getattr(repo, attr)
    elif (attr == 'group_id'):
        assert repo.group_id == getattr(repo, attr)

def assert_public_repos_attr(repo):
    for attr in attr_to_assert:
       assert hasattr(repo, attr) == True

       assert hasattr(repo, 'is_virtual')
       is_virtual = getattr(repo, 'is_virtual')

       if (is_virtual == False):
           if (attr == 'origin_repo_id' or
               attr == 'origin_path'):
               continue

       if (attr == 'origin_repo_name'):
           continue

       assert_by_attr_name(repo, attr)

def assert_group_repos_attr(repo):
    for attr in attr_to_assert:
        assert hasattr(repo, attr) == True

        assert hasattr(repo, 'is_virtual')
        is_virtual = getattr(repo, 'is_virtual')

        if (is_virtual == False):
            if (attr == 'origin_repo_id' or
                attr == 'origin_repo_name' or
                attr == 'origin_path'):
                continue

        assert_by_attr_name(repo, attr)

def test_get_group_repos(repo, group):
    api.group_share_repo(repo.id, group.id, USER, 'rw')
    repos = api.get_repos_by_group(group.id)
    assert_group_repos_attr(repos[0])

    repos = api.get_group_repos_by_owner(USER)
    assert_group_repos_attr(repos[0])

    v_repo_id = api.share_subdir_to_group(repo.id, '/dir1', USER, group.id, 'rw')
    repo = api.get_group_shared_repo_by_path(repo.id, '/dir1', group.id)
    assert_group_repos_attr(repo)
    api.unshare_subdir_for_group(repo.id, '/dir1', USER, group.id)

    repos = api.get_group_repos_by_user(USER)
    assert_group_repos_attr(repos[0])

def test_get_inner_pub_repos(repo):
    api.add_inner_pub_repo(repo.id, 'rw')
    repos = api.get_inner_pub_repo_list()
    assert_public_repos_attr(repos[0])

    repos = api.list_inner_pub_repos_by_owner(USER)
    assert_public_repos_attr(repos[0])
