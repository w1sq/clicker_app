import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *
from clicker_help import HelpRulesWindow
from error_clicker import ErrorWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect("most_finished_clicker.db")
        self.cur = self.con.cursor()
        self.nickname, self.ok_pressed = QInputDialog.getText(self, "registration/login",
                                                              "Whats your nickname?")

        uic.loadUi('clicker.ui', self)
        if self.ok_pressed:
            try:
                if not self.cur.execute('''  
                    SELECT nick FROM nicknames
                        WHERE nick = ? ''', (self.nickname,)
                                        ).fetchall():

                    self.cur.execute('''
                        INSERT INTO nicknames(nick) VALUES(?)
                            ''', (self.nickname,))
                    self.con.commit()
                    self.nick_id = self.cur.execute('''
                        SELECT id FROM nicknames
                            WHERE nick == ?
                        ''', (self.nickname,)).fetchall()[0][0]

                    self.save_data = '0;0;0;0;0;0;0;0'
                    self.cur.execute('''
                        INSERT INTO nicknames_stats(stats,nick_id) VALUES(?,?)
                    ''', (self.save_data, self.nick_id,))
                    self.con.commit()

                    self.click_number.display(1)
                    self.click_price.display(7)
                    self.grandma_price.display(50)
                    self.farm_price.display(200)
                    self.factory_price.display(1000)
                    self.mine_price.display(4000)
                    self.laboratory_price.display(15000)
                    self.portal_price.display(60000)
                else:
                    self.nick_id = self.cur.execute('''
                                        SELECT id FROM nicknames
                                            WHERE nick == ?
                                        ''', (self.nickname,)).fetchall()[0][0]
                    self.save_data = (self.cur.execute('''
                        SELECT stats FROM nicknames_stats
                            WHERE nick_id == ?
                    ''', (self.nick_id,)).fetchall())[0][0]
                    save_data1 = self.save_data.split(';')
                    self.main_display.display(int(float(save_data1[0])))
                    self.click_number.display(int(float(save_data1[1])))
                    self.click_price.display(int(7 * 1.15 ** float(save_data1[1])))
                    self.grandma_number.display(int(float(save_data1[2])))
                    self.grandma_price.display(int(50 * 1.15 ** float(save_data1[2])))
                    self.farm_number.display(int(float(save_data1[3])))
                    self.farm_price.display(int(200 * 1.15 ** float(save_data1[3])))
                    self.factory_number.display(int(float(save_data1[4])))
                    self.factory_price.display(int(1000 * 1.15 ** float(save_data1[4])))
                    self.mine_number.display(int(float(save_data1[5])))
                    self.mine_price.display(int(4000 * 1.15 ** float(save_data1[5])))
                    self.laboratory_number.display(int(float(save_data1[6])))
                    self.laboratory_price.display(int(15000 * 1.15 ** float(save_data1[6])))
                    self.portal_number.display(int(float(save_data1[7])))
                    self.portal_price.display(int(60000 * 1.15 ** float(save_data1[3])))
            except Exception:
                self.return_error()

        self.main_click.clicked.connect(self.norm_click)
        self.click_push.clicked.connect(self.increase)
        self.grandma_push.clicked.connect(self.increase)
        self.farm_push.clicked.connect(self.increase)
        self.factory_push.clicked.connect(self.increase)
        self.mine_push.clicked.connect(self.increase)
        self.laboratory_push.clicked.connect(self.increase)
        self.portal_push.clicked.connect(self.increase)
        self.save_push.clicked.connect(self.save)
        self.tabWidget.tabBarClicked.connect(self.load_leaderboard)
        self.help.clicked.connect(self.return_help)

        self.load_leaderboard()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.autoclick)
        self.timer.start(1000)

    def return_help(self):
        help_window = HelpRulesWindow()
        help_window.exec()

    def return_error(self):
        error_window = ErrorWindow()
        error_window.exec()

    def load_leaderboard(self):
        result = self.cur.execute(f'''
                    SELECT nick_id,stats FROM nicknames_stats
                    ''').fetchall()
        result1 = []
        for i in result:
            nick = self.cur.execute('''
                SELECT nick from nicknames
                WHERE id = ?
            ''', (i[0],)).fetchall()

            save = i[1]
            result1.append([nick[0][0], save.split(';')[0].split('.')[0]])
        self.table.setRowCount(len(result1))
        self.table.setColumnCount(2)
        for i, elem in enumerate(result1):
            for j, val in enumerate(elem):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))
        self.table.setHorizontalHeaderLabels(['nick', 'save'])

    def save(self):
        self.cur.execute('''
            UPDATE nicknames_stats
            SET stats = ?
            WHERE nick_id = ?
        ''', (self.get_saved_data(), self.nick_id,))
        self.con.commit()

    def autoclick(self):
        self.main_display.display(self.main_display.intValue() + self.grandma_number.intValue() * 5)
        self.main_display.display(self.main_display.intValue() + self.farm_number.intValue() * 100)
        self.main_display.display(self.main_display.intValue() + self.factory_number.intValue() * 1000)
        self.main_display.display(self.main_display.intValue() + self.mine_number.intValue() * 4000)
        self.main_display.display(self.main_display.intValue() + self.laboratory_number.intValue() * 12000)
        self.main_display.display(self.main_display.intValue() + self.portal_number.intValue() * 20000)

    def norm_click(self):
        self.main_display.display(self.main_display.value() + self.click_number.value())

    def increase(self):
        if self.sender() == self.click_push and self.main_display.value() >= self.click_price.value():
            self.click_number.display(self.click_number.intValue() + 1)
            self.main_display.display(self.main_display.value() - self.click_price.value())
            self.click_price.display(int(self.click_price.intValue() * 1.15))
        elif self.sender() == self.grandma_push and self.main_display.value() >= self.grandma_price.value():
            self.grandma_number.display(self.grandma_number.intValue() + 1)
            self.grandma_price.display(int(self.grandma_price.intValue() * 1.15))
            self.main_display.display(self.main_display.value() - self.grandma_price.value())
        elif self.sender() == self.farm_push and self.main_display.value() >= self.farm_price.value():
            self.farm_number.display(self.farm_number.intValue() + 1)
            self.main_display.display(self.main_display.value() - self.farm_price.value())
            self.farm_price.display(int(self.farm_price.intValue() * 1.15))
        elif self.sender() == self.factory_push and self.main_display.value() >= self.factory_price.value():
            self.factory_number.display(self.factory_number.intValue() + 1)
            self.main_display.display(self.main_display.value() - self.factory_price.value())
            self.factory_price.display(int(self.factory_price.intValue() * 1.15))
        elif self.sender() == self.mine_push and self.main_display.value() >= self.mine_price.value():
            self.mine_number.display(self.mine_number.intValue() + 1)
            self.main_display.display(self.main_display.value() - self.mine_price.value())
            self.mine_price.display(int(self.mine_price.intValue() * 1.15))
        elif self.sender() == self.laboratory_push and self.main_display.value() >= self.laboratory_price.value():
            self.laboratory_number.display(self.laboratory_number.intValue() + 1)
            self.main_display.display(self.main_display.value() - self.laboratory_price.value())
            self.laboratory_price.display(int(self.laboratory_price.intValue() * 1.15))
        elif self.sender() == self.portal_push and self.main_display.value() >= self.portal_price.value():
            self.portal_number.display(self.portal_number.intValue() + 1)
            self.main_display.display(self.main_display.value() - self.portal_price.value())
            self.portal_price.display(int(self.portal_price.intValue() * 1.15))

    def get_saved_data(self):
        return f'{str(self.main_display.value())};{str(self.click_number.value())};\
                {str(self.grandma_number.value())};{str(self.farm_number.value())};{str(self.factory_number.value())};\
                {str(self.mine_number.value())};{str(self.laboratory_number.value())};{str(self.portal_number.value())}'


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
