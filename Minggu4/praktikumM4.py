class Fact:
    def __init__(self, **kwargs):
        self.data = kwargs

class SmartDoorExpert:
    def __init__(self):
        self.facts = {}
        self.results = []
        self.rules_fired = []

    def declare(self, fact):
        self.facts = fact.data

    def reset(self):
        self.facts = {}
        self.results = []
        self.rules_fired = []

    def run(self):
        f = self.facts
        # Rule 1: Akses Normal
        if f.get('auth')=='success' and f.get('face')=='known' \
           and f.get('time')=='normal':
            self.results.append(('[AMAN] Akses normal', 'buka_kunci'))
            self.rules_fired.append('Rule 1')

        # Rule 2: Percobaan Tidak Sah
        if int(f.get('fail_count',0)) >= 3 \
           and f.get('motion')=='yes':
            self.results.append(('[MENCURIGAKAN] Percobaan gagal berulang',
                                 'kunci_ganda + notif_pemilik'))
            self.rules_fired.append('Rule 2')

        # Rule 3: Indikasi Perampokan
        if f.get('motion')=='yes' and f.get('face')=='unknown' \
           and f.get('time')=='night':
            self.results.append(('[BERBAHAYA] Orang asing malam hari',
                                 'alarm + rekam_video + notif_darurat'))
            self.rules_fired.append('Rule 3')

        # Rule 4: Social Engineering
        if int(f.get('guest_count',0)) > 2 \
           and f.get('owner_home')=='no':
            self.results.append(('[MENCURIGAKAN] Banyak tamu saat kosong',
                                 'interkom + notif_pemilik'))
            self.rules_fired.append('Rule 4')

        # Rule 5: Lock Picking
        if f.get('lock_pattern')=='abnormal':
            self.results.append(('[MENCURIGAKAN] Pola kunci anomali',
                                 'kunci_ganda + catat_anomali'))
            self.rules_fired.append('Rule 5')

        if not self.results:
            self.results.append(('[INFO] Tidak ada ancaman terdeteksi',
                                 'monitor_pasif'))

# ===== MAIN PROGRAM =====
engine = SmartDoorExpert()
engine.reset()
print('=== Smart Door Security Expert System ===')
motion      = input('Gerak terdeteksi? (yes/no): ')
face        = input('Wajah dikenali? (known/unknown): ')
auth        = input('Autentikasi? (success/fail/none): ')
fail_count  = input('Jumlah percobaan gagal: ')
time_access = input('Waktu akses? (normal/night): ')
owner_home  = input('Pemilik di rumah? (yes/no): ')
guest_count = input('Jumlah tamu: ')
lock_pattern= input('Pola kunci normal? (normal/abnormal): ')

engine.declare(Fact(
    motion=motion, face=face, auth=auth,
    fail_count=fail_count, time=time_access,
    owner_home=owner_home, guest_count=guest_count,
    lock_pattern=lock_pattern
))
engine.run()

print('\n=== HASIL ANALISIS SISTEM PAKAR ===')
for level, action in engine.results:
    print(f'Status : {level}')
    print(f'Aksi   : {action}')
    print('-' * 40)
print(f'Rules fired: {engine.rules_fired}')
