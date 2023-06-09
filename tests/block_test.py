import json
import random

import blockchain.block as block


def test_block_init():
    for i in range(100):
        block_index = random.randint(1, 100000)
        nonce_type = random.randint(1, 3)
        prev_hash = 'This is old TEST block'
        server_id = random.randint(1, 3)

        new_block = block.Block(block_index, prev_hash, nonce_type, server_id)

        assert new_block is not None

        assert new_block.hash is not None
        assert new_block.data is not None
        assert new_block.index is not None
        assert new_block.server_id is not None
        assert new_block.prev_hash is not None
        assert new_block.nonce is not None


def test_create_new_block():
    for i in range(100):
        block_index = random.randint(1, 100000)
        prev_hash = 'This is old TEST block'
        nonce_type = random.randint(1, 3)
        server_id = random.randint(1, 3)

        new_block = block.create_new_block(block_index, prev_hash, nonce_type, server_id)

        assert new_block.index == block_index
        assert new_block.prev_hash == prev_hash
        assert new_block.index == block_index
        assert new_block.server_id[0] == server_id


def test_generate_random_data():
    for i in range(100):
        block_index = 1
        prev_hash = 'Old_data'
        nonce_type = 1
        server_id = 1
        current_block = block.create_new_block(block_index, prev_hash, nonce_type, server_id)

        old_value_data = current_block.data
        old_value_length = len(current_block.data)
        new_value_length = random.randint(0, 255)

        current_block.generate_random_data(new_value_length)

        assert type(current_block.data) == str
        assert old_value_length != len(current_block.data)
        assert old_value_data != current_block.data
        assert len(current_block.data) == new_value_length


def test_generate_hash():
    for i in range(100):
        block_index = 1
        prev_hash = 'Old_Hash'
        nonce_type = 1
        server_id = 1
        current_block = block.create_new_block(block_index, prev_hash, nonce_type, server_id)

        assert type(current_block.hash) == str
        assert current_block.hash[-4:] == "0000"
        assert current_block.prev_hash == 'Old_Hash'


def test_block_to_json():
    for i in range(100):
        block_index = random.randint(1, 100000)
        prev_hash = 'This is old Json block'
        nonce_type = random.randint(1, 3)
        server_id = random.randint(1, 3)

        new_block = block.create_new_block(block_index, prev_hash, nonce_type, server_id)

        json_block = new_block.block_to_json()
        assert type(json_block) == str

        python_object = json.loads(json_block)

        index = int(python_object['index'])
        cur_hash = python_object['hash']
        prev_hash = python_object['prev_hash']
        data = python_object['data']
        nonce = int(python_object['nonce'])

        assert index == new_block.index
        assert cur_hash == new_block.hash
        assert prev_hash == new_block.prev_hash
        assert data == new_block.data
        assert nonce == new_block.nonce


def test_create_genesis():
    for i in range(100):
        genesis_block = block.create_genesis()

        assert genesis_block is not None
        assert type(genesis_block) == str

        python_object = json.loads(genesis_block)
        genesis_generated_by = python_object['This block generated by Node '][0]
        genesis_index = int(python_object['index'])
        genesis_hash = python_object['hash']
        genesis_prev_hash = python_object['prev_hash']
        genesis_data = python_object['data']

        assert genesis_generated_by == -1
        assert genesis_index == 0
        assert genesis_hash[-4:] == "0000"
        assert genesis_prev_hash == 'GENESIS'
        assert len(genesis_data) == 256
