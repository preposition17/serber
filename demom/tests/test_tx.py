from eospy.keys import EOSKey
from eospy.cleos import Cleos
from eospy.keys import get_curve
from binascii import hexlify, unhexlify
from eospy.types import PackedTransaction
from eospy.types import EOSBuffer
from eospy import types


ce = Cleos(url="https://testnet.waxsweden.org")
key = EOSKey("5JfLUb6bPAmJ3e2BrPBskkR5HrNrxBm1iP2DFazbwyxMwWAeFgz")


arguments = {
    "claimer": "mandytestnet",
    "drop_id": 1033,
    "amount": 1,
    "intended_delphi_median": 0,
    "authkey_key": "PUB_K1_7SeKnWrsrCFcmVY7rGY9rt1BgoqtV2kYgQz7PMfAio1bs8XTj7",
    "signature_nonce": 3452693246,
    "claim_signature": "SIG_K1_K7esVkZyxLfsVcCA5W9Ce3P2FEjyNyZj1QJXPKyceBQHVZWTSDAEosS2A6QDGYEYKtbQEnSmoR9V1BqG47nyzTkURzEqF3",
    "referrer": "NeftyBlocks",
    "country": "RU",
    "currency": "8,WAX"
}

payload = {
    "account": "neftyblocksd",
    "name": "claimdropkey",
    "authorization": [{
        "actor": "mandytestnet",
        "permission": "active",
    }],
}
# Converting payload to binary
# data = ce.abi_json_to_bin(payload['account'], payload['name'], arguments)
# print(data)
#
# tx = b"90d5cc58659fa6910904000000000000010000000000000000000000000350673f5203d5198cb79ca1c15d0fbd2653cf036a564f367a68cadba3fd58cd1bfeeacbcd00000000001f5ec44a55ab589f38240236ace6c87dc5c6a6ed34d12dab61e3002f80589d727d2f2858afe57eafcb0ae293448cce1c5b60d3ef306dd257004a99bfd225f6d0510b4e65667479426c6f636b730252550857415800000000"
tx = b"8936006284a7b5af5fc90000000003e04dc5ea1e9f979a00000000e88abca901e04dc5ea1e9f979a00000000a8ed32320000a6823403ea3055000000572d3ccdcd0190d5cc58659fa69100000000a8ed32322890d5cc58659fa691903044341e9f979a00c2eb0b000000000857415800000000076465706f736974903044341e9f979ae015acf426e94c440190d5cc58659fa69100000000a8ed32329f0190d5cc58659fa6910904000000000000010000000000000000000000000350673f5203d5198cb79ca1c15d0fbd2653cf036a564f367a68cadba3fd58cd1bfeeacbcd00000000001f5ec44a55ab589f38240236ace6c87dc5c6a6ed34d12dab61e3002f80589d727d2f2858afe57eafcb0ae293448cce1c5b60d3ef306dd257004a99bfd225f6d0510b4e65667479426c6f636b73025255085741580000000000"
# data = ce.abi_bin_to_json(payload['account'], payload['name'], tx)
# print(data)

trx = PackedTransaction(tx, ce)
trx_buf = trx._decode_header(types.AbiAction("neftyblocksd"))
print(trx.decode_actions(trx_buf))


{
  "signatures": [
    "SIG_K1_KAKExNxgvCXPw1rYhbL2PXs5x9WNdmWrhPgyp7VKeDe7QgF6mtQ2RCs4EbHyQkZ3LqMsNj8WcJz2X4xaEnZz1MDtkfBmwa"
  ],
  "compression": "none",
  "packed_context_free_data": "",
  "packed_trx": "4d52006204df6d9050910000000003e04dc5ea1e9f979a00000000e88abca901e04dc5ea1e9f979a00000000a8ed32320000a6823403ea3055000000572d3ccdcd0190d5cc58659fa69100000000a8ed32322890d5cc58659fa691903044341e9f979a00c2eb0b000000000857415800000000076465706f736974903044341e9f979ae015acf426e94c440190d5cc58659fa69100000000a8ed32329f0190d5cc58659fa6910904000000000000010000000000000000000000000350673f5203d5198cb79ca1c15d0fbd2653cf036a564f367a68cadba3fd58cd1bb09effcb00000000002025603e5baf05e5f190817bf185f3b62c93f86b0ce7d759e7ac6a425b5d6a087677883db8861667a25cfc9d54eff498b21465b8fdb73b7df67c98a40f4d7036120b4e65667479426c6f636b73025255085741580000000000"
}

