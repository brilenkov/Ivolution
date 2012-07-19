#!/usr/bin/env python

import os

import webbrowser

import logging

from gi.repository import Gtk

from AboutDialog import AboutDialog

import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) # import parent folder

from facemovie import Facemovie_lib
from facemovie import FaceParams
from facemovie import FacemovieThread

class IvolutionWindow(FacemovieThread.Observer):       
    def __init__(self, name):
        FacemovieThread.Observer.__init__(self, name)

        self.my_logger = None
        self.console_logger = None

        self.builder = Gtk.Builder()
        self.builder.add_from_file("data/ui/IvolutionWindow.glade")
        #self.builder.connect_signals({ "on_ivolutionwindow_destroy" : Gtk.main_quit })
        self.window = self.builder.get_object("ivolution_window")
        self.window.show()
        self.builder.connect_signals(self)       

        ## Defines parameters needed to run the FaceMovie
        self.root_fo = ""
        self.in_fo = "" # Input folder, where images are located
        self.out_fo = "" # Input folder, where the video will be saved
        self.mode = "crop" # type of video to be created
        self.sort = "name" # how image files will be chronologically sorted
        self.speed = 1 # Speed of the movie
        self.param = "frontal_face" # type of face profile to be searched for

        self.in_fo = "" # Input folder, where imaes are located

        self.facemovie = None

        self.AboutDialog = None # class

        self.setup()
        self.setup_logger()

    def setup(self):
        """
        Sets up all the default paramters and retrieve the element of the GUI we want to follow
        """
        self.AboutDialog = AboutDialog  # FIXME : Still not working

        self.startbutton = self.builder.get_object("startbutton")

        self.filechooserinput = self.builder.get_object("filechooserinput")
        self.filechooseroutput = self.builder.get_object("filechooseroutput")
        
        self.typecombobox = self.builder.get_object("typecombobox")
        self.typecombobox.set_active(0)

        self.speedcombobox = self.builder.get_object("speedcombobox")
        self.speedcombobox.set_active(0)

        self.cropradiobutton = self.builder.get_object("cropradiobutton")
        self.namesortradiobutton = self.builder.get_object("namesortradiobutton")

    # Signal handling related stuff

    def on_cropradiobutton_toggled(self,widget):
        """
        We need to take care only of this one as both are grouped
        """
        if widget.get_active(): # means crop is activated
            self.mode = "crop"
        else:
            self.mode = "conservative"

    def on_namesortradiobutton_toggled(self,widget):
        """
        We need to take care only of this one as both are grouped
        """
        if widget.get_active(): # means name is activated
            self.sort = "name"
        else:
            self.sort = "exif"

    def on_startbutton_pressed(self, widget):
        """
        Sets all parameters and start processing
        """
        self.set_parameters()
        self.print_parameters()
        # Instantiating the facemovie
        self.facemovie = FacemovieThread.FacemovieThread(self.face_params)
        self.facemovie.subscribe(self) # I want new information !
        self.facemovie.start()

    def on_stopbutton_pressed(self, widget):
        """
        Asks the Facemovie thread to terminate
        """
        print "Stop"    

    def on_destroy(self, widget, data=None):
        """Called when the IvolutionWindow is closed."""
        # Clean up code for saving application state should be added here.
        Gtk.main_quit()
        print "Gtk Exited"

    def on_menu_about_activate(self, widget, data=None):
        """
        Displays the about box for Ivolution
        # FIXME : Can start several about Dialogs at the same time
        """
        if self.AboutDialog is not None:
            about = self.AboutDialog()

    def on_menu_help_activate(self, widget, data=None):
        """
        Opens a browser and points to online help.
        """
        url = "http://jlengrand.github.com/FaceMovie/"
        webbrowser.open(url,new=2) # in new tab if possible
        #print "Should open help"

    #Methods processing data
    def set_parameters(self):
        """
        Sets all needed parameters for create the movie.
        """
        self.in_fo = self.filechooserinput.get_current_folder() + "/" # TODO : Find correct fix
        self.out_fo = self.filechooseroutput.get_current_folder() + "/" # TODO : Find correct fix
        self.param = self.typecombobox.get_active_text()
        self.speed = self.speedcombobox.get_active() # We need and integer between 0 and 2

        # Instantiating the face_params object that will be needed by the facemovie
        par_fo = os.path.join(self.root_fo, "haarcascades")
        self.face_params = FaceParams.FaceParams(par_fo,
                                                self.in_fo,
                                                self.out_fo,
                                                self.param,
                                                self.sort,
                                                self.mode,
                                                self.speed)

    def print_parameters(self):
        print "#########"
        print "Settings:"
        print "input folder :   %s" %( self.in_fo)
        print "output folder :   %s" %( self.out_fo)

        print "Face Type :   %s" %( self.param)
        print "Speed chosen :   %s" %( self.speed)
        print "Mode chosen :   %s" %( self.mode)
        print "Sort method :   %s" %( self.sort)

        print "#########"   


    def setup_logger(self):
        """
        Configures our logger to save error messages
        Start logging in file here
        """
        # create logger for  'facemovie'
        self.my_logger = logging.getLogger('FileLog')
        self.my_logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        fh = logging.FileHandler('log/fm.log')
        fh.setLevel(logging.DEBUG)
        # create console handler with a higher log level
        self.console_logger = logging.getLogger('ConsoleLog')
        self.console_logger.setLevel(logging.DEBUG) # not needed

        ch = logging.StreamHandler()
        #ch.setLevel(logging.DEBUG) # not needed

        # add the handlers to the logger
        self.my_logger.addHandler(fh)
        
        self.my_logger.info("######") # Separating different sessions

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # create formatter and add it to the handlers
        fh.setFormatter(formatter)
        #ch.setFormatter(formatter)

        self.console_logger.addHandler(ch)

if __name__ == "__main__":
    app = IvolutionWindow()
    Gtk.main()        