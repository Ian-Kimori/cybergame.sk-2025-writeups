import math

from pwnlib.tubes.remote import remote

# these are from full_order.sage
Gx_full = 712977160523011164332895134518255348052729919682691971969124864602027894775652001453123839198202856668553708241429
Gy_full = 8503574352361294292975077913584974507443739357604946408771151335165788809103985847037660633383854856309989071516631

# exact group orders for E1, E2, E3
N1 = 221967046828044394694688089238337659791
N2 = 304976163582561072724319063824010449966
N3 = 260513061321772526352850035108140059180


class EllipticClient:
    def __init__(self, server_host: str, server_port: int, auto_connect: bool = True):
        self.server_host = server_host
        self.server_port = server_port
        self.remote = None  # this will be remote
        if auto_connect:
            self.connect()

    def connect(self):
        self.remote = remote(self.server_host, self.server_port)
        welcome = self.remote.recvuntil(b'Welcome to ECC Oracle!\n')
        decoded = welcome.decode().strip()
        if 'Welcome to ECC Oracle!' not in decoded:
            raise ValueError('Unexpected server welcome message.')

    def send_g_x_y(self, x, y):
        self.remote.recvuntil(b'Send g.x:\n')
        self.remote.sendline(f"{x}".encode())
        self.remote.recvuntil(b'Send g.y:\n')
        self.remote.sendline(f"{y}".encode())
        self.remote.recvuntil(b'Q1 = ')
        q1 = self.remote.recvline().strip()
        self.remote.recvuntil(b'Q2 = ')
        q2 = self.remote.recvline().strip()
        self.remote.recvuntil(b'Q3 = ')
        q3 = self.remote.recvline().strip()
        self.remote.recvuntil(b'Encrypted story:\n')
        story = self.remote.recvall()
        print(f'q1 = {q1}, q2 = {q2}, q3 = {q3}')
        print(f'story = {story.hex()}')
        return q1, q2, q3, story


def main():
    # client = EllipticClient('127.0.0.1', 11337, auto_connect=False)
    client = EllipticClient('exp.cybergame.sk', 7006, auto_connect=False)
    client.connect()
    print(f"Sending full-order G = (Gx_full, Gy_full)")
    q1, q2, q3, story = client.send_g_x_y(Gx_full, Gy_full)
    # compute bits of leakage = log2(lcm(N1, N2, N3))
    leaked_bits = math.log2(math.lcm(N1, N2, N3))
    print(f"Total bits leaked in one shot: {leaked_bits:.2f} bits")
    print(f"Received Q1={q1}, Q2={q2}, Q3={q3}")


if __name__ == '__main__':
    main()
