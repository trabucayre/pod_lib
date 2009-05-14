#! /usr/bin/python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Name:     ise.py
# Purpose:  
# Author:   Fabien Marteau <fabien.marteau@armadeus.com>
# Created:  21/07/2008
#-----------------------------------------------------------------------------
#  Copyright (2008)  Armadeus Systems
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software 
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
#-----------------------------------------------------------------------------
# Revision list :
#
# Date       By        Changes
#
#-----------------------------------------------------------------------------

__doc__ = ""
__version__ = "1.0.0"
__versionTime__ = "21/07/2008"
__author__ = "Fabien Marteau <fabien.marteau@armadeus.com>"

import time
import datetime

from periphondemand.bin.define import *
from periphondemand.bin.utils.settings import Settings
from periphondemand.bin.utils.error    import Error
from periphondemand.bin.utils.display  import Display
from periphondemand.bin.utils          import wrappersystem as sy

from periphondemand.bin.core.component  import Component
from periphondemand.bin.core.port       import Port
from periphondemand.bin.core.interface  import Interface
from periphondemand.bin.core.hdl_file   import Hdl_file

settings = Settings()
display = Display()
TAB = "    "

def generatepinout(self,filename=None):
    """ Generate the constraint file .ucf for xilinx fpga
    """
    if filename is None:
        filename = settings.projectpath+ SYNTHESISPATH+"/"+\
                settings.active_project.getName()+ UCFEXT
    self.project = settings.active_project
    out = "# Constraint file, automaticaly generated by pod \n"
    for interface in self.project.getPlatform().getInterfacesList():
        for port in interface.getPortsList():
            if port.getListOfPin() != []:
                pin = port.getListOfPin()
                # Platform ports are all 1-sized, raise error if not
                if len(pin) != 1:
                    raise Error("Platform port "+port.getName()+\
                            " has size different of 1",0)
                pin = pin[0]
                # Only one connection per platform pin can be branched. 
                # If several connections found, only first is used
                if pin.getConnections() != []:
                    connect = pin.getConnections()
                    if len(connect) > 1:
                        display.msg("[WARNING] severals pin connected to "+\
                                port.getName()+\
                                ". Only "+connect[0]["instance_dest"]+"."+\
                                          connect[0]["interface_dest"]+"."+\
                                          connect[0]["port_dest"]+"."+\
                                          connect[0]["pin_dest"]+\
                                          " will be branch",0)
                    instancedest = self.project.getInstance(connect[0]["instance_dest"])
                    interfacedest = instancedest.getInterface(connect[0]["interface_dest"])
                    portdest = interfacedest.getPort(connect[0]["port_dest"])
                    out = out+'NET "'\
                            +connect[0]["instance_dest"] + "_" + connect[0]["port_dest"]
                    if self.project.getInstance(
                            connect[0]["instance_dest"]).getInterface(
                                    connect[0]["interface_dest"]).getPort(
                                            connect[0]["port_dest"]).getSize() != "1":
                        if portdest.isCompletelyConnected():
                            out=out+"<"+connect[0]["pin_dest"]+">"
                        else:
                            out=out+"_pin"+connect[0]["pin_dest"]
                    out = out +'" LOC="'+str(port.getPosition())\
                              +'" | IOSTANDARD='+str(port.getStandart());
                    if port.getDrive() != None:
                        out = out + " | DRIVE="+str(port.getDrive())
                    out = out+';'+r'# '+str(port.getName())+'\n'

                    # if port as frequency parameters, it's a clock.
                    # then had xilinx clock constraint
                    try:
                        frequency = port.getFreq()
                        out = out+"NET \""+\
                                connect[0]["instance_dest"]+\
                                "_"+connect[0]["port_dest"]+\
                                "\" TNM_NET = \""+\
                                connect[0]["instance_dest"]+\
                                "_"+connect[0]["port_dest"]+\
                                "\";\n"
                        out = out+"TIMESPEC \"TS_"+\
                                connect[0]["instance_dest"]+\
                                "_"+connect[0]["port_dest"]+\
                                "\" = PERIOD \""+\
                                connect[0]["instance_dest"]+\
                                "_"+connect[0]["port_dest"]+\
                                "\" "+\
                                "%g"%((1000/float(frequency)))+\
                                " ns HIGH 50 %;\n"
                    except:
                        pass
                    
    out = out + "#end\n"
    try:
        file = open(filename,"w")
    except IOError, e:
        raise Error(str(e),0)
    file.write(out)
    file.close()
    display.msg("Constraint file generated with name :"+filename)
    return filename

def generateTCL(self,filename=None):
    """ generate tcl script for ise
    """
    if filename is None:
        filename = settings.active_project.getName() + TCLEXT
    tclfile = open(settings.projectpath +SYNTHESISPATH+"/"+ filename,"w")
    tclfile.write("# TCL script automaticaly generated by POD\n")
    tclfile.write("cd .."+OBJSPATH+"\n")
    # create project
    tclfile.write("project new "+settings.active_project.getName()+".ise\n")
    
    # Configuration
    tclfile.write("# configure platform params\n")
    platform = settings.active_project.getPlatform()
    tclfile.write("project set family "+platform.getFamily()+"\n")
    tclfile.write("project set device "+platform.getDevice()+"\n")
    tclfile.write("project set package "+platform.getPackage()+"\n")
    tclfile.write("project set speed "+platform.getSpeed()+"\n")
    tclfile.write("project set {Preferred Language} VHDL\n")

    # Source files
    tclfile.write("## add components sources file\n")
    tclfile.write("# add top level sources file\n")
    tclfile.write("xfile add .."+SYNTHESISPATH+"/top_"+\
            settings.active_project.getName()+VHDLEXT+"\n")

    for directory in sy.listDirectory(settings.projectpath+SYNTHESISPATH):
        for file in sy.listFiles(settings.projectpath+\
                                 SYNTHESISPATH+\
                                 "/"+directory):
            tclfile.write("xfile add .."+SYNTHESISPATH+"/"+directory+"/"+file+"\n")

    # Constraints files
    tclfile.write("# add constraint file\n")
    tclfile.write("xfile add .."+SYNTHESISPATH+"/"+\
            settings.active_project.getName() + UCFEXT+" \n")
    # Run synthesis
    tclfile.write('process run "Generate Programming File"\n')

    # Run post synthesis model generation
    tclfile.write('process run "Generate Post-Synthesis Simulation Model"\n')
    #    tclfile.write('cp netgen/synthesis/top_'+settings.active_project.getName()+\
    #        '_synthesis.vhd ../simulation/\n')
    # Run post place and route model generation
    tclfile.write('process run "Generate Post-Place & Route Simulation Model"\n')
    #tclfile.write('cp netgen/par/top_'+settings.active_project.getName()+\
    #        '_timesim.vhd ../simulation/\n')

    display.msg("TCL script generated with name : "+\
            settings.active_project.getName()+TCLEXT)
    return settings.active_project.getName()+TCLEXT

def generateBitStream(self,commandname,scriptname):
    """ generate the bitstream """
    pwd = sy.pwd()
    sy.deleteAll(settings.projectpath+OBJSPATH)
    sy.chdir(settings.projectpath+SYNTHESISPATH)
    for line in sy.launchAShell(commandname,scriptname):
        if settings.color()==1:
            print COLOR_SHELL+line+COLOR_END,
        else:
            print "SHELL>"+line,
    try:
        sy.copyFile(settings.projectpath+OBJSPATH+"/"+\
                    BINARY_PREFIX+settings.active_project.getName()+\
                    BINARY_SUFFIX,
                    settings.projectpath+BINARYPROJECTPATH+"/")
    except IOError:
        raise Error("Can't copy bitstream")
    sy.chdir(pwd)
