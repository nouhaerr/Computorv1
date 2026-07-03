import computor 
computor.bonus_var = 0
from computor import computorv1


def main():
    # ==============================================================================
    # 1. DEGREE 0 CASES (Edge Cases / Edge Validation)
    # ==============================================================================
    print("\n--- Running Category 1: Degree 0 ---")
    
    # Infinite solutions (0 = 0)
    computorv1("0 * X^0 = 0")
    computorv1("3 * X^0 = 3 * X^0")
    
    # Impossible / No solution (e.g., 5 = 0 or 8 = 3)
    computorv1("5 * X^0 = 0")
    computorv1("8 * X^0 = 3 * X^0")


    # ==============================================================================
    # 2. DEGREE 1 CASES (Linear Equations - Always 1 Solution)
    # ==============================================================================
    print("\n--- Running Category 2: Degree 1 ---")
    
    # Standard positive
    computorv1("4 * X^1 + 8 * X^0 = 0")
    
    # Value reduction across equal sign
    computorv1("5 * X^0 + 4 * X^1 = 12 * X^0")
    
    # Negative variable coefficient
    computorv1("6 * X^0 = 2 * X^1")
    
    # Fractional output
    computorv1("3 * X^1 - 7 * X^0 = 0")
    
    # Scrambled input terms order
    computorv1("14 * X^0 + 2 * X^1 = 0")
    
    # Hidden Degree 1 (Highest non-zero degree is 1, X^2 collapses)
    computorv1("0 * X^2 + 3 * X^1 + 9 * X^0 = 0")


    # ==============================================================================
    # 3. DEGREE 2: DELTA EQUAL TO ZERO (Exactly 1 Unique Real Solution)
    # ==============================================================================
    print("\n--- Running Category 3: Degree 2 (Delta = 0) ---")
    
    # Classic perfect square trinomial (X - 3)^2 = 0
    computorv1("1 * X^0 - 6 * X^1 + 9 * X^2 = 0")
    
    # Flipped sign perfect square trinomial (X + 1)^2 = 0
    computorv1("1 * X^2 + 2 * X^1 + 1 * X^0 = 0")
    
    # Non-1 leading coefficient perfect square (2X - 4)^2 = 0
    computorv1("16 * X^0 - 16 * X^1 + 4 * X^2 = 0")
    
    # Fractional unique solution (2X + 1)^2 = 0
    computorv1("4 * X^2 + 4 * X^1 + 1 * X^0 = 0")
    
    # Terms split across assignment operator
    computorv1("1 * X^2 = 4 * X^1 - 4 * X^0")


    # ==============================================================================
    # 4. DEGREE 2: DELTA STRICTLY POSITIVE (Exactly 2 Real Solutions)
    # ==============================================================================
    print("\n--- Running Category 4: Degree 2 (Delta > 0) ---")
    
    # Clean integer perfect square root outcomes
    computorv1("2 * X^0 - 3 * X^1 + 1 * X^2 = 0")
    
    # Large positive delta via negative constant
    computorv1("1 * X^2 - 1 * X^1 - 6 * X^0 = 0")
    
    # The standard subject example case (Floating-point output testing)
    computorv1("5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0")
    
    # Large numbers testing Babylonian square root accuracy
    computorv1("2 * X^2 - 10 * X^1 = 48 * X^0")
    
    # Missing X^1 component (b = 0)
    computorv1("1 * X^2 - 9 * X^0 = 0")
    
    # Negative leading coefficient (a < 0)
    computorv1("-1 * X^2 + 5 * X^1 - 4 * X^0 = 0")


    # ==============================================================================
    # 5. DEGREE 2: DELTA STRICTLY NEGATIVE (Exactly 2 Complex Solutions)
    # ==============================================================================
    print("\n--- Running Category 5: Degree 2 (Delta < 0) ---")
    
    # Standard complex layout with clean integers
    computorv1("5 * X^0 + 2 * X^1 + 1 * X^2 = 0")
    
    # Pure imaginary layout (b = 0), tests your updated 'real_part == 0.0' formatting rule!
    computorv1("1 * X^2 + 4 * X^0 = 0")
    
    # Negative leading coefficient (a < 0) with complex pair
    computorv1("-2 * X^0 + 2 * X^1 - 1 * X^2 = 0")
    
    # Fractional / irrational complex decimals
    computorv1("1 * X^0 + 1 * X^1 + 2 * X^2 = 0")
    
    # Displaced components across assignment operator
    computorv1("1 * X^2 + 4 * X^1 = -13 * X^0")


    # ==============================================================================
    # 6. HIGH DEGREE ERROR HANDLING (Degrees strictly greater than 2)
    # ==============================================================================
    print("\n--- Running Category 6: High Degrees (Errors) ---")
    
    # Standard standalone high degree error
    computorv1("1 * X^3 = 0")
    
    # Complex polynomial containing a high active power
    computorv1("2 * X^0 - 3 * X^1 + 4 * X^2 - 1 * X^3 + 5 * X^4 = 0")
    
    # High degree component that does NOT cancel out
    computorv1("1 * X^3 + 2 * X^2 = 1 * X^1")
    
    # Hidden High Degree (An active high degree component hidden on the right side)
    computorv1("0 * X^3 = -5 * X^4")


    # ==============================================================================
    # 7. EXTREME PARSING COMPONENT EDGES (Empty inputs, out-of-order, duplicates)
    # ==============================================================================
    print("\n--- Running Category 7: Extreme Parser Edges ---")
    
    # Duplicate terms of same exponent on same side (Must sum up correctly)
    computorv1("1 * X^1 + 2 * X^1 + 3 * X^0 + 1 * X^0 = 0")
    
    # Completely scrambled presentation format
    computorv1("4 * X^2 + 2 * X^0 - 3 * X^1 + 1 * X^2 = 4 * X^1")
    
    # Multi-term cancellation collapsing to lower systems
    # (Looks like Degree 3, but X^3 cancels out completely to leave a Degree 2!)
    computorv1("1 * X^3 + 1 * X^2 = 1 * X^3 - 4 * X^0")

if __name__ == "__main__":
    main()