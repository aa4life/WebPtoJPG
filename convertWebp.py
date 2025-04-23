import os
import multiprocessing
import functools
import threading
import tkinter as tk
from tkinter import messagebox, filedialog, font as tkFont
from tkinter import ttk  # 匯入 ttk 模組
from PIL import Image

# === 轉換函式 ===
def convert_single_webp(webp_path, quality, keep_webp):
    """
    轉換 .webp 為 .jpg。
    若 keep_webp 為 False（預設），轉換成功後刪除原始 webp 檔案；
    若 keep_webp 為 True，則保留原始 webp，並將新生成的 jpg 檔移至原始路徑下的新建「jpg」資料夾中。
    """
    try:
        jpg_path = os.path.splitext(webp_path)[0] + ".jpg"
        with Image.open(webp_path) as img:
            img.convert("RGB").save(jpg_path, "JPEG", quality=quality)
        if keep_webp:
            original_folder = os.path.dirname(webp_path)
            jpg_folder = os.path.join(original_folder, "jpg")
            if not os.path.exists(jpg_folder):
                os.makedirs(jpg_folder)
            new_jpg_path = os.path.join(jpg_folder, os.path.basename(jpg_path))
            os.rename(jpg_path, new_jpg_path)
        else:
            if os.path.exists(jpg_path):
                os.remove(webp_path)
    except Exception:
        pass

def convert_webp_to_jpg_parallel(folder_path, quality, keep_webp):
    """
    搜尋指定資料夾內所有 .webp 檔案，使用多核心平行轉換
    """
    current_lang = language_mapping[lang_var.get()]
    if not os.path.exists(folder_path):
        messagebox.showerror(translations[current_lang]["title"],
                             translations[current_lang]["error_folder"])
        return

    webp_files = [os.path.join(folder_path, f)
                  for f in os.listdir(folder_path) if f.lower().endswith('.webp')]
    if not webp_files:
        messagebox.showerror(translations[current_lang]["title"],
                             translations[current_lang]["error_files"])
        return

    num_cores = min(multiprocessing.cpu_count(), len(webp_files))
    pool = multiprocessing.Pool(processes=num_cores)
    func = functools.partial(convert_single_webp, quality=quality, keep_webp=keep_webp)
    pool.map(func, webp_files)
    pool.close()
    pool.join()

def conversion_thread(folder_path, quality, keep_webp):
    convert_webp_to_jpg_parallel(folder_path, quality, keep_webp)
    current_lang = language_mapping[lang_var.get()]
    # 轉檔完成後，恢復按鈕樣式 (必須在主執行緒更新 GUI)
    # 轉檔完成後，恢復按鈕樣式 (必須在主執行緒更新 GUI)
    root.after(0, lambda: convert_button.config(text=translations[current_lang]["start"]))
    root.after(0, lambda: convert_button.state(['!disabled'])) # 啟用按鈕
    messagebox.showinfo(translations[current_lang]["title"],
                        translations[current_lang]["complete"])

# === GUI 相關函式 ===
def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path_entry.delete(0, tk.END)
        folder_path_entry.insert(0, folder_selected)

def start_conversion():
    folder_path = folder_path_entry.get().strip()
    current_lang = language_mapping[lang_var.get()]
    if current_lang == "zh":
        quality_map = {"低": 65, "中": 75, "高": 85, "極高": 95}
    elif current_lang == "en":
        quality_map = {"Low": 65, "Medium": 75, "High": 85, "Very High": 95}
    elif current_lang == "ja":
        quality_map = {"低い": 65, "普通": 75, "高い": 85, "最高": 95}
    quality_str = quality_var.get()
    quality = quality_map.get(quality_str, 85)
    keep_webp = keep_var.get()
    # 轉檔開始時，更新按鈕為轉檔中狀態並禁用
    convert_button.config(text=translations[current_lang]["converting"])
    convert_button.state(['disabled']) # 禁用按鈕防止重複點擊
    threading.Thread(target=conversion_thread,
                     args=(folder_path, quality, keep_webp),
                     daemon=True).start()

def update_ui_language(*args):
    current_lang = language_mapping[lang_var.get()]
    t = translations[current_lang]
    root.title(t["title"])
    folder_path_label.config(text=t["folder_label"])
    browse_button.config(text=t["browse"])
    quality_label.config(text=t["quality_label"])
    quality_menu['menu'].delete(0, 'end')
    for option in t["quality_options"]:
        quality_menu['menu'].add_command(label=option, command=tk._setit(quality_var, option))
    # 更新品質下拉選單的選項
    current_quality = quality_var.get() # 記住當前選擇
    menu = quality_menu["menu"]
    menu.delete(0, "end")
    for option in t["quality_options"]:
        menu.add_command(label=option, command=lambda value=option: quality_var.set(value))
    # 嘗試恢復之前的選擇，如果新語言中不存在，則設為第一個選項
    if current_quality in t["quality_options"]:
         quality_var.set(current_quality)
    elif t["quality_options"]:
         quality_var.set(t["quality_options"][2]) # 預設選 "高" 或 "High" 或 "高い"
    else:
         quality_var.set("") # 如果沒有選項

    keep_checkbox.config(text=t["keep_checkbox"])
    # 檢查按鈕是否處於禁用狀態 (轉檔中)，如果是，則不改變文字
    if 'disabled' not in convert_button.state():
        convert_button.config(text=t["start"])
    language_label.config(text=t["language_label"])
    # 更新語言下拉選單的顯示文字 (雖然 OptionMenu 不直接支援，但可以這樣更新)
    # language_menu # ttk.OptionMenu 的文字更新比較麻煩，通常在建立時就固定

# === 主程式 ===
if __name__ == '__main__':
    multiprocessing.freeze_support()  # Windows 下需要
    root = tk.Tk()
    root.title("WebP to JPG Converter") # 預設標題

    # --- 設定 ttk 主題 ---
    style = ttk.Style(root)
    # 嘗試使用系統可用的較佳主題
    available_themes = style.theme_names()
    if "clam" in available_themes:
        style.theme_use("clam")
    elif "vista" in available_themes: # Windows
        style.theme_use("vista")
    elif "aqua" in available_themes: # macOS
        style.theme_use("aqua")

    # --- 設定預設字型 ---
    default_font = tkFont.nametofont("TkDefaultFont")
    default_font.configure(size=10)
    root.option_add("*Font", default_font)

    # --- 主框架 ---
    main_frame = ttk.Frame(root, padding="10 10 10 10")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # 定義各語言翻譯字典 (增加了 "converting" 文字)
    translations = {
        "zh": {
            "title": "WebP 轉 JPG 轉換器",
            "folder_label": "資料夾路徑:",
            "browse": "選擇資料夾",
            "quality_label": "壓縮品質:",
            "quality_options": ["低", "中", "高", "極高"],
            "keep_checkbox": "保留原始的 webp 檔（轉檔完成檔案會存放在 'jpg' 資料夾）",
            "start": "開始轉換",
            "converting": "轉檔中...",
            "error_folder": "指定的資料夾不存在，請確認後再試。",
            "error_files": "目標資料夾內沒有 .webp 檔案。",
            "complete": "資料夾內 .webp 圖片轉檔完成！",
            "language_label": "語言:"
        },
        "en": {
            "title": "WebP to JPG Converter",
            "folder_label": "Folder Path:",
            "browse": "Browse Folder",
            "quality_label": "Compression Quality:",
            "quality_options": ["Low", "Medium", "High", "Very High"],
            "keep_checkbox": "Keep original webp file (JPG files will be saved in 'jpg' folder)",
            "start": "Start Conversion",
            "converting": "Converting...",
            "error_folder": "The specified folder does not exist. Please check and try again.",
            "error_files": "No .webp files found in the target folder.",
            "complete": ".webp to .jpg conversion completed for the folder!",
            "language_label": "Language:"
        },
        "ja": {
            "title": "WebPからJPG変換器",
            "folder_label": "フォルダパス:",
            "browse": "フォルダを選択",
            "quality_label": "圧縮品質:",
            "quality_options": ["低い", "普通", "高い", "最高"],
            "keep_checkbox": "元のwebpファイルを保持する（変換されたJPGファイルは 'jpg' フォルダに保存されます）",
            "start": "変換開始",
            "converting": "変換中...",
            "error_folder": "指定されたフォルダは存在しません。確認して再試行してください。",
            "error_files": "指定されたフォルダに.webpファイルがありません。",
            "complete": "フォルダ内の.webp画像の変換が完了しました！",
            "language_label": "言語:"
        }
    }
    language_mapping = {"繁體中文": "zh", "English": "en", "日本語": "ja"}

    # --- 介面元件 ---
    # 資料夾選擇
    folder_path_label = ttk.Label(main_frame, text="")
    folder_path_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    folder_path_entry = ttk.Entry(main_frame, width=50)
    folder_path_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=2, sticky="ew")
    browse_button = ttk.Button(main_frame, text="", command=browse_folder)
    browse_button.grid(row=1, column=2, padx=5, pady=2, sticky="w")

    # 壓縮品質
    quality_label = ttk.Label(main_frame, text="")
    quality_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    quality_var = tk.StringVar(root)
    quality_menu = ttk.OptionMenu(main_frame, quality_var, "") # 選項會在 update_ui_language 中設定
    quality_menu.grid(row=3, column=0, padx=5, pady=2, sticky="ew")

    # 保留原始檔選項
    keep_var = tk.BooleanVar(root)
    keep_var.set(False)
    keep_checkbox = ttk.Checkbutton(main_frame, text="", variable=keep_var)
    keep_checkbox.grid(row=4, column=0, columnspan=3, padx=5, pady=10, sticky="w")

    # 語言選擇
    language_label = ttk.Label(main_frame, text="")
    language_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")
    lang_var = tk.StringVar(root)
    lang_var.set("繁體中文") # 預設語言
    language_menu = ttk.OptionMenu(main_frame, lang_var, "繁體中文", *language_mapping.keys(), command=update_ui_language)
    language_menu.grid(row=6, column=0, padx=5, pady=2, sticky="ew")

    # 開始轉換按鈕
    # 使用 ttk.Style 來設定特定按鈕的樣式
    style.configure("Accent.TButton", font=("Arial", 14, "bold"), padding=10)
    # style.map("Accent.TButton",
    #           foreground=[('active', 'white'), ('!disabled', 'white')],
    #           background=[('active', '#005f5f'), ('!disabled', '#008080')]) # 範例：設定按鈕顏色

    convert_button = ttk.Button(main_frame, text="", command=start_conversion, style="Accent.TButton")
    convert_button.grid(row=7, column=0, columnspan=3, padx=5, pady=20)

    # 設定 Grid 權重，讓元件可以隨視窗縮放
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)
    # main_frame.columnconfigure(2, weight=0) # 按鈕不需要縮放

    update_ui_language() # 初始化 UI 文字

    root.mainloop()
