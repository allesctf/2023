import license_checker

assert license_checker.check_license(16622592611469926682) == 2
assert license_checker.check_license(8710154033956414455) == 1
assert license_checker.check_license(31337) == 0
