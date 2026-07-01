from computorv1 import computorv1

def main():
    # ==============================================================================
    # CATEGORY 1: LINEAR FRACTIONS (Degree 1)
    # ==============================================================================

    # 1. Simple fraction (Result: 1/2)
    # 2 * X = 1 -> X = 1/2
    print("\n--- TEST 1: Clean Positive Fraction ---")
    computorv1("2 * X^1 - 1 * X^0 = 0")

    # 2. Negative fraction reduction (Result: -3/4)
    # 4 * X = -3 -> X = -3/4
    print("\n--- TEST 2: Negative Fraction ---")
    computorv1("4 * X^1 + 3 * X^0 = 0")

    # 3. Improper fraction where numerator > denominator (Result: 7/3)
    # 3 * X = 7 -> X = 7/3
    print("\n--- TEST 3: Improper Fraction (Num > Den) ---")
    computorv1("3 * X^1 = 7 * X^0")

    # 4. Large reduction needed (Result: 1/4)
    # 100 * X = 25 -> X = 25/100 -> 1/4
    print("\n--- TEST 4: Unreduced Fraction Matrix ---")
    computorv1("100 * X^1 - 25 * X^0 = 0")

    # 5. Flat integer edge case (Result: 3)
    # 2 * X = 6 -> X = 6/2 = 3 (Should NOT show a '/' fraction format!)
    print("\n--- TEST 5: Perfect Integer Division ---")
    computorv1("2 * X^1 - 6 * X^0 = 0")


    # ==============================================================================
    # CATEGORY 2: QUADRATIC RATIONAL ROOTS (Degree 2, Positive Delta)
    # ==============================================================================

    # 6. Two clean fractional roots (Result: 1/2 and -1/3)
    # (2X - 1)(3X + 1) = 6X^2 - X - 1 = 0
    print("\n--- TEST 6: Two Real Fractional Roots ---")
    computorv1("6 * X^2 - 1 * X^1 - 1 * X^0 = 0")

    # 7. Roots sharing a denominator (Result: 3/2 and -3/2)
    # 4X^2 - 9 = 0 -> X^2 = 9/4 -> X = 3/2, -3/2
    print("\n--- TEST 7: Plus/Minus Rational Roots ---")
    computorv1("4 * X^2 - 9 * X^0 = 0")

    # 8. Decimals that evaluate to perfect fractions (Result: 4/5 and 1/2)
    # 10X^2 - 13X + 4 = 0 -> Roots: 0.8 (4/5) and 0.5 (1/2)
    print("\n--- TEST 8: Fractional Roots from Floating Point Coefficients ---")
    computorv1("10.0 * X^2 - 13.0 * X^1 + 4.0 * X^0 = 0")


    # ==============================================================================
    # CATEGORY 3: QUADRATIC DOUBLE ROOTS (Degree 2, Delta Zero)
    # ==============================================================================

    # 9. Single unique fractional root (Result: 1/3)
    # (3X - 1)^2 = 9X^2 - 6X + 1 = 0 -> Unique solution: 1/3
    print("\n--- TEST 9: Unique Double Root Fraction ---")
    computorv1("9 * X^2 - 6 * X^1 + 1 * X^0 = 0")

    # 10. Larger scaled double root fraction (Result: -5/2)
    # (2X + 5)^2 = 4X^2 + 20X + 25 = 0 -> Unique solution: -5/2
    print("\n--- TEST 10: Negative Double Root Fraction ---")
    computorv1("4 * X^2 + 20 * X^1 + 25 * X^0 = 0")


    # ==============================================================================
    # CATEGORY 4: COMPLEX RATIONAL ROOTS (Degree 2, Negative Delta)
    # ==============================================================================

    # 11. Pure imaginary rational fractions (Result: 0 + 2/3 * i and 0 - 2/3 * i)
    # 9X^2 + 4 = 0 -> X^2 = -4/9 -> X = +- sqrt(-4/9) = +- 2/3 * i
    print("\n--- TEST 11: Pure Imaginary Fraction ---")
    computorv1("9 * X^2 + 4 * X^0 = 0")

    # 12. Complete complex fraction pairs (Result: -1/2 + 3/4 * i and -1/2 - 3/4 * i)
    # 16X^2 + 16X + 13 = 0 -> Real part: -16/32 = -1/2. Imaginary part: sqrt(576)/32 = 24/32 = 3/4
    print("\n--- TEST 12: Split Complex Rational Fractions ---")
    computorv1("16 * X^2 + 16 * X^1 + 13 * X^0 = 0")


    # ==============================================================================
    # CATEGORY 5: BARE DELIMITERS & EQUATION REDUCTION TRAPS
    # ==============================================================================

    # 13. Linear fraction hidden across both sides of the '=' operator (Result: -4/3)
    # 5X + 2 = 2X - 2 -> 3X = -4 -> X = -4/3
    print("\n--- TEST 13: Scrambled Linear Fraction ---")
    computorv1("5 * X^1 + 2 * X^0 = 2 * X^1 - 2 * X^0")

    # 14. Bare constant fraction on the right-hand side (Result: 1/3)
    # 6X = 2 -> X = 2/6 = 1/3
    print("\n--- TEST 14: Bare Constant on RHS Trap ---")
    computorv1("6 * X^1 = 2")

if __name__ == "__main__":
    main()