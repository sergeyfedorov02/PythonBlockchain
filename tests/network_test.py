import threading
import time
import json

import blockchain.node as node
import blockchain.start_node as start_node


def test_start_node():
    server_id = 1
    current_node = node.Node(server_id)

    new_server = threading.Thread(target=start_node.start, args=(server_id, current_node))
    new_server.setDaemon(True)
    new_server.start()

    while current_node.block_index is None:
        time.sleep(0.1)

    assert len(current_node.blocks_array) == 1

    python_object = json.loads(current_node.blocks_array[0])
    prev_hash = python_object['prev_hash']
    index = python_object['index']

    assert prev_hash == 'GENESIS'
    assert index == 0


def test_valid_blockchain():
    node1 = node.Node(1)
    node2 = node.Node(2)
    node3 = node.Node(3)
    server1 = threading.Thread(target=start_node.start, args=(1, node1))
    server2 = threading.Thread(target=start_node.start, args=(2, node2))
    server3 = threading.Thread(target=start_node.start, args=(3, node3))
    server3.setDaemon(True)
    server2.setDaemon(True)
    server1.setDaemon(True)
    server3.start()
    server2.start()
    server1.start()

    while len(node1.blocks_array) < 50 or len(node2.blocks_array) < 50 or len(node3.blocks_array) < 50:
        time.sleep(0.1)

    for i in range(50):
        block_from_node_1 = json.loads(node1.blocks_array[i])
        block_from_node_2 = json.loads(node2.blocks_array[i])
        block_from_node_3 = json.loads(node3.blocks_array[i])

        assert block_from_node_1 == block_from_node_2 == block_from_node_3
