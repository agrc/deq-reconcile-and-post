import arcpy
import sys
from arcpy import env

uicAdmin = r'Database Connections\UICAdmin.DefaultSpecific.sde'
uicBAriotti = r'Database Connections\BAriotti.sde'
uicCCady = r'Database Connections\CCady.sde'

arcpy.env.workspace = uicAdmin

log = r'C:\\'

default = 'sde.DEFAULT'
uicSurrogate = 'UICADMIN.UIC_Surrogate_Default'
uicQA = 'UICADMIN.UIC_QA'
cCady = 'CCADY.UIC_CCady'
bAriotti = 'BARIOTTI.UIC_BAriotti'
cCady_rnp = 'UICADMIN.UIC_RnP_CCady'
bAriotti_rnp = 'UICADMIN.UIC_RnP_BAriotti'

sourceVersions = [default, uicSurrogate, uicQA, cCady, bAriotti]
versionLst = []

for version in arcpy.da.ListVersions(uicAdmin):
    versionLst.append(version.name)
    print version.name
for sVersion in sourceVersions:
    if sVersion not in versionLst:
        print 'Insufficient Versions Exist'
        sys.exit()
    else:
        continue

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




# try:
#     for version in versionDict:
#         arcpy.ReconcileVersion_management(uicAdmin, 'BLOCKING_VERSIONS', uicQA, \
#                                           version, 'LOCK_ACQUIRED', 'ABORT_CONFLICT', 'BY_OBJECT', \
#                                           '#', '#', '#', '#', log + versionDict[version] + 'ERRORS')
#
#         print 'Reconciled ' + versionDict[version]
#
# except:
#     print 'Failed to Reconcile Edit Versions'
#     sys.exit()
#
#
# try:
#     arcpy.ReconcileVersion_management(uicAdmin, 'ALL_VERSIONS', uicSurrogate, uicQA,
#                                       'LOCK_ACQUIRED', 'ABORT_CONFLICT', 'BY_OBJECT', \
#                                       '#', '#', '#', '#', log + 'UIC_QA_ERRORS')
#
#     arcpy.ReconcileVersion_management(uicAdmin, 'ALL_VERSIONS', default, uicSurrogate,
#                                       'LOCK_ACQUIRED', 'ABORT_CONFLICT', 'BY_OBJECT', \
#                                       '#', '#', '#', '#', log + 'UIC_Surrogate_ERRORS')
#
# except:
#     print 'Failed to Reconcile QA and Surrogate Versions'
#     sys.exit()
#
#
#
# for version in arcpy.da.ListVersions(uicAdmin):
#
#     if version.name != default:
#         arcpy.DeleteVersion_management(uicAdmin, version.name)
#
# arcpy.Compress_management(uicAdmin)
#
#
#
#
# #  connected as UICAdmin:
# arcpy.CreateVersion_management(uicAdmin, default, uicSurrogate, "PROTECTED")
#
# arcpy.CreateVersion_management(uicAdmin, uicSurrogate, uicQA, "PROTECTED")
#
# #  connected as BAriotti:
# arcpy.CreateVersion_management(uicBAriotti, uicQA, 'BARIOTTI.UIC_BAriotti', "PROTECTED")
#
# # connected as CCady:
# arcpy.CreateVersion_management(uicCCady, uicQA, 'CCADY.UIC_CCady', "PROTECTED")
