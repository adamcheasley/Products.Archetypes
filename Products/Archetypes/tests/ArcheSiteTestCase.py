#
# ArcheSiteTestCase
#

# $Id: ArcheSiteTestCase.py,v 1.2 2003/11/03 21:44:22 dreamcatcher Exp $

import time

from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import noSecurityManager
from Acquisition import aq_base
from Testing import ZopeTestCase

from Products.Archetypes.Extensions.Install import install as installArchetypes

from Products.CMFPlone.tests import PloneTestCase

class ArcheSiteTestCase(PloneTestCase.PloneTestCase):
    """ archetypes test case with plone site """

    def getManagerUser(self):
        uf = self.portal.acl_users
        return uf.getUserById('PloneManager').__of__(uf)

    def getMemberUser(self):
        uf = self.portal.acl_users
        return uf.getUserById('PloneMember').__of__(uf)

def setupArchetypes(app, quiet=0):
    if not hasattr(app.portal, 'archetype_tool'):
        get_transaction().begin()
        _start = time.time()
        if not quiet: ZopeTestCase._print('Adding Archetypes ... ')

        uf = app.portal.acl_users
        # setup
        uf._doAddUser('PloneMember', '', ['Members'], [])
        uf._doAddUser('PloneManager', '', ['Manager'], [])
        # login as manager
        user = uf.getUserById('PloneManager').__of__(uf)
        newSecurityManager(None, user)
        # add Archetypes
        installArchetypes(app.portal, include_demo=1)
        # Log out
        noSecurityManager()
        get_transaction().commit()
        if not quiet: ZopeTestCase._print('done (%.3fs)\n' % (time.time()-_start,))

app = ZopeTestCase.app()
setupArchetypes(app)
ZopeTestCase.close(app)
