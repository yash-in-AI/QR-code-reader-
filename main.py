import os
import webbrowser
import cv2
import qrcode
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, Screen
import threading
from datetime import datetime

# Set window size for desktop
Window.size = (400, 650)
Window.minimum_width = 350
Window.minimum_height = 600

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'main'
        
        layout = BoxLayout(orientation='vertical', padding=[20, 40, 20, 30], spacing=25)
        
        # App Title
        title_label = Label(
            text='QRBoost',
            font_size='36sp',
            bold=True,
            color=[0.1, 0.6, 0.9, 1],
            size_hint=(1, 0.2)
        )
        
        # Subtitle
        subtitle_label = Label(
            text='Your Ultimate QR Code Solution',
            font_size='14sp',
            color=[0.4, 0.4, 0.4, 1],
            size_hint=(1, 0.1)
        )
        
        layout.add_widget(title_label)
        layout.add_widget(subtitle_label)
        
        # Create buttons grid
        button_grid = GridLayout(cols=1, spacing=15, size_hint=(1, 0.6), padding=[0, 10, 0, 10])
        
        # Define button configurations
        buttons = [
            {
                'text': 'Generate QR Code',
                'color': [0.2, 0.7, 0.3, 1],
                'screen': 'generate'
            },
            {
                'text': 'Scan QR Code',
                'color': [0.9, 0.5, 0.1, 1],
                'screen': 'scan'
            },
            {
                'text': 'Scan & Open Link',
                'color': [0.1, 0.6, 0.9, 1],
                'screen': 'scan_open'
            },
            {
                'text': 'WhatsApp QR Code',
                'color': [0.4, 0.8, 0.4, 1],
                'screen': 'whatsapp'
            }
        ]
        
        # Create buttons
        for btn_config in buttons:
            btn = Button(
                text=btn_config['text'],
                background_color=btn_config['color'],
                size_hint=(1, None),
                height=dp(60),
                font_size='16sp',
                bold=True,
                background_normal=''
            )
            btn.bind(on_release=lambda instance, screen=btn_config['screen']: self.go_to_screen(screen))
            button_grid.add_widget(btn)
        
        layout.add_widget(button_grid)
        
        # Footer
        footer_label = Label(
            text='© 2024 QRBoost | All-in-One QR Solution',
            font_size='10sp',
            color=[0.5, 0.5, 0.5, 1],
            size_hint=(1, 0.1)
        )
        layout.add_widget(footer_label)
        
        self.add_widget(layout)
    
    def go_to_screen(self, screen_name):
        self.manager.current = screen_name

class GenerateQRScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'generate'
        
        layout = BoxLayout(orientation='vertical', padding=[20, 20, 20, 20], spacing=15)
        
        # Back button
        back_btn = Button(
            text='Back',
            size_hint=(None, None),
            size=(dp(70), dp(35)),
            background_color=[0.3, 0.3, 0.3, 1],
            background_normal=''
        )
        back_btn.bind(on_release=self.go_back)
        
        # Header
        header = Label(
            text='Generate QR Code',
            font_size='24sp',
            bold=True,
            color=[0.1, 0.6, 0.9, 1],
            size_hint=(1, 0.15)
        )
        
        # Input field
        self.data_input = TextInput(
            hint_text='Enter text or link here...',
            multiline=False,
            size_hint=(1, None),
            height=dp(45),
            padding=[10, 10],
            font_size='14sp'
        )
        
        # Generate button
        generate_btn = Button(
            text='Generate QR Code',
            background_color=[0.2, 0.7, 0.3, 1],
            size_hint=(1, None),
            height=dp(50),
            font_size='16sp',
            bold=True,
            background_normal=''
        )
        generate_btn.bind(on_release=self.generate_qr)
        
        # QR Code display area with smaller size
        self.qr_image = Image(
            size_hint=(0.6, 0.4),
            pos_hint={'center_x': 0.5},
            allow_stretch=True,
            keep_ratio=True
        )
        
        # Add widgets
        layout.add_widget(back_btn)
        layout.add_widget(header)
        layout.add_widget(self.data_input)
        layout.add_widget(generate_btn)
        layout.add_widget(self.qr_image)
        
        self.add_widget(layout)
    
    def go_back(self, instance):
        self.manager.current = 'main'
    
    def generate_qr(self, instance):
        data = self.data_input.text.strip()
        if not data:
            self.show_popup('Error', 'Please enter some text or link!')
            return
        
        try:
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=8,
                border=2,
            )
            qr.add_data(data)
            qr.make(fit=True)
            
            # Create image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Save temporary file
            filename = f"qr_code_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            img.save(filename)
            
            # Update image widget
            self.qr_image.source = filename
            self.qr_image.reload()
            
            self.show_popup('Success', f'QR Code generated successfully!')
            
        except Exception as e:
            self.show_popup('Error', f'Failed to generate QR code: {str(e)}')
    
    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message))
        btn = Button(text='OK', size_hint=(1, None), height=dp(40))
        popup = Popup(title=title, content=content, size_hint=(0.8, 0.3))
        btn.bind(on_release=popup.dismiss)
        content.add_widget(btn)
        popup.open()

class ScanQRScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'scan'
        self.scanning = False
        self.cap = None
        self.open_link = False
        self.last_scanned_data = None
        self.link_opened = False
        
        layout = BoxLayout(orientation='vertical', padding=[10, 10, 10, 10], spacing=8)
        
        # Back button
        back_btn = Button(
            text='Back',
            size_hint=(None, None),
            size=(dp(70), dp(35)),
            background_color=[0.3, 0.3, 0.3, 1],
            background_normal=''
        )
        back_btn.bind(on_release=self.go_back)
        
        # Header
        header_text = 'Scan QR Code'
        if self.open_link:
            header_text = 'Scan & Open Link'
        
        self.header = Label(
            text=header_text,
            font_size='24sp',
            bold=True,
            color=[0.9, 0.5, 0.1, 1] if not self.open_link else [0.1, 0.6, 0.9, 1],
            size_hint=(1, 0.1)
        )
        
        # Camera display
        self.camera_image = Image(
            size_hint=(1, 0.55),
            allow_stretch=True,
            keep_ratio=True
        )
        
        # Result display
        self.result_label = Label(
            text='Camera will start when you click Start Scanning',
            font_size='14sp',
            color=[0.4, 0.4, 0.4, 1],
            size_hint=(1, 0.1),
            halign='center',
            valign='middle'
        )
        self.result_label.bind(size=self.result_label.setter('text_size'))
        
        # Control buttons (smaller size)
        controls = BoxLayout(size_hint=(1, 0.08), spacing=10, padding=[0, 5, 0, 5])
        
        self.start_btn = Button(
            text='Start Scanning',
            background_color=[0.2, 0.7, 0.3, 1],
            background_normal='',
            font_size='14sp'
        )
        self.start_btn.bind(on_release=self.toggle_scanning)
        
        self.stop_btn = Button(
            text='Stop',
            background_color=[0.9, 0.3, 0.3, 1],
            background_normal='',
            disabled=True,
            font_size='14sp'
        )
        self.stop_btn.bind(on_release=self.stop_scanning)
        
        controls.add_widget(self.start_btn)
        controls.add_widget(self.stop_btn)
        
        # Add widgets
        layout.add_widget(back_btn)
        layout.add_widget(self.header)
        layout.add_widget(self.camera_image)
        layout.add_widget(self.result_label)
        layout.add_widget(controls)
        
        self.add_widget(layout)
    
    def go_back(self, instance):
        self.stop_scanning(instance)
        self.manager.current = 'main'
    
    def toggle_scanning(self, instance):
        if not self.scanning:
            self.start_scanning()
        else:
            self.stop_scanning(instance)
    
    def start_scanning(self):
        self.scanning = True
        self.link_opened = False
        self.last_scanned_data = None
        self.start_btn.disabled = True
        self.stop_btn.disabled = False
        self.result_label.text = 'Scanning... Point camera at QR code'
        
        # Start camera in a separate thread
        threading.Thread(target=self.capture_frames, daemon=True).start()
    
    def stop_scanning(self, instance):
        self.scanning = False
        self.link_opened = False
        self.last_scanned_data = None
        self.start_btn.disabled = False
        self.stop_btn.disabled = True
        if self.cap:
            self.cap.release()
            self.cap = None
        self.result_label.text = 'Scanning stopped'
    
    def capture_frames(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            Clock.schedule_once(lambda dt: self.show_popup('Error', 'Cannot open camera!'))
            return
        
        detector = cv2.QRCodeDetector()
        
        while self.scanning and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # Flip frame horizontally
            frame = cv2.flip(frame, 1)
            
            # Detect QR code
            try:
                data, bbox, _ = detector.detectAndDecode(frame)
                
                if data and data != self.last_scanned_data:
                    self.last_scanned_data = data
                    Clock.schedule_once(lambda dt: self.update_result(data))
                    
                    # Open link only once if enabled
                    if self.open_link and data.startswith(('http://', 'https://')):
                        if not self.link_opened:
                            self.link_opened = True
                            Clock.schedule_once(lambda dt: webbrowser.open(data))
                            Clock.schedule_once(lambda dt: self.show_popup('Link Opened', f'Opening link in browser:\n{data[:50]}...'))
                    
                    # Draw bounding box
                    if bbox is not None:
                        bbox = bbox.astype(int)
                        for i in range(len(bbox[0])):
                            cv2.line(
                                frame,
                                tuple(bbox[0][i]),
                                tuple(bbox[0][(i + 1) % len(bbox[0])]),
                                (0, 255, 0),
                                2
                            )
                
                elif not data:
                    # Reset if no QR code is detected
                    self.last_scanned_data = None
                    
            except Exception as e:
                print(f"Error in QR detection: {e}")
            
            # Convert frame to texture
            try:
                # Resize frame to reduce processing
                frame_resized = cv2.resize(frame, (640, 480))
                buf = cv2.flip(frame_resized, 0).tobytes()
                texture = Texture.create(size=(frame_resized.shape[1], frame_resized.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                
                # Update image widget
                Clock.schedule_once(lambda dt: self.update_image(texture))
            except:
                pass
        
        if self.cap:
            self.cap.release()
    
    def update_image(self, texture):
        if self.camera_image:
            self.camera_image.texture = texture
    
    def update_result(self, data):
        if self.result_label:
            display_text = data[:60] + '...' if len(data) > 60 else data
            self.result_label.text = f'Scanned: {display_text}'
    
    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message))
        btn = Button(text='OK', size_hint=(1, None), height=dp(40))
        popup = Popup(title=title, content=content, size_hint=(0.8, 0.4))
        btn.bind(on_release=popup.dismiss)
        content.add_widget(btn)
        popup.open()

class ScanAndOpenScreen(ScanQRScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'scan_open'
        self.open_link = True
        self.header.text = 'Scan & Open Link'
        self.header.color = [0.1, 0.6, 0.9, 1]

class WhatsAppQRScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'whatsapp'
        
        layout = BoxLayout(orientation='vertical', padding=[20, 20, 20, 20], spacing=15)
        
        # Back button
        back_btn = Button(
            text='Back',
            size_hint=(None, None),
            size=(dp(70), dp(35)),
            background_color=[0.3, 0.3, 0.3, 1],
            background_normal=''
        )
        back_btn.bind(on_release=self.go_back)
        
        # Header
        header = Label(
            text='WhatsApp QR Code',
            font_size='24sp',
            bold=True,
            color=[0.4, 0.8, 0.4, 1],
            size_hint=(1, 0.1)
        )
        
        # Instruction
        instruction = Label(
            text='Enter phone number with country code\nExample: +919876543210',
            font_size='14sp',
            color=[0.4, 0.4, 0.4, 1],
            size_hint=(1, 0.1),
            halign='center'
        )
        instruction.bind(size=instruction.setter('text_size'))
        
        # Phone input
        self.phone_input = TextInput(
            hint_text='+919876543210',
            multiline=False,
            size_hint=(1, None),
            height=dp(45),
            padding=[10, 10],
            font_size='14sp'
        )
        
        # Generate button
        generate_btn = Button(
            text='Generate WhatsApp QR',
            background_color=[0.4, 0.8, 0.4, 1],
            size_hint=(1, None),
            height=dp(50),
            font_size='16sp',
            bold=True,
            background_normal=''
        )
        generate_btn.bind(on_release=self.generate_whatsapp_qr)
        
        # QR Code display area with smaller size
        self.qr_image = Image(
            size_hint=(0.5, 0.35),
            pos_hint={'center_x': 0.5},
            allow_stretch=True,
            keep_ratio=True
        )
        
        # WhatsApp Info
        info = Label(
            text='Scan the QR code with WhatsApp\non your mobile device',
            font_size='12sp',
            color=[0.5, 0.5, 0.5, 1],
            size_hint=(1, 0.1),
            halign='center'
        )
        info.bind(size=info.setter('text_size'))
        
        # Add widgets
        layout.add_widget(back_btn)
        layout.add_widget(header)
        layout.add_widget(instruction)
        layout.add_widget(self.phone_input)
        layout.add_widget(generate_btn)
        layout.add_widget(self.qr_image)
        layout.add_widget(info)
        
        self.add_widget(layout)
    
    def go_back(self, instance):
        self.manager.current = 'main'
    
    def generate_whatsapp_qr(self, instance):
        phone = self.phone_input.text.strip()
        
        if not phone:
            self.show_popup('Error', 'Please enter a phone number!')
            return
        
        # Validate phone number
        if not phone.startswith('+'):
            self.show_popup('Error', 'Please include country code (e.g., +91 for India)')
            return
        
        # Remove any non-digit characters except +
        cleaned_phone = ''.join(c for c in phone if c.isdigit() or c == '+')
        
        # Create WhatsApp link
        whatsapp_link = f'https://wa.me/{cleaned_phone[1:]}' if cleaned_phone.startswith('+') else f'https://wa.me/{cleaned_phone}'
        
        try:
            # Generate QR code with smaller size
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=6,
                border=2,
            )
            qr.add_data(whatsapp_link)
            qr.make(fit=True)
            
            # Create image with WhatsApp colors
            img = qr.make_image(fill_color="#25D366", back_color="white")
            
            # Save temporary file
            filename = f"whatsapp_qr_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            img.save(filename)
            
            # Update image widget
            self.qr_image.source = filename
            self.qr_image.reload()
            
            self.show_popup('Success', 
                          f'WhatsApp QR Code generated!\n\n'
                          f'Phone: {phone}\n'
                          f'Scan to start chatting!')
            
        except Exception as e:
            self.show_popup('Error', f'Failed to generate QR code: {str(e)}')
    
    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message))
        btn = Button(text='OK', size_hint=(1, None), height=dp(40))
        popup = Popup(title=title, content=content, size_hint=(0.8, 0.4))
        btn.bind(on_release=popup.dismiss)
        content.add_widget(btn)
        popup.open()

class QRBoostApp(App):
    def build(self):
        self.title = 'QRBoost'
        
        # Create screen manager
        sm = ScreenManager()
        
        # Add screens to manager
        sm.add_widget(MainScreen())
        sm.add_widget(GenerateQRScreen())
        sm.add_widget(ScanQRScreen())
        sm.add_widget(ScanAndOpenScreen())
        sm.add_widget(WhatsAppQRScreen())
        
        return sm
    
    def on_stop(self):
        # Clean up any temporary files
        import glob
        for file in glob.glob("qr_code_*.png") + glob.glob("whatsapp_qr_*.png"):
            try:
                os.remove(file)
            except:
                pass

if __name__ == '__main__':
    QRBoostApp().run()