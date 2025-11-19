# Super Converter – PyQt5

A complete GUI program for number and code conversions, built in **Python** with **PyQt5**.  
The application displays both the result and the **step-by-step calculation** for each conversion, making it useful both as a tool and as a learning resource.

---

## ✨ Features

### 🔢 Number Conversions
- Binary ↔ Decimal  
- Decimal ↔ Binary (with padding)  
- Decimal ↔ Base‑n (2–36)  
- Octal ↔ Decimal  
- Hex ↔ Decimal  

### 🏛 Roman Numerals
- Roman ↔ Decimal  

### 🔤 ASCII/Unicode
- Character ↔ Code (ord/chr)  

### 🎨 Colors
- RGB ↔ Hex  

### 🧮 Mathematics
- Fraction ↔ Decimal ↔ Percentage  
- Prime factorization  
- Bytes ↔ KB/MB/GB  

### 🌐 Networking
- IPv4 ↔ Binary  

### 🔡 Codes
- BCD ↔ Decimal  
- Gray code ↔ Binary  

### ⚙️ Bitwise Logic
- AND, OR, XOR, NOT  
- SHIFT LEFT, SHIFT RIGHT  

### ➖ Two’s Complement
- Negative integer → binary with chosen bit width  

### ℹ️ About Tab
- Information about the program  
- Developed by **Thomas Håvarstein**

---

## 🚀 Getting Started

### Requirements
- Python 3.9+  
- PyQt5 (`pip install pyqt5`)

### Run the Program
```bash
python superkonverter.py

### Build to .exe
# Install PyInstaller:
- pip install pyinstaller

### Create .exe:
pyinstaller --onefile --noconsole --name SuperConverter superv3.3.py
- The result will be located in dist/SuperConverter.exe.
