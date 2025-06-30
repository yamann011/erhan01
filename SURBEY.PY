import tkinter as tk
from tkinter import ttk, messagebox
import sys
from datetime import datetime
from openpyxl import Workbook, load_workbook
import os
import json

class VisitorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Ziyaretçi Kayıt Sistemi")
        self.root.geometry("1250x800")
        self.root.configure(bg="#2c2c2c")
        
        # Pencereyi ekranın ortasına hizala
        self.center_window()
        
        # Tema değişkenleri
        self.is_dark_theme = True
        self.all_data = [] # Tüm ziyaretçi verilerini tutacak liste
        self.current_user_type = None  # "admin" veya "user"
        
        # Ziyaretçi Sayısı ile İlgili Değişkenler
        self.inside_visitors_count = 0 
        self.current_rgb_color_index = 0
        self.rgb_colors = ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF", "#4B0082", "#9400D3"] # Renk paleti
        self.count_label_main = None # Ana menüdeki etiket
        self.count_label_visitor = None # Ziyaretçi panelindeki etiket
        self.tree = None # Treeview widget'ını tutacak değişken (başlangıçta None)

        # Arama giriş alanları
        self.search_plate_entry = None
        self.search_name_surname_entry = None

        # Kullanıcı verilerini yükle
        self.load_users()
        
        # Ana giriş ekranını oluştur
        self.create_main_screen()
    
    def load_users(self):
        """Kullanıcı verilerini yükler"""
        self.users_file = "users.json"
        self.users = {
            "ADMIN": {"password": "admin123", "type": "admin"},
            "USER": {"password": "user123", "type": "user"}
        }
        
        # JSON dosyasından kullanıcıları yükle
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    self.users = json.load(f)
            except:
                pass # Hata durumunda varsayılan kullanıcıları kullanmaya devam et
    
    def save_users(self):
        """Kullanıcı verilerini kaydeder"""
        try:
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Hata", f"Kullanıcı verileri kaydedilemedi: {str(e)}")
        
    def center_window(self):
        """Pencereyi ekranın ortasına hizalar"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - 1250) // 2
        y = (self.root.winfo_screenheight() - 800) // 2
        self.root.geometry(f"1250x800+{x}+{y}")
    
    def create_main_screen(self):
        """Ana giriş ekranını oluşturur"""
        # Ana frame
        main_frame = tk.Frame(self.root, bg="#2c2c2c")
        main_frame.pack(fill="both", expand=True)
        
        # Başlık
        title_label = tk.Label(
            main_frame,
            text="ZİYARETÇİ KAYIT SİSTEMİ",
            font=("Arial", 36, "bold"),
            fg="orange",
            bg="#2c2c2c"
        )
        title_label.pack(pady=(150, 10)) 
        
        # İçerideki ziyaretçi sayısını gösteren etiket (Ana Menü)
        self.count_label_main = tk.Label(
            main_frame,
            text=f"İçerideki Ziyaretçi Sayısı: {self.inside_visitors_count}",
            font=("Arial", 20, "bold"),
            bg="#2c2c2c"
        )
        self.count_label_main.pack(pady=(10, 30))
        self.animate_count_label_color(self.count_label_main) # Sayı etiketinin rengini canlandırmaya başla
        
        # Alt başlık
        subtitle_label = tk.Label(
            main_frame,
            text="Lütfen giriş türünüzü seçiniz",
            font=("Arial", 16),
            fg="white",
            bg="#2c2c2c"
        )
        subtitle_label.pack(pady=(0, 50))
        
        # Buton frame
        button_frame = tk.Frame(main_frame, bg="#2c2c2c")
        button_frame.pack(pady=20)
        
        # Yönetici giriş butonu
        admin_btn = tk.Button(
            button_frame,
            text="YÖNETİCİ GİRİŞİ",
            font=("Arial", 18, "bold"),
            bg="orange",
            fg="white",
            width=20,
            height=3,
            command=self.show_admin_login,
            relief="flat",
            borderwidth=0
        )
        admin_btn.pack(side="left", padx=20)
        
        # Kullanıcı giriş butonu
        user_btn = tk.Button(
            button_frame,
            text="KULLANICI GİRİŞİ",
            font=("Arial", 18, "bold"),
            bg="orange",
            fg="white",
            width=20,
            height=3,
            command=self.show_user_login,
            relief="flat",
            borderwidth=0
        )
        user_btn.pack(side="left", padx=20)
        
        # Çıkış butonu
        exit_btn = tk.Button(
            main_frame,
            text="ÇIKIŞ",
            font=("Arial", 16, "bold"),
            bg="#cc7000",
            fg="white",
            width=25,
            height=2,
            command=self.root.quit,
            relief="flat",
            borderwidth=0
        )
        exit_btn.pack(pady=50)

        # Ana ekranda da sayıyı göstermek için veriyi yükle ve sayıyı güncelle
        self.load_data_for_count() 
        self.update_inside_visitors_count()
    
    def animate_count_label_color(self, label_widget):
        """Sayı etiketinin rengini canlandırır."""
        if label_widget.winfo_exists(): # Widget'ın hala var olup olmadığını kontrol et
            current_color = self.rgb_colors[self.current_rgb_color_index]
            label_widget.config(fg=current_color)
            self.current_rgb_color_index = (self.current_rgb_color_index + 1) % len(self.rgb_colors)
            self.root.after(500, lambda: self.animate_count_label_color(label_widget)) # Her 500ms'de rengi değiştir
        
    def show_admin_login(self):
        """Yönetici giriş formunu gösterir"""
        self.clear_window()
        self.create_login_form("YÖNETİCİ GİRİŞİ", self.admin_login)
    
    def show_user_login(self):
        """Kullanıcı giriş formunu gösterir"""
        self.clear_window()
        self.create_login_form("KULLANICI GİRİŞİ", self.user_login)
    
    def create_login_form(self, title, login_function):
        """Giriş formu oluşturur"""
        login_frame = tk.Frame(self.root, bg="#2c2c2c")
        login_frame.pack(fill="both", expand=True)
        
        # Başlık
        title_label = tk.Label(
            login_frame,
            text=title,
            font=("Arial", 28, "bold"),
            fg="orange",
            bg="#2c2c2c"
        )
        title_label.pack(pady=(100, 50))
        
        # Form frame
        form_frame = tk.Frame(login_frame, bg="#2c2c2c")
        form_frame.pack(pady=20)
        
        # Kullanıcı adı
        tk.Label(
            form_frame,
            text="KULLANICI ADI:",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#2c2c2c"
        ).grid(row=0, column=0, sticky="w", padx=10, pady=10)
        
        self.username_entry = tk.Entry(
            form_frame,
            font=("Arial", 14),
            width=30,
            bg="#4a4a4a",
            fg="white",
            insertbackground="white"
        )
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Şifre
        tk.Label(
            form_frame,
            text="ŞİFRE:",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#2c2c2c"
        ).grid(row=1, column=0, sticky="w", padx=10, pady=10)
        
        self.password_entry = tk.Entry(
            form_frame,
            font=("Arial", 14),
            width=30,
            bg="#4a4a4a",
            fg="white",
            insertbackground="white",
            show="*"
        )
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Buton frame
        btn_frame = tk.Frame(login_frame, bg="#2c2c2c")
        btn_frame.pack(pady=50)
        
        # Giriş butonu
        login_btn = tk.Button(
            btn_frame,
            text="GİRİŞ YAP",
            font=("Arial", 14, "bold"),
            bg="orange",
            fg="white",
            width=15,
            height=2,
            command=login_function,
            relief="flat"
        )
        login_btn.pack(side="left", padx=20)
        
        # Geri butonu
        back_btn = tk.Button(
            btn_frame,
            text="GERİ",
            font=("Arial", 14, "bold"),
            bg="#cc7000",
            fg="white",
            width=15,
            height=2,
            command=self.go_back,
            relief="flat"
        )
        back_btn.pack(side="left", padx=20)
        
        # Enter tuşu ile giriş
        self.password_entry.bind("<Return>", lambda event: login_function())
    
    def admin_login(self):
        """Yönetici girişini kontrol eder"""
        username = self.username_entry.get().strip().upper()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showwarning("Uyarı", "Lütfen tüm alanları doldurunuz!")
            return
        
        if username in self.users and self.users[username]["password"] == password and self.users[username]["type"] == "admin":
            self.current_user_type = "admin"
            messagebox.showinfo("Başarılı", "Yönetici girişi başarılı!")
            self.show_admin_panel()
        else:
            messagebox.showerror("Hata", "Kullanıcı adı veya şifre hatalı!")
            self.password_entry.delete(0, tk.END)
            self.username_entry.focus()
    
    def user_login(self):
        """Kullanıcı girişini kontrol eder"""
        username = self.username_entry.get().strip().upper()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showwarning("Uyarı", "Lütfen tüm alanları doldurunuz!")
            return
        
        if username in self.users and self.users[username]["password"] == password:
            self.current_user_type = self.users[username]["type"]
            messagebox.showinfo("Başarılı", "Kullanıcı girişi başarılı!")
            self.show_visitor_panel()
        else:
            messagebox.showerror("Hata", "Kullanıcı adı veya şifre hatalı!")
            self.password_entry.delete(0, tk.END)
            self.username_entry.focus()
    
    def show_admin_panel(self):
        """Yönetici panelini gösterir"""
        self.clear_window()
        self.create_admin_panel()
    
    def create_admin_panel(self):
        """Yönetici panelini oluşturur"""
        # Başlık
        title_label = tk.Label(
            self.root,
            text="YÖNETİCİ PANELİ",
            font=("Arial", 28, "bold"),
            fg="orange",
            bg="#2c2c2c"
        )
        title_label.pack(pady=(50, 30))
        
        # Ana frame
        main_frame = tk.Frame(self.root, bg="#2c2c2c")
        main_frame.pack(fill="both", expand=True, padx=50, pady=20)
        
        # Sol panel - Butonlar
        left_frame = tk.Frame(main_frame, bg="#2c2c2c", width=300)
        left_frame.pack(side="left", fill="y", padx=(0, 30))
        left_frame.pack_propagate(False)
        
        # Butonlar
        buttons = [
            ("ZİYARETÇİ PANELİ", self.show_visitor_panel),
            ("YENİ KULLANICI EKLE", self.show_add_user_form),
            ("ŞİFRE SIFIRLA", self.show_reset_password_form),
            ("KULLANICI LİSTESİ", self.show_user_list),
            ("ANA MENÜ", self.go_back)
        ]
        
        for i, (text, command) in enumerate(buttons):
            btn = tk.Button(
                left_frame,
                text=text,
                font=("Arial", 14, "bold"),
                bg="orange",
                fg="white",
                width=25,
                height=3,
                command=command,
                relief="flat"
            )
            btn.pack(pady=10, fill="x")
        
        # Sağ panel - İçerik alanı
        self.admin_content_frame = tk.Frame(main_frame, bg="#2c2c2c")
        self.admin_content_frame.pack(side="right", fill="both", expand=True)
        
        # Hoş geldin mesajı
        welcome_label = tk.Label(
            self.admin_content_frame,
            text="Hoş Geldiniz!\n\nSol menüden yapmak istediğiniz işlemi seçiniz.",
            font=("Arial", 16),
            fg="white",
            bg="#2c2c2c",
            justify="center"
        )
        welcome_label.pack(expand=True)
    
    def show_add_user_form(self):
        """Yeni kullanıcı ekleme formunu gösterir"""
        # İçerik alanını temizle
        for widget in self.admin_content_frame.winfo_children():
            widget.destroy()
        
        # Form başlığı
        title = tk.Label(
            self.admin_content_frame,
            text="YENİ KULLANICI EKLE",
            font=("Arial", 20, "bold"),
            fg="orange",
            bg="#2c2c2c"
        )
        title.pack(pady=20)
        
        # Form frame
        form_frame = tk.Frame(self.admin_content_frame, bg="#2c2c2c")
        form_frame.pack(pady=20)
        
        # Kullanıcı adı
        tk.Label(form_frame, text="KULLANICI ADI:", font=("Arial", 12, "bold"), 
                fg="white", bg="#2c2c2c").grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.new_username = tk.Entry(form_frame, font=("Arial", 14), width=25, 
                                   bg="#4a4a4a", fg="white", insertbackground="white")
        self.new_username.grid(row=0, column=1, padx=10, pady=10)
        
        # Şifre
        tk.Label(form_frame, text="ŞİFRE:", font=("Arial", 12, "bold"), 
                fg="white", bg="#2c2c2c").grid(row=1, column=0, sticky="w", padx=10, pady=10)
        self.new_password = tk.Entry(form_frame, font=("Arial", 14), width=25, 
                                   bg="#4a4a4a", fg="white", insertbackground="white")
        self.new_password.grid(row=1, column=1, padx=10, pady=10)
        
        # Kullanıcı türü
        tk.Label(form_frame, text="KULLANICI TÜRÜ:", font=("Arial", 12, "bold"), 
                fg="white", bg="#2c2c2c").grid(row=2, column=0, sticky="w", padx=10, pady=10)
        self.user_type_var = tk.StringVar(value="user")
        type_frame = tk.Frame(form_frame, bg="#2c2c2c")
        type_frame.grid(row=2, column=1, sticky="w", padx=10, pady=10)
        
        tk.Radiobutton(type_frame, text="Kullanıcı", variable=self.user_type_var, value="user",
                      bg="#2c2c2c", fg="white", selectcolor="#4a4a4a").pack(side="left")
        tk.Radiobutton(type_frame, text="Yönetici", variable=self.user_type_var, value="admin",
                      bg="#2c2c2c", fg="white", selectcolor="#4a4a4a").pack(side="left", padx=(20,0))
        
        # Butonlar
        btn_frame = tk.Frame(self.admin_content_frame, bg="#2c2c2c")
        btn_frame.pack(pady=30)
        
        tk.Button(btn_frame, text="EKLE", font=("Arial", 14, "bold"), bg="orange", fg="white",
                 width=15, height=2, command=self.add_new_user, relief="flat").pack(side="left", padx=10)
        tk.Button(btn_frame, text="TEMİZLE", font=("Arial", 14, "bold"), bg="#cc7000", fg="white",
                 width=15, height=2, command=self.clear_add_user_form, relief="flat").pack(side="left", padx=10)
    
    def add_new_user(self):
        """Yeni kullanıcı ekler"""
        username = self.new_username.get().strip().upper()
        password = self.new_password.get().strip()
        user_type = self.user_type_var.get()
        
        if not username or not password:
            messagebox.showwarning("Uyarı", "Lütfen tüm alanları doldurunuz!")
            return
        
        if username in self.users:
            messagebox.showerror("Hata", "Bu kullanıcı adı zaten mevcut!")
            return
        
        # Kullanıcıyı ekle
        self.users[username] = {"password": password, "type": user_type}
        self.save_users()
        
        messagebox.showinfo("Başarılı", f"Kullanıcı '{username}' başarıyla eklendi!")
        self.clear_add_user_form()
    
    def clear_add_user_form(self):
        """Kullanıcı ekleme formunu temizler"""
        self.new_username.delete(0, tk.END)
        self.new_password.delete(0, tk.END)
        self.user_type_var.set("user")
    
    def show_reset_password_form(self):
        """Şifre sıfırlama formunu gösterir"""
        # İçerik alanını temizle
        for widget in self.admin_content_frame.winfo_children():
            widget.destroy()
        
        # Form başlığı
        title = tk.Label(
            self.admin_content_frame,
            text="ŞİFRE SIFIRLA",
            font=("Arial", 20, "bold"),
            fg="orange",
            bg="#2c2c2c"
        )
        title.pack(pady=20)
        
        # Form frame
        form_frame = tk.Frame(self.admin_content_frame, bg="#2c2c2c")
        form_frame.pack(pady=20)
        
        # Kullanıcı seçimi
        tk.Label(form_frame, text="KULLANICI:", font=("Arial", 12, "bold"), 
                fg="white", bg="#2c2c2c").grid(row=0, column=0, sticky="w", padx=10, pady=10)
        
        self.reset_user_var = tk.StringVar()
        user_combo = ttk.Combobox(form_frame, textvariable=self.reset_user_var, 
                                 values=list(self.users.keys()), state="readonly", width=22)
        user_combo.grid(row=0, column=1, padx=10, pady=10)
        
        # Yeni şifre
        tk.Label(form_frame, text="YENİ ŞİFRE:", font=("Arial", 12, "bold"), 
                fg="white", bg="#2c2c2c").grid(row=1, column=0, sticky="w", padx=10, pady=10)
        self.reset_new_password = tk.Entry(form_frame, font=("Arial", 14), width=25, 
                                         bg="#4a4a4a", fg="white", insertbackground="white")
        self.reset_new_password.grid(row=1, column=1, padx=10, pady=10)
        
        # Butonlar
        btn_frame = tk.Frame(self.admin_content_frame, bg="#2c2c2c")
        btn_frame.pack(pady=30)
        
        tk.Button(btn_frame, text="ŞİFRE SIFIRLA", font=("Arial", 14, "bold"), bg="orange", fg="white",
                 width=15, height=2, command=self.reset_user_password, relief="flat").pack(side="left", padx=10)
        tk.Button(btn_frame, text="TEMİZLE", font=("Arial", 14, "bold"), bg="#cc7000", fg="white",
                 width=15, height=2, command=self.clear_reset_form, relief="flat").pack(side="left", padx=10)
    
    def reset_user_password(self):
        """Kullanıcı şifresini sıfırlar"""
        username = self.reset_user_var.get().strip()
        new_password = self.reset_new_password.get().strip()
        
        if not username or not new_password:
            messagebox.showwarning("Uyarı", "Lütfen tüm alanları doldurunuz!")
            return
        
        if username not in self.users:
            messagebox.showerror("Hata", "Kullanıcı bulunamadı!")
            return
        
        # Şifreyi güncelle
        self.users[username]["password"] = new_password
        self.save_users()
        
        messagebox.showinfo("Başarılı", f"'{username}' kullanıcısının şifresi başarıyla sıfırlandı!")
        self.clear_reset_form()
    
    def clear_reset_form(self):
        """Şifre sıfırlama formunu temizler"""
        self.reset_user_var.set("")
        self.reset_new_password.delete(0, tk.END)
    
    def show_user_list(self):
        """Kullanıcı listesini gösterir"""
        # İçerik alanını temizle
        for widget in self.admin_content_frame.winfo_children():
            widget.destroy()
        
        # Başlık
        title = tk.Label(
            self.admin_content_frame,
            text="KULLANICI LİSTESİ",
            font=("Arial", 20, "bold"),
            fg="orange",
            bg="#2c2c2c"
        )
        title.pack(pady=20)
        
        # Tablo frame
        table_frame = tk.Frame(self.admin_content_frame, bg="#2c2c2c")
        table_frame.pack(fill="both", expand=True, padx=20)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Kullanıcı tablosu
        columns = ["Kullanıcı Adı", "Tür"]
        self.user_tree = ttk.Treeview(table_frame, columns=columns, show="headings", 
                                     yscrollcommand=scrollbar.set, height=10)
        
        for col in columns:
            self.user_tree.heading(col, text=col)
            self.user_tree.column(col, width=200, minwidth=150)
        
        self.user_tree.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.user_tree.yview)
        
        # Kullanıcıları listele
        for username, user_data in self.users.items():
            user_type = "Yönetici" if user_data["type"] == "admin" else "Kullanıcı"
            self.user_tree.insert("", "end", values=[username, user_type])
        
        # Silme butonu
        delete_btn = tk.Button(
            self.admin_content_frame,
            text="SEÇİLİ KULLANICIYI SİL",
            font=("Arial", 14, "bold"),
            bg="#cc0000",
            fg="white",
            width=25,
            height=2,
            command=self.delete_selected_user,
            relief="flat"
        )
        delete_btn.pack(pady=20)
    
    def delete_selected_user(self):
        """Seçili kullanıcıyı siler"""
        selection = self.user_tree.selection()
        if not selection:
            messagebox.showwarning("Uyarı", "Lütfen silinecek kullanıcıyı seçiniz!")
            return
        
        username = self.user_tree.item(selection[0], "values")[0]
        
        if username == "ADMIN":
            messagebox.showerror("Hata", "Ana yönetici hesabı silinemez!")
            return
        
        if messagebox.askyesno("Onay", f"'{username}' kullanıcısını silmek istediğinizden emin misiniz?"):
            del self.users[username]
            self.save_users()
            self.user_tree.delete(selection[0])
            messagebox.showinfo("Başarılı", f"Kullanıcı '{username}' başarıyla silindi!")
    
    def show_visitor_panel(self):
        """Ana ziyaretçi panelini gösterir"""
        self.clear_window()
        self.create_visitor_panel()
    
    def create_visitor_panel(self):
        """Ziyaretçi kayıt panelini oluşturur"""
        # Ana başlık
        title_label = tk.Label(
            self.root,
            text="ZİYARETÇİ KAYIT PANELİ",
            font=("Arial", 24, "bold"),
            fg="orange",
            bg="#2c2c2c"
        )
        title_label.pack(pady=10)
        
        # İçerideki ziyaretçi sayısını gösteren etiket (Ziyaretçi Paneli)
        self.count_label_visitor = tk.Label(
            self.root,
            text=f"İçerideki Ziyaretçi Sayısı: {self.inside_visitors_count}",
            font=("Arial", 16, "bold"),
            bg="#2c2c2c"
        )
        self.count_label_visitor.pack(pady=(0, 10))
        self.animate_count_label_color(self.count_label_visitor) # Sayı etiketinin rengini canlandırmaya başla

        # Ana frame
        main_frame = tk.Frame(self.root, bg="#2c2c2c")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Sol panel - Form
        left_frame = tk.Frame(main_frame, bg="#2c2c2c", width=400)
        left_frame.pack(side="left", fill="y", padx=(0, 20))
        left_frame.pack_propagate(False)
        
        # Form alanları
        self.create_form_fields(left_frame)
        
        # Sağ panel - Tablo ve Arama
        right_panel_container = tk.Frame(main_frame, bg="#2c2c2c")
        right_panel_container.pack(side="right", fill="both", expand=True)

        # Arama alanı
        self.create_search_section(right_panel_container)
        
        # Tablo
        self.create_table(right_panel_container)
        
        # Butonlar
        self.create_buttons(left_frame)
        
        # Excel'den verileri yükle
        self.load_data_from_excel() # Bu, self.tree ve self.all_data'yı dolduracaktır
        self.update_inside_visitors_count() # Yükleme sonrası sayıyı güncelle
    
    def create_search_section(self, parent):
        """Ziyaretçi paneline arama bölümünü ekler."""
        search_frame = tk.Frame(parent, bg="#3c3c3c", bd=2, relief="groove")
        search_frame.pack(pady=10, padx=10, fill="x")

        # Plaka Arama
        tk.Label(search_frame, text="Plaka Ara:", font=("Arial", 10, "bold"), fg="white", bg="#3c3c3c").pack(side="left", padx=5, pady=5)
        self.search_plate_entry = tk.Entry(search_frame, font=("Arial", 10), width=15, bg="#5a5a5a", fg="white", insertbackground="white")
        self.search_plate_entry.pack(side="left", padx=5, pady=5)
        self.search_plate_entry.bind("<Return>", lambda event: self.search_records())

        # İsim Soyisim Arama
        tk.Label(search_frame, text="İsim/Soyisim Ara:", font=("Arial", 10, "bold"), fg="white", bg="#3c3c3c").pack(side="left", padx=10, pady=5)
        self.search_name_surname_entry = tk.Entry(search_frame, font=("Arial", 10), width=20, bg="#5a5a5a", fg="white", insertbackground="white")
        self.search_name_surname_entry.pack(side="left", padx=5, pady=5)
        self.search_name_surname_entry.bind("<Return>", lambda event: self.search_records())
        
        # Ara Butonu
        search_btn = tk.Button(search_frame, text="ARA", font=("Arial", 10, "bold"), bg="orange", fg="white", command=self.search_records, relief="flat")
        search_btn.pack(side="left", padx=10, pady=5)

        # Temizle Butonu
        clear_search_btn = tk.Button(search_frame, text="TEMİZLE", font=("Arial", 10, "bold"), bg="#cc7000", fg="white", command=self.clear_search, relief="flat")
        clear_search_btn.pack(side="left", padx=5, pady=5)

    def search_records(self):
        """Plaka veya İsim/Soyisim'e göre kayıtları arar ve tabloyu günceller."""
        plate_query = self.search_plate_entry.get().strip().upper()
        name_surname_query = self.search_name_surname_entry.get().strip().upper()

        # Tabloyu temizle
        for item in self.tree.get_children():
            self.tree.delete(item)

        found_records = []
        for record in self.all_data:
            # Her satırın beklenen uzunlukta olduğundan emin ol
            # İSİM (0), SOYİSİM (1), PLAKA (3)
            record_plate = str(record[3]).strip().upper() if len(record) > 3 else ""
            record_name = str(record[0]).strip().upper() if len(record) > 0 else ""
            record_surname = str(record[1]).strip().upper() if len(record) > 1 else ""
            
            plate_match = (not plate_query) or (plate_query in record_plate)
            name_surname_match = (not name_surname_query) or \
                                 (name_surname_query in record_name) or \
                                 (name_surname_query in record_surname) or \
                                 (name_surname_query in f"{record_name} {record_surname}".strip())
            
            if plate_match and name_surname_match:
                found_records.append(record)
                self.tree.insert("", "end", values=record)

        if not found_records and (plate_query or name_surname_query):
            messagebox.showinfo("Bilgi", "Arama kriterlerine uygun kayıt bulunamadı.")

    def clear_search(self):
        """Arama alanlarını temizler ve tabloyu tüm verilerle yeniden doldurur."""
        self.search_plate_entry.delete(0, tk.END)
        self.search_name_surname_entry.delete(0, tk.END)
        self.load_data_from_excel() # Tüm verileri yeniden yükle
        
    def create_form_fields(self, parent):
        """Form alanlarını oluşturur"""
        self.entries = {}
        
        # Form container frame
        form_container = tk.Frame(parent, bg="#2c2c2c")
        form_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        fields = [
            "İSİM", "SOYİSİM", "FİRMA", "PLAKA", "GELİŞ NEDENİ",
            "KİME GELDİ", "GİRİŞ SAATİ", "ÇIKIŞ SAATİ", "TARİH",
            "KAYIT YAPAN P.", "AÇIKLAMA"
        ]
        
        for i, field in enumerate(fields):
            # Label
            label = tk.Label(
                form_container,
                text=f"{field}:",
                font=("Arial", 11, "bold"),
                fg="white",
                bg="#2c2c2c",
                anchor="w",
                width=15
            )
            label.grid(row=i, column=0, sticky="w", padx=(5, 10), pady=5)
            
            # Entry - daha geniş input alanları
            entry = tk.Entry(
                form_container,
                font=("Arial", 11),
                width=30,
                bg="#4a4a4a",
                fg="white",
                insertbackground="white",
                relief="solid",
                bd=1
            )
            entry.grid(row=i, column=1, sticky="ew", padx=(0, 5), pady=5)
            self.entries[field] = entry
            
            # Özel alanlar için otomatik büyük harf
            if field in ["İSİM", "SOYİSİM", "FİRMA", "PLAKA", "KAYIT YAPAN P."]:
                entry.bind("<KeyRelease>", lambda event, e=entry: self.to_uppercase(e))
        
        # Grid column configure
        form_container.grid_columnconfigure(1, weight=1)
        
        # İsim alanına değişiklik olduğunda tarih ve saat doldur
        self.entries["İSİM"].bind("<KeyRelease>", self.fill_date_time)
    
    def to_uppercase(self, entry):
        """Text entry'deki metni büyük harfe çevirir"""
        current_pos = entry.index(tk.INSERT)
        current_text = entry.get()
        entry.delete(0, tk.END)
        entry.insert(0, current_text.upper())
        entry.icursor(current_pos)
    
    def create_table(self, parent):
        """Tabloyu oluşturur"""
        # Tablo frame
        table_frame = tk.Frame(parent, bg="#2c2c2c")
        table_frame.pack(fill="both", expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Treeview (tablo)
        columns = [
            "İSİM", "SOYİSİM", "FİRMA", "PLAKA", "GELİŞ NEDENİ",
            "KİME GELDİ", "GİRİŞ SAATİ", "ÇIKIŞ SAATİ", "TARİH",
            "KAYIT YAPAN P.", "AÇIKLAMA"
        ]
        
        self.tree = ttk.Treeview( # self.tree burada atanır
            table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set,
            height=15
        )
        
        # Sütun başlıkları ve genişlikler
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, minwidth=80)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.tree.yview)
        
        # Tablo satırına tıklama olayı
        self.tree.bind("<ButtonRelease-1>", self.on_table_select)
        
        # Stil ayarları
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#4a4a4a", foreground="white")
        style.configure("Treeview.Heading", background="orange", foreground="white")
    
    def create_buttons(self, parent):
        """Butonları oluşturur"""
        # Buton container frame
        btn_container = tk.Frame(parent, bg="#2c2c2c")
        btn_container.pack(fill="x", padx=10, pady=20)
        
        # İlk satır butonları
        first_row = tk.Frame(btn_container, bg="#2c2c2c")
        first_row.pack(fill="x", pady=5)
        
        buttons_row1 = [
            ("TEMİZLE", self.clear_inputs),
            ("KAYDET", self.save_to_excel),
            ("SİL", self.delete_selected_row)
        ]
        
        for text, command in buttons_row1:
            btn = tk.Button(
                first_row,
                text=text,
                font=("Arial", 11, "bold"),
                bg="orange",
                fg="white",
                width=12,
                height=2,
                command=command,
                relief="flat"
            )
            btn.pack(side="left", padx=3, fill="x", expand=True)
        
        # İkinci satır butonları
        second_row = tk.Frame(btn_container, bg="#2c2c2c")
        second_row.pack(fill="x", pady=5)
        
        buttons_row2 = [
            ("DÜZELT", self.edit_selected_row),
            ("ÇIKIŞ EKLE", self.add_exit_time),
            ("ANA MENÜ", self.go_back)
        ]
        
        for text, command in buttons_row2:
            btn = tk.Button(
                second_row,
                text=text,
                font=("Arial", 11, "bold"),
                bg="orange" if text != "ANA MENÜ" else "#cc7000",
                fg="white",
                width=12,
                height=2,
                command=command,
                relief="flat"
            )
            btn.pack(side="left", padx=3, fill="x", expand=True)
    
    def fill_date_time(self, event=None):
        """İsim girildiğinde tarih ve saati otomatik doldurur"""
        if self.entries["İSİM"].get().strip():
            now = datetime.now()
            if not self.entries["TARİH"].get():
                self.entries["TARİH"].delete(0, tk.END)
                self.entries["TARİH"].insert(0, now.strftime("%d.%m.%Y"))
            if not self.entries["GİRİŞ SAATİ"].get():
                self.entries["GİRİŞ SAATİ"].delete(0, tk.END)
                self.entries["GİRİŞ SAATİ"].insert(0, now.strftime("%H:%M"))
    
    def clear_inputs(self):
        """Tüm giriş alanlarını temizler"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
    
    def save_to_excel(self):
        """Veriyi Excel'e kaydeder"""
        # Tüm alanların dolu olup olmadığını kontrol et
        required_fields = ["İSİM", "SOYİSİM", "FİRMA", "PLAKA"]
        for field in required_fields:
            if not self.entries[field].get().strip():
                messagebox.showwarning("Uyarı", f"Lütfen {field} alanını doldurunuz!")
                self.entries[field].focus()
                return
        
        # Veriyi topla
        data = []
        for field in ["İSİM", "SOYİSİM", "FİRMA", "PLAKA", "GELİŞ NEDENİ",
                     "KİME GELDİ", "GİRİŞ SAATİ", "ÇIKIŞ SAATİ", "TARİH",
                     "KAYIT YAPAN P.", "AÇIKLAMA"]:
            val = self.entries[field].get().strip().upper()
            data.append(val if val else "") # Eğer val boşsa (None veya boş string) Excel'e "" olarak kaydedilir.
        
        # Excel'e kaydet
        try:
            if os.path.exists("ziyaretci_kayitlari.xlsx"):
                wb = load_workbook("ziyaretci_kayitlari.xlsx")
                ws = wb.active
            else:
                wb = Workbook()
                ws = wb.active
                # Başlık satırı
                headers = ["İSİM", "SOYİSİM", "FİRMA", "PLAKA", "GELİŞ NEDENİ",
                          "KİME GELDİ", "GİRİŞ SAATİ", "ÇIKIŞ SAATİ", "TARİH",
                          "KAYIT YAPAN P.", "AÇIKLAMA"]
                ws.append(headers)
            
            ws.append(data)
            wb.save("ziyaretci_kayitlari.xlsx")
            messagebox.showinfo("Başarılı", "Kayıt başarıyla kaydedildi!")
            self.clear_inputs()
            self.load_data_from_excel() # Veriyi yeniden yükle (tablo ve all_data güncellenir)
            self.update_inside_visitors_count() # Kayıt sonrası içerideki ziyaretçi sayısını güncelle
            
        except Exception as e:
            messagebox.showerror("Hata", f"Kayıt sırasında hata oluştu: {str(e)}")

    def load_data_for_count(self):
        """Excel dosyasından sadece sayı saymak için verileri yükler (Treeview'a ihtiyaç duymadan)."""
        try:
            if os.path.exists("ziyaretci_kayitlari.xlsx"):
                wb = load_workbook("ziyaretci_kayitlari.xlsx")
                ws = wb.active
                self.all_data = []
                for row in ws.iter_rows(min_row=2, values_only=True):
                    if any(cell for cell in row):  # Boş satırları atla
                        # None değerlerini "" olarak çevir ki sayım doğru olsun
                        self.all_data.append([str(cell) if cell is not None else "" for cell in row]) 
            else:
                self.all_data = [] # Dosya yoksa boş liste
        except Exception as e:
            # Bu hata uygulamanın başlangıcını engellemez, sadece konsola yazdırılır
            print(f"Sayı için veri yüklenirken hata: {e}") 

    def load_data_from_excel(self):
        """Excel dosyasından verileri yükler ve tabloya ekler."""
        # Treeview henüz oluşturulmadıysa sadece sayım için veriyi yükle
        if self.tree is None: 
            self.load_data_for_count() 
            return

        try:
            if os.path.exists("ziyaretci_kayitlari.xlsx"):
                wb = load_workbook("ziyaretci_kayitlari.xlsx")
                ws = wb.active
                
                # Mevcut verileri temizle
                for item in self.tree.get_children():
                    self.tree.delete(item)
                
                self.all_data = [] # all_data'yı sıfırla

                # Verileri yükle (başlık satırını atla)
                for row_data in ws.iter_rows(min_row=2, values_only=True):
                    if any(cell for cell in row_data):  # Boş satırları atla
                        # Excel'den gelen None değerlerini "" olarak çevir (görüntüleme ve tutarlılık için)
                        processed_row = [str(cell) if cell is not None else "" for cell in row_data]
                        self.all_data.append(processed_row)
                        # Tabloya ekle
                        self.tree.insert("", "end", values=processed_row)
                self.update_inside_visitors_count() # Yükleme sonrası içerideki ziyaretçi sayısını güncelle
                        
        except Exception as e:
            messagebox.showerror("Hata", f"Excel dosyası yüklenirken hata oluştu: {str(e)}")
    
    def update_inside_visitors_count(self):
        """İçerideki ziyaretçi sayısını günceller"""
        count = 0
        for row in self.all_data:
            # ÇIKIŞ SAATİ sütunu (index 7) boşsa, ziyaretçi içeridedir
            # Index 7'ye erişmeden önce satırın yeterli sütun içerdiğinden emin ol
            if len(row) > 7 and str(row[7]).strip() == "": # Boş stringleri de kontrol et
                count += 1
        self.inside_visitors_count = count
        
        # Etiketler var ve görünürse güncelle
        if self.count_label_main and self.count_label_main.winfo_exists():
            self.count_label_main.config(text=f"İçerideki Ziyaretçi Sayısı: {self.inside_visitors_count}")
        if self.count_label_visitor and self.count_label_visitor.winfo_exists():
            self.count_label_visitor.config(text=f"İçerideki Ziyaretçi Sayısı: {self.inside_visitors_count}")
        
    def on_table_select(self, event):
        """Tablo satırına tıklandığında input alanlarını doldurur"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            values = self.tree.item(item, "values")
            
            fields = ["İSİM", "SOYİSİM", "FİRMA", "PLAKA", "GELİŞ NEDENİ",
                     "KİME GELDİ", "GİRİŞ SAATİ", "ÇIKIŞ SAATİ", "TARİH",
                     "KAYIT YAPAN P.", "AÇIKLAMA"]
            
            for i, field in enumerate(fields):
                if i < len(values):
                    self.entries[field].delete(0, tk.END)
                    self.entries[field].insert(0, str(values[i])) # None değil, boş string olmalı
    
    def delete_selected_row(self):
        """Seçili satırı siler"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Uyarı", "Lütfen silinecek kaydı seçiniz!")
            return
        
        if messagebox.askyesno("Onay", "Seçili kaydı silmek istediğinizden emin misiniz?"):
            # Seçili öğenin index'ini al (all_data'dan silmek için)
            item_id = selection[0]
            item_index = self.tree.index(item_id)
            
            # Tablodan sil
            self.tree.delete(item_id)
            self.clear_inputs()
            
            # all_data listesinden sil
            if 0 <= item_index < len(self.all_data):
                del self.all_data[item_index]

            # Excel'i güncelle
            self.update_excel()
            self.update_inside_visitors_count() # Silme sonrası içerideki ziyaretçi sayısını güncelle
    
    def edit_selected_row(self):
        """Seçili satırı düzenler"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Uyarı", "Lütfen düzenlenecek kaydı seçiniz!")
            return
        
        # Formdan yeni değerleri al
        new_values = []
        for field in ["İSİM", "SOYİSİM", "FİRMA", "PLAKA", "GELİŞ NEDENİ",
                     "KİME GELDİ", "GİRİŞ SAATİ", "ÇIKIŞ SAATİ", "TARİH",
                     "KAYIT YAPAN P.", "AÇIKLAMA"]:
            val = self.entries[field].get().strip().upper()
            new_values.append(val if val else "") # Eğer val boşsa (None veya boş string) "" olarak kaydedilir.
        
        # Seçili öğenin index'ini al (all_data'yı güncellemek için)
        item_id = selection[0]
        item_index = self.tree.index(item_id)

        # Tabloyu güncelle
        self.tree.item(item_id, values=new_values)
        self.clear_inputs()
        
        # all_data listesini güncelle
        if 0 <= item_index < len(self.all_data):
            self.all_data[item_index] = new_values

        # Excel'i güncelle
        self.update_excel()
        self.update_inside_visitors_count() # Düzenleme sonrası içerideki ziyaretçi sayısını güncelle
        messagebox.showinfo("Başarılı", "Kayıt başarıyla güncellendi!")
    
    def add_exit_time(self):
        """Seçili kayda çıkış saati ekler"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Uyarı", "Lütfen çıkış saati eklenecek kaydı seçiniz!")
            return
        
        item_id = selection[0]
        item_index = self.tree.index(item_id)

        # Mevcut değerleri all_data'dan al (en güncel hali)
        values_from_all_data = list(self.all_data[item_index])
        
        # Çıkış saati zaten eklenmiş mi kontrol et
        if len(values_from_all_data) > 7 and str(values_from_all_data[7]).strip() != "":
            messagebox.showinfo("Bilgi", "Bu kaydın çıkış saati zaten eklenmiş.")
            return

        # Çıkış saatini güncelle
        # Liste index 7'ye kadar yeterli uzunlukta değilse genişlet
        while len(values_from_all_data) <= 7: 
            values_from_all_data.append("")
        values_from_all_data[7] = datetime.now().strftime("%H:%M")  # ÇIKIŞ SAATİ
        
        # Tabloyu güncelle
        self.tree.item(item_id, values=values_from_all_data)
        self.clear_inputs()

        # all_data listesini güncelle
        self.all_data[item_index] = values_from_all_data
            
        # Excel'i güncelle
        self.update_excel()
        self.update_inside_visitors_count() # Çıkış saati ekleme sonrası içerideki ziyaretçi sayısını güncelle
        messagebox.showinfo("Başarılı", "Çıkış saati başarıyla eklendi!")
    
    def update_excel(self):
        """Excel dosyasını all_data'daki verilerle günceller"""
        try:
            wb = Workbook()
            ws = wb.active
            
            # Başlık satırı
            headers = ["İSİM", "SOYİSİM", "FİRMA", "PLAKA", "GELİŞ NEDENİ",
                      "KİME GELDİ", "GİRİŞ SAATİ", "ÇIKIŞ SAATİ", "TARİH",
                      "KAYIT YAPAN P.", "AÇIKLAMA"]
            ws.append(headers)
            
            # all_data listesindeki verileri Excel'e ekle
            for row_values in self.all_data: 
                # Tüm değerlerin string veya boş string olduğundan emin ol
                processed_row = [str(cell) if cell is not None else "" for cell in row_values]
                ws.append(processed_row)
            
            wb.save("ziyaretci_kayitlari.xlsx")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Excel güncellenirken hata oluştu: {str(e)}")
    
    def clear_window(self):
        """Pencereyi temizler"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def go_back(self):
        """Ana menüye geri döner"""
        self.clear_window()
        self.create_main_screen()
    
    def run(self):
        """Uygulamayı başlatır"""
        self.root.mainloop()

if __name__ == "__main__":
    app = VisitorApp()
    app.run()
