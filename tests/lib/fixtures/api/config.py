import os
import json
import pytest


# TODO - create some base method/class to abstract get/set on tower settings

@pytest.fixture(scope='session')
def tower_settings_path(request, tower_config_dir):
    return os.path.join(tower_config_dir, 'settings.py')


@pytest.fixture(scope="class")
def AWX_PROOT_ENABLED(request, ansible_runner, tower_settings_path):
    # update settings.py
    contacted = ansible_runner.lineinfile(
        state='present',
        dest=tower_settings_path,
        regexp='^\s*AWX_PROOT_ENABLED\s*=',
        line='AWX_PROOT_ENABLED = True'
    )

    # assert success
    for result in contacted.values():
        assert 'failed' not in result, \
            "Failure while setting AWX_PROOT_ENABLED\n%s" % json.dumps(result, indent=2)
        changed = 'changed' in result and result['changed']

    # if changes were necesary ...
    if changed:

        # restart ansible-tower
        contacted = ansible_runner.service(
            name='ansible-tower',
            state='restarted'
        )

        # assert success
        for result in contacted.values():
            assert 'failed' not in result, \
                "Failure restarting ansible-tower\n%s" % json.dumps(result, indent=2)

    def fin():
        # if changes were necesary ...
        if changed:
            # restore settings.py
            contacted = ansible_runner.lineinfile(
                state='absent',
                dest=tower_settings_path,
                regexp='^\s*AWX_PROOT_ENABLED\s*='
            )
            # assert success
            for result in contacted.values():
                assert 'failed' not in result, \
                    "Failure while removing AWX_PROOT_ENABLED\n%s" % json.dumps(result, indent=2)

        # if changes were necesary ...
        if changed:
            # restart ansible-tower
            contacted = ansible_runner.service(
                name='ansible-tower',
                state='restarted'
            )

            # assert success
            for result in contacted.values():
                assert 'failed' not in result, \
                    "Failure restarting ansible-tower\n%s" % json.dumps(result, indent=2)

    request.addfinalizer(fin)


@pytest.fixture(scope="class")
def ORG_ADMINS_CANNOT_SEE_ALL_USERS(request, ansible_runner, tower_settings_path):
    # update settings.py
    contacted = ansible_runner.lineinfile(
        state='present',
        dest=tower_settings_path,
        regexp='^\s*ORG_ADMINS_CAN_SEE_ALL_USERS\s*=',
        line='ORG_ADMINS_CAN_SEE_ALL_USERS = False'
    )

    # assert success
    for result in contacted.values():
        assert 'failed' not in result, \
            "Failure while setting ORG_ADMINS_CAN_SEE_ALL_USERS\n%s" % json.dumps(result, indent=2)
        changed = 'changed' in result and result['changed']

    # restart ansible-tower (if changes were necesary)
    if changed:
        contacted = ansible_runner.service(
            name='ansible-tower',
            state='restarted'
        )
        for result in contacted.values():
            assert 'failed' not in result, \
                "Failure restarting ansible-tower\n%s" % json.dumps(result, indent=2)

    def fin():
        # restore settings.py (if changes were necesary)
        if changed:
            contacted = ansible_runner.lineinfile(
                state='absent',
                dest=tower_settings_path,
                regexp='^\s*ORG_ADMINS_CAN_SEE_ALL_USERS\s*='
            )
            for result in contacted.values():
                assert 'failed' not in result, \
                    "Failure while removing ORG_ADMINS_CAN_SEE_ALL_USERS\n%s" % json.dumps(result, indent=2)

        # restart ansible-tower (if changes were necesary)
        if changed:
            contacted = ansible_runner.service(
                name='ansible-tower',
                state='restarted'
            )
            for result in contacted.values():
                assert 'failed' not in result, \
                    "Failure restarting ansible-tower\n%s" % json.dumps(result, indent=2)
    request.addfinalizer(fin)
