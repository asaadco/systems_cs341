import json
import math
original_data = ""
reconstructed_data = ""

with open('Temp100_asaad_JP2000_vals.json') as f:
   original_data = json.load(f)
   real_data = list(original_data["messages"])

# print(original_data)

with open('Temp100_VidCodecs.json') as f:
   reconstructed_data = json.load(f)
   recon_data = list(reconstructed_data["messages"])


MSE = 0
for i in range(0, 100):
    msg_MSE = 0
    for j in range(len(real_data[i][66]["value"])):
        msg_MSE = msg_MSE + (real_data[i][66]["value"][j]-recon_data[i][66]["value"][j])**2
    print("MSE per message: ", msg_MSE/1038825.0)
    MSE = MSE + msg_MSE/1038825.0
print("MSE: ", MSE/100.0)