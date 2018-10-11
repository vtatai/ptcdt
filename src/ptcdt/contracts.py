import json

def parse_contract(filename):
    with open(filename) as f:
        d = json.load(f)
        return Contract.from_dict(d)

class Contract:
    def __init__(self, provider, consumer, interactions=[]):
        self.provider = provider
        self.consumer = consumer
        self.interactions = interactions

    def add_interaction(self, interaction):
        self.interactions.append(interaction)

    @classmethod
    def from_dict(cls, d):
        return Contract(Provider.from_dict(d.get('provider')), Consumer.from_dict(d.get('consumer')), 
                Interaction.from_list(d.get('interactions')))

class Provider:
    def __init__(self, name):
        self.name = name

    @classmethod
    def from_dict(cls, d):
        return Provider(d.get('name'))

class Consumer:
    def __init__(self, name):
        self.name = name

    @classmethod
    def from_dict(cls, d):
        return Consumer(d.get('name'))

class Interaction:
    def __init__(self, provider_state, description, service, request=None, response=None):
        self.provider_state = provider_state
        self.description = description
        self.service = service
        self.request = request
        self.response = response

    @classmethod
    def from_list(cls, a):
        return list(map(lambda d: cls.from_dict(d), a))

    @classmethod
    def from_dict(cls, d):
        return Interaction(d.get('providerState'), d.get('description'), d.get('service'), 
                Request.from_dict(d.get('request')), Response.from_dict(d.get('response')))

class Request:
    def __init__(self, method, arguments=[]):
        self.method = method
        self.arguments = arguments

    @classmethod
    def from_dict(cls, d):
        return Request(d.get('method'), d.get('arguments'))

class Response:
    def __init__(self, value):
        self.value = value

    @classmethod
    def from_dict(cls, d):
        return Response(d.get('value'))

class ServiceContract:
    """
    function_contracts is a map from function name (Thrift doesn't allow overloading) to a
    function contract
    """
    def __init__(self, function_contracts):
        assert isinstance(function_contracts, dict)
        self.function_contracts = function_contracts

    """
    Matches the contract, returning the FunctionCallMatcher matched.
    Throws UndefinedContractException in case no contract matches.
    """
    def match_contract(self, function_name, call_params):
        if not function_name in self.function_contracts:
            raise UndefinedContractException
        return self.function_contracts[function_name].match_contract(call_params)

class FunctionContract:
    """
    function_call_matchers is a list of FunctionCallMatcher
    """
    def __init__(self, function_call_matchers):
        self.function_call_matchers = function_call_matchers

    """
    Iterates through all the function call matchers, returning the first result found.
    If no result is found, an exception is thrown.
    """
    def match_contract(self, call_params):
        matched_pmr = None
        for fcm in self.function_call_matchers:
            params_matcher_result = fcm.match(call_params) 
            if params_matcher_result != None:
                matched_pmr = params_matcher_result
                break
        if matched_pmr == None:
            raise UndefinedContractException
        return matched_pmr.result

class UndefinedContractException(Exception):
    pass
