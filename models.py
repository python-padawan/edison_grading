# Contain the constant Model values for running the UI Metrics
rootDir = "D:\\Jenkins\\workspace\\UI Metrics\\src\\"
EstimateModels = {"Standard":{"Estimated SLR":3870,
                              "HLR Ratio":.95,
                              "LLR Ratio":1.4,
                              "TS Ratio":.2,
                              "HLTC Ratio":3.3,
                              "HLTP Ratio":(1/7),
                              "LLTC Ratio":1.5,
                              "LLTP Ratio":(1/7),
                              "Code Ratio":(1/1.75)}}

# import Estimate Models from the FeatureModels.csv
with open(rootDir + "FeatureModels.csv", "r") as csv_file:
    import csv
    csv_reader = csv.DictReader(csv_file)
    print(csv_reader.fieldnames)
    for row in csv_reader:
        EstimateModels[row["Name"]] = {"Estimated SLR":int(row["Estimated SLR"]),
                              "HLR Ratio":float(row["HLR Ratio"]),
                              "LLR Ratio":float(row["LLR Ratio"]),
                              "TS Ratio":float(row["TS Ratio"]),
                              "HLTC Ratio":float(row["HLTC Ratio"]),
                              "HLTP Ratio":float(row["HLTP Ratio"]),
                              "LLTC Ratio":float(row["LLTC Ratio"]),
                              "LLTP Ratio":float(row["LLTP Ratio"]),
                              "Code Ratio":float(row["Code Ratio"])}

hoursPerHlr = 4
hoursPerLlr = 5.5
hoursPerHlTc = 3
hoursPerLlTc = 1.5
hoursPerLlTp = 2.5*7 #Official cost model is gives cost for LLTP in terms of LLTC (2.5 hr/LLTC), multiply by ratio (7 LLTC per LLTP) gets you to cost per LLTP.
hoursPerHlTp = 1.95*7 #Official cost model gives cost for HLTP in terms of HLTC (1.95 hr/HLTC), multiply by ratio (7 HLTC per HLTP) gets you to cost per HLTP.
hoursPerCode = 5.5*1.75 #Official cost model gives cost for SWM in terms of LLR (5.5 hr/LLR for SWM creation) , multiply by ratio (1.75 LLR per SWM) gets you to cost per SWM EX. (1.75 LLR/1 SWM)*(5.5 hr/ 1 LLR) = 5.5*1.75 hr/SWM.

#Percent of work to get to each TRL level
CostModel = {"HLR":{1:.20 * hoursPerHlr,
                    2:.07 * hoursPerHlr,
                    3:.1 * hoursPerHlr,
                    4:.16 * hoursPerHlr,
                    5:.1 * hoursPerHlr,
                    6:.09 * hoursPerHlr,
                    7:.16 * hoursPerHlr,
                    8:.04 * hoursPerHlr,
                    9:.08 * hoursPerHlr},
             "HLTC":{1:.02 * hoursPerHlTc,
                    2:.07 * hoursPerHlTc,
                    3:.17 * hoursPerHlTc,
                    4:.12 * hoursPerHlTc,
                    5:.11 * hoursPerHlTc,
                    6:.13 * hoursPerHlTc,
                    7:.23 * hoursPerHlTc,
                    8:.05 * hoursPerHlTc,
                    9:.1 * hoursPerHlTc},
             "HLTP":{1:.02 * hoursPerHlTp,
                    2:.02 * hoursPerHlTp,
                    3:.02 * hoursPerHlTp,
                    4:.02 * hoursPerHlTp,
                    5:.15 * hoursPerHlTp,
                    6:.23 * hoursPerHlTp,
                    7:.39 * hoursPerHlTp,
                    8:.08 * hoursPerHlTp,
                    9:.07 * hoursPerHlTp},
             "LLR":{1:.1 * hoursPerLlr,
                    2:.15 * hoursPerLlr,
                    3:.06 * hoursPerLlr,
                    4:.15 * hoursPerLlr,
                    5:.16 * hoursPerLlr,
                    6:.11 * hoursPerLlr,
                    7:.11 * hoursPerLlr,
                    8:.09 * hoursPerLlr,
                    9:.07 * hoursPerLlr},
             "LLTC":{1:.08 * hoursPerLlTc,
                    2:.08 * hoursPerLlTc,
                    3:.08 * hoursPerLlTc,
                    4:.08 * hoursPerLlTc,
                    5:.09 * hoursPerLlTc,
                    6:.11 * hoursPerLlTc,
                    7:.31 * hoursPerLlTc,
                    8:.07 * hoursPerLlTc,
                    9:.1 * hoursPerLlTc},
             "LLTP":{1:.07 * hoursPerLlTp,
                    2:.07 * hoursPerLlTp,
                    3:.07 * hoursPerLlTp,
                    4:.07 * hoursPerLlTp,
                    5:.11 * hoursPerLlTp,
                    6:.12 * hoursPerLlTp,
                    7:.22 * hoursPerLlTp,
                    8:.1 * hoursPerLlTp,
                    9:.17 * hoursPerLlTp},
             "Code":{1:.07 * hoursPerCode,
                    2:.07 * hoursPerCode,
                    3:.07 * hoursPerCode,
                    4:.07 * hoursPerCode,
                    5:.11 * hoursPerCode,
                    6:.12 * hoursPerCode,
                    7:.22 * hoursPerCode,
                    8:.1 * hoursPerCode,
                    9:.17 * hoursPerCode}}
CostModelCombined = {}
for level in CostModel:
    CostModelCombined[level] = {}
    total = 0
    for trl in CostModel[level]:
        total += CostModel[level][trl]
        CostModelCombined[level][trl] = total
