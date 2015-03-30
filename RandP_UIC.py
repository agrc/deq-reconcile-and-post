# This script reconciles and posts versions of the UIC enterprise geodatabase

# from each editors version up through UIC_QA, UIC_Surrogate_Default, DEFAULT.

#

# The script will terminate if a conflict is detected during the reconcile

# process after writing a log of the conflicts to the following file:

#

#   conflict file:

#

# If no conflicts are detected during reconciliation, then the script will post

# to the target version.

#

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#  UIC Enterprise GDB Version Tree looks like this:

#

#                   DEFAULT

#                   Owner: sdeAdmin

#                   Access: Public

#                        |

#                   UIC_Surrogate_Default

#                   Owner: UICAdmin

#                   Access: Protected

#                       |

#                   UIC_QA

#                   Owner: UICAdmin

#                   Access: Protected

#                /                   \

#    UIC_CCady                        UIC_BAriotti

#    Owner: CCady                     Owner: BAriotti

#    Access: Protected                Access: Protected

#         |                                 |

#    UIC_RnP_CCady                    UIC_RnP_BAriotti                    The RnP versions are RnP?d

#    Owner: UICAdmin                  Owner: UICAdmin                      by UICAdmin to UIC_QA.

#    Access: Private                  Access: Private

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# After reconciling and posting up to DEFAULT, the script deletes all versions
# except DEFAULT!  (All children must be deleted before parents can be deleted.  Only owners
# can create/delete their versions.) The UIC GDB is then compressed.  Following compression
# the version tree is recreated.



import arcpy

import sys

from arcpy import env

#  Connect as UICAdmin user
uicAdmin = r'Database Connections\UICAdmin.DefaultSpecific.sde'

uicBAriotti = r'Database Connections\BAriotti.sde'  # <?? this is used when we need to delete/create Brianna?s version

uicCCady = r'Database Connections\CCady.sde' # <?? this is used when we need to delete/create Candy?s version

arcpy.env.workspace = uicAdmin

log = r'C:\\'

# Zach ? rather than counting the number of versions, let?s check to see if UIC_RnP_BAriotti and

# UIC_RnP_CCady exist.  There may be a circumstance in which I will want to create a version

# of the gdb that will not be involved in the RnP process.  So if we count versions then that

# additional version will screw up the code.

#

# If the RnP versions exist then UICAdmin will delete them then re?create them.  I know this

# sounds silly but the RnP versions may exist because there was a conflict during reconciliation

# with UIC_QA which aborted the script before the RnP versions were deleted.

#

#  Count the number of versions to which UICAdmin has access.

#  From the version tree above, UICAdmin has access to 7 versions.

#

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

#?????Create Versions?????

# Following is the syntax for Create Version

# CreateVersion_management (in_workspace, parent_version, version_name,

# {access_permission})

# Zach ? we need to make sure that the PRIVATE RnP versions are owned by UICAdmin

try:
    for version in versionDict:
        arcpy.CreateVersion_management(uicAdmin, version, versionDict[version], 'PRIVATE')
        print 'Created ' + version

except:
    print 'Failed to create versions'
    sys.exit()

#?????Reconcile Edit Versions?????

#  Following is the syntax for Reconcile Versions

#  ReconcileVersions_management (input_database, reconcile_mode, {target_version},

#  {edit_versions}, {acquire_locks}, {abort_if_conflicts}, {conflict_definition}, {conflict_resolution},

#   {with_post}, {with_delete}, {out_log})

#

#  2nd parameter: reconcile_mode ? BLOCKING_VERSIONS ? Reconciles versions that are

#  blocking the target version from compressing. This option uses the recommended reconcile

#  order which is ????????????

#

#  5th parameter: acquire_locks ? LOCK_AQUIRED ?  Acquires locks during the reconcile

#  process.  This should be used when the intention is to post edits.  It ensures that the target

#  version is not modified in the time between the reconcile and post operations. This is the

#  default.

#

#  6th parameter: abort_if_conflicts ? ABORT_CONFLICTS ? Aborts the reconcile if conflicts are

#  found.  Zach ? I think 'ABORT_CONFLICT' should be 'ABORT_CONFLICTS' with an 'S'

#

#  7th parameter: conflict_definition ? BY_OBJECT ? Any changes to the same row or feature in

#   the parent and child versions will conflict during reconcile.  This is the default.

#

#  9th parameter: with_post ? POST ? Current edit version will be posted to the target version

#  after the reconcile.

#  Zach ? I think we need to set this parameter (the 2nd ?#? in your code) to POST.  I don't see

#  anywhere else in the code where posting  is done.  I also think there is on too many

#  parameters.  There should be 11, I count 12.

try:
    for version in versionDict:
        arcpy.ReconcileVersion_management(uicAdmin, 'BLOCKING_VERSIONS', uicQA, \
                                          version, 'LOCK_ACQUIRED', 'ABORT_CONFLICT', 'BY_OBJECT', \
                                          '#', '#', '#', '#', log + versionDict[version] + 'ERRORS')

        print 'Reconciled ' + versionDict[version]

except:
    print 'Failed to Reconcile Edit Versions'
    sys.exit()

#  Zach ? shouldn't we be setting 'reconcile_mode' to 'BLOCKING_VERSIONS' in the 2 lines of

#  code below?

#  What if for some reason (unknown to me right now) I made an edit in Surrogate?  Wouldn't

#   that edit be lost by the code below?

#  And again, I think the ??with_post?? parameter needs to be set to POST when reconciling to

#  Surrogate and Default.

#

#?????Reconcile QA and Surrogate Versions?????

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

#?????Delete Versions?????

#  BLAHBLAHABLLAKLJ'DFLGK'

#  Versions can only be deleted by their owners and you can't delete a version

#  that is a parent of a child until you delete the child. (So in a weird twist,

#  parents can't die until their children die!) :s

#

#  After RnPing to DEFAULT, I have been deleting the RnP versions (connected as

#  UICAdmin); then I connect as BAriotti and delete UIC_BAriotti; then I connect

#  as CCady and delete UIC_CCady; finally I reconnect as UICAdmin and delete

#  UIC_QA and UIC_Surrogate_Default


for version in arcpy.da.ListVersions(uicAdmin):

    if version.name != default:
        arcpy.DeleteVersion_management(uicAdmin, version.name)

arcpy.Compress_management(uicAdmin)


#?????Re?Create Version Tree?????

#  connected as UICAdmin:
arcpy.CreateVersion_management(uicAdmin, default, uicSurrogate, "PROTECTED")

arcpy.CreateVersion_management(uicAdmin, uicSurrogate, uicQA, "PROTECTED")

#  connected as BAriotti:
arcpy.CreateVersion_management(uicBAriotti, uicQA, 'BARIOTTI.UIC_BAriotti', "PROTECTED")

# connected as CCady:
arcpy.CreateVersion_management(uicCCady, uicQA, 'CCADY.UIC_CCady', "PROTECTED")