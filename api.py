import math
from maya import cmds
from maya import OpenMaya
from maya import OpenMayaUI


def worldToScreen(fnCamera=None,
                  objPoint=None,
                  activeView=None):
    '''
    Returns
        (list) X Position and Y Position.

    Raises:
        None
    '''
    camPnt = OpenMaya.MVector(fnCamera.eyePoint(OpenMaya.MSpace.kWorld))
    camDir = fnCamera.viewDirection(OpenMaya.MSpace.kWorld)

    projectionMatrix = OpenMaya.MMatrix()
    activeView.projectionMatrix(projectionMatrix)
    viewMatrix = OpenMaya.MMatrix()
    activeView.modelViewMatrix(viewMatrix)

    width = activeView.portWidth()
    height = activeView.portHeight()

    pos = OpenMaya.MVector(objPoint) - camPnt
    z = pos * camDir

    if z < 0.01:
        return None, None

    point3D = objPoint * (viewMatrix * projectionMatrix)

    winX = (((point3D.x / point3D.w) + 1.0) / 2.0) * width
    winY = (((point3D.y / point3D.w) + 1.0) / 2.0) * height

    return winX, winY


def screenToWorld(point2D=None,
                  fnCamera=None,
                  activeView=None,
                  setDistance=None):
    '''
    Returns:
        MVector Worldspace point.

    Raises:
        None
    '''
    projectionMatrix = OpenMaya.MMatrix()
    activeView.projectionMatrix(projectionMatrix)
    viewMatrix = OpenMaya.MMatrix()
    activeView.modelViewMatrix(viewMatrix)

    width = activeView.portWidth()
    height = activeView.portHeight()

    point3D = OpenMaya.MPoint()
    point3D.x = (2.0 * (point2D[0] / width)) - 1.0
    point3D.y = (2.0 * (point2D[1] / height)) - 1.0

    viewProjectionMatrix = (viewMatrix * projectionMatrix)

    point3D.z = viewProjectionMatrix(3, 2)
    point3D.w = viewProjectionMatrix(3, 3)
    point3D.x = point3D.x * point3D.w
    point3D.y = point3D.y * point3D.w

    point3D *= viewProjectionMatrix.inverse()

    camPnt = OpenMaya.MVector(fnCamera.eyePoint(OpenMaya.MSpace.kWorld))
    dirVec = (OpenMaya.MVector(point3D) - camPnt)
    dirVec.normalize()

    point3D = (dirVec * setDistance) + camPnt

    return OpenMaya.MPoint(point3D)

if __name__ == '__main__':

    activeView = OpenMayaUI.M3dView.active3dView()

    dagCam = OpenMaya.MDagPath()
    activeView.getCamera(dagCam)

    fnCamera = OpenMaya.MFnCamera(dagCam)
    camPnt = fnCamera.eyePoint(OpenMaya.MSpace.kWorld)

    objPoint = OpenMaya.MPoint(*cmds.xform(
        "pSphere1",
        query=True,
        worldSpace=True,
        translation=True))

    sDirVec = (objPoint - camPnt)
    pntDist = sDirVec.length()

    x, y = worldToScreen(fnCamera=fnCamera,
                         objPoint=objPoint,
                         activeView=activeView)

    nudgeX = 0
    nudgeY = 10

    xyz = screenToWorld(point2D=[x + nudgeX, y + nudgeY],
                        activeView=activeView,
                        fnCamera=fnCamera,
                        setDistance=pntDist)

    offset = (xyz - objPoint) + OpenMaya.MVector(objPoint)

    cmds.move(offset.x,
              offset.y,
              offset.z,
              fnCamera.fullPathName(),
              relative=True)

    nDirVec = (xyz - camPnt)
    angle = -math.degrees(sDirVec.angle(nDirVec))

    cmds.rotate(angle, 0, 0,
                fnCamera.fullPathName(),
                objectSpace=True,
                relative=True)
