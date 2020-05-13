def pars(rinFileName,csvFileName):
    import datetime
    
    rinFields = []
    numFields = 0
    # Open the rinex file and extract header data
    writeMode="w"
    rinFile = open(rinFileName, "r")
    csvFile = open(csvFileName, writeMode)
    currentLine = rinFile.readline()
    while currentLine[60:].rstrip() != "END OF HEADER":
        print(currentLine)
        if currentLine[60:].rstrip() == "# / TYPES OF OBSERV": # Extract header data
            numFields = int(currentLine[1:6])
        
           # print(numFields)
            firstLine='time,'+'N_sat,'
            for j in range(int(numFields/9)):
                #print("j=",j)
                for i in range(9):
                    rinFields.append(currentLine[(7+i*6):(12+i*6)].lstrip())
                    firstLine=firstLine+currentLine[(7+i*6):(12+i*6)].lstrip()+','
                currentLine = rinFile.readline()
           # print(numFields%9)            
            for i in range(numFields%9):
                rinFields.append(currentLine[(7+i*6):(12+i*6)].lstrip())
                firstLine=firstLine+currentLine[(7+i*6):(12+i*6)].lstrip()+','
                #print(i,currentLine)
        currentLine = rinFile.readline()
   
    #print(rinFields)
    # ”‰‡ÎˇÂÏ ÔÓÒÎÂ‰Ì˛˛ Á‡ÔˇÚÛ˛
    firstLine=firstLine[:len(firstLine)-1]+""

    csvFile.write(firstLine+"\n")
    #print(firstLine)
    #print(len(firstLine),firstLine[len(firstLine)-1])
    csvFile.close()
    print("END OF HEADER")

    # —Œ«ƒ¿≈Ã —ÀŒ¬¿–‹ »« —œ»— ¿ œŒÀ≈… + ¬–≈Ãﬂ » N —œ”“Õ» ¿
    gpsRecord = dict(
      time = '0',
      prn = '0'
    )
    # create new dict from rinFields 
    d = dict.fromkeys(rinFields, 0)
    # renew gpsrecord with new dict d 
    gpsRecord.update(d)
    #print(gpsRecord)
    # convert dict to list for writing list to csv file
    csvFields=list(gpsRecord)
    #csvFields=(gpsRecord.keys())
    #for i in 
    #    csvFields.append(gpsRecord)
    #print(csvFields)

  # Open CSV file and add data
    writeMode="a"
    csvFile = open(csvFileName, writeMode)
    print("ReOpenFile")
    # write first string
    # Scroll through looking for valid epochs
    currentLine = rinFile.readline()
    while currentLine != "":
      
        if (currentLine[27:30]) == " 0 ":
            year = int(currentLine[1:3])
            if year < 80: 
                year = 2000 + year
            else: 
                1900 + year
            month = int(currentLine[4:6])
            day = int(currentLine[7:9])
            hour = int(currentLine[10:12])
            mm = int(currentLine[13:15])
            sec = float(currentLine[16:26])
            # ‚ÂÏˇ 
            # gpsRecord["time"] = str(datetime.date(year, month, day).isoweekday() \
            #  % 7 * 24 * 3600 + hour * 3600 + mm * 60 + sec)
            timef=datetime.date(year, month, day).isoweekday() \
              // 7  + hour + mm/60. + sec/3600.
            gpsRecord["time"] = str('{:.3f}'.format(timef))   
            # Parse the PRN values for this epoch
            numSats = int(currentLine[30:32]) # ˜ËÒÎÓ ÒÔÛÚÌËÍÓ‚
            #print('numSats=',numSats)
            epochPRN = []
            for j in range(int(numSats / 12)):
   
                for i in range(12):
                    epochPRN.append(currentLine[32+i*3:35+i*3])
                    #print(currentLine[32+i*3:35+i*3])
            # ÂÒÎË ÒÔÛÚÌËÍÓ‚ > 12
            if (numSats>12):
                currentLine = rinFile.readline()
            for i in range(numSats % 12):
            
                epochPRN.append(currentLine[32+i*3:35+i*3])
                #print(i,currentLine[32+i*3:35+i*3])
            for prn in epochPRN:
                gpsRecord["prn"] = prn
                for j in range(int(numFields / 5)):
                    currentLine = rinFile.readline()
                    for i in range(5):
                        record = currentLine[i*16+1:i*16+14].lstrip()
                        if record == "":
                            gpsRecord[rinFields[j*5+i]] = "0"
                        else:
                            gpsRecord[rinFields[j*5+i]] = record
                #currentLine = rinFile.readline()
                for i in range(numFields % 5):
                    currentLine = rinFile.readline()
                    record = currentLine[i*16+1:i*16+14].lstrip()
                    if record == "":
                        gpsRecord[rinFields[numFields/5*5+i]] = "0"
                    else:
                        gpsRecord[rinFields[numFields//5*5+i]] = record
            
            
                csvLine = ""
                for field in csvFields:
                    csvLine += gpsRecord[field] + ","
                csvFile.write(csvLine[:-1]+"\r\n")

        currentLine = rinFile.readline()


    # Close files 
    rinFile.close()
    csvFile.close()
    print('Parsing ',rinFileName,' end')
