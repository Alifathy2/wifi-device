import os
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk


class EasyNetApp:

  def __init__(self, root):
    self.root = root
    self.root.title("مدعي شبكة الإنترنت البسيط")
    self.root.geometry("550x400")
    self.root.config(bg="#f4f4f4")

    # عنوان
    title = tk.Label(
        root,
        text="قائمة الأجهزة النشطة على الشبكة",
        font=("Arial", 14, "bold"),
        bg="#f4f4f4",
    )
    title.pack(pady=15)

    # زر الفحص
    btn_scan = tk.Button(
        root,
        text="عرض الأجهزة المتصلة حالياً",
        bg="#007ACC",
        fg="white",
        font=("Arial", 11, "bold"),
        padx=10,
        pady=5,
        command=self.get_arp_table,
    )
    btn_scan.pack(pady=5)

    # جدول العرض
    self.tree = ttk.Treeview(
        root, columns=("IP", "MAC", "Type"), show="headings", height=8
    )
    self.tree.heading("IP", text="عنوان IP")
    self.tree.heading("MAC", text="عنوان MAC")
    self.tree.heading("Type", text="نوع الاتصال")
    self.tree.pack(fill="both", expand=True, padx=15, pady=15)

    # زر معلومات
    lbl_info = tk.Label(
        root,
        text=(
            "ملاحظة: لقطع الإنترنت أو التحكم الكامل، يفضل دائماً الدخول لصفحة"
            " الراوتر (192.168.1.1)"
        ),
        fg="gray",
        bg="#f4f4f4",
    )
    lbl_info.pack(pady=5)

  def get_arp_table(self):
    # تفريغ الجدول القديم
    for item in self.tree.get_children():
      self.tree.delete(item)

    try:
      # تنفيذ أمر ويندوز الشهير لجلب الأجهزة المتصلة بالشبكة المحلية
      output = subprocess.check_output("arp -a", universal_newlines=True)
      lines = output.split("\n")

      count = 0
      for line in lines:
        if "dynamic" in line.lower() or "static" in line.lower():
          parts = line.split()
          if len(parts) >= 3:
            ip = parts[0]
            mac = parts[1]
            conn_type = parts[2]
            self.tree.insert("", "end", values=(ip, mac, conn_type))
            count += 1

      if count > 0:
        messagebox.showinfo(
            "تم بنجاح", f"تم العثور على {count} جهاز متصل بالشبكة!"
        )
      else:
        messagebox.showwarning(
            "تنبيه", "لم يتم العثور على أجهزة نشطة حالياً، تأكد من اتصالك بالواي فاي."
        )
    except Exception as e:
      messagebox.showerror("خطأ", f"حدث خطأ أثناء فحص الشبكة: {str(e)}")


if __name__ == "__main__":
  root = tk.Tk()
  app = EasyNetApp(root)
  root.mainloop()