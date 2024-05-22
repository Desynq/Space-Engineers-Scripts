import numexpr as ne

def calculate_expression(expression):
	try:
		# Evaluate the expression using numexpr
		result = ne.evaluate(expression)
		return float(result)
	except Exception as e:
		print(f"Error evaluating expression: {e}")
		return None

def calculate_mass(force_expression, gravity=9.81):
	# Convert force from kilonewtons to newtons
	force_kN = calculate_expression(force_expression)
	if force_kN is None:
		return None
	force_newton = force_kN * 1000
	
	# Calculate the mass using the formula m = F / g
	mass_kg = force_newton / gravity
	
	return mass_kg

def kg_to_kilotons(kg):
	return kg / 1_000

def main():

	# Take inputs for gravity and force
	# gravity = float(input("Enter gravity (m/s^2): "))
	force_kN = input("Enter force (kN): ")
	
	# Calculate the mass
	mass = calculate_mass(force_kN)
	
	print(f"The mass that can be lifted is {mass:,.0f} kg")
	mass = kg_to_kilotons(mass)
	print(f"The mass that can be lifted is {mass:,.2f} kt\n\n")


if __name__ == "__main__":
	while True:
		main()