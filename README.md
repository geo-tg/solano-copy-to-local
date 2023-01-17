# solano-copy-to-local

This script is used to create a new local copy of Solano parcels from the Solano SDE.  <br>
  <br>
Running this script is recommended to be performed by each user post monthly deliverable, or weekly if preferred.  <br>
This will ensure each users local copy is as up to date as possible, and will match the SDE layer.

# Expected Folder Structure
  
    ├── Solano                    # Required Main folder where all user Solano data is stored
    |   ├──Solano_Archive         # Required Subfolder that holds archived Local gdb's
  
    ├── Solano_Local.gdb          # Naming convention for your Local gdb
    ├── sde_cxn                   # Variable that must be filled in by user for their SDE connection

# Links

For more information on the Solano Local setup, view the [Editing Locally SOP](https://geotechgroup.sharepoint.com/:w:/r/sites/SolanoCountyCA/_layouts/15/Doc.aspx?sourcedoc=%7BC50AC10B-D5DC-42EE-BA67-B43CFBF6F98C%7D&file=Editing_LocallySOP.docx&action=default&mobileredirect=true).