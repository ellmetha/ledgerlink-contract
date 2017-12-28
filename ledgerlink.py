"""

    Ledgerlink smart contract
    =========================

    The ledgerlink (A.K.A. ledgr.link) smart contract provides a way to generate shortened-URLs and
    store the related unique codes (as of the the corresponding URL) into the NEO blockchain. This
    has the advantage of allowing to store irreplaceable short URLs in the blockchain. The codes and
    the corresponding URLs cannot be changed by anybody and will live forever on the NEO blockchain.

"""

from boa.blockchain.vm.Neo.Runtime import CheckWitness, GetTrigger
from boa.blockchain.vm.Neo.TriggerType import Application, Verification


# -------------------------------------------
# TOKEN SETTINGS
# -------------------------------------------

# Script hash of the contract owner.
OWNER = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

# The URL of the associated URL shortener service.
SHORTENER_URL = 'https://ledgr.link'


# -------------------------------------------
# EVENTS
# -------------------------------------------

def Main(operation, args):
    """ Main entrypoint for the smart contract.

    :param operation: the operation to be performed
    :param args: a list of arguments (which may be empty, but not absent)
    :type operation: str
    :type args: list
    :return: a boolean indicating the successful execution of the smart contract
    :rtype: bool

    """

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
        if operation == 'shortenerURL':
            url = SHORTENER_URL
            return url

        result = 'unknown operation'
        return result

    return False
