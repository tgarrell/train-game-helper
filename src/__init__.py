#!/usr/bin/env python3

#-------------------------------------------------------------------------------
# Import Stuff
#-------------------------------------------------------------------------------
import os
from flask import Flask

#-------------------------------------------------------------------------------
# Setup Flask Config
#-------------------------------------------------------------------------------
template_dir = os.path.join( os.path.dirname( os.path.abspath( __file__ )),
                             "../templates" )
static_dir = os.path.join( os.path.dirname( os.path.abspath( __file__ )),
                           "../static" )
app = Flask( __name__, template_folder=template_dir, static_folder=static_dir )
app.config.update( TEMPLATES_AUTO_RELOAD = True )

#-------------------------------------------------------------------------------
# Import Routes
#-------------------------------------------------------------------------------
from . import api

#-------------------------------------------------------------------------------
# Additional App Config
#-------------------------------------------------------------------------------
app.debug = True
app.secret_key = "train-game"
app.session_cookie_name = "train-game"
