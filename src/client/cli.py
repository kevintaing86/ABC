''' The cmd line interface '''
import cmd
import json

from src.client.helpers import cromulon
# TODO: this module should not explicitly import persist or config. Need api fot this
from src.core import mine, create_transaction, get_block, init_configuration
from src.network.network import start_server, seed_peers


class CLI(cmd.Cmd, object):
    """
    CLI class is where the controls for the CLI exist.
    """

    prompt = 'ABC:$ '  # shows at prompt
    intro = 'Welcome to ABC - A Block Chain. Type help or ? to list commands.\n'
    conf = None  # one config file with the peers,
    wallet = {}  # wallet data
    peers = {}  # peers

    # --- CLI commands ---
    def do_start(self, arg):
        'Starts mining process... we might want to mine in background?'
        # note wasn't able to figure out how to stop it...
        mine()

    def do_stop(self, arg):
        'Pauses mining process...'

    def do_exit(self, arg):
        'Exits program'
        return True

    def do_wallet(self, arg):
        'Prints address'
        print(json.dumps(self.wallet, indent=4, sort_keys=True))

    def do_peers(self, arg):
        'Prints peer info'
        print(json.dumps(self.peers, indent=4, sort_keys=True))

    def do_balance(self, arg):
        'Prints balance'
        print(json.dumps(self.wallet["amount"], indent=4, sort_keys=True))

    def do_info(self, arg):
        'Prints the info of the node, ie block height number of peers etc'
        print(json.dumps(self.conf.get_conf(), indent=4, sort_keys=True))

    def do_block_info(self, arg):
        'Prints the info of the block'
        # TODO: need to parse and check for valid input
        b = get_block(arg[:])
        print(json.dumps(b, indent=4, sort_keys=True))

    def do_send(self, arg):
        # TODO: add exception handling for wrong input format
        try:
            args = arg.split()
            create_transaction(args[0], int(args[1]))
        except ValueError as e:
            print(e)

    def do_showmewhatyougot(self, arg):
        'Show me what you got!'
        print(cromulon())

    def onecmd(self, line):
        """
        define $ as a shortcut for the mine command. x for exit
        and ask for confirmation when the interpreter exit
        :return: returns a response r
        """
        if line[:1] == '$':
            line = 'start '+line[1:]
        elif line[:1] == 'x':
            line = 'exit ' + line[1:]
        r = super(CLI, self).onecmd(line)
        if r:
            r = input('Are you sure you want to exit?(y/n):')=='y'
        return r

    def emptyline(self):
        ''' '''
        return False

    def preloop(self):
        'Do stuff on start'
        # this is where we want to check if new user
        # initialize if new user
        # 1) generate a public private key / wallet
        # 2) create genesis block and store new chain data
        # 3) make a request to generate peers
        #
        # also we want to load up any saved data if it exists
        #
        # 1) wallets / public private keys
        # 2) blockchain data
        # 3) peer data
        #

        self.conf = init_configuration()
        self.wallet = self.conf.get_conf("wallet")
        self.peers = self.conf.get_conf("peers")

    def postloop(self):
        'Do stuff on end'
        # this is where we want to save all the data on exit
        # we should also save stuff on events
        self.conf.save_conf()