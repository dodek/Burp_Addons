from burp import IBurpExtender
from burp import IIntruderPayloadGeneratorFactory
from burp import IIntruderPayloadProcessor
from burp import IIntruderPayloadGenerator
from itertools import product

# hard-coded payloads
# [in reality, you would use an extension for something cleverer than this]

PAYLOADS = [
    bytearray("|"),
    bytearray("<script>alert(1)</script>")
]


class BurpExtender(IBurpExtender, IIntruderPayloadGeneratorFactory, IIntruderPayloadProcessor):

    #
    # implement IBurpExtender
    #

    def registerExtenderCallbacks(self, callbacks):
        # obtain an extension helpers object
        self._helpers = callbacks.getHelpers()

        # set our extension name
        callbacks.setExtensionName("Mixed Case Iterator")

        # register ourselves as an Intruder payload generator
        callbacks.registerIntruderPayloadGeneratorFactory(self)

        # register ourselves as an Intruder payload processor
        callbacks.registerIntruderPayloadProcessor(self)

    #
    # implement IIntruderPayloadGeneratorFactory
    #

    def getGeneratorName(self):
        return "Mixed Case Iterator"

    def createNewInstance(self, attack):
        # return a new IIntruderPayloadGenerator to generate payloads for this attack
        return IntruderPayloadGenerator()

    #
    # implement IIntruderPayloadProcessor
    #

    def getProcessorName(self):
        return "Serialized input wrapper"

    def processPayload(self, currentPayload, originalPayload, baseValue):
        # decode the base value
        dataParameter = self._helpers.bytesToString(
            self._helpers.base64Decode(self._helpers.urlDecode(baseValue)))

        # parse the location of the input string in the decoded data
        start = dataParameter.index("input=") + 6
        if start == -1:
            return currentPayload

        prefix = dataParameter[0:start]
        end = dataParameter.index("&", start)
        if end == -1:
            end = len(dataParameter)

        suffix = dataParameter[end:len(dataParameter)]

        # rebuild the serialized data with the new payload
        dataParameter = prefix + self._helpers.bytesToString(currentPayload) + suffix
        return self._helpers.stringToBytes(
            self._helpers.urlEncode(self._helpers.base64Encode(dataParameter)))


#
# class to generate payloads from a simple list
#

class IntruderPayloadGenerator(IIntruderPayloadGenerator):
    def __init__(self):
        self._payloadIndex = 0
        print('generate payloads here?')

    def hasMorePayloads(self):
        return self._payloadIndex < len(PAYLOADS)

    def getNextPayload(self, baseValue):
        if self._payloadIndex ==0:
            print(baseValue)
            global PAYLOADS
            PAYLOADS= self.GeneratePayloads(baseValue)
            print(PAYLOADS)

        print('generate payloads here?'+baseValue)
        payload = PAYLOADS[self._payloadIndex]
        self._payloadIndex = self._payloadIndex + 1

        return payload

    def GeneratePayloads(self, baseValue):
        return list(map(''.join, product(*(sorted(set((chr(c).upper(), chr(c).lower())))
                                       for c in baseValue))))

    def reset(self):
        self._payloadIndex = 0
