from node import Node
import logging
import argparse
from threading import Thread
import asyncio

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log = logging.getLogger('Blockchain')
log.addHandler(handler)
log.setLevel(logging.DEBUG)

node = Node()

async def command():
    while True:
        cmd = input("Input your command and if your want to make a transaction you can try: \"trans-to-data\" or \"block\" if you want to make a block.\n")
        cmd = cmd.split("-")
        if cmd[0] == "trans":
            trans = node.make_transaction(int(cmd[1]), int(cmd[2]))
            await node.broadcast_transaction(trans)
        elif cmd[0] == "new_block":
            block = node.make_block(node.trans_pool)
            await node.broadcast_block(block)
        elif cmd[0] == "utxo":
            print(node.UTXO())
        elif cmd[0] == "headers":
            node.print_block_header()
        elif cmd[0] == "block":
            node.print_block(cmd[1])
        elif cmd[0] == "pool":
            node.print_transaction_pool()

def connect_to_bootstrap_node(loop, ip, port):
    loop.set_debug(True)

    loop.run_until_complete(node.listen(8894))
    bootstrap_node = (ip, int(port))
    loop.run_until_complete(node.node_bootstrap([bootstrap_node]))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        node.stop()
        loop.close()



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    thread = Thread(target=connect_to_bootstrap_node, args=[loop, "127.0.0.1", 8888])
    thread.start()
    asyncio.run(command())