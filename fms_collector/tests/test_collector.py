'''
Tests for fms-collector
'''
import requests
from fms_collector import collector


SAMPLE_SERVER_STATS = """<?xml version="1.0" encoding="utf-8"?>
<result>
    <level>status</level>
    <code>NetConnection.Call.Success</code>
    <timestamp>Thu Apr 19 18:16:06 2012</timestamp>
    <data>
        <launchTime>Wed Apr 18 07:39:28 2012</launchTime>
        <uptime>124598</uptime>
        <cpus>24</cpus>
        <cpu_Usage>10</cpu_Usage>
        <num_cores>8</num_cores>
        <memory_Usage>0</memory_Usage>
        <physical_Mem>585613312</physical_Mem>
        <io>
            <msg_in>1274844</msg_in>
            <msg_out>553653824</msg_out>
            <msg_dropped>490747</msg_dropped>
            <bytes_in>1323912355</bytes_in>
            <bytes_out>2139994186732</bytes_out>
            <reads>28333064</reads>
            <writes>441512631</writes>
            <bw_in>1412</bw_in>
            <bw_out>2311071</bw_out>
            <total_connects>76262</total_connects>
            <total_disconnects>76235</total_disconnects>
            <connected>27</connected>
            <rtmp_connects>27</rtmp_connects>
            <rtmfp_connects>0</rtmfp_connects>
            <normal_connects>27</normal_connects>
            <virtual_connects>0</virtual_connects>
            <group_connects>0</group_connects>
            <service_connects>0</service_connects>
            <service_requests>0</service_requests>
            <admin_connects>0</admin_connects>
            <debug_connects>0</debug_connects>
            <total_threads>4704</total_threads>
            <working_threads>0</working_threads>
            <swf_verification_attempts>0</swf_verification_attempts>
            <swf_verification_exceptions>0</swf_verification_exceptions>
            <swf_verification_failures>0</swf_verification_failures>
            <swf_verification_unsupported_rejects>0</swf_verification_unsupported_rejects>
            <swf_verification_matches>0</swf_verification_matches>
            <swf_verification_remote_misses>0</swf_verification_remote_misses>
            <server_bytes_in>0</server_bytes_in>
            <server_bytes_out>0</server_bytes_out>
            <rtmfp_lookups>0</rtmfp_lookups>
            <rtmfp_remote_lookups>0</rtmfp_remote_lookups>
            <rtmfp_remote_lookup_requests>0</rtmfp_remote_lookup_requests>
            <rtmfp_redirects>0</rtmfp_redirects>
            <rtmfp_remote_redirects>0</rtmfp_remote_redirects>
            <rtmfp_remote_redirect_requests>0</rtmfp_remote_redirect_requests>
            <rtmfp_forwards>0</rtmfp_forwards>
            <rtmfp_remote_forwards>0</rtmfp_remote_forwards>
            <rtmfp_remote_forward_requests>0</rtmfp_remote_forward_requests>
            <rtmfp_lookups_denied>0</rtmfp_lookups_denied>
        </io>
    </data>
</result>"""


def test_should_get_stats_from_edge_and_post_to_stewie(monkeypatch):
    get_args = []
    def fake_get(*args, **kwargs):
        class DummyResponse(object):
            content = SAMPLE_SERVER_STATS
        get_args.append({'args': args, 'kwargs': kwargs})
        return DummyResponse()
    monkeypatch.setattr(requests, 'get', fake_get)

    post_args = []
    def fake_post(*args, **kwargs):
        post_args.append({'args': args, 'kwargs': kwargs})
    monkeypatch.setattr(requests, 'post', fake_post)


    collector.collect('edge', 1111, 'user', 'password')

    # FMS collection asserts
    assert 1 == len(get_args)
    url = get_args[0]['args'][0]
    assert 'http://edge:1111/admin/getServerStats' == url
    params = get_args[0]['kwargs']['params']
    assert {'apswd': 'password', 'auser': 'user'} == params

    # Stewie post asserts
    assert 1 == len(post_args)
    url = post_args[0]['args'][0]
    assert collector.STEWIE_SERVER + '/api/metrics/' + collector.BUCKET + '/edge'  == url
    data = post_args[0]['kwargs']['data']
    assert '4704' == data['total_threads']
