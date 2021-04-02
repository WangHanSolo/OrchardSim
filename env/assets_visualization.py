import pychrono.core as chrono
import pychrono.irrlicht as chronoirr
import math as m


print (" Demo of using the assets system to create shapes for Irrlicht visualization")


# The path to the Chrono directory containing various assets(meshes, textures, data files)
# is automatically set, relative to the default lcoation of this demo.
# If running from a different directory, you must change the path to the data directory with:
# chrono.SetChronoDataPath('relative/path/to/data/directory')

# Create a Chrono::Engine physical system
mphysicalSystem = chrono.ChSystemNSC()

# Create the Irrlicht visualization (open the Irrlicht device, bind a simple UI, etc, etc)
application = chronoirr.ChIrrApp(mphysicalSystem, "Pychrono", chronoirr.dimension2du(1024, 768))

# Set the path to the Chrono data directory
chrono.SetChronoDataPath("/home/han/chrono/orchardSim/data/")

# Easy shorcuts to add camera, lights, logo, and sky in Irrlicht scene
application.AddTypicalSky()
application.AddTypicalLogo(chrono.GetChronoDataFile('logo_pychrono_alpha.png'))
application.AddTypicalCamera(chronoirr.vector3df(0, 4, -6))
application.AddTypicalLights()


# Example 1:

# Create a ChBody, and attach some 'assets' that define 3D shapes for visualization purposes.
# Note: these assets are independent from collision shapes!

# Create a rigid body as usual, and add it
# to the physical system:
mfloor = chrono.ChBody()
mfloor.SetBodyFixed(True)


# Contact material
floor_mat = chrono.ChMaterialSurfaceNSC()


# Define a collision shape
mfloor.GetCollisionModel().ClearModel()
mfloor.GetCollisionModel().AddBox(floor_mat, 10, 0.5, 10, chrono.ChVectorD(0, -1, 0))
mfloor.GetCollisionModel().BuildModel()
mfloor.SetCollide(True)

# Add body to system
mphysicalSystem.Add(mfloor)


# ==Asset== attach a 'box' shape.
# Note that assets are managed via shared pointer, so they
# can also be shared. Do not forget AddAsset() at the end!
mboxfloor = chrono.ChBoxShape()
mboxfloor.GetBoxGeometry().Size = chrono.ChVectorD(10, 0.5, 10)
mboxfloor.GetBoxGeometry().Pos = chrono.ChVectorD(0, -1, 0)
mfloor.AddAsset(mboxfloor)


# ==Asset== attach color asset
# mfloorcolor = chrono.ChColorAsset()
# mfloorcolor.SetColor(chrono.ChColor(1., 0., 0.))
# mfloor.AddAsset(mfloorcolor)

mfloortexture = chrono.ChTexture()
mfloortexture.SetTextureFilename(chrono.GetChronoDataFile('grass.jpg'))
mfloor.AddAsset(mfloortexture)

# Textures, colors, asset levels with transformations.
# This section shows how to add more advanced typers of assets
# and how to group assets in ChAssetLevel containers.

# Create the rigid body as usual (this won't move,
# it is only for visualization tests)
mbody = chrono.ChBody()
mbody.SetBodyFixed(True)
mphysicalSystem.Add(mbody)

# ==Asset== Attach a 'shpere' shape
msphere = chrono.ChSphereShape()
msphere.GetSphereGeometry().rad = 0.5
msphere.GetSphereGeometry().center = chrono.ChVectorD(-1,0,0)
mbody.AddAsset(msphere)

msphere2 = chrono.ChSphereShape()
msphere2.GetSphereGeometry().rad = 0.7
msphere2.GetSphereGeometry().center = chrono.ChVectorD(-5,0,0)
mbody.AddAsset(msphere2)

##################################################################################################
# ==Asset== Attach a level that contains other assets
# Note: a ChAssetLevel can define a rotation/translation respect to paren level
# Note: a ChAssetLevel can contain colors or textures: if any, they affect only objects in the level
mlevelA = chrono.ChAssetLevel()

# ==Asset== Attach, in this level, a 'Wavefront mesh' asset,
# referencing a .obj file:
mobjmesh = chrono.ChObjShapeFile()
mobjmesh.SetFilename(chrono.GetChronoDataFile('tree1.obj'))
mlevelA.AddAsset(mobjmesh)

# ==Asset== Attach also a texture, taht will affect only the
# assets in mlevelA:
mtextureA = chrono.ChTexture()
mtextureA.SetTextureFilename(chrono.GetChronoDataFile('green.png'))
mlevelA.AddAsset(mtextureA)

# Change the position of mlevelA, thus moving also its sub-assets:
mlevelA.GetFrame().SetPos(chrono.ChVectorD(0,0,2))
mbody.AddAsset(mlevelA)
###################################################################################################

# mlevelB = chrono.ChAssetLevel()

# mbox = chrono.ChBoxShape()
# mbox.GetBoxGeometry().Pos = chrono.ChVectorD(1,1,0)
# mbox.GetBoxGeometry().Size = chrono.ChVectorD(0.3, 0.5, 0.1)
# mlevelB.AddAsset(mbox)

# mtextureB = chrono.ChTexture()
# mtextureB.SetTextureFilename(chrono.GetChronoDataFile('red.png'))
# mlevelB.AddAsset(mtextureB)

# mbody.AddAsset(mlevelB)

###################################################################################################

# ==Asset== Attach a video camera. This will be used by Irrlicht, 
# or POVray postprocessing, etc. Note that a camera can also be 
# put in a moving object
# mcamera = chrono.ChCamera()
# mcamera.SetAngle(50)
# mcamera.SetPosition(chrono.ChVectorD(-3, 4, -5))
# mcamera.SetAimPoint(chrono.ChVectorD(0, 1, 0))
# mbody.AddAsset(mcamera)

#####################################

# ==IMPORTANT== Use this function for adding a ChIrrNodeAsset to all items
# in the system. These ChIrrNodeAsset assets are 'proxies' to the Irrlicht meshes.
# If you need a finer control on which item really needs a visualization proxy in 
# Irrlicht, just use application.AssetBind(myitem); on a per-item basis.

application.AssetBindAll()

# ==IMPORTANT== Use this function for 'converting' into Irrlicht meshes the assets
# that you added to the bodies into 3D shapes, they can be visualized by Irrlicht!

application.AssetUpdateAll()

#
# THE SOFT-REAL-TIME CYCLE
#
application.SetTimestep(0.01)
application.SetTryRealtime(True)

while application.GetDevice().run():
    application.BeginScene()
    application.DrawAll()
    application.DoStep()
    application.EndScene()

