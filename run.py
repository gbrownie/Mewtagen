from dialgarithm.dialgarithm import *

tick = time.perf_counter()
Model.set_hyperparameters(182, 2, 0.175, 0.008)
setup_with_user_input()
# setup_without_user_input()
evolve()
output()
print("TOTAL TOOK:", time.perf_counter() - tick)
