import random
import time

from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDFloatingActionButton, MDFlatButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivymd.uix.behaviors import MagicBehavior
from kivymd.icon_definitions import md_icons
from kivymd.uix.widget import MDWidget
from kivymd.uix.behaviors.elevation import CommonElevationBehavior
from kivy.core.window import Window
from kivymd.uix.button.button import ButtonElevationBehaviour
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.button import MDRectangleFlatButton, MDIconButton
from kivy.core.window import Window
from kivy.properties import BoundedNumericProperty, StringProperty, ObjectProperty
from kivy.metrics import dp
from kivy.uix.progressbar import ProgressBar

import socket
import threading
import rsa
import asyncio
import threading
import json
import os

checkActive = None

client=None

licznik=0

selected_Language = None

C=""
spos=0


H=""

selected_jezyk = "EN"

SelectedAnswer = 'testt'
T = []
P = []
JS = []
K = []
L = []


class MainScreen(ScreenManager):
    dialog = None


    def kolejka(self):
        self.show_dialog()





    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        selected_project = StringProperty()

        menu_items = [
            {
                "text": f"Python",
                "viewclass": "OneLineListItem",
                "theme_text_color": "Custom",
                "text_color": [1, 1, 1, 1],  # White color
                "on_release": lambda x='Choose Theme': self.PythonSelection(),
            },
            {
                "text": f"JavaScript",
                "viewclass": "OneLineListItem",
                "theme_text_color": "Custom",
                "text_color": [1, 1, 1, 1],  # White color
                "on_release": lambda x='Language': self.JavaScriptSelection(),
            }
        ]

        self.menu = MDDropdownMenu(
            caller=self.ids.MenuButton,
            items=menu_items,
            width_mult=2.7,
            border_margin=dp(4),
            header_cls=MenuHeader(),
            # background_color=FirstApp().theme_cls.theme_style_light,
            radius=[24, 0, 24, 0],
            elevation=2,
            max_height=dp(112),
        )

        menu_items2 = [
            {
                "text": f"[color=#ffffff]LOGOUT[/color]",
                "viewclass": "OneLineListItem",
                "theme_text_color": "Custom",
                "on_release": lambda x='LOGOUT': self.LOGOUT(),
            }
        ]

        self.menu2 = MDDropdownMenu(
            caller=self.ids.MenuButton2,
            items=menu_items2,
            width_mult=2.7,
            border_margin=dp(4),
            header_cls=MenuHeader1(),
            radius=[24, 0, 24, 0],
            elevation=2,
            max_height=dp(112),
            position="bottom"
        )


    def wyslij(self,s,d):
        public_key, private_key = rsa.newkeys(1024)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('34.95.8.155', 5555))

        client.send(public_key.save_pkcs1("PEM"))
        public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
        wiado="JEZYK "+str(T[2])+" "+str(s)+str(d)
        wiado=wiado.encode()
        wiado=rsa.encrypt(wiado,public_partner)
        client.send(wiado)



    def POLISH(self):
        global selected_jezyk
        if selected_jezyk!= "PL":
            selected_jezyk = "PL"

            if selected_Language == "PY":
                self.ids.POINTS.text = "WYBRALES PYTHONA"
            elif selected_Language=="JS":
                self.ids.POINTS.text = "WYBRALES JAVASCRIPT"
            else:
                self.ids.POINTS.text = "WYBIERZ JEZYK"
            thread=threading.Thread(target=self.wyslij,args="PL")
            thread.start()


    def ENGLISH(self):
        global selected_jezyk
        if selected_jezyk!= "EN":
            selected_jezyk = "EN"
            if selected_Language == "PY":
                self.ids.POINTS.text = "YOU CHOOSED PYTHON LANGUAGE"
            elif selected_Language == "JS":
                self.ids.POINTS.text = "YOU CHOOSED JavaScript LANGUAGE"
            else:
                self.ids.POINTS.text = "CHOOSE LANGUAGE"
            thread = threading.Thread(target=self.wyslij, args="EN")
            thread.start()

    def LOGOUT(self):
        self.ids.LOGIN.text = "LOGIN"
        Clock.schedule_once(lambda dt: self.changescreen('test1'), .6)

    def SetIcon(self, obj):
        ItemConfirm().set_icon(obj)

    def ssas(self):
        time.sleep(5)
        if self.current == 'test3':
            return Clock.schedule_once(lambda dt: self.changescreen('test2'), .6)
        else:
            return 0




    def show_confirmation_dialog(self, odp, k):
        global selected_Language
        self.ok_callback()
        if selected_jezyk=="PL":
            print(odp)
            if odp=="you lost you marked the wrong answer and your opponent marked the right one you lost ":
                odp="PRZEGRALES zaznaczyles zla odpowiedz a twoj przeciwnik dobra przegrales "
            elif odp == "you won your opponent marked the wrong answer you won ":
                odp="WYGRALES zaznaczyles dobra odpowiedz a twoj przeciwnik zla wygrales "
            elif odp=="your opponent didnt select asnwer you won":
                odp = "Twoj przeciwnik nie zaznaczyl zadnej odpowiedzi wygrales gratulujemy :D "
            else:

                odp="LIMIT CZASU MINAL ZA POZNO :C jezeli twoj przeciwnik zaznaczyl odpowiedz straciles "
        self.dialog = MDDialog(
            title="SERVER:",
            text=odp + "(" + k + "PKT)",
            buttons=[
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    text_color=FirstApp().theme_cls.primary_color,

                    on_release=self.sss,

                ),
            ],
        )
        self.dialog.open()
        thread=threading.Thread(target=self.ssas)
        thread.start()


    def nie_dziala_info(self):
        if selected_jezyk=="PL":
            odp="SERWER NIE ODPOWIEDZIAL.Przepraszamy za trudnosci naprawimy go jak najszybciej dziekujemy za wyrozumialosc :DDD"
        else:
            odp="THE SERVER DID NOT RESPOND. We apologize for the inconvenience, we will fix it as soon as possible, thank you for your understanding :DDD"

        self.dialog = MDDialog(
            title="SERVER:",
            text=odp,
            buttons=[
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    text_color=FirstApp().theme_cls.primary_color,

                    on_release=self.sss,

                ),
            ],
        )
        self.dialog.open()

        

    def PythonSelection(self):
        global selected_Language
        selected_Language = 'PY'
        # self.show_confirmation_dialog()
        if selected_jezyk == "EN":
            self.ids.POINTS.text = "YOU CHOOSED PYTHON LANGUAGE"
        else:
            self.ids.POINTS.text = "WYBRALES PYTHONA"
        self.ids.POINTS_L.text = T[0]
        self.ids.nazwa.text = "Python RANKED"
        self.ids.item0.text = '1:' + "     "+P[0]+"PKT"
        self.ids.item1.text = '2:' + "     "+P[1]+"PKT"
        self.ids.item2.text = '3:' + "     "+P[2]+"PKT"
        self.ids.item3.text = '4:' + "     "+P[3]+"PKT"
        self.ids.item4.text = '5:' + "     "+P[4]+"PKT"
        self.ids.item5.text = '6:' + "     "+P[5]+"PKT"
        self.ids.item6.text = '7:' + "     "+P[6]+"PKT"
        self.ids.item7.text = '8:' + "     "+P[7]+"PKT"
        self.ids.item8.text = '9:' + "     "+P[8]+"PKT"
        self.ids.item9.text = '10:' + "     "+P[9]+"PKT"

    def JavaScriptSelection(self):
        global selected_Language
        selected_Language = 'JS'
        # self.show_confirmation_dialog()
        if selected_jezyk == "EN":
            self.ids.POINTS.text = "YOU CHOOSED JavaScript LANGUAGE"
        else:
            self.ids.POINTS.text = "WYBRALES JAVASCRIPT"
        self.ids.POINTS_L.text = T[1]
        self.ids.nazwa.text = "JavaScript RANKED"
        self.ids.item0.text = '1:' + "     "+str(JS[0])+"PKT"
        self.ids.item1.text = '2:' + "     "+str(JS[1])+"PKT"
        self.ids.item2.text = '3:' + "     "+str(JS[2])+"PKT"
        self.ids.item3.text = '4:' + "     "+str(JS[3])+"PKT"
        self.ids.item4.text = '5:' + "     "+str(JS[4])+"PKT"
        self.ids.item5.text = '6:' + "     "+str(JS[5])+"PKT"
        self.ids.item6.text = '7:' + "     "+str(JS[6])+"PKT"
        self.ids.item7.text = '8:' + "     "+str(JS[7])+"PKT"
        self.ids.item8.text = '9:' + "     "+str(JS[8])+"PKT"
        self.ids.item9.text = '10:' + "     "+str(JS[9])+"PKT"

    def show_confirmation_dialog1(self):
        global selected_Language
        if H!="1":
            if selected_jezyk == "PL":
                a="SERWER"
                b=SelectedAnswer+" Zostala zaznaczona czekamy na odpowiedz przeciwnika"
            else:
                a = "SERVER"
                b = SelectedAnswer+" has been marked. Waiting for the opponents response"
        else:
            if selected_jezyk == "PL":
                a="SERWER"
                b="Odpowiedz zostala juz przez ciebie zaznaczona czekamy na twojego przeciwnika (powodzenia :D)"
            else:
                a = "SERVER"
                b = "The answer has been already selected by you we are waiting for your opponents answer (good luck :D)"


        self.dialog = MDDialog(
            title=a+":",
            text=b,
        )
        self.dialog.open()

    def show_dialog(self):
        a="SERVER"
        b="sorry we already found a game for you you can't exit now get ready to play the game will be launched in a moment"
        self.dialog = MDDialog(
            title=a + ":",
            text=b,
            buttons=[
                MDFlatButton(
                    text="OK :C",
                    theme_text_color="Custom",
                    text_color=FirstApp().theme_cls.primary_color,

                    on_release=self.JGA_POTEGA,

                ),
            ],
        )
        self.dialog.open()

    def JGA_POTEGA(self,s):
        self.dialog.dismiss()
    def log(self):
        global selected_jezyk
        try:
            public_key, private_key = rsa.newkeys(1024)
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(('34.95.8.155', 5555))

            client.send(public_key.save_pkcs1("PEM"))
            public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
            message = 'L ' + str(Userinput) + " " + str(Password)
            encrypted_message = rsa.encrypt(message.encode('ascii'), public_partner)
            client.send(encrypted_message)

            encrypted_response = client.recv(1024)
            response = rsa.decrypt(encrypted_response, private_key).decode()
            response = response.split()

            client.close()
            if response[0] == 'TAK':
                print("SDA")

                T.clear()
                T.append(str(response[1]))
                T.append(str(response[2]))
                T.append(str(response[3]))
                selected_jezyk=str(response[4])
                if selected_jezyk == "PL":
                    self.ids.POINTS.text = "WYBIERZ JEZYK"
                self.hide_shadows()
                self.transition.duration = 0.4
                self.transition.direction = "left"
                public_key, private_key = rsa.newkeys(1024)

                # Inicjalizacja połączenia z serwerem
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect(('34.95.8.155', 5555))

                # Wysłanie klucza publicznego do serwera
                client.send(public_key.save_pkcs1("PEM"))
                public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
                # Wysłanie wiadomości do serwera
                message = 'top'
                encrypted_message = rsa.encrypt(message.encode('ascii'), public_partner)
                client.send(encrypted_message)

                # Odbieranie i deszyfrowanie odpowiedzi od serwera
                response = client.recv(1024).decode()

                mes = client.recv(1024).decode()

                # Zamknięcie połączenia z serwerem
                client.close()
                leaderboard = response.split(",")
                P.clear()
                JS.clear()
                for el in leaderboard:
                    P.append(el)
                self.ids.item0.text = '1:' + "     "+leaderboard[0]+"PKT"
                self.ids.item1.text = '2:' + "     "+leaderboard[1]+"PKT"
                self.ids.item2.text = '3:' + "     "+leaderboard[2]+"PKT"
                self.ids.item3.text = '4:' + "     "+leaderboard[3]+"PKT"
                self.ids.item4.text = '5:' + "     "+leaderboard[4]+"PKT"
                self.ids.item5.text = '6:' + "     "+leaderboard[5]+"PKT"
                self.ids.item6.text = '7:' + "     "+leaderboard[6]+"PKT"
                self.ids.item7.text = '8:' + "     "+leaderboard[7]+"PKT"
                self.ids.item8.text = '9:' + "     "+leaderboard[8]+"PKT"
                self.ids.item9.text = '10:' + "     "+leaderboard[9]+"PKT"
                leaderboard = mes.split(",")
                for el in leaderboard:
                    JS.append(el)

                return Clock.schedule_once(lambda dt: self.changescreen('test2'), .6)
            else:
                return Clock.schedule_once(lambda dt: self.changescreen('test1'), .6)
        except:
            return Clock.schedule_once(lambda dt: self.changescreen('test1'), .6)



    def GUZIK(self):
        global Userinput
        global Password
        file_name = "login_data.json"

        try:
            with open(file_name, "r") as file:
                login_data = json.load(file)
                username = login_data["username"]
                password = login_data["password"]

                Userinput = username
                Password = password
                self.ids.UserNick.text = f'Hey,  {Userinput}'
                thread = threading.Thread(target=self.log)
                thread.start()
        except:
            return Clock.schedule_once(lambda dt: self.changescreen('test1'), .6)


    def show_confirmation_dialog3(self, s):
        global selected_Language
        s = str(int(s) + 10)
        self.ok_callback()
        if selected_jezyk=="PL":
            a="SERWER"
            b="REMIS przygotuj sie do nastepnej rundy o "
        else:
            a="SERVER"
            b="TIE get ready to another round for "
        self.dialog = MDDialog(
            title=a+":",
            text=b + s + "PKT )",
            buttons=[
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    text_color=FirstApp().theme_cls.primary_color,

                    on_release=self.ok_callback1,

                ),
            ],
        )
        self.dialog.open()

    def dane(self):
        public_key, private_key = rsa.newkeys(1024)
        # Inicjalizacja połączenia z serwerem
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('34.95.8.155', 5555))

        # Wysłanie klucza publicznego do serwera
        client.send(public_key.save_pkcs1("PEM"))
        public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
        # Wysłanie wiadomości do serwera
        message = 'top'
        encrypted_message = rsa.encrypt(message.encode('ascii'), public_partner)
        client.send(encrypted_message)
        message = client.recv(1024)
        message = message.decode()
        message = message.split(',')
        p = message
        message = client.recv(1024).decode()
        js = message.split(',')
        P.clear()
        JS.clear()

        for k in p:
            P.append(k)
        for i in js:
            JS.append(i)
        client.close()
        id = str(T[2])
        public_key, private_key = rsa.newkeys(1024)
        # Inicjalizacja połączenia z serwerem
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('34.95.8.155', 5555))

        # Wysłanie klucza publicznego do serwera
        client.send(public_key.save_pkcs1("PEM"))
        public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
        # Wysłanie wiadomości do serwera
        message = 'POINTS ' + str(id)
        message = rsa.encrypt(message.encode('ascii'), public_partner)
        client.send(message)
        c = client.recv(1024)
        c = rsa.decrypt(c, private_key).decode()
        c = c.split()
        T.clear()
        T.append(str(c[0]))
        T.append(str(c[1]))
        T.append(id)
        client.close()
        if selected_Language == "PY":
            self.PythonSelection()
        else:
            self.JavaScriptSelection()
        return 1

    def refresh(self):
        task = threading.Thread(target=self.dane)
        task.start()
        return 1

    def sss(self, l):
        self.dialog.dismiss()
        Clock.schedule_once(lambda dt: self.changescreen('test2'), .6)
        self.refresh()

    def ok_callback(self):
        if self.dialog:
            self.dialog.dismiss()

        # self.show_confirmation_dialog()

    def ok_callback1(self, x):
        if self.dialog:
            self.dialog.dismiss()

    def Ans1(self):
        global SelectedAnswer
        SelectedAnswer = self.ids.Answerfield1.text

    def Ans2(self):
        global SelectedAnswer
        SelectedAnswer = self.ids.Answerfield2.text

    def Ans3(self):
        global SelectedAnswer
        SelectedAnswer = self.ids.Answerfield3.text

    def Ans4(self):
        global SelectedAnswer
        SelectedAnswer = self.ids.Answerfield4.text

    def changescreen(self, screen='test1'):
        self.current = screen


    def licznik1(self):
        sss=30
        s=0
        while sss-s!=0:
            if spos>0:
                s=s+1
                #self.ids.pog.text=str(sss-s)
                p=sss-s
                if p <10:
                    self.ids.czas.text="0"+str(p)
                else:
                    self.ids.czas.text=str(p)
                time.sleep(1)
            else:
                return 1

    async def gra1(self, reader, writer, rund):
        global SelectedAnswer
        SelectedAnswer = "STATASTAT"
        p = SelectedAnswer
        global H
        global sss
        global spos
        spos=0
        s=0
        H=""
        self.ids.czas.text = "30"
        s = rund * 10
        s = str(s)
        data = await reader.read(1024)
        data = data.decode()
        data = str(data)
        data = data.split(',')
        self.ids.Things.text = data[0]
        self.ids.Answerfield1.text = data[1]
        self.ids.Answerfield2.text = data[2]
        self.ids.Answerfield3.text = data[3]
        self.ids.Answerfield4.text = data[4]
        spos=1
        t=threading.Thread(target=self.licznik1)
        t.start()
        while True:
            await asyncio.sleep(2)
            if SelectedAnswer != p:
                l = SelectedAnswer.strip()
                writer.write(l.encode('ascii'))
                H="1"
                break
        p = await reader.read(1024)
        p = p.decode()
        print(p)
        K.append(p)
        K.append(s)

        SelectedAnswer = "STATASTAT"

        if p == "tie get ready to another round":
            await self.gra1(reader, writer, rund + 1)
        spos=0

        return 1

    def licznik(self):
        global licznik
        time.sleep(2)
        while self.current=="test4":
            licznik=licznik+1
            if selected_jezyk=="PL":
                self.ids.times_label.text="CZAS W KOLEJCE: "+str(licznik)+" sec"
            else:
                self.ids.times_label.text="TIME IN QUEUE: "+str(licznik)+" sec"
            time.sleep(1)
        print(self.current)
        return 0

    async def gra(self, round):
        global client
        global C
        global selected_Language
        global SelectedAnswer
        try:
            reader, writer = await asyncio.open_connection('34.95.8.155', 1234)
            client = reader, writer
            if selected_jezyk=="PL":
                self.ids.time_label.text="PRZEWIDYWANY CZAS: "+str(random.randint(20,120))+"sec"
                self.ids.times_label.text="CZAS W KOLEJCE: "+"0 sec"
                self.ids.czekanie.text="CZEKANIE W KOLEJCE"
                self.ids.tip.text="WSKAZOWKA: GRAJ CZYSTO"
            else:
                self.ids.time_label.text = "EXPECTED TIME: " + str(random.randint(20, 120)) + "sec"
                self.ids.times_label.text = "TIME IN QUEUE: " + "0 sec"
                self.ids.czekanie.text = "WAITING IN QUEUE"
                self.ids.tip.text = "TIP: PLAY FAIR "

            Clock.schedule_once(lambda dt: self.changescreen('test4'), .6)
            print(self.current)
            task = threading.Thread(target=self.licznik)
            task.start()
            L.clear()
            print(self.current)
            response = await reader.read(1024)
            response = response.decode()
            if response == "MAM":
                id = T[2]
                id = str(id)
                writer.write(f"{selected_Language},{id}".encode('ascii'))
                data = await reader.read(1024)
                if data.decode() == "MAM1":
                    Clock.schedule_once(lambda dt: self.changescreen('test3'), .6)
                    print(self.current)
                    await self.gra1(reader, writer, round)
            else:
                Clock.schedule_once(lambda dt: self.changescreen('test2'), .6)
            return 1
        except:
            C = "1"
            L.clear()
            return 0

    def run_gra_in_background(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        task = loop.create_task(self.gra(1))
        loop.run_until_complete(task)
        loop.close()
        return 1





    def PlayButtonPressed(self, *args):
        global licznik
        licznik=0
        if selected_Language == "JS" or selected_Language == "PY":
            if len(L) < 1:

                L.append("s")
                t = threading.Thread(target=self.run_gra_in_background)
                t.start()

                self.sprawdzanie()
    def sprawdzanie(self, timeout=1):
        global C
        if len(K) > 0:
            if K[0] != "tie get ready to another round":
                if K[0] == "":
                    K[0] = "time limit exceeded"
                self.show_confirmation_dialog(str(K[0]), K[1])
                K.clear()
                L.clear()
                return 1
            else:
                self.show_confirmation_dialog3(K[1])
                K.clear()
                Clock.schedule_once(lambda dt: self.sprawdzanie(timeout), timeout)

        else:
            if len(C)>0:
                if C=="1":
                    C=""
                    self.nie_dziala_info()
                    return 1

            else:
                Clock.schedule_once(lambda dt: self.sprawdzanie(timeout), timeout)

    def hide_shadows(self, a=None):
        if self.current == 'test1':
            # self.ids.toolbar1.elevation = 0
            # self.ids.MTB.elevation = 0
            pass
        elif self.current == 'test2':
            # self.ids.toolbar2.elevation = 0
            # self.ids.S2FButton.elevation = 0
            pass
        elif self.current == 'test3':
            # self.ids.S2FButton.elevation = 0
            pass

    def unhide_shodows(self, a=None):

        if self.current == 'test1':
            # self.ids.toolbar1.elevat ion = 4
            # self.ids.MTB.elevation =  0
            # self.ids.S2FButton.elevation = 3
            pass
        elif self.current == 'test2':
            # self.ids.toolbar2.elevation = 4
            # self.ids.MTB.elevation = 3
            # self.ids.S2FButton.elevation = 0
            pass
        elif self.current == 'test3':
            # self.ids.MTB.elevation = 3
            # self.ids.S2FButton.elevation = 3
            pass

    def Check2(self):
        pass

    def SigninBehave(self, MagicBehavior, MDFloatingActionButton):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
        # self.ids.Sgn.grow()

    def niezacinav2(self):
        global Userinput
        try:
            Userinput = self.ids.userinput.text
            Password = self.ids.password.text
            self.ids.UserNick.text = f'Hey,  {Userinput}'
            if self.current == 'test1':
                if str(Userinput) != "" and str(Password) != "":
                    public_key, private_key = rsa.newkeys(1024)
                    print("SDAD")
                    # Inicjalizacja połączenia z serwerem
                    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    print("DSADA")
                    client.connect(('34.95.8.155', 5555))
                    # Wysłanie klucza publicznego do serwera
                    client.send(public_key.save_pkcs1("PEM"))
                    print("ASDADA")
                    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
                    # Wysłanie wiadomości do serwera
                    message = 'R ' + str(Userinput) + " " + str(Password)
                    print("ASDASDASD")
                    encrypted_message = rsa.encrypt(message.encode('ascii'), public_partner)
                    client.send(encrypted_message)
                    print("SDADSA")

                    # Odbieranie i deszyfrowanie odpowiedzi od serwera
                    dddddd = client.recv(1024)
                    response = rsa.decrypt(dddddd, private_key).decode()
                    print(response)

                    # Zamknięcie połączenia z serwerem
                    client.close()
                    if response == "TAK":
                        self.ids.LOGIN.text = "registration was successful log in"
                    elif response == "ZAJETE":
                        self.ids.LOGIN.text = "this name is already taken"

        except:
            self.ids.LOGIN.text = "application servers are offline"

    def register(self):
        Password = self.ids.password.text
        Userinput = self.ids.userinput.text
        if str(Password) != "" and str(Userinput) != "":
            print(len(str(Password)))
            if len(str(Password)) > 5:
                if len(str(Userinput))<8:
                    self.ids.LOGIN.text = "connecting to the server"
                    thread = threading.Thread(target=self.niezacinav2)
                    thread.start()
                else:
                    self.ids.LOGIN.text = "your nick can be up to 8 characters"
            else:
                self.ids.LOGIN.text = "the password is too short"
        else:
            self.ids.LOGIN.text = "tables cannot be empty"

    def niezacina(self):
        global selected_jezyk
        try:
            # Tworzenie kluczy RSA
            public_key, private_key = rsa.newkeys(1024)
            # Inicjalizacja połączenia z serwerem
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(('34.95.8.155', 5555))
            # Wysłanie klucza publicznego do serwera
            client.send(public_key.save_pkcs1("PEM"))
            public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
            # Wysłanie wiadomości do serwera
            message = 'L ' + str(Userinput) + " " + str(Password)
            encrypted_message = rsa.encrypt(message.encode('ascii'), public_partner)
            client.send(encrypted_message)
            # Odbieranie i deszyfrowanie odpowiedzi od serwera
            encrypted_response = client.recv(1024)
            response = rsa.decrypt(encrypted_response, private_key).decode()
            response = response.split()
            # Zamknięcie połączenia z serwerem
            client.close()
            if response[0] == 'TAK':


                T.clear()
                T.append(str(response[1]))
                T.append(str(response[2]))
                T.append(str(response[3]))
                selected_jezyk=response[4]

                self.hide_shadows()
                self.transition.duration = 0.4
                self.transition.direction = "left"
                print("SDAd")

                # Inicjalizacja połączenia z serwerem
                public_key, private_key = rsa.newkeys(1024)
                # Inicjalizacja połączenia z serwerem
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect(('34.95.8.155', 5555))
                # Wysłanie klucza publicznego do serwera
                print("FASFAFASFASF")
                client.send(public_key.save_pkcs1("PEM"))
                public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
                if selected_jezyk=="PL":
                    self.ids.POINTS.text="WYBIERZ JEZYK"

                message = 'top'
                print("FASFAFASFASF")
                encrypted_message = rsa.encrypt(message.encode('ascii'), public_partner)
                client.send(encrypted_message)

                # Odbieranie i deszyfrowanie odpowiedzi od serwera
                response=client.recv(1024).decode()
                print(response)

                mes = client.recv(1024).decode()

                # Zamknięcie połączenia z serwerem
                client.close()
                leaderboard = response.split(",")
                P.clear()
                JS.clear()
                for el in leaderboard:
                    P.append(el)
                self.ids.item0.text = '1:' + leaderboard[0]
                self.ids.item1.text = '2:' + leaderboard[1]
                self.ids.item2.text = '3:' + leaderboard[2]
                self.ids.item3.text = '4:' + leaderboard[3]
                self.ids.item4.text = '5:' + leaderboard[4]
                self.ids.item5.text = '6:' + leaderboard[5]
                self.ids.item6.text = '7:' + leaderboard[6]
                self.ids.item7.text = '8:' + leaderboard[7]
                self.ids.item8.text = '9:' + leaderboard[8]
                self.ids.item9.text = '10:' + leaderboard[9]
                leaderboard = mes.split(",")
                for el in leaderboard:
                    JS.append(el)

                login_data = {
                    "username": str(Userinput),
                    "password": str(Password)
                }

                file_name = "login_data.json"

                with open(file_name, "w") as file:
                    json.dump(login_data, file)

                return Clock.schedule_once(lambda dt: self.changescreen('test2'), .6)

            elif response[0] == 'NOT':
                self.ids.LOGIN.text = "there is no such account"
                self.ids.MTB.wobble()
            else:
                self.ids.LOGIN.text = "wrong password"
                self.ids.MTB.wobble()



        except:
            self.ids.LOGIN.text = "application servers are offline"
        return 1

    def Check(self):
        global Userinput
        global Password
        Userinput = self.ids.userinput.text
        Password = self.ids.password.text
        self.ids.UserNick.text = f'Hey,  {Userinput}'
        # self.ids.UserNick.text_color = (0.2, 0.2, 0.2, 1)

        if self.current == 'test1':
            if str(Password) != "" and str(Userinput) != "":
                if len(str(Password)) > 5:
                    self.ids.LOGIN.text = "connecting to the server"
                    thread = threading.Thread(target=self.niezacina)
                    thread.start()
                else:
                    self.ids.LOGIN.text = "wrong password"


class ItemConfirm(OneLineAvatarIconListItem):
    divider = None

    def set_icon(self, instance_check):
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        for check in check_list:
            if check != instance_check:
                check.active = False


class MenuHeader(MDBoxLayout):
    pass


class MenuHeader1(MDBoxLayout):
    pass


class MagicButton(MagicBehavior, MDFloatingActionButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class SinginButton(MagicBehavior, MDFloatingActionButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class AnswerWidget(MDBoxLayout):
    Answer1 = 'Answer1'
    Answer2 = 'Answer2'
    Answer3 = 'Answer3'
    Answer4 = 'Answer4'


class ScreenOne(MDScreen):
    pass


class ScreenTwo(MDScreen):
    pass


class ScreenThree(MDScreen):
    pass


class ScreenFour(MDScreen):
    pass


class FirstApp(MDApp):
    theme_color = ObjectProperty(None)

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.primary_hue = "500"

        self.theme_cls.accent_palette = "Green"
        self.theme_cls.accent_hue = "800"
        return MainScreen()


FirstApp().run()