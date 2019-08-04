rpc_docs = {
  "/": {
    "GET": {
      "descr": "All the information about a block.",
      "args": [],
      "ret": "Object"
    }
  },
  "/chains": {
    "item": {
      "name": "chain_id",
      "descr": "A chain identifier. This is either a chain hash in Base58Check notation or a one the predefined aliases: 'main', 'test'."
    }
  },
  "/chains/{}": {
    "props": [
      "blocks",
      "chain_id",
      "checkpoint",
      "invalid_blocks",
      "mempool"
    ]
  },
  "/chains/{}/blocks": {
    "GET": {
      "descr": "Lists known heads of the blockchain sorted with decreasing fitness. Optional arguments allows to returns the list of predecessors for known heads or the list of predecessors for a given list of blocks.",
      "args": [
        {
          "name": "length",
          "descr": "The requested number of predecessors to returns (per requested head)."
        },
        {
          "name": "head",
          "descr": "An empty argument requests blocks from the current heads. A non empty list allow to request specific fragment of the chain."
        },
        {
          "name": "min_date",
          "descr": "When `min_date` is provided, heads with a timestamp before `min_date` are filtered out"
        }
      ],
      "ret": "Array"
    },
    "item": {
      "name": "block_id",
      "descr": "A block identifier. This is either a block hash in Base58Check notation, one the predefined aliases: 'genesis', 'head' or a block level (index in the chain). One might also use 'head~N' or '<hash>~N' where N is an integer to denote the Nth predecessor of the designated block.Also, '<hash>+N' denotes the Nth successor of a block."
    }
  },
  "/chains/{}/chain_id": {
    "GET": {
      "descr": "The chain unique identifier.",
      "args": [],
      "ret": "Object"
    }
  },
  "/chains/{}/checkpoint": {
    "GET": {
      "descr": "The current checkpoint for this chain.",
      "args": [],
      "ret": "Object"
    }
  },
  "/chains/{}/invalid_blocks": {
    "GET": {
      "descr": "Lists blocks that have been declared invalid along with the errors that led to them being declared invalid.",
      "args": [],
      "ret": "Array"
    },
    "item": {
      "name": "block_hash",
      "descr": "block_hash (Base58Check-encoded)"
    }
  },
  "/chains/{}/invalid_blocks/{}": {
    "GET": {
      "descr": "The errors that appears during the block (in)validation.",
      "args": [],
      "ret": "Object"
    },
    "DELETE": {
      "descr": "Remove an invalid block for the tezos storage",
      "args": [],
      "ret": "Object"
    }
  },
  "/errors": {
    "GET": {
      "descr": "Schema for all the RPC errors from the shell",
      "args": [],
      "ret": "Object"
    }
  },
  "/fetch_protocol": {
    "item": {
      "name": "Protocol_hash",
      "descr": "Protocol_hash (Base58Check-encoded)"
    }
  },
  "/fetch_protocol/{}": {
    "GET": {
      "descr": "Fetch a protocol from the network.",
      "args": [],
      "ret": "Object"
    }
  },
  "/injection": {
    "props": [
      "block",
      "operation",
      "protocol"
    ]
  },
  "/injection/block": {
    "POST": {
      "descr": "Inject a block in the node and broadcast it. The `operations` embedded in `blockHeader` might be pre-validated using a contextual RPCs from the latest block (e.g. '/blocks/head/context/preapply'). Returns the ID of the block. By default, the RPC will wait for the block to be validated before answering.",
      "args": [
        {
          "name": "async",
          "descr": "\u00af\\_(\u30c4)_/\u00af"
        },
        {
          "name": "force",
          "descr": "\u00af\\_(\u30c4)_/\u00af"
        },
        {
          "name": "chain",
          "descr": "\u00af\\_(\u30c4)_/\u00af"
        }
      ],
      "ret": "Object"
    }
  },
  "/injection/operation": {
    "POST": {
      "descr": "Inject an operation in node and broadcast it. Returns the ID of the operation. The `signedOperationContents` should be constructed using a contextual RPCs from the latest block and signed by the client. By default, the RPC will wait for the operation to be (pre-)validated before answering. See RPCs under /blocks/prevalidation for more details on the prevalidation context.",
      "args": [
        {
          "name": "async",
          "descr": "\u00af\\_(\u30c4)_/\u00af"
        },
        {
          "name": "chain",
          "descr": "\u00af\\_(\u30c4)_/\u00af"
        }
      ],
      "ret": "Object"
    }
  },
  "/injection/protocol": {
    "POST": {
      "descr": "Inject a protocol in node. Returns the ID of the protocol.",
      "args": [
        {
          "name": "async",
          "descr": "\u00af\\_(\u30c4)_/\u00af"
        },
        {
          "name": "force",
          "descr": "\u00af\\_(\u30c4)_/\u00af"
        }
      ],
      "ret": "Object"
    }
  },
  "/monitor": {
    "props": [
      "active_chains",
      "bootstrapped",
      "commit_hash",
      "heads",
      "protocols",
      "valid_blocks"
    ]
  },
  "/monitor/active_chains": {
    "GET": {
      "descr": "Monitor every chain creation and destruction. Currently active chains will be given as first elements",
      "args": [],
      "ret": "Array"
    }
  },
  "/monitor/bootstrapped": {
    "GET": {
      "descr": "Wait for the node to have synchronized its chain with a few peers (configured by the node's administrator), streaming head updates that happen during the bootstrapping process, and closing the stream at the end. If the node was already bootstrapped, returns the current head immediately.",
      "args": [],
      "ret": "Object"
    }
  },
  "/monitor/commit_hash": {
    "GET": {
      "descr": "Get information on the build of the node.",
      "args": [],
      "ret": "Object"
    }
  },
  "/monitor/heads": {
    "item": {
      "name": "chain_id",
      "descr": "A chain identifier. This is either a chain hash in Base58Check notation or a one the predefined aliases: 'main', 'test'."
    }
  },
  "/monitor/heads/{}": {
    "GET": {
      "descr": "Monitor all blocks that are successfully validated by the node and selected as the new head of the given chain.",
      "args": [
        {
          "name": "next_protocol",
          "descr": "\u00af\\_(\u30c4)_/\u00af"
        }
      ],
      "ret": "Object"
    }
  },
  "/monitor/protocols": {
    "GET": {
      "descr": "Monitor all economic protocols that are retrieved and successfully loaded and compiled by the node.",
      "args": [],
      "ret": "Object"
    }
  },
  "/monitor/valid_blocks": {
    "GET": {
      "descr": "Monitor all blocks that are successfully validated by the node, disregarding whether they were selected as the new head or not.",
      "args": [
        {
          "name": "protocol",
          "descr": "\u00af\\_(\u30c4)_/\u00af"
        },
        {
          "name": "next_protocol",
          "descr": "\u00af\\_(\u30c4)_/\u00af"
        },
        {
          "name": "chain",
          "descr": "\u00af\\_(\u30c4)_/\u00af"
        }
      ],
      "ret": "Object"
    }
  },
  "/network": {
    "props": [
      "connections",
      "greylist",
      "log",
      "peers",
      "points",
      "self",
      "stat",
      "version",
      "versions"
    ]
  },
  "/network/connections": {
    "GET": {
      "descr": "List the running P2P connection.",
      "args": [],
      "ret": "Array"
    },
    "item": {
      "name": "peer_id",
      "descr": "A cryptographic node identity (Base58Check-encoded)"
    }
  },
  "/network/connections/{}": {
    "GET": {
      "descr": "Details about the current P2P connection to the given peer.",
      "args": [],
      "ret": "Object"
    },
    "DELETE": {
      "descr": "Forced close of the current P2P connection to the given peer.",
      "args": [
        {
          "name": "wait",
          "descr": "\u00af\\_(\u30c4)_/\u00af"
        }
      ],
      "ret": "Object"
    }
  },
  "/network/greylist": {
    "props": [
      "clear"
    ]
  },
  "/network/greylist/clear": {
    "GET": {
      "descr": "Clear all greylists tables.",
      "args": [],
      "ret": "Object"
    }
  },
  "/network/log": {
    "GET": {
      "descr": "Stream of all network events",
      "args": [],
      "ret": "Object"
    }
  },
  "/network/peers": {
    "GET": {
      "descr": "List the peers the node ever met.",
      "args": [
        {
          "name": "filter",
          "descr": "\u00af\\_(\u30c4)_/\u00af"
        }
      ],
      "ret": "Array"
    },
    "item": {
      "name": "peer_id",
      "descr": "A cryptographic node identity (Base58Check-encoded)"
    }
  },
  "/network/peers/{}": {
    "GET": {
      "descr": "Details about a given peer.",
      "args": [],
      "ret": "Object"
    },
    "props": [
      "ban",
      "banned",
      "log",
      "trust",
      "unban",
      "untrust"
    ]
  },
  "/network/peers/{}/ban": {
    "GET": {
      "descr": "Blacklist the given peer and remove it from the whitelist if present.",
      "args": [],
      "ret": "Object"
    }
  },
  "/network/peers/{}/banned": {
    "GET": {
      "descr": "Check if a given peer is blacklisted or greylisted.",
      "args": [],
      "ret": "Boolean"
    }
  },
  "/network/peers/{}/log": {
    "GET": {
      "descr": "Monitor network events related to a given peer.",
      "args": [
        {
          "name": "monitor",
          "descr": "\u00af\\_(\u30c4)_/\u00af"
        }
      ],
      "ret": "Array"
    }
  },
  "/network/peers/{}/trust": {
    "GET": {
      "descr": "Whitelist a given peer permanently and remove it from the blacklist if present. The peer cannot be blocked (but its host IP still can).",
      "args": [],
      "ret": "Object"
    }
  },
  "/network/peers/{}/unban": {
    "GET": {
      "descr": "Remove the given peer from the blacklist.",
      "args": [],
      "ret": "Object"
    }
  },
  "/network/peers/{}/untrust": {
    "GET": {
      "descr": "Remove a given peer from the whitelist.",
      "args": [],
      "ret": "Object"
    }
  },
  "/network/points": {
    "GET": {
      "descr": "List the pool of known `IP:port` used for establishing P2P connections.",
      "args": [
        {
          "name": "filter",
          "descr": "\u00af\\_(\u30c4)_/\u00af"
        }
      ],
      "ret": "Array"
    },
    "item": {
      "name": "point",
      "descr": "A network point (ipv4:port or [ipv6]:port)."
    }
  },
  "/network/points/{}": {
    "GET": {
      "descr": "Details about a given `IP:addr`.",
      "args": [],
      "ret": "Object"
    },
    "PUT": {
      "descr": "Connect to a peer",
      "args": [
        {
          "name": "timeout",
          "descr": "\u00af\\_(\u30c4)_/\u00af"
        }
      ],
      "ret": "Object"
    },
    "props": [
      "ban",
      "banned",
      "log",
      "trust",
      "unban",
      "untrust"
    ]
  },
  "/network/points/{}/ban": {
    "GET": {
      "descr": "Blacklist the given address and remove it from the whitelist if present.",
      "args": [],
      "ret": "Object"
    }
  },
  "/network/points/{}/banned": {
    "GET": {
      "descr": "Check is a given address is blacklisted or greylisted.",
      "args": [],
      "ret": "Boolean"
    }
  },
  "/network/points/{}/log": {
    "GET": {
      "descr": "Monitor network events related to an `IP:addr`.",
      "args": [
        {
          "name": "monitor",
          "descr": "\u00af\\_(\u30c4)_/\u00af"
        }
      ],
      "ret": "Array"
    }
  },
  "/network/points/{}/trust": {
    "GET": {
      "descr": "Trust a given address permanently and remove it from the blacklist if present. Connections from this address can still be closed on authentication if the peer is greylisted.",
      "args": [],
      "ret": "Object"
    }
  },
  "/network/points/{}/unban": {
    "GET": {
      "descr": "Remove an address from the blacklist.",
      "args": [],
      "ret": "Object"
    }
  },
  "/network/points/{}/untrust": {
    "GET": {
      "descr": "Remove an address from the whitelist.",
      "args": [],
      "ret": "Object"
    }
  },
  "/network/self": {
    "GET": {
      "descr": "Return the node's peer id",
      "args": [],
      "ret": "Object"
    }
  },
  "/network/stat": {
    "GET": {
      "descr": "Global network bandwidth statistics in B/s.",
      "args": [],
      "ret": "Object"
    }
  },
  "/network/version": {
    "GET": {
      "descr": "Supported network layer version.",
      "args": [],
      "ret": "Object"
    }
  },
  "/network/versions": {
    "GET": {
      "descr": "DEPRECATED: use `version` instead.",
      "args": [],
      "ret": "Array"
    }
  },
  "/protocols": {
    "GET": {
      "descr": "\u00af\\_(\u30c4)_/\u00af",
      "args": [],
      "ret": "Array"
    },
    "item": {
      "name": "Protocol_hash",
      "descr": "Protocol_hash (Base58Check-encoded)"
    }
  },
  "/protocols/{}": {
    "GET": {
      "descr": "\u00af\\_(\u30c4)_/\u00af",
      "args": [],
      "ret": "Object"
    }
  },
  "/stats": {
    "props": [
      "gc",
      "memory"
    ]
  },
  "/stats/gc": {
    "GET": {
      "descr": "Gets stats from the OCaml Garbage Collector",
      "args": [],
      "ret": "Object"
    }
  },
  "/stats/memory": {
    "GET": {
      "descr": "Gets memory usage stats",
      "args": [],
      "ret": "Object"
    }
  },
  "/workers": {
    "props": [
      "block_validator",
      "chain_validators",
      "prevalidators"
    ]
  },
  "/workers/block_validator": {
    "GET": {
      "descr": "Introspect the state of the block_validator worker.",
      "args": [],
      "ret": "Object"
    }
  },
  "/workers/chain_validators": {
    "GET": {
      "descr": "Lists the chain validator workers and their status.",
      "args": [],
      "ret": "Array"
    },
    "item": {
      "name": "chain_id",
      "descr": "A chain identifier. This is either a chain hash in Base58Check notation or a one the predefined aliases: 'main', 'test'."
    }
  },
  "/workers/chain_validators/{}": {
    "GET": {
      "descr": "Introspect the state of a chain validator worker.",
      "args": [],
      "ret": "Object"
    },
    "props": [
      "peers_validators"
    ]
  },
  "/workers/chain_validators/{}/peers_validators": {
    "GET": {
      "descr": "Lists the peer validator workers and their status.",
      "args": [],
      "ret": "Array"
    },
    "item": {
      "name": "peer_id",
      "descr": "A cryptographic node identity (Base58Check-encoded)"
    }
  },
  "/workers/chain_validators/{}/peers_validators/{}": {
    "GET": {
      "descr": "Introspect the state of a peer validator worker.",
      "args": [],
      "ret": "Object"
    }
  },
  "/workers/prevalidators": {
    "GET": {
      "descr": "Lists the Prevalidator workers and their status.",
      "args": [],
      "ret": "Array"
    },
    "item": {
      "name": "chain_id",
      "descr": "A chain identifier. This is either a chain hash in Base58Check notation or a one the predefined aliases: 'main', 'test'."
    }
  },
  "/workers/prevalidators/{}": {
    "GET": {
      "descr": "Introspect the state of prevalidator workers.",
      "args": [],
      "ret": "Object"
    }
  }
}
