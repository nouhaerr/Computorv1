import computor 
computor.bonus_var = 1
from computor import computorv1

def main():
    # ==============================================================================
    # CATEGORY 1: IMPLICIT COEFFICIENTS (Naked X^p)
    # ==============================================================================

    # 1. Pure naked quadratic (Should translate to: 1*X^2 + 1*X^1 - 6*X^0 = 0)
    print("\n--- TEST 1: Naked Variables Matrix ---")
    computorv1("X^2 + X^1 - 6 = 0")

    # 2. Leading naked term with no sign (Should translate to: 1*X^2)
    print("\n--- TEST 2: Leading Naked Term ---")
    computorv1("X^2 - 4 = 0")

    # 3. Naked term directly after assignment operator
    print("\n--- TEST 3: Naked Term on RHS Boundary ---")
    computorv1("4 * X^1 = X^2")


    # ==============================================================================
    # CATEGORY 2: IMPLICIT EXPONENTS (Naked X or x)
    # ==============================================================================

    # 4. Standard lowercase linear variable (Should translate to: 4*X^1 - 3*X^0 = 0)
    print("\n--- TEST 4: Lowercase Naked Linear x ---")
    computorv1("4 * x - 3 = 0")

    # 5. Mixed uppercase naked variable with implicit coefficient (Should handle: 1*X^1)
    print("\n--- TEST 5: Naked Coefficient + Naked Exponent Combo ---")
    computorv1("X^2 + X - 12 = 0")

    # 6. Negative naked linear term boundary
    print("\n--- TEST 6: Negative Naked Variable ---")
    computorv1("5 * X^2 - X + 2 = 0")


    # ==============================================================================
    # CATEGORY 3: MISSING MULTIPLICATION MARKS (Juxtaposition)
    # ==============================================================================

    # 7. Coefficient glued directly to variable (Should translate to: 4*X^2 - 1*X^0 = 0)
    print("\n--- TEST 7: Glued Coefficient and Exponent ---")
    computorv1("4X^2 - 1 = 0")

    # 8. Decimals glued directly to naked lowercase variable (Should translate to: 2.5*X^1)
    print("\n--- TEST 8: Glued Decimal to Naked x ---")
    computorv1("2.5x + 5 = 0")

    # 9. Scrambled glued elements on both sides
    print("\n--- TEST 9: Scrambled Glued Terms across Boundary ---")
    computorv1("3X^2 + 2x = 5X^1 + 1")


    # ==============================================================================
    # CATEGORY 4: COMPACT NO-SPACE CHAOS
    # ==============================================================================

    # 10. Zero whitespace script string (Tests split boundaries)
    print("\n--- TEST 10: Zero Whitespace Script ---")
    computorv1("X^2+4X-5=0")

    # 11. Negative coefficients with zero spaces
    print("\n--- TEST 11: Negative Zero Whitespace Chaos ---")
    computorv1("-2X^2-3x+2=0")


    # ==============================================================================
    # CATEGORY 5: COMPLEX RATIONAL & FRACTION VALIDATION
    # ==============================================================================

    # 12. Free form reducing to clean fractional outputs (Result: 1/2 and -1/3)
    # 6X^2 - X - 1 = 0
    print("\n--- TEST 12: Free Form with Rational Roots ---")
    computorv1("6x^2 - x = 1")

    # 13. Double root fraction in free form (Result: -5/2)
    # 4x^2 + 20x + 25 = 0
    print("\n--- TEST 13: Free Form Double Root Fraction ---")
    computorv1("4X^2 + 20X = -25")


    # ==============================================================================
    # CATEGORY 6: EDGE CASE IMMUNITY CHECKS (Should NOT match false positives)
    # ==============================================================================

    # 14. Ensure safe translation doesn't alter things that are already correct
    print("\n--- TEST 14: Strict Syntax Safety Check ---")
    computorv1("1.0 * X^1 = 1.0 * X^1 + 1.0 * X^0")

    # 15. Ensure constant numbers don't inadvertently get treated as degrees
    print("\n--- TEST 15: Pure Floating Constants Check ---")
    computorv1("x^2 + 10.5 = 20.5")

if __name__ == "__main__":
    main()