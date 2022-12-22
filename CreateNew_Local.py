import arcpy
import os
from datetime import datetime

arcpy.env.preserveGlobalIds = True
arcpy.env.overwriteOutput = True

today = datetime.now().strftime('%Y%m%d')

solano_dir = r"" # Populate with your parent directory
archive_dir = os.path.join(solano_dir, "Solano_Archive")

solano_fgdb = os.path.join(solano_dir, f"Solano_Local.gdb")
sde_cxn = ""
sde_fdataset_name = "solano.GTG.EditData"
sde_featuredataset = os.path.join(solano_dir, sde_cxn, sde_fdataset_name)

sde_parcels = os.path.join(sde_featuredataset, "solano.GTG.Development_Parcels")

archive_fgdb = os.path.join(archive_dir, f"Solano_Local_{today}.gdb")
print(f"Archiving fgdb to {archive_fgdb}")

print("Copying Local GDB to Archive folder...")
arcpy.management.Copy(solano_fgdb, archive_fgdb)
print("Deleting Local GDB...")
arcpy.management.Delete(solano_fgdb)

print("Recreating Solano_Local.gdb...")
fgdb = str(arcpy.CreateFileGDB_management(solano_dir, "Solano_Local")[0])
print("Creating EditData feature dataset...")
fdataset = str(arcpy.CreateFeatureDataset_management(fgdb, 'EditData', sde_parcels)[0])

# Feature Class to GDB doesn't work because it doesn't bring related tables, so we use management.Copy instead

local_parcels = os.path.join(fdataset, "Development_Parcels")

print("Copying SDE parcels to Local GDB...")
arcpy.management.Copy(sde_parcels, local_parcels)

# build topology

print("Building topology...")
topology = arcpy.CreateTopology_management(fdataset, 'parcelTopology', 0.0032808333)
print("Adding parcels to topology...")
arcpy.AddFeatureClassToTopology_management(topology, local_parcels, 1)
print("Adding rules...")
arcpy.AddRuleToTopology_management(topology, "Must Not Have Gaps (Area)", local_parcels)
arcpy.AddRuleToTopology_management(topology, "Must Not Overlap (Area)", local_parcels)
print("Validating at full extent...")
arcpy.ValidateTopology_management(topology, "Full_Extent")

