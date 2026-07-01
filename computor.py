import argparse
import bonus as bonus
import time
import sys

bonus_var = 0

def abs_custom(value: float) -> float:
    return -value if value < 0 else value

def sqrt_babylonian(n, iterations=20):

    if n == 0:
        return 0.0
    # Initial guess
    x = n / 2

    # Babylonian method
    for _ in range(iterations):
        x = (x + n / x) / 2

    return x

def polynomial_parser(polynomial: str) -> dict:
    # Initialize our dictionary to store the variable part degrees and accumulated coefficients
    equation_terms = {}

    # Setup the structural state flags we discussed
    side_sign = 1      # 1 for left_side, -1 for right_side
    current_op = 1     # 1 for '+', -1 for '-'

    # Normalize whitespace chaos completely
    normalized_poly = " ".join(polynomial.split())

    # --- BONUS FEATURE: FREE FORM ENTRY NORMALIZATION ---
    if bonus_var:
        normalized_poly = bonus.free_form_entry_normalization(normalized_poly)
    # -----------------------------------------------------


    # Step 2: Tighten the inner components of the Variable Part (handling ^)
    compact_exp = normalized_poly.replace(' ^ ', '^').replace('^ ', '^').replace(' ^', '^')

    # Glue coefficients to their variable parts explicitly 
    compact_poly = compact_exp.replace(' * ', '*').replace('* ', '*').replace(' *', '*')

    # Create precise token boundaries around valid delimiters
    cleaned_poly = compact_poly.replace('=', ' = ').replace('+', ' + ').replace('-', ' - ')
    tokens = cleaned_poly.split()

    # Tokenization / Lexical Analysis Loop
    i = 0
    while i < len(tokens):
        token = tokens[i]

        # Check if we hit the assignment operator boundary
        if token == '=':
            side_sign = -1   # Change state to right_side (invert all upcoming signs)
            current_op = 1   # Reset the default operator flag for the first term on RHS
            i += 1
            continue

        # Check if we hit a sign delimiter that signals a new term
        elif token == '+':
            current_op = 1
            i += 1
            continue
        elif token == '-':
            current_op = -1
            i += 1
            continue

        # If it's not an operator or =, it must be a valid term matching "a * X^p"
        else:
            term_str = token

            # Extract the Coefficient and the Variable Part (the degree)
            # Split by the '*' character to isolate both components
            parts = term_str.split('*')
            coefficient = float(parts[0])
            if len(parts) == 1:
                degree = 0
            else:
                # Isolate the degree from the variable part (e.g., "X^2" -> 2)
                variable_part = parts[1]
                degree = int(variable_part.split('^')[1])

            # Apply your sign rule: coefficient * operator sign * side multiplier
            final_coefficient = coefficient * current_op * side_sign

            # Insertion / Accumulation Phase
            if degree in equation_terms:
                # Update the value of the current degree if it already exists
                equation_terms[degree] += final_coefficient
            else:
                # Create a new pair with the initial value
                equation_terms[degree] = final_coefficient

            i += 1

    return equation_terms

def format_solution(value: float) -> str:
    """Formats the solution: removes trailing .0 for integers, rounds to 6 decimals max."""
    if value.is_integer():
        return str(int(value))
        
    rounded_value = round(value, 6)
    
    if rounded_value.is_integer():
        return str(int(rounded_value))
        
    return str(rounded_value)

class Equation:
    def __init__(self, raw_terms: dict):
        """
        The prune logic runs instantly when the object is created
        Removes all terms whose accumulated coefficient is exactly 0.0.
        This simplifies the dictionary so we only look at active mathematical terms.
        """
        self.terms = raw_terms

    def get_terms(self) -> dict:
        return self.terms

    def get_degree(self) -> int:
        if not self.terms:
            return 0
        return max(self.terms.keys())

    def get_reduced_form(self) -> str:

        max_degree = self.get_degree()
        parts = []

        for deg in range(max_degree + 1):
            coeff = self.terms.get(deg, 0.0)
            coeff_str = f"{int(coeff)}" if coeff.is_integer() else f"{coeff}"

            if deg == 0:
                parts.append(f"{coeff_str} * X^0")
            else:
                if coeff >= 0:
                    parts.append(f"+ {coeff_str} * X^{deg}")
                else:
                    neg_coeff_str = coeff_str.lstrip('-')
                    parts.append(f"- {neg_coeff_str} * X^{deg}")

        return "Reduced form: " + " ".join(parts) + " = 0"

    def prune_zero_coefficients(self):
        """
        The prune logic runs instantly when the object is created
        Removes all terms whose accumulated coefficient is exactly 0.0.
        This simplifies the dictionary so we only look at active mathematical terms.
        """
        self.terms = {deg: coeff for deg, coeff in self.terms.items() if coeff != 0.0}

    def is_infinite_solution_state(self) -> bool:
        """
        Case 1: If the dictionary is completely empty after pruning, it means
        everything perfectly cancelled out (0 = 0). Every real number is a solution.
        """
        return not self.terms

    def is_exceeding_max_degree(self) -> bool:
        """
        Case 2: Checks if there is any active degree strictly greater than 2.
        Since we only look at remaining active keys, things like X^3 - X^3 will 
        already be pruned out, ensuring zero false positives.
        """
        if not self.terms:
            return False
        return self.get_degree() > 2

    def is_no_solution_state(self) -> bool:
        """
        Case 3: If all variables vanished, leaving exactly one constant term 
        that does not equal zero (N = 0), the equation is impossible.
        """
        return len(self.terms) == 1 and 0 in self.terms

    def is_degree_1(self) -> bool:
        return self.get_degree() == 1

    def solve_degree_1(self):
        # Fetch coefficients: b is for X^1, c is for X^0
        b = self.terms.get(1, 0.0)
        c = self.terms.get(0, 0.0)
        a = 0.0
        # Calculate the single linear solution
        solution = -c / b

        if bonus_var:
            bonus.print_intermediate_steps(a, b, c)
        print("The solution is:")
        if solution == 0.0:
            solution = 0.0
        # Bonus 4 Integration
        fraction_str = bonus.format_as_irreducible_fraction(solution)
        if "/" in fraction_str and bonus_var: # Only print if it actually reduced to a fraction representation
            print(f"{format_solution(solution)} ({fraction_str})")
        else:
            print(format_solution(solution))
        print("-----------------------------------------\n")

    def calculate_delta(self) -> float:
        # Safely fetch coefficients from the pruned dictionary, defaulting to 0.0 if missing
        a = self.terms.get(2, 0.0)
        b = self.terms.get(1, 0.0)
        c = self.terms.get(0, 0.0)
        # Delta = b^2 - 4ac
        return (b * b) - (4 * a * c)

    def solve_degree_2_delta_zero(self):
        # Fetch the coefficients from your pruned dictionary
        a = self.terms.get(2, 0.0)
        b = self.terms.get(1, 0.0)
        c = self.terms.get(0, 0.0)
        # Calculate the single double solution
        solution = -b / (2 * a)

        if bonus_var:
            bonus.print_intermediate_steps(a, b, c, 0)
        print("Discriminant is zero, the unique solution is:")
        if solution == 0.0:
            solution = 0.0
        # Bonus 4 Integration
        fraction_str = bonus.format_as_irreducible_fraction(solution)
        if "/" in fraction_str and bonus_var: # Only print if it actually reduced to a fraction representation
            print(f"{format_solution(solution)} ({fraction_str})")
        else:
            print(format_solution(solution))
        print("-----------------------------------------\n")
    
    def solve_degree_2_delta_positive(self, delta: float):
        # Fetch the coefficients from your pruned dictionary
        a = self.terms.get(2, 0.0)
        b = self.terms.get(1, 0.0)
        c = self.terms.get(0, 0.0)

        # 1. Compute the square root of delta using your Babylonian function
        sqrt_delta = sqrt_babylonian(delta)
        
        # 2. Calculate both distinct real solutions
        sol1 = (-b + sqrt_delta) / (2 * a)
        sol2 = (-b - sqrt_delta) / (2 * a)
        
        # --- ADD SANITIZATION HERE (Only inside the positive delta block) ---
        if sol1 == 0.0: sol1 = 0.0
        if sol2 == 0.0: sol2 = 0.0
        # --------------------------------------------------------------------
        # Print Bonus if bonus
        if bonus_var:
            bonus.print_intermediate_steps(a, b, c, delta)

        # 3. Print the results matching the expected format
        print("Discriminant is strictly positive, the two solutions are:")
        frac1 = bonus.format_as_irreducible_fraction(sol1)
        frac2 = bonus.format_as_irreducible_fraction(sol2)

        # Print sol1 with its fraction accompaniment if it has one
        if "/" in frac1 and bonus_var:
            print(f"{format_solution(sol1)} ({frac1})")
        else:
            print(format_solution(sol1))

        # Print sol2 with its fraction accompaniment if it has one
        if "/" in frac2 and bonus_var:
            print(f"{format_solution(sol2)} ({frac2})")
        else:
            print(format_solution(sol2))
        print("-----------------------------------------\n")

    def solve_degree_2_delta_negative(self, delta: float):
        a = self.terms.get(2, 0.0)
        b = self.terms.get(1, 0.0)
        c = self.terms.get(0, 0.0)
    
        # 1. Flip delta to positive using basic math
        abs_delta = -delta
        
        # 2. Extract the square root using your Babylonian function
        sqrt_abs_delta = sqrt_babylonian(abs_delta)
        
       # 3. Separate real and imaginary components
        real_part = -b / (2 * a)
        imaginary_part = sqrt_abs_delta / (2 * a)
        
        # Clean up the exact -0.0 edge case numerically before string conversion
        if real_part == 0.0:
            real_part = 0.0
        
        imaginary_coeff = abs_custom(imaginary_part)
        
        if bonus_var:
            bonus.print_intermediate_steps(a, b, c, delta)    

        print("Discriminant is strictly negative, the two complex solutions are:")
        
        # Format string components cleanly using your helper function
        r_str = format_solution(real_part)
        i_str = format_solution(imaginary_coeff)
        
        if real_part == 0.0:
            print(f"{i_str} * i")
            print(f"-{i_str} * i")
        else:
            print(f"{r_str} + {i_str} * i")
            print(f"{r_str} - {i_str} * i")        

        if bonus_var:
            # Pass raw numeric floats to the fraction calculator instead of strings
            real_frac = bonus.format_as_irreducible_fraction(real_part)
            imag_frac = bonus.format_as_irreducible_fraction(imaginary_coeff)

            if "/" in real_frac or "/" in imag_frac:
                print(f"As irreducible complex fractions:")
                if real_part == 0.0:
                    print(f"{imag_frac} * i")
                    print(f"-{imag_frac} * i")
                else:
                    print(f"{real_frac} + {imag_frac} * i")
                    print(f"{real_frac} - {imag_frac} * i")
            
        print("-----------------------------------------\n")



def computorv1(polynomial: str) -> str:
    
    start_total = time.perf_counter()
    
    #Benchmark the Parsing Stage 
    start_parse = time.perf_counter()
    if bonus_var:
        if not (bonus.validate_input_syntax(polynomial)):
            end_parse = time.perf_counter()
            end_total = time.perf_counter()
            bonus.print_time(end_parse - start_parse, 0, 0, end_total - start_total)
            return   
    equation_terms = polynomial_parser(polynomial)

    end_parse = time.perf_counter()

    #Benchmark the Reduction Stage
    start_reduce = time.perf_counter()

    eq = Equation(equation_terms)

    eq.prune_zero_coefficients()
    print(eq.get_reduced_form())

    print(f"Polynomial degree: {eq.get_degree()}")

    end_reduce = time.perf_counter()

    #Benchmark the Solver Stage
    start_solve = time.perf_counter()

    if bonus_var:
        print(f"Natural reduced form: {bonus.get_natural_reduced_form(eq.get_terms())}")

    # eq.prune_zero_coefficients()

    if eq.is_exceeding_max_degree():
        if bonus_var:
            bonus.print_intermediate_steps(0, 0, 0, None, "EXCEEDED_DEGREE", eq.get_degree())
        print("The polynomial degree is strictly greater than 2, I can't solve.")
        print("-----------------------------------------\n")
        end_solve = time.perf_counter()
        end_total = time.perf_counter()
        if bonus_var:
            bonus.print_time(end_parse - start_parse, end_reduce - start_reduce, end_solve - start_solve, end_total - start_total)
        return

    if eq.is_infinite_solution_state():
        if bonus_var:
            bonus.print_intermediate_steps(0, 0, 0, None, "INFINITE_SOLUTIONS")
        print("Any real number is a solution.")
        print("-----------------------------------------\n")
        end_solve = time.perf_counter()
        end_total = time.perf_counter()
        if bonus_var:
            bonus.print_time(end_parse - start_parse, end_reduce - start_reduce, end_solve - start_solve, end_total - start_total)
        return

    if eq.is_no_solution_state():
        if bonus_var:
            bonus.print_intermediate_steps(0, 0, eq.terms.get(0, 0.0), None, "NO_SOLUTION")
        print("No solution.")
        print("-----------------------------------------\n")
        end_solve = time.perf_counter()
        end_total = time.perf_counter()
        if bonus_var:
            bonus.print_time(end_parse - start_parse, end_reduce - start_reduce, end_solve - start_solve, end_total - start_total)
        return

    if eq.is_degree_1():
        eq.solve_degree_1()
        if bonus_var:
            end_solve = time.perf_counter()
            end_total = time.perf_counter()
            bonus.print_time(end_parse - start_parse, end_reduce - start_reduce, end_solve - start_solve, end_total - start_total)
        return

    Delta = eq.calculate_delta()

    if -1e-9 < Delta < 1e-9:
        Delta = 0.0  # Force it to a clean 0.0
        eq.solve_degree_2_delta_zero()
        if bonus_var:
            end_solve = time.perf_counter()
            end_total = time.perf_counter()
            bonus.print_time(end_parse - start_parse, end_reduce - start_reduce, end_solve - start_solve, end_total - start_total)
        return

    if Delta > 0:
        eq.solve_degree_2_delta_positive(Delta)
        if bonus_var:
            end_solve = time.perf_counter()
            end_total = time.perf_counter()
            bonus.print_time(end_parse - start_parse, end_reduce - start_reduce, end_solve - start_solve, end_total - start_total)
        return

    eq.solve_degree_2_delta_negative(Delta)
    end_solve = time.perf_counter()
    end_total = time.perf_counter()
    if bonus_var:
        bonus.print_time(end_parse - start_parse, end_reduce - start_reduce, end_solve - start_solve, end_total - start_total)
    return

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="computorv1",
        description="Solves polynomial equations of degree <= 2.",
        epilog='Example: python3 computorv1.py "5 * X^0 + 4 * X^1 = 4 * X^0" --bonus',
    )
    parser.add_argument(
        "equation",
        nargs="?",
        default=None,
        help='The polynomial equation to solve (e.g. "5 * X^0 + 4 * X^1 = 4 * X^0"). '
             "If omitted, it will be read from stdin.",
    )
    parser.add_argument(
        "-b", "--bonus",
        action="store_true",
        help="Enable bonus features: free-form entry, syntax error management, "
             "irreducible fractions, intermediate steps and performance benchmarking.",
    )
    return parser.parse_args()
 
 
def main():
    global bonus_var
 
    args = parse_arguments()
    bonus_var = args.bonus  # driven by --bonus on the command line, no longer hardcoded
    equation = "0 * X ^ 20 + 1 * X ^ 1 = 0"
    equation = args.equation if args.equation is not None else input("> ")

# def main():
#     test_string = "0 * X ^ 20 + 1 * X ^ 1 = 0"
#     test_string = "2 * 3 * X^1 + 3 * X ^ 4 = 2 * X^1"
#     if len(sys.argv) > 2:
#         print("Error: Invalid number of arguments.")
#         print("Usage1: python3 computorv1.py")
#         print("Usage2: python3 computorv1.py \"<equation_string>\"")
#         sys.exit(1) # Exit with an error status code
#     elif len(sys.argv) < 2:
#         test_string = input("> ")
#     else:
#         test_string = sys.argv[1]
    computorv1(equation)
    return

if __name__ == "__main__":
    main()
