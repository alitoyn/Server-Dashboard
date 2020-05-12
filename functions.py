# Functions ----------------------------------------------------------------------------------------------------------------
## pulls the data from a row in the config file
def fileParse(dataToFind, fileVariable, index):
    if dataToFind in fileVariable[index]:
        tmp = fileVariable[index].split(": ")
        length = len(tmp)
        return tmp[length - 1]
    else:
        return ""

