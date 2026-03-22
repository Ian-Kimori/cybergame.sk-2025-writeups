import hashlib
import math
import re
from typing import Tuple, Optional

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.number import long_to_bytes
from pwnlib.tubes.remote import remote
from sympy.ntheory.modular import crt


class EllipticClient:
    def __init__(self, server_host: str, server_port: int, auto_connect: bool = True):
        self.server_host = server_host
        self.server_port = server_port
        self.remote = None  # this will be remote
        self.server_pub_key: Optional[Tuple] = None
        if auto_connect:
            self.connect()

    def connect(self):
        self.remote = remote(self.server_host, self.server_port)
        welcome = self.remote.recvuntil(b'Choice: ')
        decoded = welcome.decode()
        if 'Welcome to the ECC server!' not in decoded:
            raise ValueError('Unexpected server welcome message.')
        m = re.search(r'Server public key \(x,y\):\s*(\d+)\s+(\d+)', decoded)
        if not m:
            raise ValueError('Could not parse server public key.')
        self.server_pub_key = (int(m.group(1)), int(m.group(2)))

    def read_menu(self) -> bytes:
        return self.remote.recvuntil(b'Choice: ')

    def submit_client_pub_key(self, x, y):
        self.remote.sendline(b'1')
        self.remote.recvuntil(b'Send your client public key as two integers, space-separated: ')
        self.remote.sendline(f"{x} {y}".encode())
        self.remote.recvuntil(b'Client pubkey stored.')
        self.read_menu()

    def encrypt_message(self, msg) -> bytes:
        self.remote.sendline(b'2')
        self.remote.recvuntil(b'Enter message to encrypt: ')
        self.remote.sendline(msg.encode())
        self.remote.recvuntil(b'Ciphertext (hex): ')
        ciphertext = bytes.fromhex(self.remote.recvline().strip().decode())
        assert len(ciphertext) % 16 == 0
        self.read_menu()
        print('Got ciphertext:', ciphertext.hex())
        return ciphertext

    def submit_signed_doc(self, doc: str, signature: bytes):
        self.remote.sendline(b'3')
        self.remote.recvuntil(b'Send your data (must be >= 256 bytes): ')
        self.remote.sendline(doc.encode())
        self.remote.recvuntil(b'Send signature (in hex): ')
        self.remote.sendline(signature.hex().encode())
        print('Response:', self.read_menu())  # read all the way to the end of menu

    def get_ciphertext_for_point(self, x, y, msg="A" * 16):
        self.submit_client_pub_key(x, y)
        ct = self.encrypt_message(msg)
        return ct


def ec_add(p, a, P, Q):
    if P == Q:
        lmbd = (3 * P[0] * P[0] + a) * pow(2 * P[1], -1, p) % p
    else:
        lmbd = (Q[1] - P[1]) * pow(Q[0] - P[0], -1, p) % p
    xr = (lmbd * lmbd - P[0] - Q[0]) % p
    yr = (lmbd * (P[0] - xr) - P[1]) % p
    return (xr, yr)


def ec_mul(p, a, P, n):
    R = None
    for bit in bin(n)[2:]:
        if R:
            R = ec_add(p, a, R, R)
        if bit == '1':
            R = P if not R else ec_add(p, a, R, P)
    return R


def int_to_16_bytes(i):
    # Encode integer i as a 16-byte big-endian value (pad or truncate as needed)
    b = long_to_bytes(i)
    if len(b) > 16:
        return b[-16:]
    return b.rjust(16, b'\x00')


def aes_encrypt_from_point(point, plaintext):
    # Derive key and IV by encoding point coordinates directly
    key = int_to_16_bytes(point[0])
    iv = int_to_16_bytes(point[1])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(plaintext.encode(), 16))


def recover_key_modulo_order(client, point, order, msg='A' * 16):
    ct = client.get_ciphertext_for_point(*point, msg)
    print(f"Trying to recover d mod {order} using point {point}")
    p = 6277101735386680763835789423207666416083908700390324961279
    a = -3
    for i in range(1, order):
        shared = ec_mul(p, a, point, i)
        trial_ct = aes_encrypt_from_point(shared, msg)
        if trial_ct == ct:
            print(f"Found: d ≡ {i} mod {order}")
            print('-' * 120)
            return i
    print("Failed to find a match.")
    print('-' * 120)
    return None


def main():
    # small-subgroup generators on invalid curves: mapping order -> (x, y)
    invalid_curves = {
        3: [2, 3564686572671562380205906771922891792060700741352380195279,
            1755137614723965998727149556362974207761233596493898264326, 4],
        5: [1, 5366623076200026835529673457443383901317994259874882677620,
            4786855544997766131818335138323427112075270945347105566412, 0],
        17: [1, 60967062299896558617056622727330346210143051524748125127,
             5841038380958894158166962811912259669722206087417561922036, 0],
        257: [1, 1028032976390962608864347865621899238642173453015528535841,
              4763730109054252830370599209953375671102520576076803547120, 0],
        641: [1, 2287703753713785703977632390740920009361075573119163151548,
              2233424118022853726212113288124344840639577991790713605521, 0],
        41: [1, 558649172595487002797148663526674209886609755680409266714,
             5326547105079455733029488693260390671350685838621773652647, 1],
        8123: [1, 768365060380153345504866785083086570681617459914472073305,
               34208686004103822115965638165120633705099726233512303412, 1],
        233: [1, 5574071242169118619378041649656941966914935657843907211119,
              5291880320459922475156010140424872444997345381764158985554, 3],
        1423: [1, 6191686162154322772748681008059641529768422974510125357352,
               4920636234816990609116914555506233362432061366694914116693, 3],
        239: [1, 4008655052127370879421033500736133207720204611108505303036,
              2086369860614369306957842214810915214569743285758981667461, 4],
        13: [1, 4644972655678029260717137018699262693286411721618201863106,
             2202517178366017551273947789829821527068675646811323009593, 6],
        167: [1, 3645022611433777065943509259856394173231724772818984686670,
              2621369249975321417458412123128786723400388749400936529296, 7],
        29: [1, 2925378651356186805215389121065940965763735977825177930045,
             3273783829349294045338795220123518483083173074990540050952, 8],
        3041: [1, 5426269876735728914164941922975966395232998341767577277936,
               1079770548351252653891432167077819724707746822267748989702, 8],
        3413: [1, 1665924069170038736445685934100038610540691663095918059849,
               5519820784480353138756509197536840612766817680924659280500, 8],
        3727: [1, 1982780142949105177599194001037251178177773920580356006113,
               738705568596011643247030639566989136717421702589374904131, 9],
        6899: [1, 5881158799712332288374651535907106204938193703164415652263,
               2042893853168704114846669818144954302751992973735172279470, 9],
        7: [2, 3356684854441204689117464067895344518577673104354539736849,
            4525122467008071839640952907912591437010192189921205325137, 19],
        103: [1, 4921417115736950547572508610307886108441225488412538156589,
              3047339816660032117190800913014745253048479083899469926477, 12],
        191: [1, 1027709665880694672348602020035672149114610500670466745363,
              3787383670361231999120150243828184193706915071013862633947, 13],
        743: [1, 47846793157999164008482542828815177510809361925741168976,
              4802273658261197945464701973698739506945046699669717321480, 16],
        23: [1, 4279273032968751660654484216619820778157739707508641641633,
             5273345343693100726624243340993140056935306333788646500046, 17],
        1583: [1, 2689812144576459818732464884544721273061955832733373983012,
               1549681805203873708239409837206451605807054895672521729811, 18],
        11: [1, 4356182680556737282454288385079882746425686504627869848655,
             4518345919053582119711250308650827869427096933344190523781, 20],
        53: [1, 5663476353803329395968217381331650682853731183776862397284,
             518109329918348888653240198441938218078963171905116794589, 21],
        83: [1, 5145746038573530357273202084899799727589764539731857429509,
             4329304489313480536777654659163556009219959716944360173857, 21],
        941: [1, 3547165237578891306008222585934108308319533878668551577129,
              1019449522503426423746832589765358916903692186017819171708, 21]

    }
    fake_points = {prime: (curve[1], curve[2]) for prime, curve in invalid_curves.items()}

    client = EllipticClient('exp.cybergame.sk', 7005)
    # client = EllipticClient('127.0.0.1', 10000)
    print(f'Connected! Server pubkey: {client.server_pub_key}')

    msg = "A" * 16
    residues = []
    moduli = []

    print('-' * 120)
    for order, point in fake_points.items():
        res = recover_key_modulo_order(client, point, order, msg)
        if res is not None:
            residues.append(res)
            moduli.append(order)

    # Display the product of recovered moduli for diagnostics
    product_moduli = math.prod(moduli) if moduli else 1
    print(f"Product of recovered moduli: {product_moduli}")
    print(f"Bit-length of product: {product_moduli.bit_length()}")

    # Warn if the accumulated modulus is insufficient to cover the curve group order
    curve_order = 6277101735386680763835789423176059013767194773182842284081
    curve_bits = curve_order.bit_length()
    if product_moduli <= curve_order:
        print(f"Warning: product bit-length ({product_moduli.bit_length()}) ≤ curve order bit-length ({curve_bits}).")
        print("You need more residues so that the product of moduli exceeds the curve order.")
        print("Maybe you were unlucky, if it was fairly close, try again, server has a new private key each time.")
    else:
        print(f"Product bit-length ({product_moduli.bit_length()}) > curve order bit-length ({curve_bits}). Great!")
        priv_key, _ = crt(moduli, residues)
        print(f"\nRecovered private key ≡ {priv_key} mod {math.prod(moduli)}")

        # --- Forge and submit signature ---
        # Prepare a ≥256-byte document
        document = 'B' * 256

        # Compute signature = SHA256(d_bytes ‖ document)
        d_bytes = long_to_bytes(priv_key)
        signature = hashlib.sha256(d_bytes + document.encode() + b'\n').digest()  # add \n because !@#$ my life

        client.submit_signed_doc(document, signature)


if __name__ == '__main__':
    main()
