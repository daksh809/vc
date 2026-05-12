from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.lang import Builder
from kivy.core.window import Window
import random
import re

# Screen Manager and Layout
KV = '''
MDScreenManager:
    LoginScreen:
    EMIScreen:

<LoginScreen>:
    name: "login"
    md_bg_color: 0.95, 0.96, 0.98, 1

    MDCard:
        orientation: "vertical"
        size_hint: 0.85, 0.8
        pos_hint: {"center_x": .5, "center_y": .5}
        padding: "20dp"
        spacing: "10dp"
        radius: [20,]
        elevation: 2

        MDLabel:
            text: "EMI Login"
            halign: "center"
            font_style: "H4"
            bold: True
            size_hint_y: None
            height: "60dp"

        MDBoxLayout:
            adaptive_height: True
            spacing: "10dp"
            pos_hint: {"center_x": .5}

            MDRaisedButton:
                text: "Phone"
                on_release: root.switch_mode("phone")
            MDRaisedButton:
                text: "Email"
                on_release: root.switch_mode("email")

        MDTextField:
            id: main_input
            hint_text: "Phone Number"
            icon_right: "phone"
            mode: "outline"

        MDTextField:
            id: password_input
            hint_text: "Password"
            icon_right: "key"
            mode: "outline"
            password: True
            opacity: 0
            disabled: True

        MDTextField:
            id: otp_input
            hint_text: "Enter OTP"
            mode: "outline"
            opacity: 0
            disabled: True

        MDRaisedButton:
            id: action_btn
            text: "SEND OTP"
            size_hint_x: 1
            on_release: root.handle_action()

        MDFlatButton:
            text: "Skip Login →"
            pos_hint: {"center_x": .5}
            on_release: app.root.current = "emi"

<EMIScreen>:
    name: "emi"
    MDBoxLayout:
        orientation: "vertical"
        
        MDTopAppBar:
            title: "EMI Calculator"
            right_action_items: [["logout", lambda x: root.logout()]]
            elevation: 4

        MDBoxLayout:
            orientation: "vertical"
            padding: "20dp"
            spacing: "15dp"

            MDTextField:
                id: principal
                hint_text: "Principal Amount (₹)"
                mode: "rectangle"
            
            MDTextField:
                id: rate
                hint_text: "Interest Rate (%)"
                mode: "rectangle"

            MDTextField:
                id: tenure
                hint_text: "Tenure (Years)"
                mode: "rectangle"

            MDRaisedButton:
                text: "CALCULATE"
                size_hint_x: 1
                on_release: root.calculate()

            MDCard:
                orientation: "vertical"
                padding: "15dp"
                radius: [15,]
                md_bg_color: 1, 1, 1, 1
                MDLabel:
                    id: result_label
                    text: "Results will appear here"
                    halign: "center"
                    font_style: "Subtitle1"
'''

class LoginScreen(MDScreen):
    mode = "phone"
    otp_code = ""

    def switch_mode(self, mode):
        self.mode = mode
        if mode == "phone":
            self.ids.main_input.hint_text = "Phone Number"
            self.ids.main_input.icon_right = "phone"
            self.ids.password_input.opacity = 0
            self.ids.password_input.disabled = True
            self.ids.action_btn.text = "SEND OTP"
        else:
            self.ids.main_input.hint_text = "Email Address"
            self.ids.main_input.icon_right = "email"
            self.ids.password_input.opacity = 1
            self.ids.password_input.disabled = False
            self.ids.otp_input.opacity = 0
            self.ids.action_btn.text = "LOGIN"

    def handle_action(self):
        val = self.ids.main_input.text.strip()
        
        if self.mode == "phone":
            if self.ids.action_btn.text == "SEND OTP":
                if val.isdigit() and len(val) == 10:
                    self.otp_code = str(random.randint(1000, 9999))
                    self.show_dialog("OTP Sent", f"Your OTP is: {self.otp_code}")
                    self.ids.otp_input.opacity = 1
                    self.ids.otp_input.disabled = False
                    self.ids.action_btn.text = "VERIFY & LOGIN"
                else:
                    self.show_dialog("Error", "Enter valid 10-digit number")
            else:
                if self.ids.otp_input.text == self.otp_code:
                    self.manager.current = "emi"
                else:
                    self.show_dialog("Error", "Invalid OTP")

        else: # Email Mode
            password = self.ids.password_input.text
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            
            if not re.match(email_pattern, val):
                self.show_dialog("Format Error", "Invalid Email!")
            elif len(password) < 6:
                self.show_dialog("Security", "Min 6 characters required")
            elif password == "admin123":
                self.manager.current = "emi"
            else:
                self.show_dialog("Failed", "Wrong Password!")

    def show_dialog(self, title, text):
        MDDialog(title=title, text=text, size_hint=(0.7, None)).open()

class EMIScreen(MDScreen):
    def calculate(self):
        try:
            P = float(self.ids.principal.text)
            R = float(self.ids.rate.text) / (12 * 100)
            N = float(self.ids.tenure.text) * 12
            emi = (P * R * (1+R)**N) / ((1+R)**N - 1)
            total = emi * N
            self.ids.result_label.text = f"EMI: ₹{round(emi,2)}\nTotal Int: ₹{round(total-P,2)}\nTotal: ₹{round(total,2)}"
        except:
            MDDialog(title="Error", text="Enter valid numbers").open()

    def logout(self):
        self.manager.current = "login"

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(KV)

if __name__ == "__main__":
    MainApp().run()