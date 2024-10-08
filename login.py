import tkinter as tk
from tkinter import messagebox
import csv
import os


def load_users_from_csv(file_path):
    users = {}
    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                users[row["username"]] = {"password": row["password"], "role": row["role"]}
    except Exception as e:
        messagebox.showerror("Error", f"Error reading file: {e}")
    return users


def save_user_to_csv(file_path, username, password, role):
    try:
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username, password, role])
            print(f"User {username} added to CSV.")
    except Exception as e:
        messagebox.showerror("Error", f"Error writing to file: {e}")

# Nạp dữ liệu người dùng từ file CSV
users_file = "users.csv"  # Đảm bảo file này tồn tại
if not os.path.exists(users_file):
    with open(users_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["username", "password", "role"])  # Thêm tiêu đề nếu file chưa tồn tại

users = load_users_from_csv(users_file)
print(users)  # In ra danh sách người dùng để kiểm tra

# Khởi tạo cửa sổ chính
root = tk.Tk()
root.title("Cửa Hàng Trực Tuyến")
root.geometry("400x500")

# Hàm xử lý hiển thị thông báo chức năng
def show_message(function_name):
    messagebox.showinfo("Thông báo", f"Chức năng '{function_name}' đang được phát triển")

# Khung đăng nhập
def login_screen():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Tên người dùng:").pack(pady=10)
    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)
    
    tk.Label(root, text="Mật khẩu:").pack(pady=5)
    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=5)
    
    def login():
        username = username_entry.get()
        password = password_entry.get()
        
        user = users.get(username)
        if user and user["password"] == password:
            messagebox.showinfo("Thông báo", "Đăng nhập thành công!")
            if user["role"] == "admin":
                admin_screen()
            else:
                customer_screen()
        else:
            messagebox.showerror("Lỗi", "Tên người dùng hoặc mật khẩu không chính xác!")

    tk.Button(root, text="Đăng nhập", command=login).pack(pady=20)

# Giao diện chức năng khách hàng
def customer_screen():
    for widget in root.winfo_children():
        widget.destroy()
    
    tk.Label(root, text="Chức năng Khách hàng", font=("Arial", 14, "bold")).pack(pady=10)
    functions_khach_hang = [
        "Quản lý thông tin cá nhân", 
        "Tìm kiếm sản phẩm",
        "Giỏ hàng",
        "Đơn hàng",
        "Trạng thái đơn hàng"

    ]
    for func in functions_khach_hang:
        btn = tk.Button(root, text=func, width=30, command=lambda f=func: show_message(f))
        btn.pack(pady=5)
    
    tk.Button(root, text="Đăng xuất", command=login_screen, fg="red").pack(pady=20)

# Giao diện chức năng Admin
def admin_screen():
    for widget in root.winfo_children():
        widget.destroy()
    
    tk.Label(root, text="Chức năng Admin", font=("Arial", 14, "bold")).pack(pady=10)
    functions_nhan_vien = [
        "Quản lý Kho hàng",  
        "Quản lý sản phẩm",
        "Quản lý sale",
        "Quản lý khách hàng",
        "Thêm tài khoản" 
    ]
    for func in functions_nhan_vien:
        btn = tk.Button(root, text=func, width=30, command=lambda f=func: add_user_screen() if f == "Thêm tài khoản" else show_message(f))
        btn.pack(pady=5)

    tk.Button(root, text="Đăng xuất", command=login_screen, fg="red").pack(pady=20)

# Giao diện thêm tài khoản
def add_user_screen():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Thêm Tài Khoản Mới", font=("Arial", 14, "bold")).pack(pady=10)
    
    tk.Label(root, text="Tên người dùng:").pack(pady=10)
    new_username_entry = tk.Entry(root)
    new_username_entry.pack(pady=5)
    
    tk.Label(root, text="Mật khẩu:").pack(pady=10)
    new_password_entry = tk.Entry(root, show="*")
    new_password_entry.pack(pady=5)
    
    tk.Label(root, text="Vai trò (admin/customer):").pack(pady=10)
    new_role_entry = tk.Entry(root)
    new_role_entry.pack(pady=5)
    
    def add_user():
        username = new_username_entry.get()
        password = new_password_entry.get()
        role = new_role_entry.get()
        
        if not username or not password:
            messagebox.showerror("Lỗi", "Tên người dùng và mật khẩu không được để trống!")
            return

        if role not in ["admin", "customer"]:
            messagebox.showerror("Lỗi", "Vai trò phải là 'admin' hoặc 'customer'!")
            return

        if username not in users:
            save_user_to_csv(users_file, username, password, role)  # Lưu vào file CSV
            users[username] = {"password": password, "role": role}  # Cập nhật trong bộ nhớ
            messagebox.showinfo("Thông báo", "Thêm tài khoản thành công!")
            admin_screen()  # Quay lại giao diện admin
        else:
            messagebox.showerror("Lỗi", "Tài khoản đã tồn tại!")

    tk.Button(root, text="Thêm Tài Khoản", command=add_user).pack(pady=20)
    tk.Button(root, text="Quay lại", command=admin_screen, fg="red").pack(pady=5)

# Khởi động giao diện đăng nhập
login_screen()

# Khởi chạy giao diện
root.mainloop()
