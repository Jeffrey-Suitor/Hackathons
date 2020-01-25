f=open("MLTrainingData.txt", "w+")

for i in range(200):
    f.write("gbmask_np_"+str(i)+".png image_"+str(i)+".png\n")
