from ptcdt.matchers import *

def test_params_exact_matcher():
    pem = ParamsExactMatcher([{"a": 1}, {"b": 2}])
    assert not pem.match([])
    assert not pem.match([{}, {}])
    assert pem.match([{"a": 1}, {"b": 2}])

def test_function_call_matcher():
    expected_params = [{"a": 1}, {"b": 2}]
    pem = ParamsExactMatcher(expected_params)
    matcher_result = ParamsMatcherResult(pem, "result")
    fcm = FunctionCallMatcher([matcher_result])
    assert fcm.match([]) == None
    assert fcm.match(expected_params) == matcher_result
    assert fcm.match(expected_params).result == "result"

def test_build_single_matcher():
    expected_params = [{"a": 1}, {"b": 2}]
    fcm = build_function_call_single_exact_matcher(expected_params, "result")
    assert fcm.match([]) == None
    assert fcm.match([{"a": 1}, {"b": 2}]).result == "result"
