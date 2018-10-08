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
