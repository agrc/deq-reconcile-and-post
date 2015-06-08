import arcpy
import sys
from arcpy import env

uicAdmin = r'Database Connections\DC_CAIADMIN@CAIDBTest@itdb110sp.dts.utah.gov.sde'
uicBAriotti = r'Database Connections\dc_ba_edti@CAIDBTest@itdb110sp.dts.utah.gov.sde'
uicCCady = r'Database Connections\dc_cc_edit@CAIDBTest@itdb110sp.dts.utah.gov.sde'

arcpy.env.workspace = uicAdmin

log = r'C:\\'

default = 'sde.DEFAULT'
uicSurrogate = 'CAIADMIN.Surrogate'
uicQA = 'CAIADMIN.QA'
cCady = 'CC_EDIT.UIC_CCady'
bAriotti = 'BA_EDIT.UIC_BAriotti'
cCady_rnp = 'CAIADMIN.UIC_RnP_CCady'
bAriotti_rnp = 'CAIADMIN.UIC_RnP_BAriotti'

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
