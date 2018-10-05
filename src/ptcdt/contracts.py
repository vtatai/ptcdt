class ServiceContract:
    """
    function_contracts is a map from function name (Thrift doesn't allow overloading) to a
    function contract
    """
    def __init__(self, function_contracts):
        self.function_contracts = function_contracts

    def match_contract(self, function_name, call_params):
        if not self.function_contracts.has_key(function_name):
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
        matched_fcm = None
        for fcm in self.function_call_matchers:
            params_matcher_result = fcm.match(call_params) 
            if params_matcher_result != None:
                matched_fcm = params_matcher_result
                break
        if matched_fcm == None:
            raise UndefinedContractException
        return matched_fcm.result

class UndefinedContractException(Exception):
    pass
