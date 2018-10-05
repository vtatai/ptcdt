
def build_function_call_single_exact_matcher(expected_params, result):
    pem = ParamsExactMatcher(expected_params)
    matcher_result = ParamsMatcherResult(pem, result)
    return FunctionCallMatcher([matcher_result])

class FunctionCallMatcher:
    """
    param_matcher_result_list is a list with each element representing a single match across all parameters
    Each element is a ParamsMatcherResult
    """
    def __init__(self, params_matcher_result_list):
        self.params_matcher_result_list = params_matcher_result_list

    """
    Returns a ParamsMatcherResult, or None if no match.
    It doesn't return the actual value since None is valid return value.
    """
    def match(self, param_list):
        return next((result for result in self.params_matcher_result_list if result.match(param_list)), None)
        

class ParamsMatcherResult:
    def __init__(self, params_matcher, result):
        self.params_matcher = params_matcher
        self.result = result

    def match(self, param_list):
        return self.params_matcher.match(param_list)

class ParamsMatcher:
    """
    Return true for a match, false otherwise.
    """
    def match(self, param_list):
        raise NotImplementedError("Needs to be overriden")


class ParamsExactMatcher(ParamsMatcher):
    def __init__(self, expected_params):
        self.expected_params = expected_params
    
    """
    param_list should be already deserialized to dicts
    """
    def match(self, param_list):
        if len(param_list) != len(self.expected_params):
            return False
        return all([tpl[0] == tpl[1] for tpl in zip(self.expected_params, param_list)])

