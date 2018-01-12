"""
    Ledgerlink smart contract
    =========================

    The ledgerlink (A.K.A. ledgr.link) smart contract provides a way to generate shortened-URLs and
    store the related unique codes (as of the the corresponding URL) into the NEO blockchain. This
    has the advantage of allowing to store irreplaceable short URLs in the blockchain. The codes and
    the corresponding URLs cannot be changed by anybody and will live forever on the NEO blockchain.

"""

from boa.blockchain.vm.Neo.Action import RegisterAction
from boa.blockchain.vm.Neo.Blockchain import GetHeader, GetHeight
from boa.blockchain.vm.Neo.Output import GetScriptHash
from boa.blockchain.vm.Neo.Runtime import CheckWitness, GetTrigger
from boa.blockchain.vm.Neo.Storage import Get, GetContext, Put
from boa.blockchain.vm.Neo.TriggerType import Application, Verification
from boa.blockchain.vm.System.ExecutionEngine import GetScriptContainer
from boa.code.builtins import concat, substr


# -------------------------------------------
# TOKEN SETTINGS
# -------------------------------------------

# Script hash of the contract owner.
OWNER = b'#\xba\'\x03\xc52c\xe8\xd6\xe5"\xdc2 39\xdc\xd8\xee\xe9'

# The URL of the associated URL shortener service.
INITIAL_SHORTENER_URL = b'https://ledgr.link'

# The key that will be used to store the shortener URL in the smart contract's storage.
SHORTENER_URL_STORAGE_KEY = b'__shortenerurl__'


# -------------------------------------------
# EVENTS
# -------------------------------------------

DispatchNewURLEvent = RegisterAction('urladd', 'code', 'url')


# -------------------------------------------
# CONTRACT METHODS
# -------------------------------------------

def Main(operation, args):
    """ Main entrypoint for the smart contract.

    :param operation: the operation to be performed
    :param args: a list of arguments (which may be empty, but not absent)
    :type operation: str
    :type args: list
    :return: a boolean, a string or a byte array indicating the result of the execution of the SC
    :rtype: bool, string or bytearray

    """

    arg_length_error = 'Incorrect number of arguments'

    # Uses the trigger to dertermine whether this smart contract is being run in 'verification' mode
    # or 'application' mode.
    trigger = GetTrigger()

    # The 'Verification' mode is used when trying to spend assets (eg. NEO, Gas) on behalf of this
    # contract's address.
    if trigger == Verification():
        # Checks whether the script that sent this is the owner. If so we can allow the operation.
        is_owner = CheckWitness(OWNER)
        if is_owner:
            return True
        return False
    elif trigger == Application():
        if operation == 'deploy':
            result = deploy()
            return result
        elif operation == 'addURL':
            if len(args) == 1:
                url = args[0]
                result = add_url(url)
                return result
            return arg_length_error
        elif operation == 'getShortenerURL':
            url = get_shortener_url()
            return url
        elif operation == 'getURL':
            if len(args) == 1:
                code = args[0]
                result = get_url(code)
                return result
            return arg_length_error
        elif operation == 'getURLInfo':
            if len(args) == 1:
                code = args[0]
                result = get_url_info(code)
                return result
            return arg_length_error
        elif operation == 'setShortenerURL':
            if len(args) == 1:
                url = args[0]
                result = set_shortener_url(url)
                return result
            return arg_length_error

        result = 'unknown operation'
        return result

    return False


def deploy():
    """ Deploys the smart contract and initializes the shortener URL. """
    # Checks that the user that triggered the operation is the owner. If not we cannot allow the
    # operation because only the owner of the smart contract is able to run the deploy operation.
    is_owner = CheckWitness(OWNER)
    if not is_owner:
        return False

    context = GetContext()

    is_contract_initialized = Get(context, '__initialized__')
    if not is_contract_initialized:
        # Runs deploy logic.
        Put(context, '__initialized__', 1)
        Put(context, SHORTENER_URL_STORAGE_KEY, INITIAL_SHORTENER_URL)
        return True

    return False


def add_url(url):
    """ Generates a new code and stores the <code, url> pair into the blockchain. """
    # Retrieves the current "height" of the blockchain, as of the related block and timestamp.
    current_height = GetHeight()
    header = GetHeader(current_height)

    # Retrieves the hash of the considered sender.
    tx = GetScriptContainer()
    references = tx.References
    ref = references[0]
    sender = GetScriptHash(ref)

    # Generates a random number from the consensus data of the block (the pseudo-random number
    # generated by the consensus node).
    random_number = header.ConsensusData >> 32
    url_seed = url[:16] >> 96

    # Generates a unique code.
    s1 = b58encode(current_height, 6)
    s2 = b58encode(random_number, 2)
    s3 = b58encode(url_seed, 4)
    code_p1 = concat(s1, s2)
    code = concat(code_p1, s3)

    # Puts the URL and the related information into the ledger.
    context = GetContext()
    contextkey_for_url = get_contextkey_for_url(code)
    contextkey_for_sender = get_contextkey_for_sender(code)
    # NOTE: dictionaries are not yet supported by the neo-boa compiler so we have to derive multiple
    # context keys from the code value for each item associated with the considered code.
    Put(context, contextkey_for_url, url)
    Put(context, contextkey_for_sender, sender)

    # Fires an event indicating which <code, url> pair has been persisted into the ledger.
    DispatchNewURLEvent(code, url)

    return True


def get_shortener_url():
    """ Returns the URL of the URL-shortener service. """
    context = GetContext()
    url = Get(context, SHORTENER_URL_STORAGE_KEY)
    return url


def get_url(code):
    """ Returns the URL associated with the considered code. """
    context = GetContext()
    contextkey_for_url = get_contextkey_for_url(code)
    url = Get(context, contextkey_for_url)
    return url


def get_url_info(code):
    """ Returns all the information available for the considered code. """
    context = GetContext()
    contextkey_for_url = get_contextkey_for_url(code)
    contextkey_for_sender = get_contextkey_for_sender(code)
    url = Get(context, contextkey_for_url)
    sender = Get(context, contextkey_for_sender)
    result = [url, sender]
    return result


def set_shortener_url(url):
    """ Allows to update the URL associated with the URL-shortener service. """
    # Checks that the user that triggered the operation is the owner. If not we cannot allow the
    # operation because only the owner of the smart contract can change the URL of the URL-shortener
    # service.
    is_owner = CheckWitness(OWNER)
    if not is_owner:
        return False

    context = GetContext()
    Put(context, SHORTENER_URL_STORAGE_KEY, url)

    return True


# -------------------------------------------
# UTILITIES
# -------------------------------------------


def b58encode(i, max_length):
    """ Encodes an integer using Base58. """
    alphabet = b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    code = b''

    current_length = 0
    while i and (current_length < max_length):
        newi = i // 58
        idx = i % 58
        i = newi
        c = substr(alphabet, idx, 1)

        if code == '\x00':
            code = c
        else:
            code = concat(c, code)

        current_length += 1

    return code


def get_contextkey_for_url(code):
    """ Returns the context key to use for retrieving an URL associated with a code. """
    contextkey = concat(code, '__url')
    return contextkey


def get_contextkey_for_sender(code):
    """ Returns the context key to use for retrieving a sender address associated with a code. """
    contextkey = concat(code, '__sender')
    return contextkey
