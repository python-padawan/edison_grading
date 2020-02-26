import json
import os
from json.decoder import NaN
from math import ceil
from cmath import nan
import Models
import CostActual

DEBUG = False
CurrentRatios = {}
ThemeData = {}
ReleaseData = {}
TeamData ={}
FeatureData = {}
BP5ChartData = {}
HoursData = {}

sourceDir = "D:\\Jenkins\\workspace\\UI_Metrics\\src\\"
rootDir = "D:\\Jenkins\\workspace\\UI_Metrics\\Results\\"


def RunMetrics(rootDir, sourceDir, UpdateBox=False):
    """
    Description: Creates metric report based on Theme, Release, and Team using UI requirements.
    Parameters:
        rootDir - Directory of UI_Metrics results
        sourceDir - Directory of UI_Metrics source
        UpdateBox - Boolean flag used to determine if files should be copied to Box syching directory.
        Return: None    
    """

    
    DateTag = ""
    with open(sourceDir + 'UI_Metrics-Derived.json') as json_file:
        data = json.load(json_file)
        for module in data:
            DateTag = createDerivedRequirementMaturityReport(module)

        with open(rootDir + "All\\" + DateTag + "\\UI_Metrics-Derived.json", "w") as copy_file:
            json.dump(data, copy_file, indent=4)
    with open(sourceDir + 'UI_Metrics.json') as json_file:
        data = json.load(json_file)
        for feature in data:
            DateTag = createFeatureMaturityReport(feature)

        with open(rootDir + "All\\" + DateTag + "\\UI_Metrics.json", "w") as copy_file:
            json.dump(data, copy_file, indent=4)
    createThemeReport()
    createReleaseReport()
    createTeamReport()
# Load Existing Data and append the new data
    data = {}
    with open(rootDir + "ChartData.json") as json_file:
        data = json.load(json_file)
        data[DateTag] = BP5ChartData
    with open(rootDir + "ChartData.json", "w") as json_file:
        json.dump(data, json_file, indent=4)
    Rotated = {}
    for date in data:
        for group in data[date]:
            if group not in Rotated:
                Rotated[group] = {"Teams":data[date][group]["Teams"]}
            for item in ["HLR", "V&V"]:
                if item not in Rotated[group]:
                    Rotated[group][item] = {}
                for orrCategory in data[date][group][item]:
                    if orrCategory not in Rotated[group][item]:
                        Rotated[group][item][orrCategory] = {}
                    for datum in data[date][group][item][orrCategory]:
                        if datum not in Rotated[group][item][orrCategory]:
                            Rotated[group][item][orrCategory][datum] = {}
                        Rotated[group][item][orrCategory][datum][date] = data[date][group][item][orrCategory][datum]
    with open(rootDir + "CurrentRatios.csv", "w") as csv_file:
        csv_file.write("Name, SLRs, HLR Ratio, LLR Ratio, TS Ratio, HLTC Ratio, HLTP Ratio\n")
        for name in CurrentRatios:
            csv_file.write('"'+name+'", '+str(len(CurrentRatios[name][0]))+", "+str((CurrentRatios[name][1]))+", "+str((CurrentRatios[name][2]))+", "+str((CurrentRatios[name][3]))+", "+str((CurrentRatios[name][4]))+", "+str((CurrentRatios[name][5]))+"\n")

    with open(rootDir + "ChartDataRotated.csv", "w") as csv_file:
        csv_file.write("Feature,Team 1,Team 2, Team 3, Team 4, Team 5, Item,ORR Category,Datum,")
        dates = ("2019-02-11","2019-02-12","2019-02-13","2019-02-14","2019-02-15","2019-02-16","2019-02-17",
                 "2019-02-18","2019-02-19","2019-02-20","2019-02-21","2019-02-22","2019-02-23","2019-02-24",
                 "2019-02-25","2019-02-26","2019-02-27","2019-02-28","2019-03-01","2019-03-02","2019-03-03",
                 "2019-03-04","2019-03-05","2019-03-06","2019-03-07","2019-03-08","2019-03-09","2019-03-10",
                 "2019-03-11","2019-03-12","2019-03-13","2019-03-14","2019-03-15","2019-03-16","2019-03-17")
        for date in dates:
            csv_file.write(date + ",")

        csv_file.write("\n")
        for group in Rotated:
            for item in Rotated[group]:
                if item != "Teams":
                    for orrCategory in Rotated[group][item]:
                        for datum in Rotated[group][item][orrCategory]:
                            csv_file.write(group + ",")
                            for team in Rotated[group]["Teams"]:
                                csv_file.write(str(team) + ",")

                            csv_file.write(item + "," + orrCategory + "," + datum + ",")
                            for date in dates:
                                if date in Rotated[group][item][orrCategory][datum]:
                                    csv_file.write(str(Rotated[group][item][orrCategory][datum][date]) + ",")
                                else:
                                    csv_file.write(",")

                            csv_file.write("\n")
    with open(rootDir + "HoursData.csv", "w") as csv_file:
        header = "Theme, FeatureName, Group, Datum,"
        for aml in ["AML1","AML2","AML3","AML4","AML5","AML6","AML7","AML8","AML9"]:
            header+=aml+" Remaining,"+aml +" Estimated,"
        csv_file.write(header+"\n")
        for feature in HoursData:
            totalData = {"AML1":{"Remaining":0.0,"Estimated":0.0},
                         "AML2":{"Remaining":0.0,"Estimated":0.0},
                         "AML3":{"Remaining":0.0,"Estimated":0.0},
                         "AML4":{"Remaining":0.0,"Estimated":0.0},
                         "AML5":{"Remaining":0.0,"Estimated":0.0},
                         "AML6":{"Remaining":0.0,"Estimated":0.0},
                         "AML7":{"Remaining":0.0,"Estimated":0.0},
                         "AML8":{"Remaining":0.0,"Estimated":0.0},
                         "AML9":{"Remaining":0.0,"Estimated":0.0}}
            RnVData = {"AML1":{"Remaining":0.0,"Estimated":0.0},
                         "AML2":{"Remaining":0.0,"Estimated":0.0},
                         "AML3":{"Remaining":0.0,"Estimated":0.0},
                         "AML4":{"Remaining":0.0,"Estimated":0.0},
                         "AML5":{"Remaining":0.0,"Estimated":0.0},
                         "AML6":{"Remaining":0.0,"Estimated":0.0},
                         "AML7":{"Remaining":0.0,"Estimated":0.0},
                         "AML8":{"Remaining":0.0,"Estimated":0.0},
                         "AML9":{"Remaining":0.0,"Estimated":0.0}}
            DnCData = {"AML1":{"Remaining":0.0,"Estimated":0.0},
                         "AML2":{"Remaining":0.0,"Estimated":0.0},
                         "AML3":{"Remaining":0.0,"Estimated":0.0},
                         "AML4":{"Remaining":0.0,"Estimated":0.0},
                         "AML5":{"Remaining":0.0,"Estimated":0.0},
                         "AML6":{"Remaining":0.0,"Estimated":0.0},
                         "AML7":{"Remaining":0.0,"Estimated":0.0},
                         "AML8":{"Remaining":0.0,"Estimated":0.0},
                         "AML9":{"Remaining":0.0,"Estimated":0.0}}
            if len(HoursData[feature]["Themes"])>1:
                print("********"+feature)
            theme = ""
            for theme in HoursData[feature]["Themes"]:
                for datum in ["HLR","HLTC","HLTP","LLR","LLTC","LLTP","Code"]:
                    dataString = '"'+theme+'","'+feature+'",R&V,'+datum+','
                    if datum =="LLR":
                        dataString = '"'+theme+'","'+feature+'",D&C,'+datum+','

                    #dataString+=str(HoursData[feature][datum]["Percent Complete"])+","
                    for aml in ["AML1","AML2","AML3","AML4","AML5","AML6","AML7","AML8","AML9"]:
                        dataString+=str(HoursData[feature][datum][aml]["Remaining"])+","+str(HoursData[feature][datum][aml]["Estimated"])+","
                        if datum =="LLR" or datum =="LLTC" or datum =="LLTP" or datum =="Code":
                            DnCData[aml]["Remaining"]+=HoursData[feature][datum][aml]["Remaining"]
                            DnCData[aml]["Estimated"]+=HoursData[feature][datum][aml]["Estimated"]
                        else:
                            RnVData[aml]["Remaining"]+=HoursData[feature][datum][aml]["Remaining"]
                            RnVData[aml]["Estimated"]+=HoursData[feature][datum][aml]["Estimated"]
                        totalData[aml]["Remaining"]+=HoursData[feature][datum][aml]["Remaining"]
                        totalData[aml]["Estimated"]+=HoursData[feature][datum][aml]["Estimated"]
                    csv_file.write(dataString+"\n")
            totalString = '"'+theme+'","'+feature+'",All,Total,'
            rnVString = '"'+theme+'","'+feature+'",R&V,Total,'
            dnCString = '"'+theme+'","'+feature+'",D&C,Total,'
            for aml in ["AML1","AML2","AML3","AML4","AML5","AML6","AML7","AML8","AML9"]:
                totalString+=str(totalData[aml]["Remaining"])+","+str(totalData[aml]["Estimated"])+","
                rnVString+=str(RnVData[aml]["Remaining"])+","+str(RnVData[aml]["Estimated"])+","
                dnCString+=str(DnCData[aml]["Remaining"])+","+str(DnCData[aml]["Estimated"])+","
            csv_file.write(rnVString+"\n")
            csv_file.write(dnCString+"\n")
            csv_file.write(totalString+"\n")



    if UpdateBox:
        updateBox(DateTag)

def updateBox(DateTag):
    """
    Description: Updates local file location that is synced with Box.ge.com.
    Parameters:
      DateTag - Date files were generated.
    Return: None    
    """
    import shutil
    sourceBP5Directory = rootDir +"BP5\\"+DateTag+"\\"
    sourceCompleteDirectory = rootDir +"All\\"+DateTag+"\\"

    BoxBP5Directory = "C:/Users/212333709/Box Sync/UI BP5.1.2 Scope/All/"+DateTag+"/"
    BoxBP5CurrentDirectory = "C:/Users/212333709/Box Sync/UI BP5.1.2 Scope/Current/"

    BoxCompleteDirectory = "C:/Users/212333709/Box Sync/Complete UI Metric/All/"+DateTag+"/"
    BoxCompleteCurrentDirectory = "C:/Users/212333709/Box Sync/Complete UI Metric/Current/"

    #Copy Complete Metrics to all
    CopyDir(sourceCompleteDirectory, BoxCompleteDirectory)
    #Clear Complete Current directory
    shutil.rmtree(BoxCompleteCurrentDirectory)
    #Copy Complete Metrics to the Current Folder
    CopyDir(sourceCompleteDirectory, BoxCompleteCurrentDirectory)

    #Copy BP5.1.2 Metrics
    CopyDir(sourceBP5Directory, BoxBP5Directory)
    #Clear Current BP5.1.2 directory
    shutil.rmtree(BoxBP5CurrentDirectory)
    #Copy BP5.1.2 Metrics to the Current Folder
    CopyDir(sourceBP5Directory, BoxBP5CurrentDirectory)

def CopyDir(source, dest):
    """
    Description: Copies files in a directory to a different directory.
    Parameters:
        source - Origin directory
        dest - Destination directory        
    Return: None    
    """

    import shutil
    if os.path.exists(dest):
        shutil.rmtree(dest)
    try:
        shutil.copytree(source, dest)
    # Directories are the same
    except shutil.Error as e:
        print('Directory not copied. Error: %s' % e)
    # Any error saying that the directory doesn't exist
    except OSError as e:
        print('Directory not copied. Error: %s' % e)

def UpdateChartData(group, teams, item, ORRCategory, FeatureData):
    """
    Description: 
    Parameters:
        group - 
        dest -         
    Return:     
    """
    team1 = ""
    team2 = ""
    team3 = ""
    team4 = ""
    team5 = ""
    if "Team 1" in teams:
        team1 = "X"
    if "Team 2" in teams:
        team2 = "X"
    if "Team 3" in teams:
        team3 = "X"
    if "Team 4" in teams:
        team4 = "X"
    if "Team 5" in teams:
        team5 = "X"

    if item == "HLR":
        AML0Count = FeatureData["HLR AML Report"]["AML0"]
        AML1Count = FeatureData["HLR AML Report"]["AML1"]
        AML2Count = FeatureData["HLR AML Report"]["AML2"]
        AML3Count = FeatureData["HLR AML Report"]["AML3"]
        AML4Count = FeatureData["HLR AML Report"]["AML4"]
        AML5Count = FeatureData["HLR AML Report"]["AML5"]
        AML6Count = FeatureData["HLR AML Report"]["AML6"]
        AML7Count = FeatureData["HLR AML Report"]["AML7"]
        AML8Count = FeatureData["HLR AML Report"]["AML8"]
        AML9Count = FeatureData["HLR AML Report"]["AML9"]
        CompCount = FeatureData["HLR AML Report"]["Total"]+len(FeatureData["SLRs w/o HLR"])

        # Initialize Dictionary if not already initialized
        if group not in BP5ChartData:
            BP5ChartData[group]={"Teams":[team1,team2,team3,team4,team5]}
        if item not in  BP5ChartData[group]:
            BP5ChartData[group][item]={}
        if ORRCategory not in BP5ChartData[group][item]:
            BP5ChartData[group][item][ORRCategory] = {}


        if ORRCategory == "Targeted":
            if "Est. Total" not in BP5ChartData[group][item][ORRCategory]:
                # Initalize the count
                BP5ChartData[group][item][ORRCategory]["Est. Total"]=0
                BP5ChartData[group][item][ORRCategory]["AML-0"]=0
                BP5ChartData[group][item][ORRCategory]["AML-1"]=0
                BP5ChartData[group][item][ORRCategory]["AML-2"]=0
                BP5ChartData[group][item][ORRCategory]["AML-3"]=0
                BP5ChartData[group][item][ORRCategory]["AML-4"]=0
                BP5ChartData[group][item][ORRCategory]["AML-5"]=0
                BP5ChartData[group][item][ORRCategory]["AML-6"]=0
                BP5ChartData[group][item][ORRCategory]["AML-7"]=0

            BP5ChartData[group][item][ORRCategory]["Est. Total"]+=CompCount
            BP5ChartData[group][item][ORRCategory]["AML-0"]+=AML0Count
            BP5ChartData[group][item][ORRCategory]["AML-1"]+=AML1Count
            BP5ChartData[group][item][ORRCategory]["AML-2"]+=AML2Count
            BP5ChartData[group][item][ORRCategory]["AML-3"]+=AML3Count
            BP5ChartData[group][item][ORRCategory]["AML-4"]+=AML4Count
            BP5ChartData[group][item][ORRCategory]["AML-5"]+=AML5Count
            BP5ChartData[group][item][ORRCategory]["AML-6"]+=AML6Count
            BP5ChartData[group][item][ORRCategory]["AML-7"]+=AML7Count + AML8Count + AML9Count
        elif ORRCategory == "Active Additional":
            if "Est. Total" not in BP5ChartData[group][item][ORRCategory]:
                # Initalize the count
                BP5ChartData[group][item][ORRCategory]["Est. Total"]=0
                BP5ChartData[group][item][ORRCategory]["AML-0"]=0
                BP5ChartData[group][item][ORRCategory]["AML-1"]=0
                BP5ChartData[group][item][ORRCategory]["AML-2"]=0
                BP5ChartData[group][item][ORRCategory]["AML-3"]=0
                BP5ChartData[group][item][ORRCategory]["AML-4"]=0


            BP5ChartData[group][item][ORRCategory]["Est. Total"]+=CompCount
            BP5ChartData[group][item][ORRCategory]["AML-0"]+=AML0Count
            BP5ChartData[group][item][ORRCategory]["AML-1"]+=AML1Count
            BP5ChartData[group][item][ORRCategory]["AML-2"]+=AML2Count
            BP5ChartData[group][item][ORRCategory]["AML-3"]+=AML3Count
            BP5ChartData[group][item][ORRCategory]["AML-4"]+=AML4Count + AML5Count + AML6Count +AML7Count + AML8Count + AML9Count
        #UpdateChartData(FeatureReport['Name'], "HLR", ORRCategory, FeatureReport)
    elif item == "V&V":
        if group not in BP5ChartData:
            BP5ChartData[group]={}
        if item not in  BP5ChartData[group]:
            BP5ChartData[group][item]={}
        if ORRCategory not in BP5ChartData[group][item]:
            BP5ChartData[group][item][ORRCategory] = {"HLRs w/TP":0}
        BP5ChartData[group][item][ORRCategory]["HLRs w/TP"]+=FeatureData

def updateDict(currentDict, addedDict):
    """
    Description: Utility used to update dictionaries
    Parameters:
        currentDict - 
        addedDict -         
    Return:     
    """
    for key in currentDict:
        if key in addedDict:
            if type(currentDict[key]) == dict:
                currentDict[key].update(addedDict[key])
            elif type(currentDict[key]) == list:
                # If list removed duplicates
                currentDict[key] = list(set(currentDict[key]))
            elif type(currentDict[key]) == int:
                currentDict[key] += addedDict[key]
            elif type(currentDict[key]) == float:
                currentDict[key] += addedDict[key]
            else:
                if currentDict[key] != addedDict[key]:
                    print(key)
                    currentDict[key] = addedDict[key]
        else:
            print("****"+key)

def EmptyDictionary():
    """
    Description: Returns a default dictionary containing a report parameters (i.e SLRs w/o HLR, HLRs w/o SLR)
    Parameters:    None
    Return: 
        result - dictionary of artifact metrics used to indicate completeness
    """

    result = {}
    result["TimeStamp"] = ""
    result["Features"] = {}
    result["Themes"] = list()
    result["Teams"] = list()
    result["Total SLRs"] = {}
    result["UADF-Only SLRs"] ={}
    result["SW SLRs"] = {}
    result["Total HLRs"] = {}
    result["Coverage HLRs"] = {}
    result["Table HLRs"] = {}
    result["Total LLRs"] = {}
    result["Coverage LLRs"] = {}
    result["Total LLTCs"] = {}
    result["Coverage LLTCs"] = {}
    result["Total LLTPs"] = {}
    result["Coverage LLTPs"] = {}
    result["Total TSs"] = {}
    result["Coverage TSs"] = {}
    result["Total HLTCs"] = {}
    result["Coverage HLTCs"] = {}
    result["Total HLTPs"] = {}
    result["Coverage HLTPs"] = {}
    result["Total Code"] = {}
    result["Coverage Code"] = {}
    result["HLR AML Report"] = {}
    result["LLR AML Report"] = {}
    result["HLTC AML Report"] = {}
    result["HLTP AML Report"] = {}
    result["LLTC AML Report"] = {}
    result["LLTP AML Report"] = {}
    result["Code AML Report"] = {}
    result["SLRs w/o HLR"] = {}
    result["HLRs w/o SLR"] = {}
    result["HLRs w/o LLR"] = {}
    result["HLRs w/o TS"] = {}
    result["HLRs w/o TC"] = {}
    result["HLRs w/o TP"] = {}
    result["LLRs w/o Code"] = {}
    result["LLRs w/o TC"] = {}
    result["LLTCs w/o TP"] = {}
    result["TCs w/o TP"] = {}
    result["LLRs w/o HLR"] = {}
    result["Remaining CLRs"] = {}
    result["SLR Estimate"] = 0
    result["SLR Estimate -UADF Only"] = 0
    result["HLR Estimate"] = 0
    result["LLR Estimate"] = 0
    result["HLTC Estimate"] = 0
    result["TS Estimate"] = 0
    result["HLTP Estimate"] = 0
    result["LLTC Estimate"] = 0
    result["LLTP Estimate"] = 0
    result["Code Estimate"] = 0
    return result

def appendLine(text):
    """
    Description: Appends new line.
    Parameters:        
        text - string passed in to be displayed before new line
    Return:     
        text - text entered + new line
    """
    if DEBUG:
        print(text)
    return text + "\n"

def AMLReport(items):
    """
    Description: Gets AMLs for a list of requirements. Calculates average AML.
    Parameters:    
        items - a dictionary of requirements, contains AML per requirement
    Return:     
        result - string describing average AML for the dictionary of requirements provided
    """
    result = ""
    count = [0,0,0,0,0,0,0,0,0,0]
    for obj in items:
        if items[obj]['AML'] == "":
            items[obj]['AML'] = "0"

        aml = int(items[obj]['AML'])

        count[aml]+=1
    aml = 0
    sumT = 0
    total = 0
    repDict = {}
    for i in count:
        result += "    AML " + str(aml) +" : " + str(i)+"\n"
        repDict["AML" + str(aml)] = i
        sumT += i*aml
        total += i
        repDict["Total"] = total
        aml+=1
    if total!=0:
        result = "    Average AML : "+str(sumT/total) +"\n"+ result
    else:
        result = "    Average AML : 0\n" + result
    return result, repDict

def isUI_Hlr(hlr):
    """
    Description: Returns true if the HLR belongs to UI.
    Parameters:
        hlr - HLR object id prefix
    Return: 
        result - determination of whether or not HLR belongs to UI
    """
    result = False

    if hlr['Identifier'].startswith("FMPL.HLR.UI-"):
        result = True
    if hlr['Identifier'].startswith("C919.DTR.HLR-"):
        result = True
    if hlr['Identifier'].startswith("C919.DST.HLR-"):
        result = True
    if hlr['Identifier'].startswith("C919_UI.HLR-"):
        result = True
    if not (hlr['Requirement']=="Decomposed" or hlr['Requirement']=="Derived" or hlr['Requirement']==""):
        result = False
    return result

def ItemByTheme(itemDictionary):
    """
    Description: Gets all items by theme
    Parameters:        
        itemDictionary - dictionary of requirements
    Return:     
        result - dictionary of themes with requirements that were linked to them
    """
    result = {}
    for i in itemDictionary:
        themes = itemDictionary[i]["Theme"].split("|")
        for theme in themes:
            if not theme in result:
                result[theme] = {}
            result[theme][i] = itemDictionary[i]

    return result

def createTeamReport():
    """
    Description: Creates report based on features assigned to teams. Includes metrics on time remaining for each artifact based on AML.
    Parameters:    None    
    Return: None    
    """
    
    print("Team Report")
    for team in TeamData:
        print("_____"+team)

        #Use the "Standard" Estimation Model unless a Team Specific Module is defined
        EstRatios = Models.EstimateModels["Standard"]
        if team in  Models.EstimateModels:
            EstRatios =  Models.EstimateModels[team]

        # Count the Number of UADF-Only SLRs
        TeamData[team]["UADF-Only SLRs"] = 0
        for slr in TeamData[team]["Total SLRs"]:
            if TeamData[team]["Total SLRs"][slr]["UADF Only"]:
                TeamData[team]["UADF-Only SLRs"] += 1

        #Create Artifact Estimates Based on the estimate model


        if team == "All":
            TeamData[team]["SLR Estimate"] = EstRatios["Estimated SLR"]
            TeamData[team]["SLR Estimate -UADF Only"] = ceil(EstRatios["Estimated SLR"]*.05)
            #5% of SLRs are UADF only
            TeamData[team]["HLR Estimate"] = ceil((TeamData[team]["SLR Estimate"]-TeamData[team]["SLR Estimate -UADF Only"]) * EstRatios["HLR Ratio"])
        else:
            TeamData[team]["HLR Estimate"] = ceil((len(TeamData[team]["Total SLRs"])-TeamData[team]["UADF-Only SLRs"]) * EstRatios["HLR Ratio"])
        TeamData[team]["LLR Estimate"] = ceil(TeamData[team]["HLR Estimate"]*EstRatios["LLR Ratio"])
        TeamData[team]["HLTC Estimate"] = ceil(TeamData[team]["HLR Estimate"]*EstRatios["HLTC Ratio"])
        TeamData[team]["TS Estimate"] = ceil(TeamData[team]["HLR Estimate"]*EstRatios["TS Ratio"])
        TeamData[team]["HLTP Estimate"] = ceil(TeamData[team]["HLTC Estimate"]*EstRatios["HLTP Ratio"])

        reportString =  appendLine("==============================================================")
        reportString += appendLine("Executive Report: " + team)
        reportString += appendLine("  as of " + TeamData[team]["TimeStamp"])
        reportString += appendLine("==============================================================")
        reportString += appendLine("Features:")
        for feature in TeamData[team]["Features"]:
            reportString += appendLine("  "+feature)
        reportString += appendLine("==============================================================")
        if team == "All":
            reportString += appendLine(" "+str(TeamData[team]["SLR Estimate"]) + " Estimated SLRs")
            reportString += appendLine(" "+str(TeamData[team]["SLR Estimate -UADF Only"]) + " Estimated UADF Only SLRs")
            reportString += appendLine(" "+str(len(TeamData[team]["Total SLRs"])) + " Current Total SLRs")
            reportString += appendLine(" "+str(TeamData[team]["UADF-Only SLRs"]) + " Current UADF Only SLRs")
        else:
            reportString += appendLine(" "+str(len(TeamData[team]["Total SLRs"])) + " Total SLRs")
            reportString += appendLine(" "+str(TeamData[team]["UADF-Only SLRs"]) + " UADF Only SLRs")
        reportString += appendLine("--------------------------------------------------------------")
        reportString += appendLine(" "+str(len(TeamData[team]["SLRs w/o HLR"])) + " SLRs w/o HLR")
        reportString += appendLine("==============================================================")
        reportString += appendLine(" "+ str(TeamData[team]["HLR Estimate"]) + " Estimated HLRs")
        reportString += appendLine(" "+str(len(TeamData[team]["Total HLRs"])) + " Total HLRs")
        temp, TeamData[team]["HLR AML Report"] = (AMLReport(TeamData[team]["Total HLRs"]))
        reportString += temp
        reportString += appendLine("--------------------------------------------------------------")
        reportString += appendLine(" "+str(len(TeamData[team]["HLRs w/o SLR"])) + " HLR w/o SLR")
        reportString += appendLine("--------------------------------------------------------------")
        reportString += appendLine(" "+str(len(TeamData[team]["HLRs w/o LLR"])) + " HLR w/o LLRs")
        reportString += appendLine("--------------------------------------------------------------")
        reportString += appendLine(" "+str(len(TeamData[team]["HLRs w/o TS"])) + " HLR w/o TS")
        reportString += appendLine("--------------------------------------------------------------")
        reportString += appendLine(" "+str(len(TeamData[team]["HLRs w/o TC"])) + " HLR w/o TC")
        reportString += appendLine("==============================================================")
        reportString += appendLine(" "+ str(TeamData[team]["LLR Estimate"]) + " Estimated LLRs")
        reportString += appendLine(" "+str(len(TeamData[team]["Total LLRs"])) + " Total LLRs")
        temp, TeamData[team]["LLR AML Report"] = (AMLReport(TeamData[team]["Total LLRs"]))
        reportString += temp
        reportString += appendLine("--------------------------------------------------------------")
        reportString += appendLine(" "+str(len(TeamData[team]["LLRs w/o Code"])) + " LLRs w/o Code")
        reportString += appendLine("--------------------------------------------------------------")
        reportString += appendLine(" "+str(len(TeamData[team]["LLRs w/o HLR"])) + " LLRs w/o HLRs")
        reportString += appendLine("==============================================================")
        reportString += appendLine(" "+ str(TeamData[team]["TS Estimate"]) + " Estimated TSs")
        reportString += appendLine(" "+str(len(TeamData[team]["Total TSs"])) + " Total TSs")
        temp, TeamData[team]["TS AML Report"] = (AMLReport(TeamData[team]["Total TSs"]))
        reportString += temp
        reportString += appendLine("==============================================================")
        reportString += appendLine(" "+ str(TeamData[team]["HLTC Estimate"]) + " Estimated TCs")
        reportString += appendLine(" "+str(len(TeamData[team]["Total HLTCs"])) + " Total TCs")
        temp, TeamData[team]["HLTC AML Report"] = (AMLReport(TeamData[team]["Total HLTCs"]))
        reportString += temp
        reportString += appendLine("--------------------------------------------------------------")
        reportString += appendLine(" "+str(len(TeamData[team]["TCs w/o TP"])) + " TCs w/o TPs")

        reportString += appendLine("==============================================================")
        reportString += appendLine(" "+ str(TeamData[team]["HLTP Estimate"]) + " Estimated TPs")
        reportString += appendLine(" "+str(len(TeamData[team]["Total HLTPs"])) + " Total TPs")
        temp, TeamData[team]["HLTP AML Report"] = (AMLReport(TeamData[team]["Total HLTPs"]))
        reportString += temp

        reportString += appendLine("==============================================================")
        reportString += appendLine(" "+ str(TeamData[team]["LLTC Estimate"]) + " Estimated TCs")
        #TODO get Low Level Metrics
        temp, TeamData[team]["LLTC AML Report"] = (AMLReport(list()))
        reportString += temp
        reportString += appendLine("--------------------------------------------------------------")
        reportString += appendLine(" "+str(len(TeamData[team]["TCs w/o TP"])) + " TCs w/o TPs")

        reportString += appendLine("==============================================================")
        reportString += appendLine(" "+ str(TeamData[team]["HLTP Estimate"]) + " Estimated TPs")
        #TODO get Low Level Metrics
        temp, TeamData[team]["LLTP AML Report"] = (AMLReport(list()))
        reportString += temp

        reportString += appendLine("==============================================================")
        reportString += appendLine(" Remaining HLR Work by AML")
        reportString += appendLine("==============================================================")
        reportString +=remainingWorkReport(TeamData[team])

        # Decomposition Ratio
        HlrRatio = NaN
        LlrRatio = NaN
        TcRatio = NaN
        TsRatio = NaN
        try:
            HlrRatio =  len(TeamData[team]["Total HLRs"])/(len(TeamData[team]["Total SLRs"])-TeamData[team]["UADF-Only SLRs"]-len(TeamData[team]["SLRs w/o HLR"]))
        except:
            pass
        try:
            LlrRatio = len(TeamData[team]["Total LLRs"])/(len(TeamData[team]["Total HLRs"])-len(TeamData[team]["HLRs w/o LLR"]))
        except:
            pass
        try:
            TcRatio = len(TeamData[team]["Total HLTCs"])/(len(TeamData[team]["Total HLRs"])-len(TeamData[team]["HLRs w/o TC"]))
        except:
            pass
        try:
            TsRatio = len(TeamData[team]["Total TSs"])/(len(TeamData[team]["Total HLRs"])-len(TeamData[team]["HLRs w/o TS"]))
        except:
            pass
        try:
            LLTCRatio = len(TeamData[team]["Total LLTCs"])/(len(TeamData[team]["Total LLRs"])-len(TeamData[team]["LLRs w/o TC"]))
        except:
            pass
        try:
            LLTPRatio = len(TeamData[team]["Total LLTPs"])/(len(TeamData[team]["Total LLTCs"])-len(TeamData[team]["LLTCs w/o TP"]))
        except:
            pass


        reportString += appendLine("===================================")
        reportString += appendLine("HLR Ratio: "+str(HlrRatio))
        reportString += appendLine("LLR Ratio: "+str(LlrRatio))
        reportString += appendLine("HLTC Ratio: "+str(TcRatio))
        reportString += appendLine("TS Ratio: "+str(TsRatio))
        reportString += appendLine("LLTC Ratio: "+str(LLTCRatio))
        reportString += appendLine("LLTP Ratio: "+str(LLTPRatio))

        reportDir = rootDir +"All\\"+ TeamData[team]["TimeStamp"]+"\\"
        if not os.path.exists(reportDir+"Team\\"):
            os.mkdir(reportDir+"Team\\")
        if not os.path.exists(reportDir+"Team\\Json\\"):
            os.mkdir(reportDir+"Team\\Json\\")

        with open(reportDir+"Team\\Json\\__"+team+".json", "w") as featureOut:
            json.dump(TeamData[team],featureOut, indent=4)

        with open(reportDir+"Team\\"+team+".txt", "w") as featureOut:
            featureOut.write(reportString)

def remainingWorkReport(FeatureReport):
    """
    Description: Calculates remaining work using missing artifacts and cost model.
    Parameters:
        FeatureReport - dictionary of artifact metrics used to indicate completeness, defaulted using EmptyDictionary() function
    Return: 
        reportString - returns remaining HLR Work by AML, LLR Work by AML, HLTC Work by AML, HLTP Work by AML, LLTC Work by AML, LLTP Work by AML, Code Work by AML")
    """
    reportString = ""
    reportString += appendLine("==============================================================")
    reportString += appendLine(" Remaining HLR Work by AML")
    reportString += appendLine("==============================================================")
    countMissingHlrs = ceil(FeatureReport["HLR Estimate"] - len(FeatureReport["Total HLRs"]))
    if countMissingHlrs < 0:
        countMissingHlrs = 0
    temp, FeatureReport["HLR Hours"] = remainingWork(FeatureReport["HLR AML Report"], countMissingHlrs, "HLR", FeatureReport["HLR Estimate"])
    reportString += temp

    reportString += appendLine("==============================================================")
    reportString += appendLine(" Remaining LLR Work by AML")
    reportString += appendLine("==============================================================")
    countMissingLlrs = ceil(FeatureReport["LLR Estimate"] - len(FeatureReport["Total LLRs"]))
    if countMissingLlrs < 0:
        countMissingLlrs = 0
    temp, FeatureReport["LLR Hours"] = remainingWork(FeatureReport["LLR AML Report"], countMissingLlrs, "LLR", FeatureReport["LLR Estimate"])
    reportString += temp

    reportString += appendLine("==============================================================")
    reportString += appendLine(" Remaining HLTC Work by AML")
    reportString += appendLine("==============================================================")
    countMissingTCs = ceil(FeatureReport["HLTC Estimate"] - len(FeatureReport["Total HLTCs"]))
    if countMissingTCs < 0:
        countMissingTCs = 0
    temp, FeatureReport["HLTC Hours"] = remainingWork(FeatureReport["HLTC AML Report"], countMissingTCs, "HLTC", FeatureReport["HLTC Estimate"])
    reportString += temp

    reportString += appendLine("==============================================================")
    reportString += appendLine(" Remaining HLTP Work by AML")
    reportString += appendLine("==============================================================")
    countMissingTps = ceil(FeatureReport["HLTP Estimate"] - len(FeatureReport["Total HLTPs"]))
    if countMissingTps < 0:
        countMissingTps = 0
    temp, FeatureReport["HLTP Hours"] = remainingWork(FeatureReport["HLTP AML Report"], countMissingTps, "HLTP", FeatureReport["HLTP Estimate"])
    reportString += temp

    reportString += appendLine("==============================================================")
    reportString += appendLine(" Remaining LLTC Work by AML")
    reportString += appendLine("==============================================================")
    countMissingTCs = ceil(FeatureReport["LLTC Estimate"])
    if countMissingTCs < 0:
        countMissingTCs = 0
    temp, FeatureReport["LLTC Hours"] = remainingWork(FeatureReport["LLTC AML Report"], countMissingTCs, "LLTC", FeatureReport["LLTC Estimate"])
    reportString += temp

    reportString += appendLine("==============================================================")
    reportString += appendLine(" Remaining LLTP Work by AML")
    reportString += appendLine("==============================================================")
    countMissingTps = ceil(FeatureReport["LLTP Estimate"])
    if countMissingTps < 0:
        countMissingTps = 0
    temp, FeatureReport["LLTP Hours"] = remainingWork(FeatureReport["LLTP AML Report"], countMissingTps, "LLTP", FeatureReport["LLTP Estimate"])
    reportString += temp

    reportString += appendLine("==============================================================")
    reportString += appendLine(" Remaining Code Work by AML")
    reportString += appendLine("==============================================================")
    countMissingCode = ceil(FeatureReport["Code Estimate"])
    if countMissingCode < 0:
        countMissingCode = 0
    temp, FeatureReport["Code Hours"] = remainingWork(FeatureReport["Code AML Report"], countMissingCode, "Code", FeatureReport["Code Estimate"])
    reportString += temp

    return reportString

def createThemeReport():
    """
    Description: Creates text file metric report based on requriements assigned to a theme. Uses cost model to estimate remaining work.
    Parameters:    
        None
    Return:     
        None
    """

    print("Theme Reports")
    for theme in ThemeData:
        print("_____"+theme)

        #Use the "Standard" Estimation Model unless a Theme Specific Module is defined
        EstRatios =  Models.EstimateModels["Standard"]
        if theme in  Models.EstimateModels:
            EstRatios =  Models.EstimateModels[theme]

        # Count the Number of UADF-Only SLRs
        ThemeData[theme]["UADF-Only SLRs"] = list()
        for slr in ThemeData[theme]["Total SLRs"]:
            if ThemeData[theme]["Total SLRs"][slr]["UADF Only"]:
                ThemeData[theme]["UADF-Only SLRs"].append(ThemeData[theme]["Total SLRs"][slr])

        #Create Artifact Estimates Based on the estimate model


        #=======================================================================
        if theme == "All":
            print(len(ThemeData[theme]["Total SLRs"]))
            print(ThemeData[theme]["SLR Estimate -UADF Only"])
            ThemeData[theme]["SLR Estimate"] = EstRatios["Estimated SLR"]
            ThemeData[theme]["SLR Estimate -UADF Only"] = ceil(EstRatios["Estimated SLR"]*.05)
            #5% of SLRs are UADF only
            ThemeData[theme]["New SLRs - SLR Estimate"] = ceil(((ThemeData[theme]["SLR Estimate"]-len(ThemeData[theme]["Total SLRs"])-(ThemeData[theme]["SLR Estimate -UADF Only"]))))
            ThemeData[theme]["New SLRs - HLR Estimate"] = ceil(ThemeData[theme]["New SLRs - SLR Estimate"] * EstRatios["HLR Ratio"])
            ThemeData[theme]["New SLRs - LLR Estimate"] = ceil(ThemeData[theme]["New SLRs - HLR Estimate"]*EstRatios["LLR Ratio"])
            ThemeData[theme]["New SLRs - HLTC Estimate"] = ceil(ThemeData[theme]["New SLRs - HLR Estimate"]*EstRatios["HLTC Ratio"])
            ThemeData[theme]["New SLRs - TS Estimate"] = ceil(ThemeData[theme]["New SLRs - HLR Estimate"]*EstRatios["TS Ratio"])
            ThemeData[theme]["New SLRs - HLTP Estimate"] = ceil(ThemeData[theme]["New SLRs - HLTC Estimate"]*EstRatios["HLTP Ratio"])
            ThemeData[theme]["New SLRs - LLTC Estimate"] = ceil(ThemeData[theme]["New SLRs - LLR Estimate"]*EstRatios["LLTC Ratio"])
            ThemeData[theme]["New SLRs - LLTP Estimate"] = ceil(ThemeData[theme]["New SLRs - LLTC Estimate"]*EstRatios["LLTP Ratio"])
            ThemeData[theme]["New SLRs - Code Estimate"] = ceil(ThemeData[theme]["New SLRs - LLR Estimate"]*EstRatios["Code Ratio"])
            ThemeData[theme]["HLR Estimate"] += ThemeData[theme]["New SLRs - HLR Estimate"]
            ThemeData[theme]["LLR Estimate"] += ThemeData[theme]["New SLRs - LLR Estimate"]
            ThemeData[theme]["TS Estimate"] += ThemeData[theme]["New SLRs - TS Estimate"]
            ThemeData[theme]["HLTC Estimate"] += ThemeData[theme]["New SLRs - HLTC Estimate"]
            ThemeData[theme]["HLTP Estimate"] += ThemeData[theme]["New SLRs - HLTP Estimate"]
            ThemeData[theme]["LLTC Estimate"] += ThemeData[theme]["New SLRs - LLTC Estimate"]
            ThemeData[theme]["LLTP Estimate"] += ThemeData[theme]["New SLRs - LLTP Estimate"]
            ThemeData[theme]["Code Estimate"] += ThemeData[theme]["New SLRs - Code Estimate"]
            temp = EmptyDictionary()
            temp["HLR Estimate"] = ThemeData[theme]["New SLRs - HLR Estimate"]
            temp["LLR Estimate"] = ThemeData[theme]["New SLRs - LLR Estimate"]
            temp["TS Estimate"] = ThemeData[theme]["New SLRs - TS Estimate"]
            temp["HLTC Estimate"] = ThemeData[theme]["New SLRs - HLTC Estimate"]
            temp["HLTP Estimate"] = ThemeData[theme]["New SLRs - HLTP Estimate"]
            temp["LLTC Estimate"] = ThemeData[theme]["New SLRs - LLTC Estimate"]
            temp["LLTP Estimate"] = ThemeData[theme]["New SLRs - LLTP Estimate"]
            temp["Code Estimate"] = ThemeData[theme]["New SLRs - Code Estimate"]
            temp["HLR AML Report"] =AMLReport(list())[1]
            temp["LLR AML Report"] =AMLReport(list())[1]
            temp["HLTC AML Report"] =AMLReport(list())[1]
            temp["HLTP AML Report"] =AMLReport(list())[1]
            temp["LLTC AML Report"] =AMLReport(list())[1]
            temp["LLTP AML Report"] =AMLReport(list())[1]
            temp["Code AML Report"] =AMLReport(list())[1]
            remainingWorkReport(temp)
            HoursData["Undefined"]=  {"Themes":list(["None"]),
                                   "HLR":temp["HLR Hours"],
                                   "LLR":temp["LLR Hours"],
                                   "HLTC":temp["HLTC Hours"],
                                   "LLTC":temp["LLTC Hours"],
                                   "HLTP":temp["HLTP Hours"],
                                   "LLTP":temp["LLTP Hours"],
                                   "Code":temp["Code Hours"]}

        #=======================================================================

        Date = ThemeData[theme]["TimeStamp"]
        reportString =  appendLine("==============================================================")
        reportString += appendLine("Executive Report: " + theme)
        reportString += appendLine("  as of " + Date)
        reportString += appendLine("==============================================================")

        reportString += SlrReport(ThemeData[theme])

        temp, ThemeData[theme]["HLR AML Report"] = HlrReport(ThemeData[theme])
        reportString += temp

        temp, ThemeData[theme]["LLR AML Report"] = LlrReport(ThemeData[theme])
        reportString += temp


        temp, ThemeData[theme]["Code AML Report"] = CodeReport(ThemeData[theme])
        reportString += temp

        temp, ThemeData[theme]["TS AMLs"] = TsReport(ThemeData[theme])
        reportString += temp

        temp, ThemeData[theme]["HLTC AML Report"] = HlTcReport(ThemeData[theme])
        reportString += temp

        temp, ThemeData[theme]["HLTP AML Report"] = HlTpReport(ThemeData[theme])
        reportString += temp

        temp, ThemeData[theme]["LLTC AML Report"] = LlTcReport(ThemeData[theme])
        reportString += temp

        temp, ThemeData[theme]["LLTP AML Report"] = LlTpReport(ThemeData[theme])
        reportString += temp

        reportString += remainingWorkReport(ThemeData[theme])

        reportString += DecompositionRatioReport(ThemeData[theme])


        reportString += ReviewReport(ThemeData[theme])
        reportString += ReviewEstimateReport(ThemeData[theme])
        reportString += ObjectReport(ThemeData[theme])




        reportDir = rootDir +"All\\"+ Date.split(" ")[0]+"\\"
        if not os.path.exists(reportDir+"Theme\\"):
            os.mkdir(reportDir+"Theme\\")
        if not os.path.exists(reportDir+"Theme\\Json\\"):
            os.mkdir(reportDir+"Theme\\Json\\")

        with open(reportDir+"Theme\\Json\\__"+theme.replace("/","_")+".json", "w") as featureOut:
            json.dump(ThemeData[theme],featureOut, indent=4)

        with open(reportDir+"Theme\\"+theme.replace("/","_")+".txt", "w") as featureOut:
            featureOut.write(reportString)

def remainingWork(amlDict, missingCount, Model, EstimatedItems):
    """
    Description: Estimates the Hours remaining to each AML based on the common hours estimate model
                This function does not take in account complexity of the feature because that it
                accounted for in the estimate for number of items
    Parameters:        
        amlDict - Dictionary of AML range (0-10)
        missingCount - count of requirements without a defined AML
        Model - cost model used to estimate remaining work
        EstimatedItems - Number of estimated artifacts to be created from development of feature.
    Return: 
        result - string containing hours remaining and estimated hours by AML and percent complete
        tempDict - dictionary containing hours remaining and estimated hours by AML
    """

    result = "Hours to :\n"
    count = missingCount + amlDict["AML0"]
    estimatedHours = 0
    aml = 1
    hours = 0
    hoursRemaining = 0
    tempDict = {}
    while aml<10:
        hours = count*Models.CostModel[Model][aml]
        estimatedHours += EstimatedItems*Models.CostModel[Model][aml]
        hoursRemaining += hours
        result+= "  AML {0} - {1:.2f} - ({2:.2f})\n".format(aml, hoursRemaining, estimatedHours)
        count += amlDict["AML"+str(aml)]
        tempDict["AML"+str(aml)] = {"Remaining":hoursRemaining, "Estimated":estimatedHours}
        aml+=1

    percentComplete = 0
    if estimatedHours>0:
        percentComplete = (estimatedHours-hoursRemaining)/estimatedHours *100
    tempDict["Percent Complete"] = percentComplete
    result+= "Total % Complete: {0:.2f}\n".format(percentComplete)
    return result, tempDict

def costHlrWork(amlDict, theme):
    """
    Description: Uses Cost Model to calculate the expected, actual, and average cost for HLRs per HLR.
    Parameters:    
        amlDict - Dictionary of AML levels (0-10)
        theme - theme used for HLR calculations
    Return:     
        result - string containing expected, actual, and average cost of work performed.
    """
    
    workModel =  Models.CostModelCombined["HLR"]
    ActualCostWorkPerformed =0
    if theme in CostActual.costs:
        ActualCostWorkPerformed = CostActual.costs[theme]["HLR"]

    ExpectedCostWorkPerformed = 0
    for aml in workModel:
        ExpectedCostWorkPerformed += workModel[aml]*amlDict["AML"+str(aml)]
    CPI = nan
    if ActualCostWorkPerformed != 0:
        CPI = ExpectedCostWorkPerformed/ActualCostWorkPerformed
    result = "--------------------------------------------------------------\n"
    result += "Expected Cost of Work Performed : {0:.1f}\n".format(ExpectedCostWorkPerformed)
    result += "Actual Cost of Work Performed : {0:.1f}\n".format(ActualCostWorkPerformed)
    result += "HLR CPI {0:.3f}\n".format(CPI)
    result += "--------------------------------------------------------------\n"
    result += "HLRs Averaged Cost to:\n"
    for aml in workModel:
        result+= "  AML {0} - {1:.2f}\n".format(aml, workModel[aml]/CPI)
    return result

def costVVWork(TCDict,TPDict, theme):
    """
    Description: Uses Cost Model to calculate the expected, actual, and average cost for high level test cases and high level test procedures.
    Parameters:    
        TCDict - Dictionary of AML levels (0-10)
        TPDict - Dictionary of AML levels (0-10)
        theme - theme used for HLTC & HLTP calculations
    Return:     
        result - string containing expected, actual, and average cost of work performed.
    """
    
    tcWorkModel =  Models.CostModelCombined["HLTC"]
    tpWorkModel =  Models.CostModelCombined["HLTP"]
    ActualCostWorkPerformed = 0
    if theme in CostActual.costs:
        ActualCostWorkPerformed = CostActual.costs[theme]["V&V"]


    ExpectedCostWorkPerformed = 0
    for aml in tcWorkModel:
        ExpectedCostWorkPerformed += tcWorkModel[aml]*TCDict["AML"+str(aml)]

    for aml in tpWorkModel:
        ExpectedCostWorkPerformed += tpWorkModel[aml]*TPDict["AML"+str(aml)]

    CPI = nan
    if ActualCostWorkPerformed != 0:
        CPI = ExpectedCostWorkPerformed/ActualCostWorkPerformed
    result = "--------------------------------------------------------------\n"
    result += "Expected Cost of Work Performed : {0:.1f}\n".format(ExpectedCostWorkPerformed)
    result += "Actual Cost of Work Performed : {0:.1f}\n".format(ActualCostWorkPerformed)
    result += "HLR CPI {0:.3f}\n".format(CPI)
    result += "--------------------------------------------------------------\n"
    result += "Test Case Averaged Cost to:\n"
    for aml in tcWorkModel:
        result+= "  AML {0} - {1:.2f}\n".format(aml, tcWorkModel[aml]/CPI)
    result += "Test Procedure Averaged Cost to:\n"
    for aml in tpWorkModel:
        result+= "  AML {0} - {1:.2f}\n".format(aml, tpWorkModel[aml]/CPI)
    return result

def createReleaseReport():
    """
    Description: Creates executive report of HLR, LLR, TS, HLTC, LLTC, HLTP, LLTP, and Code. Report contains estimated and actual artifacts, and artifacts
    without linked downstream artifacts where applicable.
    Parameters:    None
    Return: None    
    """
    
    print("Release Report")
    for release in ReleaseData:
        print("_____"+release)

        Date = ReleaseData[release]["TimeStamp"]
        reportString =  appendLine("==============================================================")
        reportString += appendLine("Executive Report: " + release)
        reportString += appendLine("  as of " + Date)
        reportString += appendLine("==============================================================")

        reportString += SlrReport(ReleaseData[release])

        temp, ReleaseData[release]["HLR AML Report"] = HlrReport(ReleaseData[release])
        reportString += temp

        temp, ReleaseData[release]["LLR AML Report"] = LlrReport(ReleaseData[release])
        reportString += temp


        temp, ReleaseData[release]["Code AML Report"] = CodeReport(ReleaseData[release])
        reportString += temp

        temp, ReleaseData[release]["TS AMLs"] = TsReport(ReleaseData[release])
        reportString += temp

        temp, ReleaseData[release]["HLTC AML Report"] = HlTcReport(ReleaseData[release])
        reportString += temp

        temp, ReleaseData[release]["HLTP AML Report"] = HlTpReport(ReleaseData[release])
        reportString += temp

        temp, ReleaseData[release]["LLTC AML Report"] = LlTcReport(ReleaseData[release])
        reportString += temp

        temp, ReleaseData[release]["LLTP AML Report"] = LlTpReport(ReleaseData[release])
        reportString += temp

        reportString += remainingWorkReport(ReleaseData[release])

        reportString += DecompositionRatioReport(ReleaseData[release])

        reportString += ObjectReport(ReleaseData[release])

        reportString += ReviewEstimateReport(ReleaseData[release])

        reportDir = rootDir +"All\\"+ Date.split(" ")[0]+"\\"
        if not os.path.exists(reportDir+"Release\\"):
            os.mkdir(reportDir+"Release\\")
        if not os.path.exists(reportDir+"Release\\Json\\"):
            os.mkdir(reportDir+"Release\\Json\\")

        with open(reportDir+"Release\\Json\\__"+release+".json", "w") as featureOut:
            json.dump(ReleaseData[release],featureOut, indent=4)

        with open(reportDir+"Release\\"+release+".txt", "w") as featureOut:
            featureOut.write(reportString)

def reviewString(requirements):
    """
    Description: Returns the review status for a list of requriements
    Parameters:
        requriements - dictionary of requirement containing review status (In Work, ReadyForReview, Reviewed, Complete, Unassigned)
    Return: 
        reportString - string containing report of reqs reviewed for BP512.
        PercentOrrComplete - Percentage of requirements complete using Review Status as indicator
    """
    
    InWork= list()
    ReadyForReview = list()
    Reviewed = list()
    Complete = list()
    Unassigned = list()
    for hlrId in requirements:
        hlr = requirements[hlrId]
        if hlr["Object Status"] == "In Work":
            InWork.append(hlr)
        elif hlr["Object Status"] == "Ready for Review":
            ReadyForReview.append(hlr)
        elif hlr["Object Status"] == "Reviewed":
            Reviewed.append(hlr)
        elif hlr["Object Status"] == "Complete":
            Complete.append(hlr)
        else:
            Unassigned.append(hlr)
    OrrComplete = list()
    OrrIncomplete = list()
    for hlr in Reviewed:
        if hlr["BP5.1.2 Reviewed?"] == "Y":
            OrrComplete.append(hlr)
        else:
            OrrIncomplete.append(hlr)
    for hlr in Complete:
        if hlr["BP5.1.2 Reviewed?"] == "Y":
            OrrComplete.append(hlr)
        else:
            OrrIncomplete.append(hlr)
    PercentOrrComplete = 0.0
    try:
        PercentOrrComplete = len(OrrComplete)/len(requirements) * 100
    except:
        pass
    reportString = appendLine("    Object Status")
    reportString += appendLine("     " + str(len(InWork)) + " In Work")
    reportString += appendLine("     " + str(len(ReadyForReview)) + " Ready for Review")
    reportString += appendLine("     " + str(len(Reviewed)) + " Reviewed")
    reportString += appendLine("     " + str(len(Complete)) + " Complete")
    reportString += appendLine("     " + str(len(Unassigned)) + " Unassigned")
    reportString += appendLine("-------------------------------------------------------")
    temp = "Review Incomplete:\n     "
    for hlr in OrrIncomplete:
        temp+= hlr["Identifier"] +", "
    temp = temp.rstrip(", ")
    reportString += appendLine(temp)
    return reportString, PercentOrrComplete

def ReviewReport(FeatureReport):
    """
    Description: Creates a report including percent complete based on review status for HLRs, LLRs, and TPs.
    Parameters:    
        FeatureReport - dictionary of artifact metrics used to indicate completeness, defaulted using EmptyDictionary() function
    Return:     
        reportString - string with status of each artifact to be converted into a text file.
    """

    reportString = appendLine("==============================================================")
    temp, PercentOrrComplete = reviewString(FeatureReport["Total HLRs"])
    reportString += appendLine(" HLR Review Status :  {0:.2f}% ORR Ready".format(PercentOrrComplete))
    reportString += temp
    reportString += appendLine("--------------------------------------------------------------")
    temp, PercentOrrComplete = reviewString(FeatureReport["Total LLRs"])
    reportString += appendLine(" LLR Review Status :  {0:.2f}% ORR Ready".format(PercentOrrComplete))
    reportString += temp
    reportString += appendLine("--------------------------------------------------------------")
    temp, PercentOrrComplete = reviewString(FeatureReport["Total HLTPs"])
    reportString += appendLine(" TP Review Status :  {0:.2f}% ORR Ready".format(PercentOrrComplete))
    reportString += temp
    reportString += appendLine("--------------------------------------------------------------")
    return reportString

def SlrReport(FeatureReport):
    """
    Description: Creates report of system level requirements based on feature. Includes SLR Estimate, Total SLRs, SW SLRs, UADF SLRs, and SLRs w/o HLRs.
    Parameters:    
        FeatureReport - dictionary of artifact metrics used to indicate completeness, defaulted using EmptyDictionary() function
    Return:     
        reportString - string containing SLR coverage information: SLR estimate, UADF-Only, Total SLRs, SW SLRs, SLRs w/o HLRs
    """
    
    #=========================================
    # SLR Report
    #=========================================
    reportString = appendLine("==============================================================")
    reportString += appendLine(" " + str((FeatureReport["SLR Estimate"])) + " Estimated SLRs")
    reportString += appendLine(" " + str((FeatureReport["SLR Estimate -UADF Only"])) + " Estimated UADF Only SLRs")
    reportString += appendLine(" " + str(len(FeatureReport["Total SLRs"])) + " Total SLRs")
    reportString += appendLine("  " + str(len(FeatureReport["SW SLRs"])) + " non-UADF Only SLRs")
    reportString += appendLine("  " + str(len(FeatureReport["UADF-Only SLRs"])) + " UADF Only SLRs")
    reportString += appendLine("--------------------------------------------------------------")
    reportString += appendLine(" " + str(len(FeatureReport["SLRs w/o HLR"])) + " SLRs w/o HLRs")
    ids = ""
    for slr in FeatureReport["SLRs w/o HLR"]:
        ids += slr + ", "

    reportString += appendLine("    " + ids.rstrip(", "))
    return reportString

def HlrReport(FeatureReport):
    """
    Description: Creates report of HLR completeness status. Includes HLR estimate, total HLRs, Table HLRs, HLRs w/o LLRs, TS, TC, and TPs
    Parameters:    
        FeatureReport - dictionary of artifact metrics used to indicate completeness, defaulted using EmptyDictionary() function
    Return:     
        reportString - formatted report to be converted containing HLR estimate, total HLRs, Table HLRs, HLRs w/o LLRs, TS, TC, and TPs
        hlrAMLRep - AMl Report for Coverage HLRs, contains average AML
    """
    
    #=========================================
    # HLR Report
    #=========================================
    reportString = appendLine("==============================================================")
    reportString += appendLine(" " + str((FeatureReport["HLR Estimate"])) + " Estimated HLRs")
    reportString += appendLine(" " + str(len(FeatureReport["Total HLRs"])) + " Total HLRs")
    reportString += appendLine(" " + str(len(FeatureReport["Table HLRs"])) + " HLRs Allocated to Table")
    temp, hlrAMLRep = AMLReport(FeatureReport["Coverage HLRs"])
    reportString += temp
    #LLRs
    reportString += appendLine("--------------------------------------------------------------")
    reportString += appendLine(" " + str(len(FeatureReport["HLRs w/o LLR"])) + " HLR w/o LLRs")
    ids = ""
    for hlr in FeatureReport["HLRs w/o LLR"]:
        ids += hlr + ", "

    reportString += appendLine("    " + ids.rstrip(", "))
    #Test Strategies
    reportString += appendLine("--------------------------------------------------------------")
    reportString += appendLine(" " + str(len(FeatureReport["HLRs w/o TS"])) + " HLR w/o TS")
    ids = ""
    for hlr in FeatureReport["HLRs w/o TS"]:
        ids += hlr + ", "

    reportString += appendLine("    " + ids.rstrip(", "))
    # Test Cases
    reportString += appendLine("--------------------------------------------------------------")
    reportString += appendLine(" " + str(len(FeatureReport["HLRs w/o TC"])) + " HLR w/o TC")
    ids = ""
    for hlr in FeatureReport["HLRs w/o TC"]:
        ids += hlr + ", "

    reportString += appendLine("    " + ids.rstrip(", "))

    #Test Procedures
    reportString += appendLine("--------------------------------------------------------------")
    reportString += appendLine(" " + str(len(FeatureReport["HLRs w/o TP"])) + " HLR w/o TP")
    ids = ""
    for hlr in FeatureReport["HLRs w/o TP"]:
        ids += hlr + ", "

    reportString += appendLine("    " + ids.rstrip(", "))
    return reportString, hlrAMLRep

def LlrReport(FeatureReport):
    """
    Description: Creates report of LLR completeness. Contains LLR estimate, total LLRs, LLRs w/0 HLRs, code, and remaining CLRs
    Parameters:    
        FeatureReport - dictionary of artifact metrics used to indicate completeness, defaulted using EmptyDictionary() function
    Return:     
        reportString - formatted report to be converted containing LLR estimate,  total LLRs, LLRs w/0 HLRs, code, and remaining CLRs
        llrAMLRep - AMl Report for Coverage HLRs, contains average AML
    """
    
    #=========================================
    # LLR Report
    #=========================================
    reportString = appendLine("==============================================================")
    reportString += appendLine(" " + str((FeatureReport["LLR Estimate"])) + " Estimated LLRs")
    reportString += appendLine(" " + str(len(FeatureReport["Total LLRs"])) + " Total LLRs")
    temp, llrAMLRep = AMLReport(FeatureReport["Coverage LLRs"])
    reportString += temp
    reportString += appendLine("--------------------------------------------------------------")
    reportString += appendLine(" " + str(len(FeatureReport["LLRs w/o HLR"])) + " LLR w/o HLRs")
    ids = ""
    for llr in FeatureReport["LLRs w/o HLR"]:
        ids += llr + ", "
    reportString += appendLine("    " + ids.rstrip(", "))
    reportString += appendLine("--------------------------------------------------------------")
    reportString += appendLine(" " + str(len(FeatureReport["LLRs w/o Code"])) + " LLR w/o Code")
    ids = ""
    for llr in FeatureReport["LLRs w/o Code"]:
        ids += llr + ", "
    reportString += appendLine("    " + ids.rstrip(", "))
    reportString += appendLine("--------------------------------------------------------------")
    reportString += appendLine(" " + str(len(FeatureReport["Remaining CLRs"])) + " CLRs Remaining")
    ids = ""
    for llr in FeatureReport["Remaining CLRs"]:
        ids += llr + ", "
    reportString += appendLine("    " + ids.rstrip(", "))
    return reportString, llrAMLRep

def TsReport(FeatureReport):
    """
    Description: Creates report of Test Strategy completeness. Contains TS estimate & total TSs
    Parameters:    
        FeatureReport - dictionary of artifact metrics used to indicate completeness, defaulted using EmptyDictionary() function
    Return:     
        reportString - formatted report to be converted containing TS estimate & total TSs
        tsAMLRep - AMl Report for coverage of TSs, contains average AML
    """
    
    #=========================================
    # Test Strategy Report
    #=========================================
    reportString = appendLine("==============================================================")
    reportString += appendLine(" " + str((FeatureReport["TS Estimate"])) + " Estimated TSs")
    reportString += appendLine(" " + str(len(FeatureReport["Total TSs"])) + " Total TSs")
    temp, tsAMLRep = AMLReport(FeatureReport["Coverage TSs"])
    reportString += temp
    return reportString, tsAMLRep

def HlTcReport(FeatureReport):
    """
    Description: Creates report of Test Case completeness. Contains TC estimate, total TCs, and TCs w/o TPs
    Parameters:    
        FeatureReport - dictionary of artifact metrics used to indicate completeness, defaulted using EmptyDictionary() function
    Return:     
        reportString - formatted report containing TC estimate, total TCs, and TCs w/o TPs
        tcAMLRep - AMl Report for coverage of HLTCs, contains average AML
    """
    
    #=========================================
    # Test Case Report
    #=========================================
    reportString = appendLine("==============================================================")
    reportString += appendLine(" " + str((FeatureReport["HLTC Estimate"])) + " Estimated HLTCs")
    reportString += appendLine(" " + str(len(FeatureReport["Total HLTCs"])) + " Total HLTCs")
    temp, tcAMLRep = AMLReport(FeatureReport["Coverage HLTCs"])
    reportString += temp
    reportString += appendLine("--------------------------------------------------------------")
    reportString += appendLine(" " + str(len(FeatureReport["TCs w/o TP"])) + " HLTC w/o TPs")
    ids = ""
    for tc in FeatureReport["TCs w/o TP"]:
        ids += tc + ", "

    reportString += appendLine("    " + ids.rstrip(", "))
    return reportString, tcAMLRep

def HlTpReport(FeatureReport):
    """
    Description: Creates report of High Level Test Procedure completeness. Contains TP estimate & total TPs
    Parameters:    
        FeatureReport - dictionary of artifact metrics used to indicate completeness, defaulted using EmptyDictionary() function
    Return:     
        reportString - formatted report to be converted containing TS estimate & total TSs
        tpAMLRep - AMl Report for coverage of HLTPs, contains average AML
    """
    
    #=========================================
    # Test Procedure Report
    #=========================================
    reportString = appendLine("==============================================================")
    reportString += appendLine(" " + str((FeatureReport["HLTP Estimate"])) + " Estimated HLTPs")
    reportString += appendLine(" " + str(len(FeatureReport["Total HLTPs"])) + " Total TPs")
    temp, tpAMLRep = AMLReport(FeatureReport["Coverage HLTPs"])
    reportString += temp
    return reportString, tpAMLRep

def LlTcReport(FeatureReport):
    """
    Description: Creates report of Low Level Test Case completeness. Contains LLTC estimate & total LLTCs
    Parameters:    
        FeatureReport - dictionary of artifact metrics used to indicate completeness, defaulted using EmptyDictionary() function
    Return:     
        reportString - formatted report containing LLTC estimate & total LLTCs
        tcAMLRep - AMl Report for coverage of LLTCs, contains average AML
    """
    
    #=========================================
    # Test Case Report
    #=========================================
    reportString = appendLine("==============================================================")
    reportString += appendLine(" " + str((FeatureReport["LLTC Estimate"])) + " Estimated LLTCs")
    reportString += appendLine(" " + str(len(FeatureReport["Total LLTCs"])) + " Total LLTCs")
    temp, tcAMLRep = AMLReport(FeatureReport["Coverage LLTCs"])
    reportString += temp
    return reportString, tcAMLRep

def LlTpReport(FeatureReport):
    """
    Description: Creates report of Low Level Test Procedure completeness. Contains LLTP estimate & total LLTPs
    Parameters:    
        FeatureReport - dictionary of artifact metrics used to indicate completeness, defaulted using EmptyDictionary() function
    Return:     
        reportString - formatted report containing LLTP estimate & total LLTPs
        tcAMLRep - AMl Report for coverage of LLTPs, contains average AML
    """
    
    #=========================================
    # Test Procedure Report
    #=========================================
    reportString = appendLine("==============================================================")
    reportString += appendLine(" " + str((FeatureReport["LLTP Estimate"])) + " Estimated LLTPs")
    reportString += appendLine(" " + str(len(FeatureReport["Total LLTPs"])) + " Total LLTPs")
    temp, tcAMLRep = AMLReport(FeatureReport["Coverage LLTPs"])
    reportString += temp
    return reportString, tcAMLRep

def CodeReport(FeatureReport):
    """
    Description: Creates report of Low Level Test Procedure completeness. Contains total code packages.
    Parameters:    
        FeatureReport - dictionary of artifact metrics used to indicate completeness, defaulted using EmptyDictionary() function
    Return:     
        reportString - formatted report containing total code packages
        codeAMLRep - AMl Report for coverage of code, contains average AML
    """
    
    #=========================================
    # Code Report
    #=========================================
    reportString = appendLine("==============================================================")
    reportString += appendLine(" " + str(len(FeatureReport["Total Code"])) + " Total Code Packages")
    temp, codeAMLRep = AMLReport(FeatureReport["Coverage Code"])
    reportString += temp
    return reportString, codeAMLRep

def ReviewEstimateReport(FeatureReport):
    """
    Description: Creates report that estimates time required to review artifacts based on Review Status attribute of object and cost model
    Parameters:    
        FeatureReport - dictionary of artifact metrics used to indicate completeness, defaulted using EmptyDictionary() function
    Return:     
        reportString - formatted report containing hours needed to review HLRs and LLRs
    """
    
    reportString=""
    hlrReview = 30 / 60
    llrReview = 30 / 60
    vvReview = 15 / 60
    reportString += appendLine("--------------------------------------------------------------")
    reportString += appendLine("Review Estimate")
    reportString += appendLine("HLRs:" + str(len(FeatureReport["Total HLRs"]) * hlrReview) + " Hours")
    reportString += appendLine("    " + str(len(FeatureReport["Total HLRs"])) + " HLRs x " + str(hlrReview) + " hours/HLR")
    reportString += appendLine("LLR/Code:" + str(len(FeatureReport["Total LLRs"]) * llrReview) + " Hours")
    reportString += appendLine("    " + str(len(FeatureReport["Total LLRs"])) + " LLRs x " + str(llrReview) + " hours/LLR")
    reportString += appendLine("V&V:" + str(len(FeatureReport["Total HLRs"]) * vvReview) + " Hours")
    reportString += appendLine("    " + str(len(FeatureReport["Total HLRs"])) + " HLRs x " + str(vvReview) + " hours/HLR")
    reportString += appendLine("--------------------------------------------------------------")
    return reportString

def ObjectReport(FeatureReport):
    """
    Description: Creates a report containing Total SLRs, HLRs, LLRs, HLTCs, HLTPs,  and Code using "Total SLRs" in the FeatureReport
    Parameters:        
        FeatureReport - dictionary of artifact metrics used to indicate completeness, defaulted using EmptyDictionary() function
    Return:  
        reportString - Formatted string containing Total SLRs, HLRs, LLRs, HLTCs, HLTPs,  and Code
    """
    
    reportString = appendLine("SLR Listing: ")
    ids = ""
    for slr in FeatureReport["Total SLRs"]:
        ids += slr + ", "

    reportString += appendLine("    " + ids.rstrip(", "))
    reportString += appendLine("--------------------------------------------------------------")
    reportString += appendLine("HLR Listing:")
    ids = ""
    for hlr in FeatureReport["Total HLRs"]:
        ids += hlr + ", "

    reportString += appendLine("    " + ids.rstrip(", "))
    reportString += appendLine("--------------------------------------------------------------")
    reportString += appendLine("LLR Listing:")
    ids = ""
    for llr in FeatureReport["Total LLRs"]:
        ids += llr + ", "

    reportString += appendLine("    " + ids.rstrip(", "))
    reportString += appendLine("--------------------------------------------------------------")
    reportString += appendLine("TC Listing:")
    ids = ""
    for tc in FeatureReport["Total HLTCs"]:
        ids += tc + ", "

    reportString += appendLine("    " + ids.rstrip(", "))
    reportString += appendLine("--------------------------------------------------------------")
    reportString += appendLine("TP Listing:")
    ids = ""
    for tp in FeatureReport["Total HLTPs"]:
        ids += tp + ", "

    reportString += appendLine("    " + ids.rstrip(", "))
    reportString += appendLine("--------------------------------------------------------------")
    reportString += appendLine("Code Proxy Listing:")
    ids = ""
    for tp in FeatureReport["Total Code"]:
        ids += tp + ", "

    reportString += appendLine("    " + ids.rstrip(", "))
    reportString += appendLine("Code Package Listing:")
    ids = ""
    for tp in FeatureReport["Total Code"]:
        ids += "    " + FeatureReport["Total Code"][tp]["File Name"] + "\n"

    reportString += appendLine(ids.rstrip("\n"))
    return reportString

def DecompositionRatioReport(FeatureReport, featureName = ""):
    """
    Description: Creates report containing ratio of completeness for each artifact type. Child_Ratio = Total_Child_Artifacts / (Total_Parents - Total_Parents_No_Child)
    Parameters:        
        FeatureReport - dictionary of artifact metrics used to indicate completeness, defaulted using EmptyDictionary() function
        featureName - name of feature to do anaysis on
    Return:  
        reportString - Formatted string containing ratios for HLRs, LLRs, HLTCs, HLTPs,  and Code
    """
    
    # Decomposition Ratio
    HlrRatio = NaN
    LlrRatio = NaN
    HLTcRatio = NaN
    TsRatio = NaN
    HLTpRatio = NaN
    LLTcRatio = NaN
    LLTpRatio = NaN

    try:
        HlrRatio = len(FeatureReport["Total HLRs"]) / (len(FeatureReport["SW SLRs"]) - len(FeatureReport["SLRs w/o HLR"]))
    except:
        pass
    try:
        LlrRatio = len(FeatureReport["Total LLRs"]) / (len(FeatureReport["Total HLRs"]) - len(FeatureReport["HLRs w/o LLR"]))
    except:
        pass
    try:
        HLTcRatio = len(FeatureReport["Total HLTCs"]) / (len(FeatureReport["Total HLRs"]) - len(FeatureReport["HLRs w/o TC"]))
    except:
        pass
    try:
        TsRatio = len(FeatureReport["Total TSs"]) / (len(FeatureReport["Total HLRs"]) - len(FeatureReport["HLRs w/o TS"]))
    except:
        pass
    try:
        HLTpRatio = len(FeatureReport["Total HLTPs"]) / (len(FeatureReport["Total HLRs"]) - len(FeatureReport["HLRs w/o TP"]))
    except:
        pass
    try: #todo need LLR info
        LLTcRatio = len(FeatureReport["Total HLTPs"]) / (len(FeatureReport["Total HLRs"]) - len(FeatureReport["HLRs w/o TP"]))
    except:
        pass
    try: #todo need LLR info
        LLTpRatio = len(FeatureReport["Total HLTPs"]) / (len(FeatureReport["Total HLRs"]) - len(FeatureReport["HLRs w/o TP"]))
    except:
        pass
    reportString = appendLine("==============================================================")
    reportString += appendLine("HLR Ratio: " + str(HlrRatio))
    reportString += appendLine("LLR Ratio: " + str(LlrRatio))
    reportString += appendLine("HLTC Ratio: " + str(HLTcRatio))
    reportString += appendLine("TS Ratio: " + str(TsRatio))
    reportString += appendLine("HLTP Ratio: " + str(HLTpRatio))
    reportString += appendLine("LLTC Ratio: " + str(LLTcRatio))
    reportString += appendLine("LLTP Ratio: " + str(LLTpRatio))

    reportString += appendLine("==============================================================")
    if featureName != "":
        CurrentRatios[featureName] = [FeatureReport["Total SLRs"], HlrRatio, LlrRatio, HLTcRatio, TsRatio, HLTpRatio]
    return reportString

def createFeatureMaturityReport(feature):
    """
    Description: 
    Parameters:        
    Return:     
    """
    
    print(feature['Name'])

    ORRCategory = "Out"
    if (feature['C919 Blockpoints'] == "5"):
        ORRCategory = "Targeted"
    elif (feature['C919 Blockpoints'] == "5+"):
        ORRCategory = "Active Additional"
    testingRequired = (feature['C919 Blockpoints'] == "5")
    FeatureReport = EmptyDictionary()
    if feature['Name'] in FeatureData:
        FeatureReport = FeatureData[feature['Name']]
        # Can add count of derived here if desired by counting HLR and LRR before processing the feature data

    FeatureReport["Features"].update({feature['Name']:{'RTC Feature ID':feature['RTC Feature ID'],'Identifier':feature['Identifier']}})
    FeatureReport["TimeStamp"] = feature['TimeStamp'].split(" ")[0]
    reportString = ""

    #=========================================
    # Collect Data
    #=========================================
    for slr in feature['SLRs']:
        FeatureReport["Total SLRs"][slr['Identifier']] = slr
        if slr['UADF Only']:
            FeatureReport["UADF-Only SLRs"][slr['Identifier']] = slr
        else:
            FeatureReport["SW SLRs"][slr['Identifier']] = slr

    for slr in FeatureReport["SW SLRs"]:
        if len(FeatureReport["SW SLRs"][slr]["HLRs"]) == 0:
            FeatureReport["SLRs w/o HLR"][slr] = FeatureReport["SW SLRs"][slr]

    for slr in FeatureReport["Total SLRs"]:
        for hlr in FeatureReport["Total SLRs"][slr]["HLRs"]:
            if isUI_Hlr(hlr):
                FeatureReport["Total HLRs"][hlr['Identifier']] = hlr
                uniqueify(hlr,FeatureReport["Coverage HLRs"])

    for hlr in FeatureReport["Total HLRs"]:
        if len(FeatureReport["Total HLRs"][hlr]["LLRs"]) == 0 and FeatureReport["Total HLRs"][hlr]["Allocation"] != "Table":
            FeatureReport["HLRs w/o LLR"][hlr] = FeatureReport["Total HLRs"][hlr]
        if len(FeatureReport["Total HLRs"][hlr]["TCs"]) == 0:
            FeatureReport["HLRs w/o TC"][hlr] = FeatureReport["Total HLRs"][hlr]
        if len(FeatureReport["Total HLRs"][hlr]["TSs"]) == 0:
            FeatureReport["HLRs w/o TS"][hlr] = FeatureReport["Total HLRs"][hlr]
        if FeatureReport["Total HLRs"][hlr]["Allocation"] == "Table":
            FeatureReport["Table HLRs"][hlr] = FeatureReport["Total HLRs"][hlr]
        for llr in FeatureReport["Total HLRs"][hlr]["LLRs"]:
            if llr["Functional Area"] == "UI" or llr["Functional Area"] == "":
                FeatureReport["Total LLRs"][llr['Identifier']] = llr
                uniqueify(llr,FeatureReport["Coverage LLRs"])
        for tc in FeatureReport["Total HLRs"][hlr]['TCs']:
            if tc['Object Type'] == "Test Case":
                uniqueify(tc,FeatureReport["Coverage HLTCs"])
                FeatureReport["Total HLTCs"][tc['Identifier']] = tc
        for ts in FeatureReport["Total HLRs"][hlr]['TSs']:
            uniqueify(ts,FeatureReport["Coverage TSs"])
            FeatureReport["Total TSs"][ts['Identifier']] = ts
    for llr in FeatureReport["Total LLRs"]:
        if len(FeatureReport["Total LLRs"][llr]["Code"]) == 0:
            FeatureReport["LLRs w/o Code"][llr] = FeatureReport["Total LLRs"][llr]
        if llr.find("CLR")!=-1:
            FeatureReport["Remaining CLRs"][llr] = FeatureReport["Total LLRs"][llr]
        for tc in FeatureReport["Total LLRs"][llr]['TCs']:
            if tc['Object Type'] == "Test Case":
                uniqueify(tc,FeatureReport["Coverage LLTCs"])
                FeatureReport["Total LLTCs"][tc['Identifier']] = tc
        for code in FeatureReport["Total LLRs"][llr]["Code"]:
            FeatureReport["Total Code"][code['Identifier']] = code
            uniqueify(code,FeatureReport["Coverage Code"])

    for tc in FeatureReport["Total HLTCs"]:
        if len(FeatureReport["Total HLTCs"][tc]["TPs"]) == 0:
            FeatureReport["TCs w/o TP"][tc] = FeatureReport["Total HLTCs"][tc]
        for tp in FeatureReport["Total HLTCs"][tc]["TPs"]:
            FeatureReport["Total HLTPs"][tp['Identifier']] = tp
            uniqueify(tp, FeatureReport["Coverage HLTPs"])
    for tc in FeatureReport["Total LLTCs"]:
        if len(FeatureReport["Total LLTCs"][tc]["TPs"]) == 0:
            FeatureReport["LLTCs w/o TP"][tc] = FeatureReport["Total LLTCs"][tc]
        for tp in FeatureReport["Total LLTCs"][tc]["TPs"]:
            FeatureReport["Total LLTPs"][tp['Identifier']] = tp
            uniqueify(tp, FeatureReport["Coverage LLTPs"])

    # Calculate Estimates at completion
    EstRatios = Models.EstimateModels["Standard"]
    #first check to see if the models contain a improved estimate model
    if feature['Name'] in Models.EstimateModels:
            EstRatios =  Models.EstimateModels[feature['Name']]

    # Implement "Blending" of standard ratio (gathered directly above) and the
    # actual ratio.  Blending to be based on the percent coverage of the parent
    # artifacts for a given feature
    for model in EstRatios:
        #Assume all the feature are complete

        #Assume removing the existing UADF only HLRs as part of the HLR estimate
        FeatureReport["SLR Estimate"] = len(FeatureReport["Total SLRs"])

        FeatureReport["HLR Estimate"] = ceil(len(FeatureReport["Total HLRs"])+(len(FeatureReport["SLRs w/o HLR"])*EstRatios["HLR Ratio"]))
        #FeatureReport["HLR Estimate"] = ceil((FeatureReport["SLR Estimate"]-len(FeatureReport["UADF-Only SLRs"])*EstRatios["HLR Ratio"]))
        # If the Estimate based on current HLRs comes back as  then we need to do a SLR based estimate
        if FeatureReport["HLR Estimate"]<=0:
            FeatureReport["HLR Estimate"] = ceil((FeatureReport["SLR Estimate"]-len(FeatureReport["UADF-Only SLRs"])*EstRatios["HLR Ratio"]))

        FeatureReport["LLR Estimate"] = ceil(FeatureReport["HLR Estimate"]*EstRatios["LLR Ratio"])
        #FeatureReport["LLR Estimate"] = ceil(len(FeatureReport["Total LLRs"])+(len(FeatureReport["HLRs w/o LLR"])*EstRatios["LLR Ratio"]))

        FeatureReport["HLTC Estimate"] = ceil(FeatureReport["HLR Estimate"]*EstRatios["HLTC Ratio"])
        if FeatureReport["HLTC Estimate"] < len(FeatureReport["Total HLTCs"]):
            FeatureReport["HLTC Estimate"] = len(FeatureReport["Total HLTCs"])

        FeatureReport["LLTC Estimate"] = ceil(FeatureReport["LLR Estimate"]*EstRatios["LLTC Ratio"])

        FeatureReport["TS Estimate"] = ceil(FeatureReport["HLR Estimate"]*EstRatios["TS Ratio"])
        if FeatureReport["TS Estimate"] < len(FeatureReport["Total TSs"]):
            FeatureReport["TS Estimate"] = len(FeatureReport["Total TSs"])

        FeatureReport["HLTP Estimate"] = ceil(FeatureReport["HLTC Estimate"]*EstRatios["HLTP Ratio"])
        #print(FeatureReport["HLTP Estimate"])

        FeatureReport["LLTP Estimate"] = ceil(FeatureReport["LLTC Estimate"]*EstRatios["LLTP Ratio"])

        FeatureReport["Code Estimate"] = ceil(FeatureReport["LLR Estimate"]*EstRatios["Code Ratio"])

        # TODO handle errors for div by 0 here
        try:
            if model=="HLR Ratio":
                scaling=(len(FeatureReport["Total SLRs"])-len(FeatureReport["SLRs w/o HLR"]))/FeatureReport["SLR Estimate"]
                ActRatio=len(FeatureReport["Total HLRs"])/len(FeatureReport["Total SLRs"])
            elif model=="LLR Ratio":
                scaling=(len(FeatureReport["Total HLRs"])-len(FeatureReport["HLRs w/o LLR"]))/FeatureReport["HLR Estimate"]
                ActRatio=len(FeatureReport["Total LLRs"])/len(FeatureReport["Total HLRs"])
            elif model=="HLTC Ratio":
                scaling=(len(FeatureReport["Total HLRs"])-len(FeatureReport["HLRs w/o TC"]))/FeatureReport["HLR Estimate"]
                ActRatio=len(FeatureReport["Total HLTCs"])/len(FeatureReport["Total HLRs"])
            elif model=="LLTC Ratio":#need LLR Info
                scaling=(len(FeatureReport["Total LLRs"])-len(FeatureReport["LLRs w/o TC"]))/FeatureReport["LLR Estimate"]
                ActRatio=len(FeatureReport["Total LLTCs"])/len(FeatureReport["Total LLRs"])
            #elif model=="TS Ratio":
                #scaling=len(FeatureReport["HLRs w/o TC"])/len(FeatureReport["Total HLRs"])
                #ActRatio=len(FeatureReport["Coverage HLTCs"])/len(FeatureReport["Total HLRs"])
            elif model=="HLTP Ratio":
                scaling=(len(FeatureReport["Total HLTCs"])-len(FeatureReport["TCs w/o TP"]))/FeatureReport["HLTC Estimate"]
                ActRatio=len(FeatureReport["Total HLTPs"])/len(FeatureReport["Total HLTCs"])
            elif model=="LLTP Ratio":#need LLR info
                scaling=(len(FeatureReport["Total LLTCs"])-len(FeatureReport["LLTCs w/o TP"]))/FeatureReport["LLTC Estimate"]
                print(scaling)
                print(len(FeatureReport["Total LLTCs"]))
                print(len(FeatureReport["LLTCs w/o TP"]))
                print(FeatureReport["LLTC Estimate"])

                ActRatio=len(FeatureReport["Total LLTPs"])/len(FeatureReport["Total LLTCs"])
            elif model=="Code Ratio":
                scaling=(len(FeatureReport["Total LLRs"])-len(FeatureReport["LLRs w/o Code"]))/FeatureReport["LLR Estimate"]
                ActRatio=len(FeatureReport["Total Code"])/len(FeatureReport["Total LLRs"])
            else:
                scaling=0
                ActRatio=0
        except ZeroDivisionError:
            print("Handle div 0")
            scaling=0
            ActRatio=0

        if scaling>1:
            scaling=1
        if ActRatio==0:
            scaling=0
        EstRatios[model]=scaling*ActRatio + (1-scaling)*EstRatios[model]

    print(EstRatios)




    # Find HLRs without test procedures
    for hlr in FeatureReport['Total HLRs']:
        found = False
        #if DTR or DST mark found as no additional verification needed beyond the functional
        if hlr.startswith("C919.DST") or hlr.startswith("C919.DTR"):
            found = True
        for tc in FeatureReport['Total HLRs'][hlr]["TCs"]:
            for tp in tc['TPs']:
                found = True
        if not found:
            FeatureReport['HLRs w/o TP'][hlr] = FeatureReport['Total HLRs'][hlr]

    reportString += appendLine("==============================================================")
    reportString += appendLine(" RTC " + feature['RTC Feature ID']+ " : "+feature['Name'])
    reportString += appendLine("  Theme : " + feature['Theme'])
    reportString += appendLine("  as of " + feature['TimeStamp'])
    reportString += appendLine("==============================================================")

    reportString += SlrReport(FeatureReport)

    temp, FeatureReport["HLR AML Report"] = HlrReport(FeatureReport)
    reportString += temp

    temp, FeatureReport["LLR AML Report"] = LlrReport(FeatureReport)
    reportString += temp


    temp, FeatureReport["Code AML Report"] = CodeReport(FeatureReport)
    reportString += temp

    temp, FeatureReport["TS AMLs"] = TsReport(FeatureReport)
    reportString += temp

    temp, FeatureReport["HLTC AML Report"] = HlTcReport(FeatureReport)
    reportString += temp

    temp, FeatureReport["HLTP AML Report"] = HlTpReport(FeatureReport)
    reportString += temp

    temp, FeatureReport["LLTC AML Report"] = LlTcReport(FeatureReport)
    reportString += temp

    temp, FeatureReport["LLTP AML Report"] = LlTpReport(FeatureReport)
    reportString += temp

    reportString += remainingWorkReport(FeatureReport)



    #=========================================
    # create Complete Report
    #=========================================
    HoursData[feature['Name']] =  {"Themes":feature['Theme'].split("|"),
                                   "HLR":FeatureReport["HLR Hours"],
                                   "LLR":FeatureReport["LLR Hours"],
                                   "HLTC":FeatureReport["HLTC Hours"],
                                   "HLTP":FeatureReport["HLTP Hours"],
                                   "LLTC":FeatureReport["LLTC Hours"],
                                   "LLTP":FeatureReport["LLTP Hours"],
                                   "Code":FeatureReport["Code Hours"]}

    themes = feature['Theme'].split("|")
    for theme in themes:
        FeatureReport["Themes"].append(theme)
        if theme not in ThemeData:
            ThemeData[theme] = EmptyDictionary()


    teams = feature['Team'].split("|")
    for team in teams:
        if team not in TeamData:
            TeamData[team] = EmptyDictionary()
            TeamData[team]["Teams"].append(team)
        updateDict(TeamData[team],FeatureReport)

    #after updating the Team dictionaries include the team assignment with the Feature Report
    for team in teams:
        FeatureReport["Teams"].append(team)

    for theme in themes:
        updateDict(ThemeData[theme],FeatureReport)

    #Write to All report
    if "All" not in ThemeData:
        ThemeData["All"] = EmptyDictionary()
    updateDict(ThemeData["All"],FeatureReport)

    #Write to Release report
    release = feature['C919 Blockpoints']
    if release not in ReleaseData:
        ReleaseData[release] = EmptyDictionary()
    updateDict(ReleaseData[release],FeatureReport)

    #Write to BP report
    if (feature['C919 Blockpoints'] == "5+" or feature['C919 Blockpoints'] == "5"):
        if "All BP5" not in ThemeData:
            ThemeData["All BP5"] = EmptyDictionary()
        updateDict(ThemeData["All BP5"],FeatureReport)





    #Chart Data
    if ORRCategory != "Out":
        UpdateChartData(feature['Name'], teams, "HLR", ORRCategory, FeatureReport)
        UpdateChartData(feature['Name'], teams, "V&V", ORRCategory, len(FeatureReport['Total HLRs'])-len(FeatureReport['HLRs w/o TP']))




    reportString +=ReviewReport(FeatureReport)
    reportString += ReviewEstimateReport(FeatureReport)
    reportString += ObjectReport(FeatureReport)
    reportString += DecompositionRatioReport(FeatureReport, feature['Name'])

    FeatureString = "_"+feature['Name'].replace(":"," ").replace("/"," ")
    DateTag = FeatureReport["TimeStamp"]
    allDir = rootDir +"All\\"+ FeatureReport["TimeStamp"]+"\\"
    allJson = rootDir +"All\\"+ FeatureReport["TimeStamp"]+"\\Json\\"

    bp5Dir = rootDir +"BP5\\"+ FeatureReport["TimeStamp"]+"\\"
    bp5Json = rootDir +"BP5\\"+ FeatureReport["TimeStamp"]+"\\Json\\"

    q2Dir = rootDir +"Q2\\"+ FeatureReport["TimeStamp"]+"\\"
    q2Json = rootDir +"Q2\\"+ FeatureReport["TimeStamp"]+"\\Json\\"

    allRootDir = rootDir +"All\\"+ FeatureReport["TimeStamp"]+"\\"
    bp5RootDir = rootDir +"All\\"+ FeatureReport["TimeStamp"]+"\\"
    q2RootDir = rootDir +"Q2\\"+ FeatureReport["TimeStamp"]+"\\"

    if not os.path.exists(allRootDir):
        os.mkdir(allRootDir)
    if not os.path.exists(bp5RootDir):
        os.mkdir(bp5RootDir)
    if not os.path.exists(allDir):
        os.mkdir(allDir)
    if not os.path.exists(allJson):
        os.mkdir(allJson)
    if not os.path.exists(bp5Dir):
        os.mkdir(bp5Dir)
    if not os.path.exists(bp5Json):
        os.mkdir(bp5Json)

    if not os.path.exists(q2RootDir):
        os.mkdir(q2RootDir)
    if not os.path.exists(q2Dir):
        os.mkdir(q2Dir)
    if not os.path.exists(q2Json):
        os.mkdir(q2Json)


    with open(allJson+FeatureString+".json", "w") as featureOut:
        json.dump(FeatureReport,featureOut, indent=4)
    with open(allDir + FeatureString+".txt", "w") as featureOut:
        featureOut.write(reportString)
    if (feature['C919 Blockpoints'] == "5+" or feature['C919 Blockpoints'] == "5"):
        with open(bp5Json+FeatureString+".json", "w") as featureOut:
            json.dump(FeatureReport,featureOut, indent=4)
        with open(bp5Dir + FeatureString+".txt", "w") as featureOut:
            featureOut.write(reportString)

    if (feature['C919 Blockpoints'] == "6"):
        with open(q2Json+FeatureString+".json", "w") as featureOut:
            json.dump(FeatureReport,featureOut, indent=4)
        with open(q2Dir + FeatureString+".txt", "w") as featureOut:
            featureOut.write(reportString)
    return FeatureReport["TimeStamp"]

def createDerivedRequirementMaturityReport(feature):
    """
    Description: 
    Parameters:        
    Return:     
    """
    
    FeatureReport = EmptyDictionary()
    FeatureReport["Module"] = feature['Module']
    FeatureReport["TimeStamp"] = feature['TimeStamp'].split(" ")[0]
    reportString = ""

    reportString += appendLine("==============================================================")
    reportString += appendLine(feature['Module'])
    reportString += appendLine("  as of " + feature['TimeStamp'])
    reportString += appendLine("==============================================================")
    if "HLRs" in feature:
        print(feature["Module"])
        for hlr in feature["HLRs"]:
            if hlr["Feature"] == "":
                FeatureReport["Total HLRs"][hlr["Identifier"]] = hlr
            else:
                if hlr["Feature"] not in FeatureData:
                    FeatureData[hlr["Feature"]] = EmptyDictionary()
                FeatureData[hlr["Feature"]]["Total HLRs"][hlr["Identifier"]] = hlr

        for hlr in FeatureReport["Total HLRs"]:
            if FeatureReport["Total HLRs"][hlr]['Requirement']!="Derived":
                FeatureReport["HLRs w/o SLR"][hlr] = FeatureReport["Total HLRs"][hlr]
            if FeatureReport["Total HLRs"][hlr]['Allocation']!="Table":
                FeatureReport["Table HLRs"][hlr] = FeatureReport["Total HLRs"][hlr]
            if len(FeatureReport["Total HLRs"][hlr]["LLRs"]) == 0 and FeatureReport["Total HLRs"][hlr]['Allocation']!="Table":
                FeatureReport["HLRs w/o LLR"][hlr] = FeatureReport["Total HLRs"][hlr]
            if len(FeatureReport["Total HLRs"][hlr]["TCs"]) == 0:
                FeatureReport["HLRs w/o TC"][hlr] = FeatureReport["Total HLRs"][hlr]
            if len(FeatureReport["Total HLRs"][hlr]["TSs"]) == 0:
                FeatureReport["HLRs w/o TS"][hlr] = FeatureReport["Total HLRs"][hlr]
            for llr in FeatureReport["Total HLRs"][hlr]["LLRs"]:
                if llr["Functional Area"] == "UI":
                    FeatureReport["Total LLRs"][llr['Identifier']] = llr
            for tc in FeatureReport["Total HLRs"][hlr]['TCs']:
                if tc['Object Type'] == "Test Case":
                    FeatureReport["Total HLTCs"][tc['Identifier']] = tc
            for ts in FeatureReport["Total HLRs"][hlr]['TSs']:
                FeatureReport["Total TSs"][ts['Identifier']] = ts

        for llr in FeatureReport["Total LLRs"]:
            if len(FeatureReport["Total LLRs"][llr]["Code"]) == 0:
                FeatureReport["LLRs w/o Code"][llr] = FeatureReport["Total LLRs"][llr]
            for code in FeatureReport["Total LLRs"][llr]["Code"]:
                FeatureReport["Total Code"][code['Identifier']] = code
            for tc in FeatureReport["Total LLRs"][llr]['TCs']:
                if tc['Object Type'] == "Test Case":
                    FeatureReport["Total LLTCs"][tc['Identifier']] = tc

        for tc in FeatureReport["Total LLTCs"]:
            if len(FeatureReport["Total LLTCs"][tc]["TPs"]) == 0:
                FeatureReport["LLTCs w/o TP"][tc] = FeatureReport["Total LLTCs"][tc]
            for tp in FeatureReport["Total LLTCs"][tc]["TPs"]:
                FeatureReport["Total LLTPs"][tp['Identifier']] = tp

        for tc in FeatureReport["Total HLTCs"]:
            if len(FeatureReport["Total HLTCs"][tc]["TPs"]) == 0:
                FeatureReport["TCs w/o TP"][tc] = FeatureReport["Total HLTCs"][tc]
            for tp in FeatureReport["Total HLTCs"][tc]["TPs"]:
                FeatureReport["Total HLTPs"][tp['Identifier']] = tp

        temp, FeatureReport["HLR AML Report"] = HlrReport(FeatureReport)
        reportString += temp

        #Decomposed Missing SLRs
        reportString += appendLine("--------------------------------------------------------------")
        reportString += appendLine(" " + str(len(FeatureReport["HLRs w/o SLR"])) + " Decomposed HLR w/o SLR")
        ids = ""
        for hlr in FeatureReport["HLRs w/o SLR"]:
            ids += hlr + ", "
        reportString += appendLine("    " + ids.rstrip(", "))

        temp, FeatureReport["LLR AML Report"] = LlrReport(FeatureReport)
        reportString += temp

        temp, FeatureReport["Code AML Report"] = CodeReport(FeatureReport)
        reportString += temp

        temp, FeatureReport["TS AMLs"] = TsReport(FeatureReport)
        reportString += temp

        temp, FeatureReport["HLTC AML Report"] = HlTcReport(FeatureReport)
        reportString += temp

        temp, FeatureReport["HLTC AML Report"] = HlTpReport(FeatureReport)
        reportString += temp

        temp, FeatureReport["LLTC AML Report"] = LlTcReport(FeatureReport)
        reportString += temp

        temp, FeatureReport["LLTC AML Report"] = LlTpReport(FeatureReport)
        reportString += temp



    if "LLRs" in feature:
        print(feature["Module"])
        for llr in feature["LLRs"]:
            if llr["Functional Area"] == "UI":
                if llr["Feature"] == "":
                    FeatureReport["Total LLRs"][llr['Identifier']] = llr
                else:
                    if llr["Feature"] not in FeatureData:
                        FeatureData[llr["Feature"]] = EmptyDictionary()
                    FeatureData[llr["Feature"]]["Total LLRs"][llr["Identifier"]] = llr
        for llr in FeatureReport["Total LLRs"]:
            if FeatureReport["Total LLRs"][llr]['Requirement']!="Derived":
                FeatureReport["LLRs w/o HLR"][llr] = FeatureReport["Total LLRs"][llr]
            if len(FeatureReport["Total LLRs"][llr]["Code"]) == 0:
                FeatureReport["LLRs w/o Code"][llr] = FeatureReport["Total LLRs"][llr]
            for code in FeatureReport["Total LLRs"][llr]["Code"]:
                FeatureReport["Total Code"][code['Identifier']] = code

        for tc in FeatureReport["Total LLTCs"]:
            if len(FeatureReport["Total LLTCs"][tc]["TPs"]) == 0:
                FeatureReport["LLTCs w/o TP"][tc] = FeatureReport["Total LLTCs"][tc]
            for tp in FeatureReport["Total LLTCs"][tc]["TPs"]:
                FeatureReport["Total LLTPs"][tp['Identifier']] = tp

        for tc in FeatureReport["Total HLTCs"]:
            if len(FeatureReport["Total HLTCs"][tc]["TPs"]) == 0:
                FeatureReport["TCs w/o TP"][tc] = FeatureReport["Total HLTCs"][tc]
            for tp in FeatureReport["Total HLTCs"][tc]["TPs"]:
                FeatureReport["Total HLTPs"][tp['Identifier']] = tp

        temp, FeatureReport["LLR AML Report"] = LlrReport(FeatureReport)
        reportString += temp

        #Decomposed Missing HLRs
        reportString += appendLine("--------------------------------------------------------------")
        reportString += appendLine(" " + str(len(FeatureReport["LLRs w/o HLR"])) + " Decomposed LLR w/o HLR")
        ids = ""
        for hlr in FeatureReport["LLRs w/o HLR"]:
            ids += hlr + ", "
        reportString += appendLine("    " + ids.rstrip(", "))

        temp, FeatureReport["Code AML Report"] = CodeReport(FeatureReport)
        reportString += temp

        temp, FeatureReport["TS AML Report"] = TsReport(FeatureReport)
        reportString += temp

        temp, FeatureReport["HLTC AML Report"] = HlTcReport(FeatureReport)
        reportString += temp

        temp, FeatureReport["HLTC AML Report"] = HlTpReport(FeatureReport)
        reportString += temp

        temp, FeatureReport["LLTC AML Report"] = LlTcReport(FeatureReport)
        reportString += temp

        temp, FeatureReport["LLTC AML Report"] = LlTpReport(FeatureReport)
        reportString += temp

    #=========================================
    # create Complete Report Json
    #=========================================

    if "Derived" not in ThemeData:
        ThemeData["Derived"] = EmptyDictionary()
    updateDict(ThemeData["Derived"],FeatureReport)

    if "All" not in ThemeData:
        ThemeData["All"] = EmptyDictionary()
    updateDict(ThemeData["All"],FeatureReport)

    reportString += appendLine("==============================================================")
    reportString += appendLine("SLR Listing: ")
    ids = ""
    for slr in FeatureReport["Total SLRs"]:
        ids += slr + ", "
    reportString += appendLine("    " + ids.rstrip(", "))
    reportString += appendLine("--------------------------------------------------------------")
    reportString += appendLine("HLR Listing:")
    ids = ""
    for hlr in FeatureReport["Total HLRs"]:
        ids += hlr + ", "
    reportString += appendLine("    " + ids.rstrip(", "))
    reportString += appendLine("--------------------------------------------------------------")
    reportString += appendLine("LLR Listing:")
    ids = ""
    for llr in FeatureReport["Total LLRs"]:
        ids += llr + ", "
    reportString += appendLine("    " + ids.rstrip(", "))
    reportString += appendLine("--------------------------------------------------------------")
    reportString += appendLine("HLTC Listing:")
    ids = ""
    for tc in FeatureReport["Total HLTCs"]:
        ids += tc + ", "
    reportString += appendLine("    " + ids.rstrip(", "))
    reportString += appendLine("--------------------------------------------------------------")
    reportString += appendLine("HLTP Listing:")
    ids = ""
    for tp in FeatureReport["Total HLTPs"]:
        ids += tp + ", "
    reportString += appendLine("    " + ids.rstrip(", "))
    FeatureString = "_"+feature['Module'].replace("/","_").replace("__","_")

    allDir = rootDir +"All\\"+ FeatureReport["TimeStamp"]+"\\"
    allJson = rootDir +"All\\"+ FeatureReport["TimeStamp"]+"\\Json\\"
    bp5Dir = rootDir +"BP5\\"+ FeatureReport["TimeStamp"]+"\\"
    bp5Json = rootDir +"BP5\\"+ FeatureReport["TimeStamp"]+"\\Json\\"
    allRootDir = rootDir +"All\\"+ FeatureReport["TimeStamp"]+"\\"
    bp5RootDir = rootDir +"All\\"+ FeatureReport["TimeStamp"]+"\\"

    if not os.path.exists(allRootDir):
        os.mkdir(allRootDir)
    if not os.path.exists(bp5RootDir):
        os.mkdir(bp5RootDir)
    if not os.path.exists(allDir):
        os.mkdir(allDir)
    if not os.path.exists(allJson):
        os.mkdir(allJson)
    if not os.path.exists(bp5Dir):
        os.mkdir(bp5Dir)
    if not os.path.exists(bp5Json):
        os.mkdir(bp5Json)


    with open(allJson+FeatureString+"-Derived.json", "w") as featureOut:
        json.dump(FeatureReport,featureOut, indent=4)
    with open(allDir + FeatureString+"-Derived.txt", "w") as featureOut:
        featureOut.write(reportString)
    with open(bp5Json+FeatureString+"-Derived.json", "w") as featureOut:
        json.dump(FeatureReport,featureOut, indent=4)
    with open(bp5Dir + FeatureString+"-Derived.txt", "w") as featureOut:
        featureOut.write(reportString)
    return FeatureReport["TimeStamp"]
def uniqueify(item,search):
    """
    Description: 
    Parameters:        
    Return:     
    """
    
    occurance=0
    ModIdent=item['Identifier']
    #print (ModIdent)
    #print("****************************************************************************")
    #print (search)
    #print("----------------------------------------------------------------------------")
    while ModIdent in search:
        occurance=occurance+1
        ModIdent=item['Identifier'] + "_" + str(occurance)
        #print(ModIdent)
    search[ModIdent] = item

# Run the UI Metrics program
RunMetrics(rootDir, sourceDir, False)

print("UI Metrics report is complete!")
