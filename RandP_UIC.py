import arcpy
import sys
import datetime
from arcpy import env

uicAdmin = r'Database Connections\UICAdmin.DefaultSpecific.sde'
uicBAriotti = r'Database Connections\BAriotti.sde'
uicCCady = r'Database Connections\CCady.sde'

default = 'sde.DEFAULT'
uicSurrogate = 'UICADMIN.UIC_Surrogate_Default'
uicQA = 'UICADMIN.UIC_QA'
cCady = 'CCADY.UIC_CCady'
bAriotti = 'BARIOTTI.UIC_BAriotti'
cCady_rnp = 'UICADMIN.UIC_RnP_CCady'
bAriotti_rnp = 'UICADMIN.UIC_RnP_BAriotti'

arcpy.env.workspace = uicAdmin

#---Reconcile and Post---
def RandP_Versions():

    #---Check for necessary versions
    versionLst = []
    sourceVersions = [default, uicSurrogate, uicQA, cCady, bAriotti]
    log = r'C:\\'

    for version in arcpy.da.ListVersions(uicAdmin):
        versionLst.append(version.name)
    for sVersion in sourceVersions:
        if sVersion not in versionLst:
            print 'Insufficient Versions Exist'
            sys.exit()
        else:
            continue


    #---Create RnP versions if they don't exist
    if cCady_rnp not in versionLst:
        try:
            arcpy.CreateVersion_management(uicAdmin, cCady, 'UIC_RnP_CCady', 'PRIVATE')
        except:
            print 'Could not create ' + cCady_rnp
            sys.exit()

    if bAriotti_rnp not in versionLst:
        try:
            arcpy.CreateVersion_management(uicAdmin, bAriotti, 'UIC_RnP_BAriotti', 'PRIVATE')
        except:
            print 'Could not create ' + bAriotti_rnp
            sys.exit()


    today = str(datetime.date.today())

    #---Reconcile/Post RnP Versions to QA
    print 'Reconcile and Post ' + cCady_rnp
    arcpy.ReconcileVersions_management(uicAdmin, 'ALL_VERSIONS', uicQA, cCady_rnp, 'LOCK_ACQUIRED', 'ABORT_CONFLICTS', \
                                       'BY_OBJECT', 'FAVOR_EDIT_VERSION', 'POST', '#', log + cCady_rnp + '_RnP' + today + '.txt')

    print 'Reconcile and Post ' + bAriotti_rnp
    arcpy.ReconcileVersions_management(uicAdmin, 'ALL_VERSIONS', uicQA, bAriotti_rnp, 'LOCK_ACQUIRED', 'ABORT_CONFLICTS', \
                                       'BY_OBJECT', 'FAVOR_EDIT_VERSION', 'POST', '#', log + bAriotti_rnp + '_RnP' + today + '.txt')

    #---Reconcile/Post QA Version to Surrogate
    print 'Reconcile and Post ' + uicQA
    arcpy.ReconcileVersions_management(uicAdmin, 'ALL_VERSIONS', uicSurrogate, uicQA, 'LOCK_ACQUIRED', 'ABORT_CONFLICTS', \
                                       'BY_OBJECT', 'FAVOR_EDIT_VERSION', 'POST', '#', log + uicQA + '_RnP' + today + '.txt')

    #---Reconcile/Post Surrogate to Default
    print 'Reconcile and Post ' + uicSurrogate
    arcpy.ReconcileVersions_management(uicAdmin, 'ALL_VERSIONS', default, uicSurrogate, 'LOCK_ACQUIRED', 'ABORT_CONFLICTS', \
                                       'BY_OBJECT', 'FAVOR_EDIT_VERSION', 'POST', '#', log + uicSurrogate + '_RnP' + today + '.txt')





#---Delete old versions---
def deleteVersions():
    versionOwner_Dict = {default:uicAdmin, uicSurrogate:uicAdmin, uicQA:uicAdmin, cCady:uicCCady, \
                     bAriotti:uicBAriotti, cCady_rnp:uicAdmin, bAriotti_rnp:uicAdmin}
    childList = []

    for version in arcpy.da.ListVersions(uicAdmin):
        for child in version.children:
            childList.append(child.name)

    for deleteChild in reversed(childList):
        arcpy.DeleteVersion_management(versionOwner_Dict[deleteChild], deleteChild)
        print 'DELETED ' + deleteChild

#---Compress UIC Geodatabase to State 0---

def createVersions():
    arcpy.CreateVersion_management(uicAdmin, default, uicSurrogate.split('.')[1], 'PROTECTED')
    arcpy.CreateVersion_management(uicAdmin, uicSurrogate, uicQA.split('.')[1], 'PROTECTED')
    arcpy.CreateVersion_management(uicCCady, uicQA, cCady.split('.')[1], 'PROTECTED')
    arcpy.CreateVersion_management(uicBAriotti, uicQA, bAriotti.split('.')[1], 'PROTECTED')




RandP_Versions()
deleteVersions()
createVersions()
