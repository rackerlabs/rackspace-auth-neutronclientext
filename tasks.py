#!/usr/bin/env python
# -*- coding: utf-8 -*-


from invoke import run, task

@task
def test(verbose=True):
    py_test_line = "py.test -s"
    if(verbose):
        py_test_line += " --verbose"
    run(py_test_line, pty=True)

@task
def coverage(report_type="term"):
    run("py.test -s --verbose --cov-report {} ".format(report_type) +
        "--cov=rackspace_auth_openstack test_rackspace_auth_openstack.py")

