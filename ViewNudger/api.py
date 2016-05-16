# -*- coding: utf-8 -*-

from __future__ import division

import math
import logging

try:
    from maya import cmds
    from maya import OpenMaya
    from maya import OpenMayaUI
except:
    pass


log = logging.getLogger('ViewNudger')


def parseArgs(transformName,
              view=None):
    """
    Checks input values.

    :param transformName: Name of a transform to nudge from.
    :type transformName: str
    :param view: Optional desired M3dView.
    :type view: OpenMaya.M3dView or Str

    :raises RuntimeError: If transformName isn't a transform or doesn't exist.
    :raises RuntimeError: If view set is not a view.

    :return: view
    :rtype: OpenMaya.M3dView
    """
    if not transformName:
        log.error("No transformName supplied.")
        raise

    if not cmds.objExists(transformName) or \
            not cmds.nodeType(transformName) == "transform":

        log.error("%s either does not exist or"
                  " isn't a transform.")
        raise

    if not view:
        log.debug("Getting active view...")
        view = OpenMayaUI.M3dView.active3dView()

    else:
        if not type(view) is OpenMayaUI.M3dView and type(view) is str:

            log.debug("Converting %s to OpenMayaUI.M3dView..." % view)

            viewStr = view
            view = OpenMayaUI.M3dView()

            try:
                OpenMayaUI.M3dView.getM3dViewFromModelPanel(
                    viewStr, view)

            except:
                log.error("%s is not a model panel or view." % view)
                raise

        else:
            log.error("%s is not a view." % view)
            raise

    return view


def nudge(transformName=None,
          pixelAmount=[1.0, 1.0],
          moveObject=False,
          rotateView=False,
          view=None):
    """
    Moves object/camera by pixel amount in x and y.

    :param transformName: Name of a transform to nudge from.
    :type transformName: str
    :param pixelAmount: Pixel amount to nudge in x and y.
    :type pixelAmount: list of 2 floats
    :param moveObject: Move the object instead of view.
    :type moveObject: bool
    :param rotateView: Rotate the camera back at point after nudge.
    :type rotateView: bool
    :param view: View to calculate nudge one.
    :type view: OpenMaya.M3dView

    :raises: None

    :return: None
    :rtype: NoneType
    """
    view = parseArgs(transformName,
                     view=view)

    fnCamera = getCamera(view)
    cameraPoint = fnCamera.eyePoint(OpenMaya.MSpace.kWorld)
    transformPoint = OpenMaya.MPoint(*cmds.xform(
        transformName,
        query=True,
        worldSpace=True,
        translation=True))

    startDirVec = (transformPoint - cameraPoint)
    pointDist = startDirVec.length()
    startDirVec.normalize()

    x, y = worldToScreen(fnCamera=fnCamera,
                         cameraPoint=cameraPoint,
                         transformPoint=transformPoint,
                         view=view)

    log.debug("Object is %s, %s in screen space..." % (x, y))

    xyz_x = screenToWorld(point2D=[x + pixelAmount[0], y],
                          cameraPoint=cameraPoint,
                          setDistance=pointDist,
                          view=view)

    xyz_y = screenToWorld(point2D=[x, y + pixelAmount[1]],
                          cameraPoint=cameraPoint,
                          setDistance=pointDist,
                          view=view)

    offsetX = (xyz_x - transformPoint) + OpenMaya.MVector(transformPoint)
    offsetY = (xyz_y - transformPoint) + OpenMaya.MVector(transformPoint)

    log.debug("Offset X: %s, %s, %s..." % (offsetX.x, offsetX.y, offsetX.z))
    log.debug("Offset Y: %s, %s, %s..." % (offsetY.x, offsetY.y, offsetY.z))

    cmds.undoInfo(openChunk=True)

    if moveObject:

        cmds.move(offsetX.x,
                  offsetX.y,
                  offsetX.z,
                  transformName,
                  relative=True)

        cmds.move(offsetY.x,
                  offsetY.y,
                  offsetY.z,
                  transformName,
                  relative=True)

    else:
        cmds.move(offsetX.x,
                  offsetX.y,
                  offsetX.z,
                  fnCamera.fullPathName(),
                  relative=True)

        cmds.move(offsetY.x,
                  offsetY.y,
                  offsetY.z,
                  fnCamera.fullPathName(),
                  relative=True)

        if rotateView:

            x_nDirVec = (xyz_x - cameraPoint)
            x_nDirVec.normalize()
            angleX = math.degrees(startDirVec.angle(x_nDirVec))

            y_nDirVec = (xyz_y - cameraPoint)
            y_nDirVec.normalize()
            angleY = -math.degrees(startDirVec.angle(y_nDirVec))

            log.debug("Rotating camera in Y: %s..." % angleX)
            log.debug("Rotating camera in X: %s..." % angleY)

            cmds.rotate(angleY, angleX, 0,
                        fnCamera.fullPathName(),
                        objectSpace=True,
                        relative=True)

    cmds.undoInfo(closeChunk=True)


def getCamera(view):
    """
    Gets the camera from the current view.

    :param view: View to get camera from.
    :type view: OpenMaya.M3dView

    :raises: None

    :return: Camera function set.
    :rtype: OpenMaya.MFnCamera
    """
    dagCam = OpenMaya.MDagPath()
    view.getCamera(dagCam)

    fnCamera = OpenMaya.MFnCamera(dagCam)

    return fnCamera


def worldToScreen(fnCamera=None,
                  cameraPoint=None,
                  transformPoint=None,
                  view=None):
    '''
    Converts a world point into a screen point.

    :param fnCamera: Camera function set.
    :type fnCamera: OpenMaya.MFnCamera
    :param cameraPoint: Position to test.
    :type cameraPoint: OpenMaya.MPoint
    :param transformPoint: Position to test.
    :type transformPoint: OpenMaya.MPoint
    :param view: View to convert point.
    :type view: OpenMaya.M3dView

    :raises: None

    :return: x and y position of 3d point.
    :rtype: list of 2 floats
    '''
    # Get camera direction.
    cameraDir = fnCamera.viewDirection(OpenMaya.MSpace.kWorld)

    # Grab project and view matrices.
    projectionMatrix = OpenMaya.MMatrix()
    view.projectionMatrix(projectionMatrix)

    viewMatrix = OpenMaya.MMatrix()
    view.modelViewMatrix(viewMatrix)

    # Grab viewport width/height.
    width = view.portWidth()
    height = view.portHeight()

    # Check to see that point is in view by checking dot product.
    # Positive means it's facing the camera.
    pointDir = transformPoint - cameraPoint
    z = pointDir * cameraDir

    if z < 0.01:
        return None, None

    # Calculate 2d Screen space.
    point3D = transformPoint * (viewMatrix * projectionMatrix)

    x = (((point3D.x / point3D.w) + 1.0) / 2.0) * width
    y = (((point3D.y / point3D.w) + 1.0) / 2.0) * height

    return x, y


def screenToWorld(point2D=None,
                  cameraPoint=None,
                  setDistance=1.0,
                  view=None):
    '''
    Converts a screen point to world.

    :param point2D: x and y values to convert to 3d value.
    :type point2D: list of 2 floats
    :param cameraPoint: Position to test.
    :type cameraPoint: OpenMaya.MPoint
    :param setDistance: Distance to set returned point from camera.
    :type setDistance: float
    :param view: View to convert point.
    :type view: OpenMaya.M3dView

    :raises: None

    :return: 2d Point converted to 3d point.
    :rtype: OpenMaya.MPoint
    '''
    # Grab project and view matrices.
    projectionMatrix = OpenMaya.MMatrix()
    view.projectionMatrix(projectionMatrix)

    viewMatrix = OpenMaya.MMatrix()
    view.modelViewMatrix(viewMatrix)

    # Grab viewport width/height.
    width = view.portWidth()
    height = view.portHeight()

    # Get 2d point in 3d.
    point3D = OpenMaya.MPoint()
    point3D.x = (2.0 * (point2D[0] / width)) - 1.0
    point3D.y = (2.0 * (point2D[1] / height)) - 1.0

    viewProjectionMatrix = (viewMatrix * projectionMatrix)

    point3D.z = viewProjectionMatrix(3, 2)
    point3D.w = viewProjectionMatrix(3, 3)
    point3D.x = point3D.x * point3D.w
    point3D.y = point3D.y * point3D.w

    point3D *= viewProjectionMatrix.inverse()

    # Project point into setDistance depth.
    directionVec = (point3D - cameraPoint)
    directionVec.normalize()

    point3D = (directionVec * setDistance) + OpenMaya.MVector(cameraPoint)

    return OpenMaya.MPoint(point3D)

if __name__ == '__main__':

    pixelAmount = [10.0, 10.0]
    nudgeView = nudge(transformName="pSphere1",
                      pixelAmount=pixelAmount,
                      moveObject=False,
                      rotateView=True)
