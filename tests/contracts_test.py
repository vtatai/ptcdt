from ptcdt.contracts import *
from ptcdt.matchers import *
import utils

def test_service_contract_simple_string():
    expected_params = ["first"]
    function_call_matcher = build_function_call_single_exact_matcher(expected_params, "result")
    function_contract = FunctionContract([function_call_matcher])
    service_contract = ServiceContract({"testFunction": function_contract})

    assert service_contract.match_contract("testFunction", expected_params) == "result"


def test_service_contract_simple_struct():
    expected_params = [{"a": 1}, {"b": 2}]
    function_call_matcher = build_function_call_single_exact_matcher(expected_params, "result")
    function_contract = FunctionContract([function_call_matcher])
    service_contract = ServiceContract({"testFunction": function_contract})

    assert service_contract.match_contract("testFunction", expected_params) == "result"
    
def test_simple_contract_parsing():
    filename = utils.test_resource_path("contracts/simple.tpact")
    contract = parse_contract(filename)
    assert contract.provider.name == "ThriftTest"
    assert contract.consumer.name == "ThriftTestConsumer"
    assert len(contract.interactions) == 1
    interaction = contract.interactions[0]
    assert interaction.provider_state == "Test struct constant returns"
    assert interaction.description == "Description"
    assert interaction.service == "ThriftTest"
    assert interaction.request.method == "testStruct"
    assert len(interaction.request.arguments) == 1
    assert interaction.request.arguments[0] == {"string_thing": "string_thingy", 
            "byte_thing": 0, "i16_thing": 16, "i32_thing": 32, "i64_thing": 64}
    assert interaction.response.value == {"string_thing": "string_thingy2", 
            "byte_thing": 1, "i16_thing": 17, "i32_thing": 33, "i64_thing": 65}

