import arcpy
import sys
from arcpy import env

uicAdmin = r'Database Connections\UICAdmin.DefaultSpecific.sde'

uicBAriotti = r'Database Connections\BAriotti.sde'
uicCCady = r'Database Connections\CCady.sde' 

arcpy.env.workspace = uicAdmin

log = r'C:\\'


versionCount = 0

for version in arcpy.da.ListVersions(uicAdmin):
    versionCount = versionCount + 1
    print version.name

if versionCount > 5:
    print 'RnP Version(s) might already exist'
    sys.exit()

versionDict = {'BARIOTTI.UIC_BAriotti':'UIC_RnP_BAriotti', 'CCADY.UIC_CCady':'UIC_RnP_CCady'}

uicQA = 'UICADMIN.UIC_QA'

uicSurrogate = 'UICADMIN.UIC_Surrogate_Default'

default = 'sde.DEFAULT'


try:
    for version in versionDict:
        arcpy.CreateVersion_management(uicAdmin, version, versionDict[version], 'PRIVATE')
        print 'Created ' + version

except:
    print 'Failed to create versions'
    sys.exit()


try:
    for version in versionDict:
        arcpy.ReconcileVersion_management(uicAdmin, 'BLOCKING_VERSIONS', uicQA, \
                                          version, 'LOCK_ACQUIRED', 'ABORT_CONFLICT', 'BY_OBJECT', \
                                          '#', '#', '#', '#', log + versionDict[version] + 'ERRORS')

        print 'Reconciled ' + versionDict[version]

except:
    print 'Failed to Reconcile Edit Versions'
    sys.exit()


try:
    arcpy.ReconcileVersion_management(uicAdmin, 'ALL_VERSIONS', uicSurrogate, uicQA,
                                      'LOCK_ACQUIRED', 'ABORT_CONFLICT', 'BY_OBJECT', \
                                      '#', '#', '#', '#', log + 'UIC_QA_ERRORS')

    arcpy.ReconcileVersion_management(uicAdmin, 'ALL_VERSIONS', default, uicSurrogate,
                                      'LOCK_ACQUIRED', 'ABORT_CONFLICT', 'BY_OBJECT', \
                                      '#', '#', '#', '#', log + 'UIC_Surrogate_ERRORS')

except:
    print 'Failed to Reconcile QA and Surrogate Versions'
    sys.exit()



for version in arcpy.da.ListVersions(uicAdmin):

    if version.name != default:
        arcpy.DeleteVersion_management(uicAdmin, version.name)

arcpy.Compress_management(uicAdmin)




#  connected as UICAdmin:
arcpy.CreateVersion_management(uicAdmin, default, uicSurrogate, "PROTECTED")

arcpy.CreateVersion_management(uicAdmin, uicSurrogate, uicQA, "PROTECTED")

#  connected as BAriotti:
arcpy.CreateVersion_management(uicBAriotti, uicQA, 'BARIOTTI.UIC_BAriotti', "PROTECTED")

# connected as CCady:
arcpy.CreateVersion_management(uicCCady, uicQA, 'CCADY.UIC_CCady', "PROTECTED")
