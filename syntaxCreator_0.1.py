#======================================================================
# Author: John Broussard
# Date: 1/29/2014
# Original: 01/24/2014
# Purpose: This script reads a list of variables and whether the var
#           is open-ended or not (along with a work-around list of
#           var labels) and creates SPSS syntax to run freqs and
#           bar charts for each closed-ended question.
#======================================================================

import spss, spssaux

##listLocation = r'C:\Users\jcbrou\Documents\SAO\varList.txt'
##labelLocation = r'C:\Users\jcbrou\Documents\SAO\varLabels.txt'
##varName, varType = np.genfromtxt(listLocation, dtype='str')

# File to hold created SPSS script
outScriptSPSS = r'Y:\SAO\outScript.sps'
outfile = open(outScriptSPSS, 'w')

# Print out the output management system details to the .sps file
outfile.write('OMS /DESTINATION Viewer = No.\n')
outfile.write('OMS /Select Tables /ExceptIf Labels = ["Statistics", "Notes", "Export Summary"] /Destination Viewer = Yes.\n')
outfile.write('OMS /Select Charts /DESTINATION Viewer = Yes.\n')

# Open the SPSS data file
dataset = spssaux.OpenDataFile(r'Y:\SAO\sao_summer2013_20130918_20131209_forGrad.sav')

# Get list of variables, their labels and measurement level.
varList = list(enumerate(spssaux.VariableDict()))
labelList = []
formatList = []
for i in range(len(varList)):
    labelList.append(spss.GetVariableLabel(i))
    formatList.append(spss.GetVariableFormat(i))

variables = zip(varList, formatList, labelList)

for var in variables:
    varName = str(var[0][1])
    varFormat = var[1]
    varLabel = var[2]
    if ("A" not in varFormat) and ("Q" in varName):
        # If the variable is not a string, do this:
        outfile.write('Frequencies var = %s\n' % (varName))
        outfile.write('/Statistics=None.\n')
        outfile.write('GGraph\n')
        outfile.write('/Graphdataset Name="graphdataset" Variables= %s Missing=Listwise ReportMissing=No\n' % (varName))
        outfile.write('/Graphspec Source=Inline.\n')
        outfile.write('Begin GPL\n')
        outfile.write('SOURCE: s=userSource(id("graphdataset"))\n')
        outfile.write('DATA: %s=col(source(s), name("%s"), unit.category())\n' % (varName, varName))
        outfile.write('GUIDE: axis(dim(1), label("%s"))\n' % (varLabel))
        outfile.write('GUIDE: axis(dim(2), label("Percent"))\n')
        outfile.write('SCALE: cat(dim(1), include("0", "1"))\n')
        outfile.write('SCALE: linear(dim(2), include(0))\n')
        outfile.write('ELEMENT: interval(position(summary.percent.count(%s)), shape.interior(shape.square))\n' % (varName))
        outfile.write('End GPL.\n')
        outfile.write('Title "".\n\n')
    elif ("Q" in varName):
        varWidth = int(var[1][1:])
        if (varWidth < 51):
            # If the variable has a 'Q' in it's name (meaning it's a question in the survey), then if it's a string
            # not longer than 30 characters, do this:
            outfile.write('Frequencies var = %s\n' % (varName))
            outfile.write('/Statistics=None.\n')
            outfile.write('GGraph\n')
            outfile.write('/Graphdataset Name="graphdataset" Variables= %s Missing=Listwise ReportMissing=No\n' % (varName))
            outfile.write('/Graphspec Source=Inline.\n')
            outfile.write('Begin GPL\n')
            outfile.write('SOURCE: s=userSource(id("graphdataset"))\n')
            outfile.write('DATA: %s=col(source(s), name("%s"), unit.category())\n' % (varName, varName))
            outfile.write('GUIDE: axis(dim(1), label("%s"))\n' % (varLabel))
            outfile.write('GUIDE: axis(dim(2), label("Percent"))\n')
            outfile.write('SCALE: cat(dim(1), include("0", "1"))\n')
            outfile.write('SCALE: linear(dim(2), include(0))\n')
            outfile.write('ELEMENT: interval(position(summary.percent.count(%s)), shape.interior(shape.square))\n' % (varName))
            outfile.write('End GPL.\n')
            outfile.write('Title "".\n\n')
        ##else:
            ## print out all open-ended responses in format of
            ## Question Num:
            ## responses...

# Print out the export and formatting syntax to the .sps file
outfile.write('Output Export\n')
outfile.write('/Contents  Export=Visible  Layers=Printsetting  ModelViews=Printsetting\n')
outfile.write('/Doc  DocumentFile=  "Y:\\SAO\\test.doc"\n')
outfile.write('PageSize=Inches(8.5, 11)\n')
outfile.write('TopMargin=Inches(0.5)\n')
outfile.write('BottomMargin=Inches(0.5)\n')
outfile.write('LeftMargin=Inches(0.5)\n')
outfile.write('RightMargin=Inches(0.5)\n')
outfile.write('NotesCaptions=YES\n')
outfile.write('WideTables = Shrink.\n')
outfile.write('OMSEND.')
outfile.close()
