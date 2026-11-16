import random
import time
from collections import Counter
from dataclasses import dataclass
from typing import Callable

MAX_ENERGY = 100
MAX_BURNOUTS = 3
DROP_CHANCE = 0.35          # ders geçince eşya düşme ihtimali
WINTER_BREAK_ENERGY = 20    # sömestr tatili, kısa olduğu için az
SUMMER_BREAK_ENERGY = 50    # yaz tatili


# dersler
@dataclass
class Course:
    code: str
    name: str
    pass_chance: int   # yüzde olarak
    energy_cost: int   # kalınca giden enerji


@dataclass
class Semester:
    title: str
    courses: list[Course]
    required: int = 0   # 0 ise dönemdeki bütün dersler lazım

    @property
    def needed(self) -> int:
        return self.required or len(self.courses)


# dersleri ÇOMÜ EEM ders içerikleri pdf'inden aldım
# pdf'te dönem yazmıyordu, tek kodluları güze çiftleri bahara koydum
# 3 ve 4. sınıfta seçmeliler var o yüzden hepsini geçmek gerekmiyor
SEMESTERS = [
    Semester("1. Yıl - Güz", [
        Course("EEM1001", "Matematik I",                                   65, 22),
        Course("EEM1003", "Fizik I",                                       65, 22),
        Course("EEM1005", "Lineer Cebir",                                  65, 22),
        Course("EEM1007", "EEM'ye Giriş ve Mühendislik Etiği",             85, 15),
    ]),
    Semester("1. Yıl - Bahar", [
        Course("EEM1002", "Matematik II",                                  60, 22),
        Course("EEM1004", "Fizik II",                                      60, 22),
        Course("EEM1008", "Olasılık ve İstatistik",                        65, 22),
        Course("EEM1010", "Programlamaya Giriş",                           75, 15),
    ]),
    Semester("2. Yıl - Güz", [
        Course("EEM2001", "Devre Teorisi I",                               55, 22),
        Course("EEM2003", "Lojik Devreler",                                65, 22),
        Course("EEM2005", "Mühendislikte Programlama",                     70, 15),
        Course("EEM2007", "Diferansiyel Denklemler",                       55, 22),
        Course("EEM2009", "Sinyaller ve Sistemler",                        50, 30),
        Course("EEM2011", "Mühendislikte Modern Fizik",                    60, 22),
    ]),
    Semester("2. Yıl - Bahar", [
        Course("EEM2002", "Devre Teorisi II",                              55, 22),
        Course("EEM2004", "Devre Teorisi Lab",                             80, 15),
        Course("EEM2006", "Elektronik I",                                  50, 30),
        Course("EEM2008", "Malzeme Bilimi",                                65, 22),
        Course("EEM2010", "Elektromanyetik Alan Teorisi",                  45, 30),
        Course("EEM2012", "Mesleki İngilizce",                             80, 15),
    ]),
    Semester("3. Yıl - Güz", [
        Course("EEM3001", "Elektronik II",                                 50, 30),
        Course("EEM3003", "Elektronik Laboratuvarı",                       75, 15),
        Course("EEM3005", "Elektrik Enerji Sistemleri",                    55, 22),
        Course("EEM3007", "Kontrol Sistemleri",                            50, 30),
        Course("EEM3011", "Akıllı Şebekelere Giriş",                       70, 15),
        Course("EEM3013", "Kontrol Sistemlerinin Tasarımı",                50, 30),
        Course("EEM3015", "Elektromanyetik Dalga Teorisi",                 45, 30),
        Course("EEM3017", "Sayısal Sinyal İşleme",                         50, 30),
        Course("EEM3019", "Makine Öğrenmesinin Temelleri",                 65, 22),
    ], required=6),
    Semester("3. Yıl - Bahar", [
        Course("EEM3002", "Optik Elektronik",                              60, 22),
        Course("EEM3004", "Endüstriyel Otomasyon Sistemleri",              65, 22),
        Course("EEM3006", "Mikrodenetleyiciler",                           60, 22),
        Course("EEM3008", "Yenilenebilir Enerji Sistemleri",               70, 15),
        Course("EEM3010", "Elektromanyetik Enerji Dönüşümü",               50, 30),
        Course("EEM3012", "Fonksiyonel Güvenliğe Giriş",                   70, 15),
        Course("EEM3014", "Optik",                                         55, 22),
        Course("EEM3016", "Haberleşmenin Temelleri",                       50, 30),
        Course("EEM3018", "Veri Analizi",                                  65, 22),
    ], required=6),
    Semester("4. Yıl - Güz", [
        Course("EEM4011", "Endüstriyel Otomasyon Sistemleri Tasarımı",     60, 22),
        Course("EEM4013", "Enerji İletim Hatları",                         60, 22),
        Course("EEM4015", "Elektrikli Araçlar",                            65, 22),
        Course("EEM4017", "Derin Öğrenmenin Temelleri",                    55, 22),
        Course("EEM4019", "Biyomedikal Görüntüleme I",                     55, 22),
        Course("EEM4021", "Görüntü İşlemeye Giriş",                        60, 22),
        Course("EEM4023", "Fotonik",                                       55, 22),
    ], required=5),
    Semester("4. Yıl - Bahar", [
        Course("EEM4010", "Endüstriyel Otomasyon Sistemleri Lab.",         75, 15),
        Course("EEM4012", "Bilgisayar Destekli Tasarım",                   75, 15),
        Course("EEM4014", "Elektrik Enerji Üretimi",                       60, 22),
        Course("EEM4016", "Veri Tabanı ve Uygulamaları",                   70, 15),
        Course("EEM4018", "Kompleks Ağ Teorisine Giriş",                   50, 30),
        Course("EEM4020", "Biyomedikal Görüntüleme II",                    50, 30),
        Course("EEM4022", "Nümerik Analiz",                                55, 22),
        Course("EEM4024", "Lazer Teorisi ve Uygulamaları",                 50, 30),
    ], required=5),
]

TOTAL_COURSES = sum(s.needed for s in SEMESTERS)


# eşyalar
@dataclass
class Item:
    name: str
    description: str
    effect: Callable[["Game"], None]
    weight: int  # büyükse daha sık düşüyor


def use_caffeine(g):    g.bonus_chance += 15
def use_past_papers(g): g.bonus_chance += 25
def use_ritalin(g):     g.reroll = True
def use_nap(g):         g.energy = min(MAX_ENERGY, g.energy + 30)
def use_energy_drink(g):
    g.energy = min(MAX_ENERGY, g.energy + 40)
    g.penalty_mult *= 2


ITEMS = [
    Item("Kahve",              "Sonraki sınavda +%15 geçme şansı",                 use_caffeine,     5),
    Item("Kestirme",           "+30 enerji",                                       use_nap,          4),
    Item("Enerji İçeceği",     "+40 enerji, sonraki sınavda kalırsan ceza 2 kat",  use_energy_drink, 3),
    Item("Ritalin",            "Sonraki sınavda kalırsan bir hak daha",            use_ritalin,      2),
    Item("Çıkmış Sorular",     "Sonraki sınavda +%25 geçme şansı",                 use_past_papers,  2),
]


def random_item() -> Item:
    return random.choices(ITEMS, weights=[i.weight for i in ITEMS])[0]


# oyun
class Game:
    def __init__(self):
        self.reset()

    def reset(self):
        self.energy = MAX_ENERGY
        self.burnouts_left = MAX_BURNOUTS
        self.semester_index = 0
        self.passed: list[str] = []             # sadece bu dönemkiler
        self.completed_courses = 0              # eski dönemlerden gelenler
        self.backpack: list[Item] = [ITEMS[0]]  # başta bir kahve veriyoruz
        self.clear_effects()

    def clear_effects(self):
        self.bonus_chance = 0
        self.reroll = False
        self.penalty_mult = 1.0

    @property
    def semester(self) -> Semester:
        return SEMESTERS[self.semester_index]

    @property
    def dropped_out(self) -> bool:
        return self.burnouts_left <= 0

    @property
    def graduated(self) -> bool:
        return self.semester_index >= len(SEMESTERS)

    def remaining_courses(self) -> list[Course]:
        return [c for c in self.semester.courses if c.code not in self.passed]

    def show_status(self):
        bar = "█" * (self.energy // 10) + "░" * (10 - self.energy // 10)
        items = Counter(i.name for i in self.backpack)
        effects = []
        if self.bonus_chance: effects.append(f"+%{self.bonus_chance} geçme şansı")
        if self.reroll: effects.append("Ekstra hak hazır")
        if self.penalty_mult != 1.0: effects.append(f"Kalma cezası x{self.penalty_mult:g}")

        total_passed = self.completed_courses + len(self.passed)
        print("\n" + "=" * 55)
        print(f"{self.semester.title}  (Dönem {self.semester_index + 1}/{len(SEMESTERS)})")
        print(f"Enerji: [{bar}] {self.energy}/{MAX_ENERGY}")
        print(f"Kalan tükenmişlik hakkı: {self.burnouts_left}   "
              f"Toplam ders: {total_passed}/{TOTAL_COURSES}")
        print(f"Bu dönem: {len(self.passed)}/{self.semester.needed} ders geçildi"
              f" ({', '.join(self.passed) or 'henüz yok'})")
        print(f"Çanta: {', '.join(f'{n} x{c}' for n, c in items.items()) or '(boş)'}")
        if effects:
            print(f"Aktif etkiler: {', '.join(effects)}")
        print("=" * 55)

    def use_item(self):
        if not self.backpack:
            print("  Çantan boş.")
            return
        for i, item in enumerate(self.backpack, 1):
            print(f"  {i}. {item.name} - {item.description}")
        choice = input("  Hangi eşyayı kullanacaksın? (iptal için Enter): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(self.backpack):
            item = self.backpack.pop(int(choice) - 1)
            item.effect(self)
            print(f"  {item.name} kullandın.")

    def roll(self, chance: int) -> bool:
        print("  Sınava giriyorsun", end="", flush=True)
        for _ in range(3):
            time.sleep(0.4)
            print(".", end="", flush=True)
        roll = random.randint(1, 100)
        passed = roll <= chance
        print(f" zar: {roll}, gereken ≤ {chance} → {'GEÇTİ' if passed else 'KALDI'}")
        return passed

    def take_exam(self, course: Course):
        chance = min(95, course.pass_chance + self.bonus_chance)
        print(f"\n{course.code} - {course.name} | geçme şansı: %{chance}")

        passed = self.roll(chance)
        if not passed and self.reroll:
            print("  Ritalin odaklanmanı sağlıyor. Bir şans daha!")
            passed = self.roll(chance)

        if passed:
            self.passed.append(course.code)
            print(f"  {course.code} dersini geçtin!")
            if random.random() < DROP_CHANCE:
                item = random_item()
                self.backpack.append(item)
                print(f"  Bir sınıf arkadaşın sana verdi: {item.name}")
        else:
            cost = round(course.energy_cost * self.penalty_mult)
            self.energy = max(0, self.energy - cost)
            print(f"  {course.code} dersinden kaldın. -{cost} enerji.")

        self.clear_effects()  # eşyalar sadece bir sınavlık
        if self.energy == 0:
            self.burnout()
        elif len(self.passed) >= self.semester.needed:
            self.next_semester()

    def next_semester(self):
        print(f"\n  {self.semester.title} dönemini tamamladın!")
        self.completed_courses += len(self.passed)
        self.passed.clear()
        self.semester_index += 1
        if not self.graduated:
            if self.semester_index % 2 == 0:   # güze geçiyorsak yaz tatili olmuş demek
                gain, label = SUMMER_BREAK_ENERGY, "Yaz tatili"
            else:
                gain, label = WINTER_BREAK_ENERGY, "Sömestr tatili"
            before = self.energy
            self.energy = min(MAX_ENERGY, self.energy + gain)
            print(f"  {label}: +{self.energy - before} enerji. "
                  f"Sıradaki: {self.semester.title}")

    def burnout(self):
        self.burnouts_left -= 1
        print(f"\n  TÜKENMİŞLİK! Bu dönem geçtiğin {len(self.passed)} dersi "
              f"ve {len(self.backpack)} eşyayı kaybettin.")
        self.passed.clear()
        self.backpack.clear()
        if not self.dropped_out:
            self.energy = MAX_ENERGY
            print(f"  {self.semester.title} dönemini baştan alıyorsun. "
                  f"Kalan tükenmişlik hakkı: {self.burnouts_left}")

    def run(self) -> str:
        # "restart" ya da "quit" döner
        while not self.dropped_out and not self.graduated:
            self.show_status()
            remaining = self.remaining_courses()
            if self.semester.required:
                print(f"  (Seçmeli dönem: listeden {self.semester.needed} ders geçmen yeterli)")
            for i, c in enumerate(remaining, 1):
                print(f"  {i}. {c.code} {c.name} (%{c.pass_chance} geçme, kalırsan -{c.energy_cost})")
            choice = input("Ders no seç | [e] eşya kullan | [r] yeniden başla | [q] çıkış: ").strip().lower()

            if choice == "q":
                return "quit"
            if choice == "r":
                return "restart"
            if choice == "e":
                self.use_item()
            elif choice.isdigit() and 1 <= int(choice) <= len(remaining):
                self.take_exam(remaining[int(choice) - 1])
            else:
                print("  Geçersiz seçim.")

        if self.graduated:
            print("\nTEBRİKLER! 4 yılı bitirdin ve mühendislik diplomanı aldın!")
        else:
            print(f"\nOKULDAN ATILDIN ({self.semester.title}). "
                  f"Üç kez tükenmişlik çok fazlaydı.")

        again = input("Yeni bir bölüme kaydolmak ister misin? (e/h): ").strip().lower()
        return "restart" if again == "e" else "quit"


def main():
    print("MÜHENDİSLİK DİPLOMASI HAYATTA KALMA")
    print("4 yıl, 8 dönem. Her dönemin derslerini geçerek bir sonrakine geç.")
    print("Enerjin 0 olursa tükenirsin ve o dönemi baştan alırsın.")
    print(f"{MAX_BURNOUTS} kez tükenirsen okuldan atılırsın.\n")
    while True:
        if Game().run() == "quit":
            print("Finallerde bol şans!")
            break
        print("\nYeniden kayıt yapılıyor...\n")


if __name__ == "__main__":
    main()
