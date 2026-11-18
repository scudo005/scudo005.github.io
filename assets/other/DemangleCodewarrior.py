#@category Symbol
from ghidra.program.model.symbol import SourceType, SymbolType

MAX_LEN = 2000

OPERATORS = {
    "__nw": "operator new",
    "__nwa": "operator new[]",
    "__dl": "operator delete",
    "__dla": "operator delete[]",
    "__pl": "operator+",
    "__mi": "operator-",
    "__ml": "operator*",
    "__dv": "operator/",
    "__md": "operator%",
    "__er": "operator^",
    "__ad": "operator&",
    "__or": "operator|",
    "__co": "operator~",
    "__nt": "operator!",
    "__as": "operator=",
    "__lt": "operator<",
    "__gt": "operator>",
    "__apl": "operator+=",
    "__ami": "operator-=",
    "__amu": "operator*=",
    "__adv": "operator/=",
    "__amd": "operator%=",
    "__aer": "operator^=",
    "__aad": "operator&=",
    "__aor": "operator|=",
    "__ls": "operator<<",
    "__rs": "operator>>",
    "__als": "operator<<=",
    "__ars": "operator>>=",
    "__eq": "operator==",
    "__ne": "operator!=",
    "__le": "operator<=",
    "__ge": "operator>=",
    "__aa": "operator&&",
    "__oo": "operator||",
    "__pp": "operator++",
    "__mm": "operator--",
    "__cm": "operator,",
    "__rm": "operator->*",
    "__rf": "operator->",
    "__cl": "operator()",
    "__vc": "operator[]",
}

PRIMITIVES = {
    "v": "void",
    "b": "bool",
    "c": "char",
    "s": "short",
    "i": "int",
    "l": "long",
    "x": "long long",
    "f": "float",
    "d": "double",
    "r": "long double",
    "w": "wchar_t",
    "e": "...",
}


def read_int(s, pos):
    start = pos
    while pos < len(s) and s[pos].isdigit():
        pos += 1
    if pos == start:
        return None, start
    return int(s[start:pos]), pos


def demangle_template_args(inner):
    # Try to demangle comma-separated arguments inside <...>
    parts = []
    depth = 0
    cur = []
    for ch in inner:
        if ch == "<":
            depth += 1
        elif ch == ">":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    parts.append("".join(cur))

    out = []
    for p in parts:
        p = p.strip()
        t, next_pos = parse_type(p, 0, [])
        if t is not None and next_pos == len(p):
            out.append(t)
        else:
            out.append(p)
    return ", ".join(out)


def format_ident(name):
    if "<" in name and name.endswith(">"):
        idx = name.find("<")
        prefix = name[:idx]
        inner = name[idx + 1:-1]
        return "{}<{}>".format(prefix, demangle_template_args(inner))
    return name


def parse_len_ident(s, pos):
    length, pos = read_int(s, pos)
    if length is None or length <= 0 or pos + length > len(s):
        return None, pos
    raw = s[pos:pos + length]
    return format_ident(raw), pos + length


def parse_qualified(s, pos):
    if pos >= len(s):
        return None, pos
    if s[pos] == "Q":
        pos += 1
        if pos >= len(s):
            return None, pos
        if s[pos] == "_":
            pos += 1
            count, pos = read_int(s, pos)
            if count is None or pos >= len(s) or s[pos] != "_":
                return None, pos
            pos += 1
        elif s[pos].isdigit():
            count = int(s[pos])
            pos += 1
        else:
            return None, pos
        if count <= 0:
            return None, pos
        parts = []
        for _ in range(count):
            ident, pos = parse_len_ident(s, pos)
            if ident is None:
                return None, pos
            parts.append(ident)
        return parts, pos
    elif s[pos].isdigit():
        ident, pos = parse_len_ident(s, pos)
        if ident is None:
            return None, pos
        return [ident], pos
    return None, pos


def parse_param_list(s, pos, stop_on_underscore=True):
    params = []
    while pos < len(s):
        if stop_on_underscore and s[pos] == "_":
            break
        if s[pos] == "T" and pos + 1 < len(s) and s[pos + 1].isdigit():
            idx = int(s[pos + 1]) - 1
            if idx < 0 or idx >= len(params):
                return None, pos
            params.append(params[idx])
            pos += 2
            continue
        if s[pos] == "N" and pos + 2 < len(s) and s[pos + 1].isdigit() and s[pos + 2].isdigit():
            rep = int(s[pos + 1])
            idx = int(s[pos + 2]) - 1
            if idx < 0 or idx >= len(params) or rep <= 0:
                return None, pos
            for _ in range(rep):
                params.append(params[idx])
            pos += 3
            continue

        t, next_pos = parse_type(s, pos, params)
        if t is None:
            return None, pos
        params.append(t)
        pos = next_pos
    return params, pos


def parse_type(s, pos, params):
    if pos >= len(s):
        return None, pos

    # External CV qualifiers
    cv = []
    while pos < len(s) and s[pos] in ("C", "V"):
        cv.append("const" if s[pos] == "C" else "volatile")
        pos += 1

    if pos >= len(s):
        return None, pos

    ch = s[pos]
    base = None

    if ch == "P":
	# Pointer (check to see if it points to a PF function)
        if pos + 1 < len(s) and s[pos + 1] == "F":
            fparams, next_pos = parse_param_list(s, pos + 2, stop_on_underscore=True)
            if fparams is None:
                return None, pos
            ret = "void"
            if next_pos < len(s) and s[next_pos] == "_":
                ret, next_pos = parse_type(s, next_pos + 1, params)
                if ret is None:
                    return None, pos
            base = "{} (*)({})".format(ret, ", ".join(fparams))
            pos = next_pos
        else:
            inner, pos = parse_type(s, pos + 1, params)
            if inner is None:
                return None, pos
            base = inner + "*"
    elif ch == "R":
        inner, pos = parse_type(s, pos + 1, params)
        if inner is None:
            return None, pos
        base = inner + "&"
    elif ch == "A":
        arr_len, next_pos = read_int(s, pos + 1)
        if arr_len is None or next_pos >= len(s) or s[next_pos] != "_":
            return None, pos
        elem, pos = parse_type(s, next_pos + 1, params)
        if elem is None:
            return None, pos
        base = "{}[{}]".format(elem, arr_len)
    elif ch == "M":
        cls_parts, next_pos = parse_qualified(s, pos + 1)
        if cls_parts is None:
            return None, pos
        member_t, pos = parse_type(s, next_pos, params)
        if member_t is None:
            return None, pos
        base = "{} ({}::*)".format(member_t, "::".join(cls_parts))
    elif ch in ("U", "S"):
        sign = "unsigned" if ch == "U" else "signed"
        if pos + 1 < len(s) and s[pos + 1] in PRIMITIVES:
            base = "{} {}".format(sign, PRIMITIVES[s[pos + 1]])
            pos += 2
        else:
            return None, pos
    elif ch in PRIMITIVES:
        base = PRIMITIVES[ch]
        pos += 1
    elif ch == "Q" or ch.isdigit():
        qparts, pos = parse_qualified(s, pos)
        if qparts is None:
            return None, pos
        base = "::".join(qparts)
    else:
        return None, pos

    if cv:
        if base.endswith("*") or base.endswith("&"):
            base = base + " " + " ".join(cv)
        else:
            base = " ".join(cv) + " " + base

    return base, pos


def parse_suffix(suffix):
    pos = 0
    cls_parts = []
    if pos < len(suffix) and (suffix[pos] == "Q" or suffix[pos].isdigit()):
        cls_parts, pos = parse_qualified(suffix, pos)
        if cls_parts is None:
            return None

    # Method qualifiers (eg. CFv = const method)
    method_cv = []
    while pos < len(suffix) and suffix[pos] in ("C", "V"):
        method_cv.append("const" if suffix[pos] == "C" else "volatile")
        pos += 1

    # Static class variable or vtable (no trailing 'F')
    if pos == len(suffix):
        if not cls_parts:
            return None
        return cls_parts, None, None, method_cv

    if suffix[pos] != "F":
        return None

    fparams, pos = parse_param_list(suffix, pos + 1, stop_on_underscore=True)
    if fparams is None:
        return None

    ret_type = None
    if pos < len(suffix) and suffix[pos] == "_":
        ret_type, pos = parse_type(suffix, pos + 1, fparams)
        if ret_type is None:
            return None

    if pos != len(suffix):
        return None

    return cls_parts, fparams, ret_type, method_cv


def demangle_cw(name):
    if "__" not in name:
        return None

    # Find all possible "__" separators outside of template brackets 
    candidates = []
    depth = 0
    i = 0
    while i < len(name) - 1:
        ch = name[i]
        if ch == "<":
            depth += 1
        elif ch == ">":
            depth = max(0, depth - 1)
        elif depth == 0 and i > 0 and name[i:i + 2] == "__":
            candidates.append(i)
        i += 1

    for idx in candidates:
        base_name = name[:idx]
        suffix = name[idx + 2:]
        parsed = parse_suffix(suffix)
        if parsed is None:
            continue

        cls_parts, fparams, ret_type, method_cv = parsed

	# Resolve special names
        if base_name == "__ct":
            short_name = cls_parts[-1] if cls_parts else "__ct"
        elif base_name == "__dt":
            short_name = "~" + cls_parts[-1] if cls_parts else "__dt"
        elif base_name == "__vt":
            short_name = "vtable"
        elif base_name in OPERATORS:
            short_name = OPERATORS[base_name]
        elif base_name.startswith("__op"):
            op_type, op_end = parse_type(base_name, 4, [])
            if op_type is None or op_end != len(base_name):
                continue
            short_name = "operator " + op_type
        else:
            short_name = format_ident(base_name)

        full_name = "::".join(cls_parts + [short_name]) if cls_parts else short_name
        if fparams is not None:
            sig = "{}({})".format(full_name, ", ".join(fparams))
            if method_cv:
                sig += " " + " ".join(method_cv)
            if ret_type:
                sig = "{} {}".format(ret_type, sig)
        else:
            sig = full_name

        return cls_parts, short_name, sig

    return None


def get_or_create_ns(st, global_ns, parts):
    ns = global_ns
    for p in parts:
        p_clean = p.replace(" ", "_")
        if len(p_clean) > MAX_LEN:
            p_clean = p_clean[:MAX_LEN]
        existing = st.getNamespace(p_clean, ns)
        if existing is not None:
            ns = existing
        else:
            ns = st.createNameSpace(ns, p_clean, SourceType.USER_DEFINED)
    return ns


def sanitize_ghidra_name(s):
    s = s.replace(" ", "_")
    if len(s) > MAX_LEN:
        s = s[:MAX_LEN]
    return s


def recover_full_name_if_truncated(sym):
    name = sym.getName()
    if len(name) >= MAX_LEN - 10:
        comment = getPlateComment(sym.getAddress())
        if comment and comment.startswith("Full symbol name:\n"):
            first_rest = comment[len("Full symbol name:\n"):].splitlines()[0].strip()
            if first_rest:
                return first_rest
    return name


def main():
    st = currentProgram.getSymbolTable()
    fm = currentProgram.getFunctionManager()
    global_ns = currentProgram.getGlobalNamespace()

    # Copy the whole list beforehand to avoid edits during iteration
    all_symbols = list(st.getDefinedSymbols())

    demangled_count = 0
    errors = 0

    for sym in all_symbols:
        if monitor.isCancelled():
            break
        if sym.getSource() == SourceType.DEFAULT:
            continue

        stype = sym.getSymbolType()
        if stype not in (SymbolType.FUNCTION, SymbolType.LABEL):
            continue
	# Avoid local labels inside functions
        if stype == SymbolType.LABEL and sym.getParentNamespace() != global_ns:
            continue

        orig_name = recover_full_name_if_truncated(sym)
        res = demangle_cw(orig_name)
        if res is None:
            continue

        cls_parts, short_name, full_sig = res
        addr = sym.getAddress()

        try:
            ns = get_or_create_ns(st, global_ns, cls_parts) if cls_parts else global_ns
            clean_short = sanitize_ghidra_name(short_name)

            if stype == SymbolType.FUNCTION:
                func = fm.getFunctionAt(addr)
                if func is not None:
                    func.setParentNamespace(ns)
                    func.setName(clean_short, SourceType.USER_DEFINED)
            else:
                sym.setNamespace(ns)
                sym.setName(clean_short, SourceType.USER_DEFINED)

            old_comment = getPlateComment(addr)
            if old_comment is None:
                setPlateComment(addr, full_sig)
            elif full_sig not in old_comment:
                setPlateComment(addr, full_sig + "\n\n" + old_comment)

            demangled_count += 1
        except Exception as e:
            print("Demangling error: {} @ {}: {}".format(orig_name[:60], addr, e))
            errors += 1

    print("Demangling complete! Demangled symbols: {}, errors: {}".format(
        demangled_count, errors
    ))


main()
