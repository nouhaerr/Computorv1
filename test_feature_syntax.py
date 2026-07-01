import computor 
computor.bonus_var = 1
from computor import computorv1


def run_test(title, expr):
    print("\n==============================")
    print(title)
    print(expr)
    print("==============================")
    computorv1(expr)


def main():

    # ==============================================================================
    # CATEGORY 1: ILLEGAL VOCABULARY TOKENS
    # ==============================================================================

    run_test("TEST 1: lowercase variable", "5 * x^0 = 0")
    run_test("TEST 2: multiple variables", "5 * X^0 + 2 * Y^1 = 0")
    run_test("TEST 3: illegal division operator", "5 * X^0 / 2 = 0")
    run_test("TEST 4: random text input", "hello world = 0")
    run_test("TEST 5: emoji injection", "5 * X^0 😀 + 2 * X^1 = 0")
    run_test("TEST 6: SQL-like injection attempt", "DROP TABLE X = 0")
    run_test("TEST 7: unicode math symbols", "5 × X^0 + 2 ÷ X^1 = 0")


    # ==============================================================================
    # CATEGORY 2: EQUAL SIGN VIOLATIONS
    # ==============================================================================

    run_test("TEST 8: missing '='", "5 * X^0 + 2 * X^1")
    run_test("TEST 9: double '='", "5 * X^0 = 2 * X^1 = 0")
    run_test("TEST 10: triple '='", "5 * X^0 = 2 * X^1 = 0 = 3")
    run_test("TEST 11: empty string", "")


    # ==============================================================================
    # CATEGORY 3: STRUCTURE ERRORS
    # ==============================================================================

    run_test("TEST 12: empty RHS", "5 * X^0 + 2 * X^1 = ")
    run_test("TEST 13: empty LHS", " = 5 * X^0")
    run_test("TEST 14: only '='", "=")
    run_test("TEST 15: only spaces", "     ")
    run_test("TEST 16: only operators", "+ - * / =")
    run_test("TEST 17: trailing operator", "5 * X^0 + 2 * X^1 +")
    run_test("TEST 18: leading operator", "+ 5 * X^0 + 2 * X^1 = 0")


    # ==============================================================================
    # CATEGORY 4: EXPONENT CORRUPTION
    # ==============================================================================

    run_test("TEST 19: missing exponent", "5 * X^ = 0")
    run_test("TEST 20: double caret", "5 * X^^2 = 0")
    run_test("TEST 21: non-numeric exponent", "5 * X^a = 0")
    run_test("TEST 22: negative exponent", "5 * X^-2 = 0")
    run_test("TEST 23: float exponent", "5 * X^2.5 = 0")
    # run_test("TEST 24: huge exponent", "5 * X^999999999 = 0")


    # ==============================================================================
    # CATEGORY 5: NUMERIC EDGE CASES
    # ==============================================================================

    run_test("TEST 25: leading zeros", "0005 * X^0 + 0002 * X^1 = 0")
    run_test("TEST 26: negative constant", "-5 = 0")
    run_test("TEST 27: messy negatives", "--5 * X^0 + - -2 * X^1 = 0")
    run_test("TEST 28: decimals", "5.5 * X^0 + 2.2 * X^1 = 0")
    run_test("TEST 29: scientific notation", "1e3 * X^0 + 2e-2 * X^1 = 0")
    run_test("TEST 30: all zeros", "0 * X^0 + 0 * X^1 + 0 = 0")


    # ==============================================================================
    # CATEGORY 6: MIXED CHAOS INPUTS
    # ==============================================================================

    run_test("TEST 31: valid + garbage", "5 * X^0 + hello + 2 * X^1 = 0")
    run_test("TEST 32: broken exponent", "5 * X^2 + 3 * X^ = 0")
    run_test("TEST 33: extra equals", "5 * X^2 + 3 * X^1 = 0 = garbage")
    run_test("TEST 34: invalid symbol", "5 * X^2 + 3 * @X^1 = 0")


    # ==============================================================================
    # CATEGORY 7: STRESS TESTS
    # ==============================================================================

    run_test("TEST 35: long polynomial", " + ".join(["2 * X^2"] * 1000) + " = 0")
    run_test("TEST 36: huge noise string", "A" * 5000 + " = 0")
    run_test("TEST 37: operator spam", "+++++-----*****===== X = 0")
    run_test("TEST 38: broken tokens", "5 X 6 Y 7 Z = 0")
    run_test("TEST 39: repeated equation", ("5 * X^0 + 2 * X^1 = 0 = ") * 100)
    run_test("TEST 40: near garbage structure", "X^0 X^1 X^2 = X X X")

if __name__ == "__main__":
    main()