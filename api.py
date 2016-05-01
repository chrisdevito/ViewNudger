import math
from maya import cmds
from maya import OpenMaya
from maya import OpenMayaUI


def worldToScreen(fnCamera=None,
                  objectPoint=None,
                  activeView=None):
    '''
    :param fnCamera(OpenMaya.MFnCamera): Active Camera function set.
    :param objectPoint(OpenMaya.MPoint): Position to test.
    :param activeView(OpenMayaUI.M3dView): Active view to get coordinates.

    Returns
        (list of floats) x and y position of 3d point.

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

    pos = OpenMaya.MVector(objectPoint) - camPnt
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

    :param point2D(list of floats): x and y values to convert to 3d value.
    :param fnCamera(OpenMaya.MFnCamera): Active Camera function set.
    :param activeView(OpenMayaUI.M3dView): Active view to get coordinates.
    :param setDistance(float): Distance to set returned point from camera.

    Returns:
        (OpenMaya.MPoint) 2d Point converted to 3d point.

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

    nudgeX = 0
    nudgeY = 10
    doRotate = False

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
                         objectPoint=objPoint,
                         activeView=activeView)

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

    if doRotate:
        nDirVec = (xyz - camPnt)
        angle = -math.degrees(sDirVec.angle(nDirVec))

        cmds.rotate(angle, 0, 0,
                    fnCamera.fullPathName(),
                    objectSpace=True,
                    relative=True)
