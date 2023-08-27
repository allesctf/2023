from pyboolector import *
btor = Boolector()
btor.Set_opt(BTOR_OPT_MODEL_GEN, True)
(result, status, error_msg) = btor.Parse("log.smt2")
print("Expect: sat")
print("Boolector: ", end='')
if result == btor.SAT:
    print("sat")
elif result == btor.UNSAT:
    print("unsat")
else:
    print("unknown")
print("")
btor.Print_model("btor")

flag = [btor.Match_by_symbol(f"flag{i}") for i in range(1032)]
for f in flag:
    print(chr(int(f.assignment,2)), end="")
print()