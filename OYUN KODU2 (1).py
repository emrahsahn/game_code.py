import random
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, \
    QLabel, QDialog, QVBoxLayout, QRadioButton, QMessageBox, QLineEdit, QAction, QHBoxLayout
from PyQt5.QtGui import QColor
from PyQt5.QtCore import pyqtSignal

class Savasci:
    def __init__(self, tip, x, y):
        self.tip = tip
        self.x = x
        self.y = y
        self.kaynak = 0
        self.can = 0
        self.hedef = 0
        self.hasar = 0
        self.menzil = ()

    def move(self):
        print(f"{self.tip} hareket ediyor.")

    def attack(self):
        print(f"{self.tip} saldırıyor.")

    def __str__(self):
        return f"Tip: {self.tip}, Konum: ({self.x}, {self.y}), Can: {self.can}, Hedef: {self.hedef}, Hasar: {self.hasar}"

class Guard(Savasci):
    def __init__(self, x, y):
        super().__init__('Guard', x, y)
        self.kaynak = 10
        self.can = 80
        self.hedef = "Menzildeki tüm düşmanlar"
        self.hasar = 20             # -20 can
        self.menzil = (1, 1, 1)     # yatay, dikey, capraz
        self.sembol = "M"

    def attack(self):
        print("Koruma Saldirisi")

class Archery(Savasci):
    def __init__(self, x, y):
        super().__init__('Archery', x, y)
        self.kaynak = 20
        self.can = 30
        self.hedef = "Menzilde en yüksek canı olan 3 düşman"
        self.hasar = 60             # -%60 can
        self.menzil = (2, 2, 2)     # yatay, dikey, capraz
        self.sembol = "O"

    def attack(self):
        print("Okçu Saldirisi")

class Gunner(Savasci):
    def __init__(self, x, y):
        super().__init__('Gunner', x, y)
        self.kaynak = 50
        self.can = 30
        self.hedef = "Menzilde en yüksek canı olan 1 düşman"
        self.hasar = 100           # -%100 can
        self.menzil = (2, 2, 2)    # yatay, dikey, capraz
        self.sembol = "T"

    def attack(self):
        print("Topçu Saldirisi")

class Horseman(Savasci):
    def __init__(self, x, y):
        super().__init__('Horseman', x, y)
        self.kaynak = 30
        self.can = 40
        self.hedef = "Menzildeki tüm düşmanlar"
        self.hasar = 30            # -30 can
        self.menzil = (0, 0, 3)    # yatay, dikey, capraz
        self.sembol = "A"

    def attack(self):
        print("Süvari Saldirisi")

class Healer(Savasci):
    def __init__(self, x, y):
        super().__init__('Healer', x, y)
        self.kaynak = 10
        self.can = 100
        self.hedef = "Menzilde en az canı olan 3 düşman"
        self.hasar = 50           # +%50 can
        self.menzil = (2, 2, 2)   # yatay, dikey, capraz
        self.sembol = "S"

    def attack(self):
        print("Heal Saldirisi")



####################################################################

class GridButton(QPushButton):

    clickedWithCoords = pyqtSignal(int, int)
    def __init__(self, row, col, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.row = row
        self.col = col
        self.clicked.connect(self.emitCoords)

    def emitCoords(self):
        self.clickedWithCoords.emit(self.row, self.col)

class Oyun:
    # oyun sınıfımızı oluşturuyoruz
    def __init__(self, boyut, oyuncu_sayisi):
        self.boyut = boyut
        self.oyuncu_sayisi = oyuncu_sayisi
        self.savascilar = []
        self.kaynaklar = 200
        self.el_sayisi = 10
        self.kose_haritasi = {}

    def append_warrior(self, savasci):
        self.savascilar.append(savasci)
        self.savascilar = list(set(self.savascilar))
        return self.savascilar

    def kaynak_kazan(self):
        self.kaynaklar += len(self.savascilar)

    def savasci_sec(self, tip, x, y):
        if tip == "Muhafız":
            self.savasci = Guard(x, y)
        elif tip == "Okçu":
            self.savasci = Archery(x, y)
        elif tip == "Nişancı":
            self.savasci = Gunner(x, y)
        elif tip == "Süvari":
            self.savasci = Horseman(x, y)
        elif tip == "Şifacı":
            self.savasci = Healer(x, y)
        self.append_warrior(self.savasci)

    def first_tour(self,grid_window):
        '''ilk turda köşelere muhafız atama işlemini burda yapıyoruz'''
        corners = [(0, 0), (0, self.boyut - 1), (self.boyut - 1, 0), (self.boyut - 1, self.boyut - 1)]
        # rastgele eleman atıcağımız için köşe koordinatlarını bir listede tutuyoruz

        for i in range(self.oyuncu_sayisi):
            corner = random.choice(corners)
            savasci = Guard(corner[0], corner[1])
            print(savasci)
            self.append_warrior(savasci)
            grid_window.selectCell(corner[0], corner[1])  # Köşe butonuna tıkla
            self.kose_haritasi[corner] = f"M{i + 1}"      # Köşe haritasına oyuncu sembolünü ekle
            grid_window.updateGrid(self.getWorldState())  # Izgarayı güncelle
            corners.remove(corner)


    def getWorldState(self):
        '''Bu fonksiyon oyun durumunu temsil eden bir matris döndürür. Her hücre, oyun alanında bir
        savaşçı olup olmadığını belirtir. Eğer savaşçı varsa, o savaşçının sembolünü içerir.
        Eğer hücre boşsa nokta işaretini koyar'''
        world_state = [['.' for _ in range(self.boyut)] for _ in range(self.boyut)]
        for savasci in self.savascilar:
            world_state[savasci.x][savasci.y] = savasci
        return world_state


class GridWindow(QMainWindow):
    def __init__(self, size, player_count):
        super().__init__()
        self.title = 'Izgara Seçici'
        self.rows = size
        self.columns = size
        self.player_count = player_count  # Oyuncu sayısını saklayın
        self.oyun = Oyun(size, player_count)
        self.player_symbols = []          # Oyuncu sembollerini saklamak için bir sözlük
        self.initUI()
        self.selected_warriors = {}
        self.savasci = None
        self.current_player_index = 0
        self.player_colors = [QColor('red'), QColor('blue'), QColor('green'), QColor('yellow')]
        self.returnn = None

    def initUI(self):
        self.setWindowTitle(self.title)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QGridLayout(self.central_widget)
        self.createGrid()

    def createGrid(self):
        '''Kullanıcı arayüzünde bir ızgara oluşturu. Bu ızgara, oyun alanını temsil eder ve kullanıcıların
        oyunu oynamak için hücreleri seçmesine olanak tanır.'''
        self.buttons = []
        for i in range(self.rows):
            row_buttons = []
            for j in range(self.columns):
                button = GridButton(i, j, '.')  # GridButton nesneleri oluşturulurken koordinatlar atanır
                button.setStyleSheet("background-color: black;color: white")
                button.setFixedSize(40, 40)
                button.clickedWithCoords.connect(self.startGame)  # Butonlar clickedWithCoords sinyaline bağlanır
                self.layout.addWidget(button, i, j)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

    def startGame(self, row=0, col=0):
        self.updateGrid(self.oyun.getWorldState())


        while True:
            for i in range(self.player_count):

                # Kullanıcıya buton seçtir
                selected_cell = self.selectCell(row, col)
                if selected_cell:
                    self.current_player_index = (self.current_player_index + 1) % self.player_count
                    savasci = self.assignWarrior(row, col)
                    print(savasci)
                    if savasci:
                        # print("değiştirme")
                        self.updateGrid(self.oyun.getWorldState())
                        # print("buraya da giriyor")
                        break

                # Tüm oyuncuların savaşçıları seçtiği durumda döngü sona erer
                if len(self.oyun.savascilar) >= self.player_count:
                    return
            break

    def assignWarrior(self, row, col):
        '''Kullanıcının seçtiği hücreye savaşçı ataması yap'''
        i = 0
        while True:
            if self.savasci:
                player_name = self.getUnusedPlayerName()
                self.savasci.sembol = f"{self.savasci.sembol}"  # Oyuncu adı sembole eklenir
                self.selected_warriors[player_name] = (self.savasci, row, col)  # Seçilen savaşçılar sözlüğe eklenir
                self.buttons[row][col].setText(self.savasci.sembol)

                i += 1
                if self.player_count == 4:
                    self.player_colors1 = [QColor('green'), QColor('yellow'), QColor('red'), QColor('blue')]
                    # print(self.current_player_index)
                    # print(self.player_count)
                    player_color = self.player_colors1[self.current_player_index]  # Sıradaki oyuncunun rengini al
                    self.current_player_index = int((self.current_player_index - 1) % self.player_count)  # Sıradaki oyuncuyu güncelle

                    # print(self.current_player_index)

                    for r in range(max(0, row - 1), min(self.rows, row + 2)):
                        for c in range(max(0, col - 1), min(self.columns, col + 2)):
                            if (r, c) != (row, col):
                                self.changeColor(r, c, player_color)

                elif self.player_count == 3:
                    self.player_colors2 = [QColor('blue'), QColor('green'), QColor('red'), QColor('yellow')]
                    # print(self.current_player_index)
                    # print(self.player_count)
                    player_color = self.player_colors2[self.current_player_index]  # Sıradaki oyuncunun rengini al
                    self.current_player_index = int((self.current_player_index - 1) % self.player_count)  # Sıradaki oyuncuyu güncelle

                    # print(self.current_player_index)

                    for r in range(max(0, row - 1), min(self.rows, row + 2)):
                        for c in range(max(0, col - 1), min(self.columns, col + 2)):
                            if (r, c) != (row, col):
                                self.changeColor(r, c, player_color)
                else:
                    self.player_colors3 = [QColor('red'), QColor('blue'), QColor('green'), QColor('yellow')]
                    print(self.current_player_index)
                    # print(self.player_count)
                    player_color = self.player_colors3[self.current_player_index]  # Sıradaki oyuncunun rengini al
                    self.current_player_index = int((self.current_player_index - 1) % self.player_count)  # Sıradaki oyuncuyu güncelle

                    # print(self.current_player_index)

                    for r in range(max(0, row - 1), min(self.rows, row + 2)):
                        for c in range(max(0, col - 1), min(self.columns, col + 2)):
                            if (r, c) != (row, col):
                                self.changeColor(r, c, player_color)
                return self.savasci  # Atanan savaşçıyı döndür


    def selectCell(self, row, col):
        self.changeColor(row, col)

        dialog = CharacterSelectionDialog(self)
        if dialog.exec_():
            selected_character = dialog.character
            if selected_character:
                if len(self.selected_warriors) < self.player_count:  # En fazla 4 savaşçı seçilebilir
                    if selected_character == "Muhafız":
                        self.savasci = Guard(row, col)
                    elif selected_character == "Okçu":
                        self.savasci = Archery(row, col)
                    elif selected_character == "Nişancı":
                        self.savasci = Gunner(row, col)
                    elif selected_character == "Süvari":
                        self.savasci = Horseman(row, col)
                    elif selected_character == "Şifacı":
                        self.savasci = Healer(row, col)

                    player_name = self.getUnusedPlayerName()  # Kullanılmayan bir oyuncu adı alınır
                    self.savasci.sembol = f"{self.savasci.sembol}"  # Oyuncu adı sembole eklenir
                    self.selected_warriors[player_name] = (self.savasci, row, col)  # Seçilen savaşçılar sözlüğe eklenir
                    self.updateGrid(self.oyun.getWorldState())


        player_color = self.player_colors[self.current_player_index] # Sıradaki oyuncunun rengini al
        self.current_player_index = (self.current_player_index + 1) % self.player_count  # Sıradaki oyuncuyu güncelle


        for r in range(max(0, row - 1), min(self.rows, row + 2)):
            for c in range(max(0, col - 1), min(self.columns, col + 2)):
                if (r, c) != (row, col):
                    self.changeColor(r, c, player_color)

        return row,col


    def getUnusedPlayerName(self):
            player_names = [f"{i}" for i in range(1,self.player_count+1)]  # Müsait oyuncu isimleri listesi
            for name in player_names:
                return name


    def changeColor(self, row, col, color=QColor('light grey')):
        self.buttons[row][col].setStyleSheet(f"background-color: {color.name()}")


    def updateGrid(self, world_state):
        for i in range(self.rows):
            for j in range(self.columns):
                if isinstance(world_state[i][j], Savasci):
                    if (i, j) in self.oyun.kose_haritasi:  # Eğer bu hücre bir köşede ise
                        player_symbol = self.oyun.kose_haritasi[(i, j)]  # Köşe haritasından oyuncu sembolünü al
                        self.buttons[i][j].setText(player_symbol)  # Butona oyuncu sembolünü ekle
                    else:
                        self.buttons[i][j].setText(world_state[i][j].sembol)  # Karakter sembolünü ekle
                    self.buttons[i][j].setStyleSheet("background-color: grey;color: white")


##################################################################

class CharacterSelectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Karakter Seçimi")
        layout = QVBoxLayout()

        self.character = None

        # kullanıcı ızgara üzerindeki herhangi bir butonu seçtiğinde
        # açılan küçük pencerede savaşçıları gösteren dialog penceresi
        self.guard_button = QRadioButton("Muhafız")
        self.archery_button = QRadioButton("Okçu")
        self.gunner_button = QRadioButton("Nişancı")
        self.horseman_button = QRadioButton("Süvari")
        self.healer_button = QRadioButton("Şifacı")

        layout.addWidget(self.guard_button)
        layout.addWidget(self.archery_button)
        layout.addWidget(self.gunner_button)
        layout.addWidget(self.horseman_button)
        layout.addWidget(self.healer_button)

        select_button = QPushButton("Seç")
        select_button.clicked.connect(self.selectCharacter)
        layout.addWidget(select_button)

        self.setLayout(layout)

    def selectCharacter(self):

        # kullanıcının seçtiği savaşçıyı sınıf değerine atayıp gönderme
        if self.guard_button.isChecked():
            self.character = "Muhafız"
        elif self.archery_button.isChecked():
            self.character = "Okçu"
        elif self.gunner_button.isChecked():
            self.character = "Nişancı"
        elif self.horseman_button.isChecked():
            self.character = "Süvari"
        elif self.healer_button.isChecked():
            self.character = "Şifacı"
        else:
            self.character = None
        self.accept()


class MainInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Main Interface'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        #kullanıcıdan bir girdi almak için sorsuğu soru satırı ve girdi satırı
        self.player_count_label = QLabel("Kaç oyuncu ile oyun oynanacak:")
        self.layout.addWidget(self.player_count_label)

        # Kullanıcı dialog penceresinde kaç oyuncuyla oynayacaksa o değeri seçtiği alan
        self.player_count_input2 = QRadioButton("2")
        self.player_count_input3 = QRadioButton("3")
        self.player_count_input4 = QRadioButton("4")

        self.hbox = QHBoxLayout(self.central_widget)
        self.hbox.addWidget(self.player_count_input2)
        self.hbox.addWidget(self.player_count_input3)
        self.hbox.addWidget(self.player_count_input4)

        self.layout.addLayout(self.hbox)

        # kullanıcıdan ızgara boyutunu aldığı yer
        self.size_label = QLabel("Kaça kaçlık bir ızgara istiyorsunuz:")
        self.layout.addWidget(self.size_label)

        self.size_input = QLineEdit()
        self.layout.addWidget(self.size_input)

        self.start_game_button = QPushButton("Oyunu Başlat")
        self.start_game_button.clicked.connect(self.startGame)
        self.layout.addWidget(self.start_game_button)

        self.action = QAction(self)
        self.action.setShortcut("Ctrl+Return")

    def startGame(self):
        if self.player_count_input2.isChecked():
            player_count = 2
        elif self.player_count_input3.isChecked():
            player_count = 3
        elif self.player_count_input4.isChecked():
            player_count = 4
        else:
            QMessageBox.warning(self, "Hata", "En az 2 oyuncu, en fazla 4 oyuncu ile oyun oynanmalıdır.")
            return

        size = self.size_input.text()
        if not size.isdigit():
            QMessageBox.warning(self, "Hata", "Geçersiz ızgara boyutu. Lütfen bir sayı girin.")
            return
        if not 8 <= int(size) <= 32:
            QMessageBox.warning(self, "Hata", "Geçersiz ızgara boyutu. Lütfen 8 ve 32 arasında geçerli bir boyut girin.")
            return
        size = int(size)

        self.grid_window = GridWindow(size, player_count)
        self.grid_window.show()

        self.grid_window.oyun.first_tour(self.grid_window)
        # self.grid_window.startGame()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainInterface()
    ex.show()
    sys.exit(app.exec_())

