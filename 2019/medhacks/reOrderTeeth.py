def reOrderTeeth():

    f = open("teethCleaningOrder.txt")
    fileList = f.read().split()
    open("toothOrder.txt", "w").close()  # Clears txt file
    g = open("toothOrder.txt", "w")

    toothPositions = [["Right_maxillary_3rd_molar", "(22, 26)"],  # [Name, position tuple (x,y)]
                      ["Right_maxillary_2nd_molar", "(128, 70)"],
                      ["Right_maxillary_1st_molar", "(224, 48)"],
                      ["Right_maxillary_1st_bicuspid", "(392, 38)"],
                      ["Right_maxillary_2nd_bicuspid", "(329, 47)"],
                      ["Right_maxillary_cuspid", "(454, -14)"],
                      ["Right_maxillary_lateral_incisor", "(526, 14)"],
                      ["Right_maxillary_central_incisor", "(582, -10)"],
                      ["Left_maxillary_central_incisor", "(649, -15)"],
                      ["Left_maxillary_lateral_incisor", "(719, 31)"],
                      ["Left_maxillary_cuspid", "(772, 0)"],
                      ["Left_maxillary_1st_bicuspid", "(841, 8)"],
                      ["Left_maxillary_2nd_bicuspid", "(904, 12)"],
                      ["Left_maxillary_1st_molar", "(972, 41)"],
                      ["Left_maxillary_2nd_molar", "(1069, 47)"],
                      ["Left_maxillary_3rd_molar", "(1167, 43)"],
                      ["Right_mandibular_3rd_molar", "(7, 300)"],
                      ["Right_mandibular_2nd_molar", "(110, 303)"],
                      ["Right_mandibular_1st_molar", "(206, 272)"],
                      ["Right_mandibular_1st_bicuspid", "(395, 303)"],
                      ["Right_mandibular_2nd_bicuspid", "(323, 290)"],
                      ["Right_mandibular_cuspid", "(467, 289)"],
                      ["Right_mandibular_lateral_incisor", "(538, 284)"],
                      ["Right_mandibular_central_incisor", "(597, 279)"],
                      ["Left_mandibular_central_incisor", "(651, 268)"],
                      ["Left_mandibular_lateral_incisor", "(700, 286)"],
                      ["Left_mandibular_cuspid", "(754, 265)"],
                      ["Left_mandibular_1st_bicuspid", "(834, 292)"],
                      ["Left_mandibular_2nd_bicuspid", "(904, 295)"],
                      ["Left_mandibular_1st_molar", "(963, 306)"],
                      ["Left_mandibular_2nd_molar", "(1075, 300)"],
                      ["Left_mandibular_3rd_molar", "(1173, 306)"]]

    for i in range(len(fileList)):
        for j in range(len(toothPositions)):
            if fileList[i] == toothPositions[j][0]:
                g.write(str(i+1).ljust(20) + fileList[i].ljust(40) + toothPositions[j][1] + "\n")
                # Write the file as     number  name    tuple(x,y)
