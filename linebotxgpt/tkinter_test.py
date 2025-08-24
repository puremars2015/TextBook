import threading
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

def choose_file():
    path = filedialog.askopenfilename(title="選擇檔案")
    if path:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, path)

def long_task():
    btn_run.config(state=tk.DISABLED)
    progress.start(10)  # 動起來表示忙碌
    status_var.set("執行中…")

    def worker():
        time.sleep(3)  # 模擬長任務
        # 回主執行緒更新 UI
        root.after(0, finish_task)

    threading.Thread(target=worker, daemon=True).start()

def finish_task():
    progress.stop()
    btn_run.config(state=tk.NORMAL)
    status_var.set("完成 ✅")
    messagebox.showinfo("完成", "長任務已結束！")

root = tk.Tk()
root.title("Tkinter GUI 範例")
root.geometry("420x220")

frm = ttk.Frame(root, padding=12)
frm.pack(fill=tk.BOTH, expand=True)

ttk.Label(frm, text="選擇檔案：").grid(row=0, column=0, sticky="w")
entry_path = ttk.Entry(frm, width=36)
entry_path.grid(row=0, column=1, sticky="we", padx=6)
ttk.Button(frm, text="瀏覽…", command=choose_file).grid(row=0, column=2)

ttk.Label(frm, text="輸入文字：").grid(row=1, column=0, sticky="w", pady=(10,0))
entry_text = ttk.Entry(frm, width=36)
entry_text.grid(row=1, column=1, sticky="we", padx=6, pady=(10,0))
btn_run = ttk.Button(frm, text="執行長任務", command=long_task)
btn_run.grid(row=1, column=2, pady=(10,0))

progress = ttk.Progressbar(frm, mode="indeterminate")
progress.grid(row=2, column=0, columnspan=3, sticky="we", pady=12)

status_var = tk.StringVar(value="就緒")
status = ttk.Label(frm, textvariable=status_var, anchor="w")
status.grid(row=3, column=0, columnspan=3, sticky="we")

frm.columnconfigure(1, weight=1)  # 讓中間欄位可自動拉伸
root.mainloop()
