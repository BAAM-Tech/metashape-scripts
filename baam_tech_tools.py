import Metashape

# Checking compatibility
compatible_major_version = "1.8"
found_major_version = ".".join(Metashape.app.version.split('.')[:2])
if found_major_version != compatible_major_version:
    raise Exception("Incompatible Metashape version: {} != {}".format(found_major_version, compatible_major_version))


def transform_cameras(xshift = 0, yshift = 0, zshift = 0, scale = 1, angle = 0):
    doc = Metashape.app.document
    if not len(doc.chunks):
        raise Exception("No chunks!")

    chunk = doc.chunk

    # Define the rotation matrix
    R = Metashape.Utils.ypr2mat(Metashape.Vector([angle, 0, 0]))
    for camera in chunk.cameras:
        if camera.reference.location:
            coord = camera.reference.location
            camera.reference.location = R * Metashape.Vector([(coord.x + xshift) * scale, (coord.y + yshift) * scale, (coord.z + zshift)])

def scale():
    # Collect user inputs
    px = Metashape.app.getFloat("Please specify the x-coordinate to scale about (default 0, scale about origin)", 0)
    py = Metashape.app.getFloat("Please specify the y-coordinate to scale about (default 0, scale about origin)", 0)
    scale = Metashape.app.getFloat("Please specify your scale factor",1)
    
    print(f"Scale about ({px}, {py}), {scale} (scale factor)")

    # Move origin and perform scale transformation
    transform_cameras(xshift = (-px), yshift = (-py), scale=scale)
    
    # Put cameras back where they belong
    transform_cameras(xshift=px, yshift=py)

def translate():   
    xshift = Metashape.app.getFloat("Please specify your X shift", 0)
    yshift = Metashape.app.getFloat("Please specify your y shift", 0)
    zshift = Metashape.app.getFloat("Please specify your z shift", 0)
    print(f'Translate (X,Y,Z): ({xshift}, {yshift}, {zshift})')
    transform_cameras(xshift = xshift, yshift = yshift, zshift=zshift, scale=1)

def rotate_2d():
    # Collect user inputs
    px = Metashape.app.getFloat("Please specify the x-coordinate to rotate about (default 0, rotation about origin)", 0)
    py = Metashape.app.getFloat("Please specify the y-coordinate to rotate about (default 0, rotation about origin)", 0)
    degrees = Metashape.app.getFloat("Please specify your rotation (θ)", 0)
    
    # Translate center of rotation to origin and apply rotation
    transform_cameras(xshift=(-px), yshift=(-py), angle = degrees)

    # Translate points back 
    transform_cameras(xshift=px, yshift=py)
    
    print(f"Rotation (2d) about ({px}, {py}), {degrees} (θ)")

Metashape.app.addMenuItem("BAAM.Tech Tools/Scale", scale)
Metashape.app.addMenuItem("BAAM.Tech Tools/Translate", translate)
Metashape.app.addMenuItem("BAAM.Tech Tools/Rotate", rotate_2d)

print("To execute this script select an option from the BAAM.Tech Tools menu")