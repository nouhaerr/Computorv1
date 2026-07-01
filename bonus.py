import re
import computor as cp

def free_form_entry_normalization(normalized_poly: str) -> str:
    # 1. Standardize variable casing cleanly
    polynomial_clean = normalized_poly.replace('x', 'X')
    
    # 2. Case: Missing multiplication marks (e.g., "4X^2" -> "4 * X^2")
    polynomial_clean = re.sub(r'([0-9.]+)\s*X', r'\1 * X', polynomial_clean)
    
    # 3. Case: Add implicit power to lone X terms (e.g., "4 * X" -> "4 * X^1")
    polynomial_clean = re.sub(r'(?<![a-zA-Z0-9])X(?!\^)', 'X^1', polynomial_clean)
    
    # 4. Case: Naked "X^p" at the absolute START of the string (e.g., "X^2" -> "1 * X^2")
    polynomial_clean = re.sub(r'^X\^', '1 * X^', polynomial_clean)
    
    # 5. Case: Naked "X^p" sitting after an operator (e.g., "+ X^1" -> "+ 1 * X^1")
    # We explicitly omit \s from the group so it never multi-intercepts an existing '*' arrangement
    polynomial_clean = re.sub(r'([=+-])\s*X\^', r'\1 1 * X^', polynomial_clean)
    
    # Feed our cleanly modified string back into the pipeline assignment
    normalized_poly = polynomial_clean

    return normalized_poly

def validate_input_syntax(expression: str) -> bool:
    """Bonus 1: Free-Form Syntax & Vocabulary Error Management"""
    # 1. Allowed vocabulary check
    allowed_chars = "0123456789Xx^ *+-=."
    for char in expression:
        if char not in allowed_chars:
            print(f"Syntax Error: Invalid character '{char}' detected.")
            return False

    # 2. Equal sign count check
    equal_count = sum(1 for char in expression if char == '=')
    if equal_count != 1:
        print(f"Syntax Error: Equation must contain exactly one '=' sign. Found {equal_count}.")
        return False

    # 3. Split sides and check for empty sides
    sides = expression.split('=')
    left_side = sides[0].strip()
    right_side = sides[1].strip()
    
    if not left_side or not right_side:
        print("Syntax Error: Equation cannot have an empty side.")
        return False
        
    # 4. CRITICAL FIX: Check the trailing character of BOTH sides individually!
    # This catches "2 * X^ = 0" because the left side ends with '^'
    # This also catches "5 * X^0 + = 0" because the left side ends with '+'
    operators = "+-*/^"
    if left_side[-1] in operators or right_side[-1] in operators:
        print("Syntax Error: Equation cannot contain a dangling or naked operator.")
        return False

    # 4B. NEW FIX: Check the LEADING character of BOTH sides individually!
    # A side cannot start with '*', or '^'. 
    # (It CAN start with '+' or '-' for negative/positive coefficients).
    illegal_leading_ops = "*^"
    if left_side[0] in illegal_leading_ops or right_side[0] in illegal_leading_ops:
        print("Syntax Error: Equation cannot start with a dangling multiplier or exponent operator.")
        return False

    # 5. Extra structural check: Make sure '^' is always followed by a digit AND Fixed structural check: Ensure '^' is followed STRICTLY by a whole integer power
    # (Just in case there are spaces like "X^ + 2 = 0")
    # 5. Fixed structural check: Ensure '^' is followed STRICTLY by a whole integer power
    for i, char in enumerate(expression):
        if char == '^':
            # Isolate the text following the caret
            after_caret = expression[i+1:]
            
            # Extract characters up until we hit a space, operator, or boundary
            exponent_chars = []
            for idx, c in enumerate(after_caret):
                # Allow a minus sign ONLY if it's the absolute first character after '^'
                if c == '-' and idx == 0:
                    exponent_chars.append(c)
                elif c in "0123456789.": # Collect numbers and dots
                    exponent_chars.append(c)
                elif c in " +=-": # Stop tracking the exponent when hitting boundaries
                    break
                else:
                    break
            
            exponent_str = "".join(exponent_chars).strip()
            
            # Check A: Make sure it's not empty OR just a naked minus sign (e.g., "X^ = 0" or "X^- = 0")
            if not exponent_str or exponent_str == "-":
                print("Syntax Error: Naked exponent hook detected. '^' must be followed by a power.")
                return False
                
            # Check B: Catch negative exponents cleanly (e.g., "X^-2")
            if exponent_str.startswith('-'):
                print(f"Syntax Error: Invalid exponent '{exponent_str}'. Negative exponent powers are strictly forbidden.")
                return False
                
            # Check C: Catch float/decimal exponents (e.g., "X^2.5")
            if '.' in exponent_str:
                print(f"Syntax Error: Invalid exponent '{exponent_str}'. Fractional or float exponents are strictly forbidden.")
                return False
                
            # Check D: Ensure the isolated exponent string is purely an integer
            if not exponent_str.isdigit():
                print(f"Syntax Error: Invalid exponent power '{exponent_str}'. Must be a whole non-negative integer.")
                return False
    # ==============================================================================
    # 6. CRITICAL ADDITION: Strict Term Structural Validation
    # ==============================================================================
    # Check for consecutive operators directly in the original expression string first
    # This immediately stops things like "--5", "+ -", or "* -"
    # We strip out whitespace to see if symbols are back-to-back
    compact_expr = "".join(expression.split())
    
    # Track operator combinations
    for i in range(len(compact_expr) - 1):
        curr = compact_expr[i]
        nxt = compact_expr[i+1]
        
        # A multiplication or caret cannot be followed immediately by a sign or operator
        # This catches "2 * -X^1" or "5 * +X^1" or "X^*2"
        if curr in "*^" and nxt in "+-*/^":
            print(f"Syntax Error: Invalid operator sequence '{curr}{nxt}' detected.")
            return False
            
        # Signs (+ or -) cannot be back-to-back
        # This catches "--5" or "+ -" or "- -"
        if curr in "+-" and nxt in "+-":
            print(f"Syntax Error: Consecutive signs '{curr}{nxt}' are strictly forbidden.")
            return False

    # Now run token checks by replacing boundaries with spaces to isolate strings
    raw_expression = expression.replace('=', ' + ').replace('-', ' + ')
    terms = [t.strip() for t in raw_expression.split('+') if t.strip()]

    for term in terms:
        # Check A: Catch multiple multiplication symbols in a single term (e.g., "2 * 3 * X^1")
        if term.count('*') > 1:
            print(f"Syntax Error: Malformed term '{term}'. Multiple '*' multipliers are strictly forbidden.")
            return False
            
        # Check B: Catch multiple exponent caret symbols in a single term (e.g., "1 * X^1^2")
        if term.count('^') > 1:
            print(f"Syntax Error: Malformed term '{term}'. Multiple '^' exponent components are strictly forbidden.")
            return False
            
        # Check C: Catch missing operators between constants and variables (e.g., "X^0  2")
        # Ensure a term containing 'X' doesn't have broken spaces separating raw numbers
        if 'X' in term or 'x' in term:
            parts = term.split('*')
            for part in parts:
                sub_parts = part.split()
                if len(sub_parts) > 1:
                    print(f"Syntax Error: Disconnected components '{part}' inside term. Missing operator.")
                    return False
                    
    return True

def print_intermediate_steps(a:float, b: float, c: float, delta: float = None, special_state: str = None, degree: int = None):
    if a.is_integer():
        a = int(a)
    if b.is_integer():
        b = int(b)
    if c.is_integer():
        c = int(c)
    print("--- [INTERMEDIATE CALCULATION STEPS] ---")
    
    # Handle the High Degree Error step
    if special_state == "EXCEEDED_DEGREE":
        print(f"Step 1: Analyzed system variables and found maximum power exponent.")
        print(f"        Detected Polynomial Degree: {degree}")
        print(f"Step 2: Degree {degree} > 2. Halting solver execution path.")
        return

    # Handle Identity / Infinite Solutions step
    if special_state == "INFINITE_SOLUTIONS":
        print(f"Step 1: Reduced equation format down completely.")
        print(f"        Resulting Identity: 0 * X^0 = 0 (or 0 = 0)")
        print(f"Step 2: Statement is universally true for any value assigned to X.")
        return

    # Handle Parallel Contradiction / No Solution step
    if special_state == "NO_SOLUTION":
        print(f"Step 1: Reduced equation format down completely.")
        print(f"        Resulting Contradiction: {c} = 0 (where constant value != 0)")
        print(f"Step 2: Mathematically impossible statement. No value of X can satisfy this balance.")
        return

    # --- Your standard degree 1 & 2 logic continues cleanly below here ---
    print(f"Step 1: Extracted Coefficients -> a = {a}, b = {b}, c = {c}")
    if delta is not None:
        print(f"Step 2: Apply Discriminant Formula -> Delta = b² - 4ac")
        print(f"        Delta = ({b})² - 4 * ({a}) * ({c}) = {delta}")
        if delta > 0:
            print("Step 3: Delta > 0 -> Two distinct real solutions via (-b ± √Δ) / 2a")
        elif delta == 0:
            print("Step 3: Delta = 0 -> One unique real solution via -b / 2a")
        else:
            print("Step 3: Delta < 0 -> Two distinct complex solutions via (-b ± i√|Δ|) / 2a")
    else:
        print("Step 2: Linear Equation (Degree 1) -> Isolate X via -c / b")


def get_natural_reduced_form(terms: dict) -> str:
    """Bonus 3: Natural Variable Expression (Clean Reduced Form Layout)"""
    parts = []
    sorted_degrees = sorted(list(terms.keys()))
    
    # --- NEW: Mapping table for superscript numbers ---
    superscripts = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
    
    for deg in sorted_degrees:
        coeff = terms[deg]
        if coeff == 0.0:
            continue
            
        if len(parts) > 0:
            sign_str = "+ " if coeff > 0 else "- "
            display_coeff = -coeff if coeff < 0 else coeff
        else:
            sign_str = "" if coeff >= 0 else "-"
            display_coeff = -coeff if coeff < 0 else coeff

        # Convert float to clean string representation immediately
        abs_val_str = str(int(display_coeff)) if display_coeff.is_integer() else str(display_coeff)
        
        # Check for numerical 1/1.0 value directly to hide it on variables
        clean_coeff = "" if (display_coeff == 1.0 and deg != 0) else abs_val_str

        if deg == 0:
            term_str = abs_val_str
        elif deg == 1:
            term_str = f"{clean_coeff}X"
        else:
            # --- UPDATED: Converts any degree (like 2, 3, 4, 12) into superscripts ---
            deg_str = str(deg).translate(superscripts)
            term_str = f"{clean_coeff}X{deg_str}"
            
        parts.append(f"{sign_str}{term_str}")
        
    if not parts:
        return "0 = 0"
        
    reduced_str = ""
    for idx, part in enumerate(parts):
        reduced_str += part if idx == 0 else f" {part}"
        
    return f"{reduced_str} = 0"


def format_as_irreducible_fraction(decimal_value: float) -> str:
    """Bonus 4: Irreducible Fraction Converter"""
    if decimal_value == int(decimal_value):
        return f"{int(decimal_value)}"
        
    def get_custom_gcd(x: int, y: int) -> int:
        while y:
            x, y = y, x % y
        return -x if x < 0 else x

    precision_multiplier = 100000000
    numerator = int(round(decimal_value * precision_multiplier))
    denominator = precision_multiplier
    
    common_factor = get_custom_gcd(numerator, denominator)
    reduced_num = numerator // common_factor
    reduced_den = denominator // common_factor
    
    if reduced_den > 10000:
        return f"{cp.format_solution(decimal_value)}"
        
    return f"{reduced_num}/{reduced_den}"


def print_time(parse_time: float, reduce_time: float, solve_time: float, total_time: float):
    """
    Bonus 5: High-Precision Engine Performance Profiler
    Accepts raw delta timestamps (seconds) and prints them out in milliseconds.
    """
    print("--- [ENGINE PERFORMANCE BENCHMARK] ---")
    # Multiplying by 1000 converts raw seconds into clean milliseconds (ms)
    print(f"Parsing & Tokenization Stage : {parse_time * 1000:.3f} ms")
    print(f"Equation Reduction Matrix    : {reduce_time * 1000:.3f} ms")
    print(f"Core Mathematical Solver     : {solve_time * 1000:.3f} ms")
    print(f"Total Pipeline Execution Time: {total_time * 1000:.3f} ms")
    print("--------------------------------------\n")