# WebP 轉 JPG 轉換器 / WebP to JPG Converter / WebPからJPG変換器

## 簡介 (繁體中文)
這是一個使用 Python 與 Tkinter 建立的圖形介面應用程式，可將指定資料夾中的 .webp 圖片轉換成 .jpg 格式。此應用程式支援多核心平行轉檔，可有效加速轉檔過程。使用者可選擇轉換品質，以及是否保留原始的 .webp 檔案（若選擇保留，新生成的 .jpg 檔案會存放在原始路徑下新建的「jpg」資料夾中）。介面支援繁體中文、英文及日文三種語言。

## Introduction (English)
This is a graphical application built with Python and Tkinter that converts .webp images to .jpg format from a specified folder. The application supports multi-core parallel processing to speed up the conversion process. Users can choose the conversion quality and decide whether to keep the original .webp files (if kept, the newly generated .jpg files will be moved to a new "jpg" folder in the original directory). The interface is available in Traditional Chinese, English, and Japanese.

## 概要 (日本語)
本アプリケーションは、Python と Tkinter を使用して作成されたグラフィカルなツールで、指定フォルダ内の .webp 画像を .jpg 形式に変換します。マルチコア並列処理により、変換処理を高速化しています。ユーザーは変換品質を選択し、元の .webp ファイルを保持するかどうかを決定できます（保持する場合、新しく生成された .jpg ファイルは元のディレクトリ内に新規作成される「jpg」フォルダに保存されます）。インターフェースは繁体字中国語、英語、日本語に対応しています。

---

## 功能 Features / 機能 / 機能
- **資料夾選擇 / Folder Selection / フォルダ選択**  
  透過圖形介面選擇包含 .webp 檔案的資料夾。
- **多核心平行轉檔 / Multi-core Parallel Processing / マルチコア並列処理**  
  利用多核心技術加速圖片轉換。
- **壓縮品質選擇 / Compression Quality Options / 圧縮品質選択**  
  提供低、中、高及極高四種品質選項。
- **原始檔案保留選項 / Option to Keep Original Files / 元ファイル保持オプション**  
  使用者可決定是否保留原始 .webp 檔案（若保留，轉換後的 .jpg 檔將存放在「jpg」資料夾中）。
- **多語言支援 / Multi-language Support / 多言語サポート**  
  介面支援繁體中文、英文及日文。

---

## 使用方法 Usage / 使い方 / 使用方法
1. **選擇資料夾 / Select Folder / フォルダを選択**  
   使用者點選「選擇資料夾」按鈕，選擇包含 .webp 檔案的資料夾。
2. **設定轉檔參數 / Set Conversion Parameters / 変換パラメータを設定**  
   選擇壓縮品質，並決定是否保留原始 .webp 檔案。
3. **切換語言 / Choose Language / 言語を選択**  
   從下拉式選單中選擇介面語言（繁體中文、English、または 日本語）。
4. **開始轉換 / Start Conversion / 変換開始**  
   按下醒目的「開始轉換」按鈕後，轉檔開始（轉檔中按鈕會變成紅色，顯示「轉檔中...」/ "Converting..." / "変換中..."）。
5. **完成提示 / Completion Notice / 完了通知**  
   轉檔完成後，系統會顯示完成訊息，並恢復按鈕原始樣式。

---

## 打包與部署 Packaging and Deployment / パッケージングと展開
此應用程式可使用 [PyInstaller](https://pyinstaller.readthedocs.io/) 打包成獨立可執行檔。  
例如，在命令列中執行以下指令（適用於 Windows 與 macOS）：
```bash
pyinstaller --onefile --windowed convertWebp.py
```

## 授權 License / ライセンス / 授權
本專案採用 MIT License。  
詳情請參閱 LICENSE 檔案。

This project is licensed under the MIT License.  
Please refer to the LICENSE file for details.

本プロジェクトは MIT License の下でライセンスされています。  
詳細は LICENSE ファイルを参照してください。

## 聯絡 Contact / お問い合わせ / 聯絡方式
若有任何問題或建議，請提交 Issue。

If you have any questions or suggestions, please submit an Issue.

ご質問やご提案がある場合は、Issue をご提出ください。

