import csv, os

FILE = "data_jadwal_kuliah.csv"
HEADER = ["id", "mata_kuliah", "dosen", "hari", "jam", "ruangan"]

# ================= LINKED LIST =================
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def tambah(self, data):
        node = Node(data)
        if not self.head:
            self.head = node
            return

        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = node

    def tampil(self):
        data = []
        cur = self.head
        while cur:
            data.append(cur.data)
            cur = cur.next
        return data

    def cari(self, id_jadwal):
        cur = self.head
        while cur:
            if cur.data["id"] == id_jadwal:
                return cur.data
            cur = cur.next
        return None

    def hapus(self, id_jadwal):
        cur = self.head
        prev = None

        while cur:
            if cur.data["id"] == id_jadwal:
                if prev:
                    prev.next = cur.next
                else:
                    self.head = cur.next
                return True

            prev = cur
            cur = cur.next

        return False


# ================= QUEUE =================
class Queue:
    def __init__(self):
        self.data = []

    def enqueue(self, jadwal):
        self.data.append(jadwal)

    def dequeue(self):
        if self.data:
            return self.data.pop(0)
        return None

    def tampil(self):
        return self.data


# ================= CSV =================
def load_csv(ll):
    if not os.path.exists(FILE):
        with open(FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(HEADER)
        return

    with open(FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ll.tambah(row)

def save_csv(ll):
    with open(FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=HEADER)
        writer.writeheader()
        writer.writerows(ll.tampil())


# ================= FITUR =================
def generate_id(ll):
    return "J" + str(len(ll.tampil()) + 1).zfill(3)

def tambah_jadwal(ll):
    data = {
        "id": generate_id(ll),
        "mata_kuliah": input("Mata Kuliah : "),
        "dosen": input("Dosen       : "),
        "hari": input("Hari        : "),
        "jam": input("Jam         : "),
        "ruangan": input("Ruangan     : ")
    }

    ll.tambah(data)
    save_csv(ll)
    print("Jadwal kuliah berhasil ditambahkan!")

def lihat_jadwal(ll):
    data = ll.tampil()

    if not data:
        print("Data jadwal kuliah kosong.")
    else:
        print("\n=== DATA JADWAL KULIAH ===")
        for j in data:
            print(
                j["id"], "-",
                j["mata_kuliah"], "-",
                j["dosen"], "-",
                j["hari"], "-",
                j["jam"], "- Ruang:",
                j["ruangan"]
            )

def cari_jadwal(ll):
    id_jadwal = input("Masukkan ID jadwal: ")
    jadwal = ll.cari(id_jadwal)

    if jadwal:
        print("Ditemukan:", jadwal)
    else:
        print("Jadwal tidak ditemukan.")

def update_jadwal(ll):
    id_jadwal = input("Masukkan ID jadwal: ")
    jadwal = ll.cari(id_jadwal)

    if jadwal:
        jadwal["mata_kuliah"] = input("Mata kuliah baru : ")
        jadwal["dosen"] = input("Dosen baru       : ")
        jadwal["hari"] = input("Hari baru        : ")
        jadwal["jam"] = input("Jam baru         : ")
        jadwal["ruangan"] = input("Ruangan baru     : ")

        save_csv(ll)
        print("Data jadwal berhasil diupdate!")
    else:
        print("Jadwal tidak ditemukan.")

def hapus_jadwal(ll):
    id_jadwal = input("Masukkan ID jadwal: ")

    if ll.hapus(id_jadwal):
        save_csv(ll)
        print("Data jadwal berhasil dihapus!")
    else:
        print("Jadwal tidak ditemukan.")

def sorting_jadwal(ll):
    data = ll.tampil()
    data.sort(key=lambda x: x["hari"])

    print("\nHasil sorting berdasarkan hari:")
    for j in data:
        print(
            j["id"], "-",
            j["mata_kuliah"], "-",
            j["hari"], "-",
            j["jam"], "- Ruang:",
            j["ruangan"]
        )

def antrean_perubahan_jadwal(ll, q):
    id_jadwal = input("Masukkan ID jadwal yang ingin diajukan perubahan: ")
    jadwal = ll.cari(id_jadwal)

    if jadwal:
        q.enqueue(jadwal)
        print("Jadwal masuk antrean perubahan.")
    else:
        print("Jadwal tidak ditemukan.")

def proses_perubahan_jadwal(q):
    jadwal = q.dequeue()

    if jadwal:
        print("Perubahan jadwal sedang diproses:", jadwal["mata_kuliah"])
    else:
        print("Antrean perubahan jadwal kosong.")


# ================= MAIN PROGRAM =================
def main():
    ll = LinkedList()
    q = Queue()

    load_csv(ll)

    while True:
        print("\n=== SISTEM PENJADWALAN KULIAH ===")
        print("1. Tambah Jadwal Kuliah")
        print("2. Lihat Jadwal Kuliah")
        print("3. Cari Jadwal Kuliah")
        print("4. Update Jadwal Kuliah")
        print("5. Hapus Jadwal Kuliah")
        print("6. Sorting Jadwal Kuliah")
        print("7. Tambah Antrean Perubahan Jadwal")
        print("8. Proses Perubahan Jadwal")
        print("9. Keluar")

        pilih = input("Pilih menu: ")

        if pilih == "1":
            tambah_jadwal(ll)
        elif pilih == "2":
            lihat_jadwal(ll)
        elif pilih == "3":
            cari_jadwal(ll)
        elif pilih == "4":
            update_jadwal(ll)
        elif pilih == "5":
            hapus_jadwal(ll)
        elif pilih == "6":
            sorting_jadwal(ll)
        elif pilih == "7":
            antrean_perubahan_jadwal(ll, q)
        elif pilih == "8":
            proses_perubahan_jadwal(q)
        elif pilih == "9":
            save_csv(ll)
            print("Program selesai.")
            break
        else:
            print("Pilihan tidak valid!")


main()
