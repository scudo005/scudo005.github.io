import re
import sys

# Standard section mapping for CodeWarrior Wii to base symbol name
SECTION_SYMBOLS = {
    1: "_f_init",
    2: "_f_text",
    # 3 and 4 are usually .ctors/.dtors or extab/extabindex (they rarely have exported symbols)
    5: "_f_rodata",
    6: "_f_data",
    7: "_f_bss",
    8: "_f_sdata",
    9: "_f_sbss",
    10: "_f_sdata2",
    11: "_f_sbss2",
}

CODE_SECTIONS = {1, 2}  # .init and .text contain code

def convert(input_path, output_path, output_typed_path=None):
    with open(input_path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    abs_symbols = []
    rel_symbols = []

    re_abs = re.compile(r"^(\S+)\s+(0x[0-9a-fA-F]+)\s*$")
    re_rel = re.compile(
        r"StrOffset:\s*[0-9a-fA-F]+\s*-\s*"
        r"Address:\s*([0-9a-fA-F]+)\s*-\s*"
        r"Section:\s*([0-9a-fA-F]+)\s*-\s*"
        r"ElfHash:\s*[0-9a-fA-F]+\s*-\s*(\S+)"
    )

    in_symbols = False
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if s == "=== Symbols ===":
            in_symbols = True
            continue
        if not in_symbols:
            continue

        m_abs = re_abs.match(s)
        if m_abs:
            name = m_abs.group(1)
            addr = int(m_abs.group(2), 16)
            abs_symbols.append((name, addr))
            continue

        m_rel = re_rel.search(s)
        if m_rel:
            offset = int(m_rel.group(1), 16)
            sec_id = int(m_rel.group(2), 16)
            name = m_rel.group(3)
            rel_symbols.append((name, sec_id, offset))

    # Compute base addresses from _f_* symbols
    sym_lookup = {name: addr for name, addr in abs_symbols}
    section_bases = {}
    for sec_id, f_sym in SECTION_SYMBOLS.items():
        if f_sym in sym_lookup:
            section_bases[sec_id] = sym_lookup[f_sym]

    # Write output
    unmapped_sections = {}
    results = []

    for name, addr in abs_symbols:
        results.append((name, addr, "l"))

    for name, sec_id, offset in rel_symbols:
        if sec_id not in section_bases:
            unmapped_sections[sec_id] = unmapped_sections.get(sec_id, 0) + 1
            continue
        real_addr = section_bases[sec_id] + offset
        kind = "f" if sec_id in CODE_SECTIONS else "l"
        results.append((name, real_addr, kind))

    with open(output_path, "w", encoding="utf-8") as out:
        for name, addr, _ in results:
            out.write(f"{name} 0x{addr:08x}\n")

    if output_typed_path:
        with open(output_typed_path, "w", encoding="utf-8") as out:
            for name, addr, kind in results:
                out.write(f"{name} 0x{addr:08x} {kind}\n")

    print(f"Converted {len(results)} symbols")
    if unmapped_sections:
        print("WARNING - Unmapped sections found (check Memory Map in Ghidra:")
        for sec_id, count in sorted(unmapped_sections.items()):
            print(f"  Section 0x{sec_id:08x} ({sec_id}): {count} symbols skipped")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python convert_sel_to_ghidra.py input.txt ghidra_symbols.txt [ghidra_typed.txt]")
        sys.exit(1)
    typed = sys.argv[3] if len(sys.argv) > 3 else None
    convert(sys.argv[1], sys.argv[2], typed)
