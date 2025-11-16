# Superkonverter – PyQt5
# Utviklet av Thomas Håvarstein

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QSpinBox
)

# ------------------------------
# Funksjoner (returnerer resultat + stegtekst)
# ------------------------------

def binary_to_decimal(binary_str: str):
    total = 0
    power = 0
    steps = []
    for ch in binary_str:
        if ch not in "01":
            raise ValueError("Kun 0 og 1 er tillatt i binært tall.")
    for bit in reversed(binary_str):
        if bit == '1':
            value = 1
            for _ in range(power):
                value *= 2
            total += value
            steps.append(f"2^{power} = {value}")
        elif bit != '0':
            raise ValueError("Kun 0 og 1 er tillatt.")
        power += 1
    steps_text = (" + ".join(steps) if steps else "0") + f" = {total}"
    return total, steps_text

def decimal_to_binary(n: int, pad_to: int = 0):
    if n < 0:
        raise ValueError("Bruk Two’s complement for negative tall.")
    if n == 0:
        s = "0"
        return s, "0"
    bits = []
    steps = []
    m = n
    while m > 0:
        r = m % 2
        steps.append(f"{m} ÷ 2 = {m//2} rest {r}")
        bits.append(str(r))
        m //= 2
    s = "".join(reversed(bits))
    if pad_to > 0 and len(s) < pad_to:
        zeros = []
        for _ in range(pad_to - len(s)):
            zeros.append("0")
        s = "".join(zeros) + s
    steps_text = "\n".join(steps) + f"\n= {s}"
    return s, steps_text

def decimal_to_base(n: int, base: int):
    if base < 2 or base > 36:
        raise ValueError("Base må være mellom 2 og 36.")
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if n == 0:
        return "0", "0"
    out = []
    steps = []
    m = n
    while m > 0:
        r = m % base
        steps.append(f"{m} ÷ {base} = {m//base} rest {digits[r]}")
        out.append(digits[r])
        m //= base
    s = "".join(reversed(out))
    steps_text = "\n".join(steps) + f"\n= {s}"
    return s, steps_text

def octal_to_decimal(octal_str: str):
    total = 0
    steps = []
    for ch in octal_str:
        if ch < '0' or ch > '7':
            raise ValueError("Oktal kan kun inneholde 0–7.")
    p = 0
    for ch in reversed(octal_str):
        digit = ord(ch) - ord('0')
        value = digit
        for _ in range(p):
            value *= 8
        total += value
        steps.append(f"{digit}·8^{p} = {value}")
        p += 1
    steps_text = " + ".join(steps) + f" = {total}"
    return total, steps_text

def hex_to_decimal(hex_str: str):
    s = hex_str.strip().lstrip("#").upper()
    hex_digits = "0123456789ABCDEF"
    total = 0
    steps = []
    p = 0
    for ch in s:
        if ch not in hex_digits:
            raise ValueError("Hex kan kun inneholde 0–9 og A–F.")
    for ch in reversed(s):
        val = 0
        found = False
        for i in range(16):
            if hex_digits[i] == ch:
                val = i
                found = True
                break
        if not found:
            raise ValueError("Ugyldig hex-tegn.")
        value = val
        for _ in range(p):
            value *= 16
        total += value
        steps.append(f"{val}·16^{p} = {value}")
        p += 1
    steps_text = " + ".join(steps) + f" = {total}"
    return total, steps_text

ROMAN_MAP = {'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000}

def roman_to_decimal(roman: str):
    r = roman.upper().strip()
    if not r:
        return 0, "0"
    total = 0
    steps_lines = []
    i = 0
    while i < len(r):
        if r[i] not in ROMAN_MAP:
            raise ValueError("Ugyldig romertall-tegn.")
        if i + 1 < len(r) and ROMAN_MAP[r[i]] < ROMAN_MAP[r[i+1]]:
            val = ROMAN_MAP[r[i+1]] - ROMAN_MAP[r[i]]
            steps_lines.append(f"{r[i]}{r[i+1]} = {ROMAN_MAP[r[i+1]]} - {ROMAN_MAP[r[i]]} = {val}")
            total += val
            i += 2
        else:
            val = ROMAN_MAP[r[i]]
            steps_lines.append(f"{r[i]} = {val}")
            total += val
            i += 1
    steps_text = "\n".join(steps_lines) + f"\n= {total}"
    return total, steps_text

def decimal_to_roman(n: int):
    if n <= 0:
        raise ValueError("Romertall støtter kun positive heltall.")
    val = [1000,900,500,400,100,90,50,40,10,9,5,4,1]
    syms = ["M","CM","D","CD","C","XC","L","XL","X","IX","V","IV","I"]
    out = []
    steps = []
    m = n
    i = 0
    while m > 0:
        cnt = m // val[i]
        if cnt > 0:
            steps.append(f"{m} ÷ {val[i]} = {cnt} → {syms[i]} × {cnt}")
        for _ in range(cnt):
            out.append(syms[i])
            m -= val[i]
        i += 1
    s = "".join(out)
    steps_text = "\n".join(steps) + f"\n= {s}"
    return s, steps_text

def char_to_code(ch: str):
    if len(ch) != 1:
        raise ValueError("Skriv inn ett tegn.")
    code = ord(ch)
    return code, f"ord('{ch}') = {code}"

def code_to_char(code: int):
    if code < 0 or code > 0x10FFFF:
        raise ValueError("Kode utenfor Unicode-området.")
    ch = chr(code)
    return ch, f"chr({code}) = '{ch}'"

def rgb_to_hex(r: int, g: int, b: int):
    for val in (r, g, b):
        if val < 0 or val > 255:
            raise ValueError("RGB-verdier må være 0–255.")
    hex_digits = "0123456789ABCDEF"
    parts = []
    steps = []
    for val in (r, g, b):
        hi = val // 16
        lo = val % 16
        steps.append(f"{val} = {hi}·16 + {lo} → {hex_digits[hi]}{hex_digits[lo]}")
        parts.append(hex_digits[hi] + hex_digits[lo])
    s = "#" + "".join(parts)
    steps_text = "\n".join(steps) + f"\n= {s}"
    return s, steps_text

def hex_to_rgb(hs: str):
    s = hs.strip().lstrip("#").upper()
    if len(s) != 6:
        raise ValueError("Hex-farge må være 6 tegn (RRGGBB).")
    hex_digits = "0123456789ABCDEF"
    rgb = []
    steps = []
    for i in range(0, 6, 2):
        hi_ch = s[i]
        lo_ch = s[i+1]
        hi = -1
        lo = -1
        for idx in range(16):
            if hex_digits[idx] == hi_ch:
                hi = idx
            if hex_digits[idx] == lo_ch:
                lo = idx
        if hi == -1 or lo == -1:
            raise ValueError("Ugyldige hex-tegn.")
        val = hi * 16 + lo
        steps.append(f"{hi_ch}{lo_ch} = {hi}·16 + {lo} = {val}")
        rgb.append(val)
    steps_text = "\n".join(steps) + f"\n= RGB{tuple(rgb)}"
    return tuple(rgb), steps_text

def fraction_to_decimal(numerator: int, denominator: int):
    if denominator == 0:
        raise ValueError("Nevner kan ikke være 0.")
    dec = numerator / denominator
    pct = dec * 100
    return (dec, pct), f"{numerator}/{denominator} = {dec} = {pct:.2f}%"

def prime_factorization(n: int):
    if n < 2:
        return [], "Ingen primtallsfaktorer for n < 2"
    factors = []
    steps = []
    d = 2
    m = n
    while m > 1:
        while m % d == 0:
            steps.append(f"{m} ÷ {d} = {m//d}")
            factors.append(d)
            m //= d
        d += 1
    steps_text = " → ".join(steps) + f"\n= {' x '.join(map(str, factors))}"
    return factors, steps_text

def bytes_to_units(b: int):
    if b < 0:
        raise ValueError("Bytes kan ikke være negativt.")
    kb = b / 1024
    mb = kb / 1024
    gb = mb / 1024
    return (kb, mb, gb), f"{b} B = {kb:.2f} KB = {mb:.2f} MB = {gb:.6f} GB"

def ipv4_to_binary(ip: str):
    parts = ip.strip().split(".")
    if len(parts) != 4:
        raise ValueError("Ugyldig IPv4-adresse.")
    bins = []
    steps = []
    for p in parts:
        if not p.isdigit():
            raise ValueError("Hver del må være et tall.")
        val = int(p)
        if val < 0 or val > 255:
            raise ValueError("Hver oktett må være 0–255.")
        s, _ = decimal_to_binary(val, pad_to=8)
        bins.append(s)
        steps.append(f"{val} → {s}")
    res = ".".join(bins)
    steps_text = "\n".join(steps) + f"\n= {res}"
    return res, steps_text

def decimal_to_bcd(n: int):
    if n < 0:
        raise ValueError("BCD her for ikke-negative heltall.")
    s = str(n)
    out = []
    steps = []
    for ch in s:
        if ch < '0' or ch > '9':
            raise ValueError("Kun sifre 0–9 i BCD.")
        digit = ord(ch) - ord('0')
        nibble, _ = decimal_to_binary(digit, pad_to=4)
        out.append(nibble)
        steps.append(f"{digit} → {nibble}")
    res = " ".join(out)
    steps_text = "\n".join(steps) + f"\n= {res}"
    return res, steps_text

def bcd_to_decimal(bcd: str):
    cleaned = bcd.replace(" ", "")
    if len(cleaned) == 0:
        return 0, "0"
    if len(cleaned) % 4 != 0:
        raise ValueError("BCD må være grupper av 4 bits.")
    groups = []
    for i in range(0, len(cleaned), 4):
        groups.append(cleaned[i:i+4])
    digits = []
    steps = []
    for grp in groups:
        for ch in grp:
            if ch not in "01":
                raise ValueError("BCD kan kun inneholde 0 og 1.")
        val, _ = binary_to_decimal(grp)
        if val > 9:
            raise ValueError("Hver BCD-nibble må representere 0–9.")
        digits.append(str(val))
        steps.append(f"{grp} → {val}")
    res = int("".join(digits))
    steps_text = "\n".join(steps) + f"\n= {res}"
    return res, steps_text

def binary_to_gray(b: str):
    for ch in b:
        if ch not in "01":
            raise ValueError("Kun 0/1 i binært.")
    if not b:
        return "", ""
    g = [b[0]]
    steps = [f"g0 = b0 = {b[0]}"]
    for i in range(1, len(b)):
        g.append('1' if (b[i] != b[i-1]) else '0')
        steps.append(f"g{i} = b{i} XOR b{i-1} = {b[i]} XOR {b[i-1]} → {g[-1]}")
    res = "".join(g)
    steps_text = "\n".join(steps) + f"\n= {res}"
    return res, steps_text

def gray_to_binary(g: str):
    for ch in g:
        if ch not in "01":
            raise ValueError("Kun 0/1 i Gray.")
    if not g:
        return "", ""
    b = [g[0]]
    steps = [f"b0 = g0 = {g[0]}"]
    for i in range(1, len(g)):
        b.append('1' if (g[i] != b[i-1]) else '0')
        steps.append(f"b{i} = g{i} XOR b{i-1} = {g[i]} XOR {b[i-1]} → {b[-1]}")
    res = "".join(b)
    steps_text = "\n".join(steps) + f"\n= {res}"
    return res, steps_text

def bitwise_and(a: str, b: str):
    if len(a) != len(b):
        raise ValueError("Strenger må ha lik lengde.")
    out = []
    steps = []
    for i in range(len(a)):
        if a[i] not in "01" or b[i] not in "01":
            raise ValueError("Kun 0/1.")
        res = '1' if (a[i] == '1' and b[i] == '1') else '0'
        out.append(res)
        steps.append(f"{a[i]} AND {b[i]} → {res}")
    s = "".join(out)
    steps_text = "\n".join(steps) + f"\n= {s}"
    return s, steps_text

def bitwise_or(a: str, b: str):
    if len(a) != len(b):
        raise ValueError("Strenger må ha lik lengde.")
    out = []
    steps = []
    for i in range(len(a)):
        if a[i] not in "01" or b[i] not in "01":
            raise ValueError("Kun 0/1.")
        res = '1' if (a[i] == '1' or b[i] == '1') else '0'
        out.append(res)
        steps.append(f"{a[i]} OR {b[i]} → {res}")
    s = "".join(out)
    steps_text = "\n".join(steps) + f"\n= {s}"
    return s, steps_text

def bitwise_xor(a: str, b: str):
    if len(a) != len(b):
        raise ValueError("Strenger må ha lik lengde.")
    out = []
    steps = []
    for i in range(len(a)):
        if a[i] not in "01" or b[i] not in "01":
            raise ValueError("Kun 0/1.")
        res = '1' if (a[i] != b[i]) else '0'
        out.append(res)
        steps.append(f"{a[i]} XOR {b[i]} → {res}")
    s = "".join(out)
    steps_text = "\n".join(steps) + f"\n= {s}"
    return s, steps_text

def bitwise_not(a: str):
    out = []
    steps = []
    for ch in a:
        if ch not in "01":
            raise ValueError("Kun 0/1.")
        res = '0' if ch == '1' else '1'
        out.append(res)
        steps.append(f"NOT {ch} → {res}")
    s = "".join(out)
    steps_text = "\n".join(steps) + f"\n= {s}"
    return s, steps_text

def shift_left(a: str, k: int):
    for ch in a:
        if ch not in "01":
            raise ValueError("Kun 0/1.")
    out = []
    for ch in a:
        out.append(ch)
    zeros = []
    for _ in range(k):
        zeros.append('0')
    s = "".join(out) + "".join(zeros)
    steps = f"{a} << {k} → {s}"
    return s, steps

def shift_right(a: str, k: int):
    for ch in a:
        if ch not in "01":
            raise ValueError("Kun 0/1.")
    if k >= len(a):
        s = "0" * len(a)
        return s, f"{a} >> {k} → {s}"
    s = a[:-k] + ("0" * k)
    return s, f"{a} >> {k} → {s}"

def twos_complement_negative(n: int, bits: int):
    if n >= 0:
        raise ValueError("Tall må være negativt for Two’s complement.")
    if bits <= 0:
        raise ValueError("Bitbredde må være > 0.")
    pos = -n
    pos_bin, _ = decimal_to_binary(pos, pad_to=bits)
    if len(pos_bin) > bits:
        raise ValueError("Bitbredde for liten for tallet.")
    flipped = []
    for ch in pos_bin:
        if ch not in "01":
            raise ValueError("Intern feil i binær.")
        flipped.append('0' if ch == '1' else '1')
    flipped_str = "".join(flipped)
    carry = 1
    result_bits = []
    for i in range(bits-1, -1, -1):
        b = 1 if flipped_str[i] == '1' else 0
        s = b + carry
        if s == 2:
            result_bits.append('0')
            carry = 1
        else:
            result_bits.append('1' if s == 1 else '0')
            carry = 0
    result_bits.reverse()
    res = "".join(result_bits)
    steps_text = (
        f"Start med |{n}| = {pos}\n"
        f"1) {pos} → binært ({bits} biter): {pos_bin}\n"
        f"2) Flip alle biter: {flipped_str}\n"
        f"3) Legg til 1: {flipped_str} + 1 = {res}"
    )
    return res, steps_text

# ------------------------------
# GUI Tabs
# ------------------------------

class BinDecTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Binært → Desimal
        self.bin_input = QLineEdit(); self.bin_input.setPlaceholderText("Binært (f.eks. 101101)")
        self.btn_bin_to_dec = QPushButton("Binært → Desimal")
        self.out_bin_dec = QLabel("")
        self.steps_bin_dec = QTextEdit(); self.steps_bin_dec.setReadOnly(True)
        self.btn_bin_to_dec.clicked.connect(self.on_bin_to_dec)

        # Desimal → Binært
        self.dec_input = QLineEdit(); self.dec_input.setPlaceholderText("Desimal (≥ 0)")
        self.pad_spin = QSpinBox(); self.pad_spin.setRange(0, 64); self.pad_spin.setValue(8)
        self.btn_dec_to_bin = QPushButton("Desimal → Binært")
        self.out_dec_bin = QLabel("")
        self.steps_dec_bin = QTextEdit(); self.steps_dec_bin.setReadOnly(True)
        self.btn_dec_to_bin.clicked.connect(self.on_dec_to_bin)

        layout.addWidget(QLabel("Binært → Desimal"))
        layout.addWidget(self.bin_input)
        layout.addWidget(self.btn_bin_to_dec)
        layout.addWidget(self.out_bin_dec)
        layout.addWidget(QLabel("Utregning:"))
        layout.addWidget(self.steps_bin_dec)

        layout.addWidget(QLabel("Desimal → Binært (med padding)"))
        row = QHBoxLayout()
        row.addWidget(self.dec_input)
        row.addWidget(QLabel("Pad til:")); row.addWidget(self.pad_spin)
        layout.addLayout(row)
        layout.addWidget(self.btn_dec_to_bin)
        layout.addWidget(self.out_dec_bin)
        layout.addWidget(QLabel("Utregning:"))
        layout.addWidget(self.steps_dec_bin)

        self.setLayout(layout)

    def on_bin_to_dec(self):
        try:
            s = self.bin_input.text().strip()
            res, steps = binary_to_decimal(s)
            self.out_bin_dec.setText(f"Resultat: {res}")
            self.steps_bin_dec.setText(steps)
        except Exception as e:
            self.out_bin_dec.setText(f"Feil: {e}")
            self.steps_bin_dec.clear()

    def on_dec_to_bin(self):
        try:
            n = int(self.dec_input.text().strip())
            pad = self.pad_spin.value()
            res, steps = decimal_to_binary(n, pad_to=pad)
            self.out_dec_bin.setText(f"Resultat: {res}")
            self.steps_dec_bin.setText(steps)
        except Exception as e:
            self.out_dec_bin.setText(f"Feil: {e}")
            self.steps_dec_bin.clear()

class BaseTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Desimal → Base-n
        self.dec_input = QLineEdit(); self.dec_input.setPlaceholderText("Desimal (≥ 0)")
        self.base_spin = QSpinBox(); self.base_spin.setRange(2, 36); self.base_spin.setValue(16)
        self.btn_convert = QPushButton("Desimal → Base-n")
        self.out = QLabel("")
        self.steps = QTextEdit(); self.steps.setReadOnly(True)
        self.btn_convert.clicked.connect(self.on_convert)

        layout.addWidget(QLabel("Desimal → Base-n (2–36)"))
        row = QHBoxLayout()
        row.addWidget(self.dec_input)
        row.addWidget(QLabel("Base:")); row.addWidget(self.base_spin)
        layout.addLayout(row)
        layout.addWidget(self.btn_convert)
        layout.addWidget(self.out)
        layout.addWidget(QLabel("Utregning:"))
        layout.addWidget(self.steps)

        # Oktal → Desimal
        self.octal_input = QLineEdit(); self.octal_input.setPlaceholderText("Oktal (f.eks. 157)")
        self.btn_o2d = QPushButton("Oktal → Desimal")
        self.o2d_out = QLabel(""); self.o2d_steps = QTextEdit(); self.o2d_steps.setReadOnly(True)
        self.btn_o2d.clicked.connect(self.on_o2d)

        # Hex → Desimal
        self.hex_input = QLineEdit(); self.hex_input.setPlaceholderText("Hex (f.eks. 2FA eller #FF)")
        self.btn_h2d = QPushButton("Hex → Desimal")
        self.h2d_out = QLabel(""); self.h2d_steps = QTextEdit(); self.h2d_steps.setReadOnly(True)
        self.btn_h2d.clicked.connect(self.on_h2d)

        layout.addWidget(QLabel("Oktal/Hex konverteringer"))
        layout.addWidget(self.octal_input); layout.addWidget(self.btn_o2d); layout.addWidget(self.o2d_out); layout.addWidget(self.o2d_steps)
        layout.addWidget(self.hex_input); layout.addWidget(self.btn_h2d); layout.addWidget(self.h2d_out); layout.addWidget(self.h2d_steps)

        self.setLayout(layout)

    def on_convert(self):
        try:
            n = int(self.dec_input.text().strip())
            base = self.base_spin.value()
            res, steps = decimal_to_base(n, base)
            self.out.setText(f"Resultat: {res}")
            self.steps.setText(steps)
        except Exception as e:
            self.out.setText(f"Feil: {e}")
            self.steps.clear()

    def on_o2d(self):
        try:
            s = self.octal_input.text().strip()
            res, steps = octal_to_decimal(s)
            self.o2d_out.setText(f"Resultat: {res}")
            self.o2d_steps.setText(steps)
        except Exception as e:
            self.o2d_out.setText(f"Feil: {e}")
            self.o2d_steps.clear()

    def on_h2d(self):
        try:
            s = self.hex_input.text().strip()
            res, steps = hex_to_decimal(s)
            self.h2d_out.setText(f"Resultat: {res}")
            self.h2d_steps.setText(steps)
        except Exception as e:
            self.h2d_out.setText(f"Feil: {e}")
            self.h2d_steps.clear()

class RomanTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.roman_input = QLineEdit(); self.roman_input.setPlaceholderText("Romertall (I,V,X,L,C,D,M)")
        self.btn_r2d = QPushButton("Romertall → Desimal")
        self.out_r2d = QLabel(""); self.steps_r2d = QTextEdit(); self.steps_r2d.setReadOnly(True)
        self.btn_r2d.clicked.connect(self.on_r2d)

        self.dec_input = QLineEdit(); self.dec_input.setPlaceholderText("Desimal (≥ 1)")
        self.btn_d2r = QPushButton("Desimal → Romertall")
        self.out_d2r = QLabel(""); self.steps_d2r = QTextEdit(); self.steps_d2r.setReadOnly(True)
        self.btn_d2r.clicked.connect(self.on_d2r)

        layout.addWidget(QLabel("Romertall ↔ Desimal"))
        layout.addWidget(self.roman_input); layout.addWidget(self.btn_r2d); layout.addWidget(self.out_r2d); layout.addWidget(self.steps_r2d)
        layout.addWidget(self.dec_input); layout.addWidget(self.btn_d2r); layout.addWidget(self.out_d2r); layout.addWidget(self.steps_d2r)
        self.setLayout(layout)

    def on_r2d(self):
        try:
            s = self.roman_input.text().strip()
            res, steps = roman_to_decimal(s)
            self.out_r2d.setText(f"Resultat: {res}")
            self.steps_r2d.setText(steps)
        except Exception as e:
            self.out_r2d.setText(f"Feil: {e}")
            self.steps_r2d.clear()

    def on_d2r(self):
        try:
            n = int(self.dec_input.text().strip())
            res, steps = decimal_to_roman(n)
            self.out_d2r.setText(f"Resultat: {res}")
            self.steps_d2r.setText(steps)
        except Exception as e:
            self.out_d2r.setText(f"Feil: {e}")
            self.steps_d2r.clear()

class AsciiTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.char_input = QLineEdit(); self.char_input.setPlaceholderText("Tegn (ett tegn)")
        self.btn_c2code = QPushButton("Tegn → Kode")
        self.out_c2code = QLabel(""); self.steps_c2code = QTextEdit(); self.steps_c2code.setReadOnly(True)
        self.btn_c2code.clicked.connect(self.on_c2code)

        self.code_input = QLineEdit(); self.code_input.setPlaceholderText("Kode (0–1114111)")
        self.btn_code2c = QPushButton("Kode → Tegn")
        self.out_code2c = QLabel(""); self.steps_code2c = QTextEdit(); self.steps_code2c.setReadOnly(True)
        self.btn_code2c.clicked.connect(self.on_code2c)

        layout.addWidget(QLabel("ASCII/Unicode ↔ Tegn"))
        layout.addWidget(self.char_input); layout.addWidget(self.btn_c2code); layout.addWidget(self.out_c2code); layout.addWidget(self.steps_c2code)
        layout.addWidget(self.code_input); layout.addWidget(self.btn_code2c); layout.addWidget(self.out_code2c); layout.addWidget(self.steps_code2c)
        self.setLayout(layout)

    def on_c2code(self):
        try:
            ch = self.char_input.text()
            res, steps = char_to_code(ch)
            self.out_c2code.setText(f"Resultat: {res}")
            self.steps_c2code.setText(steps)
        except Exception as e:
            self.out_c2code.setText(f"Feil: {e}")
            self.steps_c2code.clear()

    def on_code2c(self):
        try:
            code = int(self.code_input.text().strip())
            res, steps = code_to_char(code)
            self.out_code2c.setText(f"Resultat: {res}")
            self.steps_code2c.setText(steps)
        except Exception as e:
            self.out_code2c.setText(f"Feil: {e}")
            self.steps_code2c.clear()

class ColorTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # RGB → Hex
        self.r_input = QSpinBox(); self.r_input.setRange(0,255)
        self.g_input = QSpinBox(); self.g_input.setRange(0,255)
        self.b_input = QSpinBox(); self.b_input.setRange(0,255)
        self.btn_rgb2hex = QPushButton("RGB → Hex")
        self.out_rgb2hex = QLabel(""); self.steps_rgb2hex = QTextEdit(); self.steps_rgb2hex.setReadOnly(True)
        self.btn_rgb2hex.clicked.connect(self.on_rgb2hex)

        row = QHBoxLayout()
        row.addWidget(QLabel("R:")); row.addWidget(self.r_input)
        row.addWidget(QLabel("G:")); row.addWidget(self.g_input)
        row.addWidget(QLabel("B:")); row.addWidget(self.b_input)

        # Hex → RGB
        self.hex_input = QLineEdit(); self.hex_input.setPlaceholderText("Hex (#RRGGBB eller RRGGBB)")
        self.btn_hex2rgb = QPushButton("Hex → RGB")
        self.out_hex2rgb = QLabel(""); self.steps_hex2rgb = QTextEdit(); self.steps_hex2rgb.setReadOnly(True)
        self.btn_hex2rgb.clicked.connect(self.on_hex2rgb)

        layout.addWidget(QLabel("Farger"))
        layout.addLayout(row)
        layout.addWidget(self.btn_rgb2hex); layout.addWidget(self.out_rgb2hex); layout.addWidget(self.steps_rgb2hex)
        layout.addWidget(self.hex_input); layout.addWidget(self.btn_hex2rgb); layout.addWidget(self.out_hex2rgb); layout.addWidget(self.steps_hex2rgb)
        self.setLayout(layout)

    def on_rgb2hex(self):
        try:
            r = self.r_input.value(); g = self.g_input.value(); b = self.b_input.value()
            res, steps = rgb_to_hex(r, g, b)
            self.out_rgb2hex.setText(f"Resultat: {res}")
            self.steps_rgb2hex.setText(steps)
        except Exception as e:
            self.out_rgb2hex.setText(f"Feil: {e}")
            self.steps_rgb2hex.clear()

    def on_hex2rgb(self):
        try:
            s = self.hex_input.text().strip()
            res, steps = hex_to_rgb(s)
            self.out_hex2rgb.setText(f"Resultat: {res}")
            self.steps_hex2rgb.setText(steps)
        except Exception as e:
            self.out_hex2rgb.setText(f"Feil: {e}")
            self.steps_hex2rgb.clear()

class MathTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Fraction
        self.num_input = QLineEdit(); self.num_input.setPlaceholderText("Teller (heltall)")
        self.den_input = QLineEdit(); self.den_input.setPlaceholderText("Nevner (≠ 0)")
        self.btn_frac = QPushButton("Brøk → Desimal/Prosent")
        self.out_frac = QLabel(""); self.steps_frac = QTextEdit(); self.steps_frac.setReadOnly(True)
        self.btn_frac.clicked.connect(self.on_frac)

        # Prime factors
        self.pf_input = QLineEdit(); self.pf_input.setPlaceholderText("Heltall ≥ 2")
        self.btn_pf = QPushButton("Primtallsfaktorisering")
        self.out_pf = QLabel(""); self.steps_pf = QTextEdit(); self.steps_pf.setReadOnly(True)
        self.btn_pf.clicked.connect(self.on_pf)

        # Bytes
        self.bytes_input = QLineEdit(); self.bytes_input.setPlaceholderText("Bytes (heltall ≥ 0)")
        self.btn_bytes = QPushButton("Bytes → KB/MB/GB")
        self.out_bytes = QLabel(""); self.steps_bytes = QTextEdit(); self.steps_bytes.setReadOnly(True)
        self.btn_bytes.clicked.connect(self.on_bytes)

        layout.addWidget(QLabel("Brøk"))
        row = QHBoxLayout(); row.addWidget(self.num_input); row.addWidget(self.den_input)
        layout.addLayout(row)
        layout.addWidget(self.btn_frac); layout.addWidget(self.out_frac); layout.addWidget(self.steps_frac)

        layout.addWidget(QLabel("Primtallsfaktorisering"))
        layout.addWidget(self.pf_input); layout.addWidget(self.btn_pf); layout.addWidget(self.out_pf); layout.addWidget(self.steps_pf)

        layout.addWidget(QLabel("Byte-enheter"))
        layout.addWidget(self.bytes_input); layout.addWidget(self.btn_bytes); layout.addWidget(self.out_bytes); layout.addWidget(self.steps_bytes)
        self.setLayout(layout)

    def on_frac(self):
        try:
            num = int(self.num_input.text().strip()); den = int(self.den_input.text().strip())
            res, steps = fraction_to_decimal(num, den)
            dec, pct = res
            self.out_frac.setText(f"Resultat: {dec} ({pct:.2f}%)")
            self.steps_frac.setText(steps)
        except Exception as e:
            self.out_frac.setText(f"Feil: {e}")
            self.steps_frac.clear()

    def on_pf(self):
        try:
            n = int(self.pf_input.text().strip())
            factors, steps = prime_factorization(n)
            self.out_pf.setText(f"Resultat: {' x '.join(map(str, factors)) if factors else 'Ingen'}")
            self.steps_pf.setText(steps)
        except Exception as e:
            self.out_pf.setText(f"Feil: {e}")
            self.steps_pf.clear()

    def on_bytes(self):
        try:
            b = int(self.bytes_input.text().strip())
            res, steps = bytes_to_units(b)
            kb, mb, gb = res
            self.out_bytes.setText(f"Resultat: {kb:.2f} KB, {mb:.2f} MB, {gb:.6f} GB")
            self.steps_bytes.setText(steps)
        except Exception as e:
            self.out_bytes.setText(f"Feil: {e}")
            self.steps_bytes.clear()

class NetworkTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.ip_input = QLineEdit(); self.ip_input.setPlaceholderText("IPv4 (f.eks. 192.168.0.1)")
        self.btn_ip = QPushButton("IPv4 → Binær")
        self.out_ip = QLabel(""); self.steps_ip = QTextEdit(); self.steps_ip.setReadOnly(True)
        self.btn_ip.clicked.connect(self.on_ip)

        layout.addWidget(QLabel("Nettverk"))
        layout.addWidget(self.ip_input); layout.addWidget(self.btn_ip); layout.addWidget(self.out_ip); layout.addWidget(self.steps_ip)
        self.setLayout(layout)

    def on_ip(self):
        try:
            s = self.ip_input.text().strip()
            res, steps = ipv4_to_binary(s)
            self.out_ip.setText(f"Resultat: {res}")
            self.steps_ip.setText(steps)
        except Exception as e:
            self.out_ip.setText(f"Feil: {e}")
            self.steps_ip.clear()

class CodesTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # BCD
        self.bcd_dec_input = QLineEdit(); self.bcd_dec_input.setPlaceholderText("Desimal (≥ 0)")
        self.btn_d2bcd = QPushButton("Desimal → BCD")
        self.out_d2bcd = QLabel(""); self.steps_d2bcd = QTextEdit(); self.steps_d2bcd.setReadOnly(True)
        self.btn_d2bcd.clicked.connect(self.on_d2bcd)

        self.bcd_input = QLineEdit(); self.bcd_input.setPlaceholderText("BCD (grupper av 4 bits, f.eks. 0001 0010)")
        self.btn_bcd2d = QPushButton("BCD → Desimal")
        self.out_bcd2d = QLabel(""); self.steps_bcd2d = QTextEdit(); self.steps_bcd2d.setReadOnly(True)
        self.btn_bcd2d.clicked.connect(self.on_bcd2d)

        # Gray
        self.gray_bin_input = QLineEdit(); self.gray_bin_input.setPlaceholderText("Binært for Gray (f.eks. 1011)")
        self.btn_bin2gray = QPushButton("Binært → Gray")
        self.out_bin2gray = QLabel(""); self.steps_bin2gray = QTextEdit(); self.steps_bin2gray.setReadOnly(True)
        self.btn_bin2gray.clicked.connect(self.on_bin2gray)

        self.gray_input = QLineEdit(); self.gray_input.setPlaceholderText("Gray (f.eks. 1110)")
        self.btn_gray2bin = QPushButton("Gray → Binært")
        self.out_gray2bin = QLabel(""); self.steps_gray2bin = QTextEdit(); self.steps_gray2bin.setReadOnly(True)
        self.btn_gray2bin.clicked.connect(self.on_gray2bin)

        layout.addWidget(QLabel("BCD"))
        layout.addWidget(self.bcd_dec_input); layout.addWidget(self.btn_d2bcd); layout.addWidget(self.out_d2bcd); layout.addWidget(self.steps_d2bcd)
        layout.addWidget(self.bcd_input); layout.addWidget(self.btn_bcd2d); layout.addWidget(self.out_bcd2d); layout.addWidget(self.steps_bcd2d)

        layout.addWidget(QLabel("Gray-kode"))
        layout.addWidget(self.gray_bin_input); layout.addWidget(self.btn_bin2gray); layout.addWidget(self.out_bin2gray); layout.addWidget(self.steps_bin2gray)
        layout.addWidget(self.gray_input); layout.addWidget(self.btn_gray2bin); layout.addWidget(self.out_gray2bin); layout.addWidget(self.steps_gray2bin)
        self.setLayout(layout)

    def on_d2bcd(self):
        try:
            n = int(self.bcd_dec_input.text().strip())
            res, steps = decimal_to_bcd(n)
            self.out_d2bcd.setText(f"Resultat: {res}")
            self.steps_d2bcd.setText(steps)
        except Exception as e:
            self.out_d2bcd.setText(f"Feil: {e}")
            self.steps_d2bcd.clear()

    def on_bcd2d(self):
        try:
            s = self.bcd_input.text().strip()
            res, steps = bcd_to_decimal(s)
            self.out_bcd2d.setText(f"Resultat: {res}")
            self.steps_bcd2d.setText(steps)
        except Exception as e:
            self.out_bcd2d.setText(f"Feil: {e}")
            self.steps_bcd2d.clear()

    def on_bin2gray(self):
        try:
            s = self.gray_bin_input.text().strip()
            res, steps = binary_to_gray(s)
            self.out_bin2gray.setText(f"Resultat: {res}")
            self.steps_bin2gray.setText(steps)
        except Exception as e:
            self.out_bin2gray.setText(f"Feil: {e}")
            self.steps_bin2gray.clear()

    def on_gray2bin(self):
        try:
            s = self.gray_input.text().strip()
            res, steps = gray_to_binary(s)
            self.out_gray2bin.setText(f"Resultat: {res}")
            self.steps_gray2bin.setText(steps)
        except Exception as e:
            self.out_gray2bin.setText(f"Feil: {e}")
            self.steps_gray2bin.clear()

class BitwiseTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.a_input = QLineEdit(); self.a_input.setPlaceholderText("Binær A (f.eks. 10101010)")
        self.b_input = QLineEdit(); self.b_input.setPlaceholderText("Binær B (lik lengde som A)")
        self.btn_and = QPushButton("AND")
        self.btn_or = QPushButton("OR")
        self.btn_xor = QPushButton("XOR")
        self.btn_not = QPushButton("NOT (på A)")
        self.out_bitwise = QLabel(""); self.steps_bitwise = QTextEdit(); self.steps_bitwise.setReadOnly(True)

        self.btn_and.clicked.connect(self.on_and)
        self.btn_or.clicked.connect(self.on_or)
        self.btn_xor.clicked.connect(self.on_xor)
        self.btn_not.clicked.connect(self.on_not)

        layout.addWidget(QLabel("Bitvise operasjoner"))
        layout.addWidget(self.a_input); layout.addWidget(self.b_input)
        row = QHBoxLayout()
        row.addWidget(self.btn_and); row.addWidget(self.btn_or); row.addWidget(self.btn_xor); row.addWidget(self.btn_not)
        layout.addLayout(row)
        layout.addWidget(self.out_bitwise); layout.addWidget(self.steps_bitwise)

        # Shift
        self.shift_k = QSpinBox(); self.shift_k.setRange(0, 64)
        self.btn_shl = QPushButton("SHIFT LEFT (A)")
        self.btn_shr = QPushButton("SHIFT RIGHT (A)")
        self.btn_shl.clicked.connect(self.on_shl)
        self.btn_shr.clicked.connect(self.on_shr)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Skift med:")); row2.addWidget(self.shift_k)
        row2.addWidget(self.btn_shl); row2.addWidget(self.btn_shr)
        layout.addLayout(row2)

        self.setLayout(layout)

    def on_and(self):
        try:
            res, steps = bitwise_and(self.a_input.text().strip(), self.b_input.text().strip())
            self.out_bitwise.setText(f"Resultat: {res}")
            self.steps_bitwise.setText(steps)
        except Exception as e:
            self.out_bitwise.setText(f"Feil: {e}")
            self.steps_bitwise.clear()

    def on_or(self):
        try:
            res, steps = bitwise_or(self.a_input.text().strip(), self.b_input.text().strip())
            self.out_bitwise.setText(f"Resultat: {res}")
            self.steps_bitwise.setText(steps)
        except Exception as e:
            self.out_bitwise.setText(f"Feil: {e}")
            self.steps_bitwise.clear()

    def on_xor(self):
        try:
            res, steps = bitwise_xor(self.a_input.text().strip(), self.b_input.text().strip())
            self.out_bitwise.setText(f"Resultat: {res}")
            self.steps_bitwise.setText(steps)
        except Exception as e:
            self.out_bitwise.setText(f"Feil: {e}")
            self.steps_bitwise.clear()

    def on_not(self):
        try:
            res, steps = bitwise_not(self.a_input.text().strip())
            self.out_bitwise.setText(f"Resultat: {res}")
            self.steps_bitwise.setText(steps)
        except Exception as e:
            self.out_bitwise.setText(f"Feil: {e}")
            self.steps_bitwise.clear()

    def on_shl(self):
        try:
            k = self.shift_k.value()
            res, steps = shift_left(self.a_input.text().strip(), k)
            self.out_bitwise.setText(f"Resultat: {res}")
            self.steps_bitwise.setText(steps)
        except Exception as e:
            self.out_bitwise.setText(f"Feil: {e}")
            self.steps_bitwise.clear()

    def on_shr(self):
        try:
            k = self.shift_k.value()
            res, steps = shift_right(self.a_input.text().strip(), k)
            self.out_bitwise.setText(f"Resultat: {res}")
            self.steps_bitwise.setText(steps)
        except Exception as e:
            self.out_bitwise.setText(f"Feil: {e}")
            self.steps_bitwise.clear()

class TwosComplementTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.neg_input = QLineEdit(); self.neg_input.setPlaceholderText("Negativt heltall (f.eks. -51)")
        self.bits_spin = QSpinBox(); self.bits_spin.setRange(1, 64); self.bits_spin.setValue(8)
        self.btn_twos = QPushButton("Two’s complement")
        self.out_twos = QLabel("")
        self.steps_twos = QTextEdit(); self.steps_twos.setReadOnly(True)
        self.btn_twos.clicked.connect(self.on_twos)

        row = QHBoxLayout()
        row.addWidget(self.neg_input)
        row.addWidget(QLabel("Bitbredde:"))
        row.addWidget(self.bits_spin)

        layout.addWidget(QLabel("Two’s complement (negativt heltall → binært)"))
        layout.addLayout(row)
        layout.addWidget(self.btn_twos)
        layout.addWidget(self.out_twos)
        layout.addWidget(QLabel("Utregning:"))
        layout.addWidget(self.steps_twos)

        self.setLayout(layout)

    def on_twos(self):
        try:
            n = int(self.neg_input.text().strip())
            bits = self.bits_spin.value()
            res, steps = twos_complement_negative(n, bits)
            self.out_twos.setText(f"Resultat: {res}")
            self.steps_twos.setText(steps)
        except Exception as e:
            self.out_twos.setText(f"Feil: {e}")
            self.steps_twos.clear()

class AboutTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        info = QTextEdit()
        info.setReadOnly(True)
        info.setHtml("""
        <h2>Superkonverter</h2>
        <p>Dette programmet samler mange ulike konverteringer og utregninger fra informatikk og digitalteknologi.</p>
        <p><b>Utviklet av:</b> Thomas Håvarstein</p>
        <p>Bygget med Python og PyQt5.</p>
        <hr>
        <p><b>Funksjoner:</b></p>
        <ul>
          <li>Binært ↔ Desimal</li>
          <li>Desimal ↔ Base-n, Oktal, Hex</li>
          <li>Romertall ↔ Desimal</li>
          <li>ASCII/Unicode ↔ Tegn</li>
          <li>RGB ↔ Hex</li>
          <li>BCD ↔ Desimal</li>
          <li>Gray code ↔ Binær</li>
          <li>Two’s complement</li>
          <li>Brøk ↔ Desimal ↔ Prosent</li>
          <li>Primtallsfaktorisering</li>
          <li>Bytes ↔ KB/MB/GB</li>
          <li>IPv4 ↔ Binær</li>
          <li>Bitvise operasjoner</li>
        </ul>
        """)
        layout.addWidget(info)
        self.setLayout(layout)

# ------------------------------
# Main Window
# ------------------------------

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Superkonverter – med utregning (PyQt5) – Utviklet av Thomas Håvarstein")
        self.resize(1150, 950)
        layout = QVBoxLayout()
        tabs = QTabWidget()

        tabs.addTab(BinDecTab(), "Binært/Desimal")
        tabs.addTab(BaseTab(), "Base-n, Oktal, Hex")
        tabs.addTab(RomanTab(), "Romertall")
        tabs.addTab(AsciiTab(), "ASCII/Unicode")
        tabs.addTab(ColorTab(), "Farger")
        tabs.addTab(MathTab(), "Matematikk")
        tabs.addTab(NetworkTab(), "Nettverk")
        tabs.addTab(CodesTab(), "BCD & Gray")
        tabs.addTab(BitwiseTab(), "Bitvise operasjoner")
        tabs.addTab(TwosComplementTab(), "Two’s complement")
        tabs.addTab(AboutTab(), "Om")

        layout.addWidget(tabs)
        self.setLayout(layout)

def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()