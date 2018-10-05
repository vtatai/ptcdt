from ptcdt.contracts import *
from ptcdt.matchers import *

def test_service_contract():
    expected_params = [{"a": 1}, {"b": 2}]
    function_call_matcher = build_function_call_single_exact_matcher(expected_params, "result")
    function_contract = FunctionContract([function_call_matcher])
    service_contract = ServiceContract({"testFunction": function_contract})

    assert service_contract.match_contract("testFunction", expected_params) == "result"
