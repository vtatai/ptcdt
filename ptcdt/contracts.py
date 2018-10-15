import json
import logging

logger = logging.getLogger(__name__)

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

    def match(self, service, method, call_params):
        try:
            return next(res.value for res in map(lambda i: i.match(service, method, call_params), self.interactions) if res != None)
        except StopIteration:
            raise UndefinedContractException(f"Could not match {service}.{method}({call_params})")

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

    """
    Checks if the response for this interaction matches, and if so returns 
    the response of type Response. Response might encapsulate either a dict; a simple value; or None.
    If no match is found, None is returned (as opposed to Response.value == None, which can be used for
    void returning methods, or if None is the actual expected value.
    """
    def match(self, service, method, call_params):
        if self.service != service:
            return None
        if self.request.match(method, call_params):
            logger.info(f"Matched interaction {self.description} to params {call_params}.")
            return self.response
        return None

class Request:
    def __init__(self, method, arguments=[]):
        self.method = method
        self.arguments = arguments

    @classmethod
    def from_dict(cls, d):
        return Request(d.get('method'), d.get('arguments'))

    """
    Just does an exact match *for now*.
    """
    def match(self, method, call_params):
        assert isinstance(call_params, list)
        if self.method != method or len(call_params) != len(self.arguments):
            return False
        return all([tpl[0] == tpl[1] for tpl in zip(self.arguments, call_params)])


class Response:
    def __init__(self, value=None):
        self.value = value

    @classmethod
    def from_dict(cls, d):
        return Response(d.get('value'))

class UndefinedContractException(Exception):
    pass
