# deq-reconcile-and-post
Script to automate deq SDE reconciling and posting
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
