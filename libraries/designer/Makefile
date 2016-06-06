###### EDIT ##################### 
#Directory with ui and resource files
RESOURCE_DIR = .
 
#Directory for compiled resources
COMPILED_DIR = ..
COMPILED_RESOURCES_DIR = ../..
 
#UI files to compile
#UI_FILES = $(wildcard *.ui)
UI_FILES = mainwindow.ui
#Qt resource files to compile
RESOURCES = resources.qrc 
 
#pyuic4 and pyrcc4 binaries
PYUIC = pyuic4
PYRCC = pyrcc4
 
#################################
# DO NOT EDIT FOLLOWING
 
COMPILED_UI = $(UI_FILES:%.ui=$(COMPILED_DIR)/%_ui.py)
COMPILED_RESOURCES = $(RESOURCES:%.qrc=$(COMPILED_RESOURCES_DIR)/%_rc.py)
 
all : resources ui 
 
resources : $(COMPILED_RESOURCES) 
 
ui : $(COMPILED_UI)
 
$(COMPILED_DIR)/%_ui.py : $(RESOURCE_DIR)/%.ui
	$(PYUIC) $< -o $@
 
$(COMPILED_RESOURCES_DIR)/%_rc.py : $(RESOURCE_DIR)/%.qrc
	$(PYRCC) $< -py3 -o $@
 
clean : 
	$(RM) $(COMPILED_UI) $(COMPILED_RESOURCES) $(COMPILED_UI:.py=.pyc) $(COMPILED_RESOURCES:.py=.pyc)  
