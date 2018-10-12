from ptcdt.contracts import *
import pytest
import utils

@pytest.fixture
def simple_contract():
    filename = utils.test_resource_path("contracts/simple.tpact")
    return parse_contract(filename)

def test_simple_contract_parsing(simple_contract):
    assert simple_contract.provider.name == "ThriftTest"
    assert simple_contract.consumer.name == "ThriftTestConsumer"
    assert len(simple_contract.interactions) == 1
    interaction = simple_contract.interactions[0]
    assert interaction.provider_state == "Test struct constant returns"
    assert interaction.description == "Description"
    assert interaction.service == "ThriftTest"
    assert interaction.request.method == "testStruct"
    assert len(interaction.request.arguments) == 1
    assert interaction.request.arguments[0] == {"string_thing": "string_thingy", 
            "byte_thing": 0, "i16_thing": 16, "i32_thing": 32, "i64_thing": 64}
    assert interaction.response.value == {"string_thing": "string_thingy2", 
            "byte_thing": 1, "i16_thing": 17, "i32_thing": 33, "i64_thing": 65}

