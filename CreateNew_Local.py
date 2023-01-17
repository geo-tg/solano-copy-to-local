'''
CreateNew_Local.py

Creates a local copy of Solano's parcel dataset from SDE feature dataset.
Process was created due to latency in SDE conenctions and unreliability
in connection. The project manager or current technical lead of Solano project
should be consulted before the process in run. 

Variables requiring updates:
    - solano_dir: path to parent directory. The folder "Solano_Archive" and the 
    file geodatabase "Solano_Local.gdb" should be stored in this path. 
    - sde_cxn: connection file name to Solano SDE. Consult with technical lead to 
    determine requirements of database connection (user, version, etc.) This file 
    must be stored in the solano_dir path. 

Author:
    D. Allcott, GTG

Version History:
    12/22/2022  |   D. Allcott  | Script created
    01/04/2023  |   J. Beasley  | Changed from copy to export/import XML. 
        Found error with copying feature class that has attrbute rules using
        a database sequence. Users other than the owner of the sequence cannot
        copy the feature class. We cannot share the user's credentials. The
        import and export XML methods do not have this restriction. Changes 
        implemented in ArcGIS Pro 2.9.x environment. 

'''

import arcpy
import os
from datetime import datetime
import traceback

arcpy.env.preserveGlobalIds = True
arcpy.env.overwriteOutput = True

today = datetime.now().strftime('%Y%m%d')

solano_dir = r"" # Populate with your parent directory

archive_dir = os.path.join(solano_dir, "Solano_Archive")
solano_fgdb = os.path.join(solano_dir, f"Solano_Local.gdb")

sde_cxn = os.path.join(solano_dir, "") # Populate with your SDE connection name
sde_fdataset_name = "solano.GTG.EditData"
sde_featuredataset = os.path.join(sde_cxn, sde_fdataset_name)

sde_parcels = os.path.join(sde_featuredataset, "solano.GTG.Development_Parcels")

archive_fgdb = os.path.join(archive_dir, f"Solano_Local_{today}.gdb")
print(f"Archiving fgdb to {archive_fgdb}")

print("Starting processing...")

try:
    print("Copying Local GDB to Archive folder...")
    arcpy.management.Copy(solano_fgdb, archive_fgdb)

    print("Deleting Local GDB...")
    arcpy.management.Delete(solano_fgdb)

    print("Recreating Solano_Local.gdb...")
    fgdb = str(arcpy.management.CreateFileGDB(solano_dir, "Solano_Local")[0])

    print("Exporting EditData feature dataset from SDE...")
    out_xml = os.path.join(solano_dir, f"solano_EditData_{today}.xml")
    arcpy.management.ExportXMLWorkspaceDocument(sde_featuredataset, out_xml, "DATA")

    print("Importing XML workspace to local fgdb...")
    arcpy.management.ImportXMLWorkspaceDocument(fgdb, out_xml, "DATA")

    fdataset = os.path.join(fgdb, "EditData")
    local_parcels = os.path.join(fdataset, "Development_Parcels")

    print("Deleting topology...")
    arcpy.management.Delete(f"{fdataset}\parcelTopology")

    print("Building topology...")
    topology = arcpy.management.CreateTopology(fdataset, 'parcelTopology', 0.0032808333)

    print("Adding parcels to topology...")
    arcpy.management.AddFeatureClassToTopology(topology, local_parcels, 1)

    print("Adding rules...")
    arcpy.management.AddRuleToTopology(topology, "Must Not Have Gaps (Area)", local_parcels)
    arcpy.management.AddRuleToTopology(topology, "Must Not Overlap (Area)", local_parcels)
    
    print("Validating at full extent...")
    arcpy.management.ValidateTopology(topology, "Full_Extent")

    print("Done!")

except Exception as e:

    print(e)
    traceback.print_exc()
    

