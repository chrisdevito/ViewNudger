# -*- coding: utf-8 -*-

import math

try:
    from maya import cmds
    from maya import OpenMaya
    from maya import OpenMayaUI
except:
    pass


def nudge(transformName,
          nudgeX=0,
          nudgeY=0,
          moveObject=False,
          rotateView=False,
          view=None):
    """
    Nudges a camera view/object by a pixel amount.

    :param transformName (str): Name of a transform to nudge from.
    :param nudgeX (float): Pixel amount to nudge in x.
    :param nudgeY (float): Pixel amount to nudge in y.
    :param moveObject (bool): Move the object instead of view.
    :param rotateView (bool): Rotate the camera back to aim
                              at point after nudge.
    :param view (OpenMaya.M3dView): Optional desired M3dView.
                                    Active view is default.

    Raises:
        ``RuntimeError`` If transformName isn't a transform or doesn't exist.
        ``RuntimeError`` If view set is not a view.

    Returns:
        None
    """
    if not transformName:
        raise RuntimeError("No transformName supplied.")

    if not cmds.objExists(transformName) or \
            not cmds.nodeType(transformName) == "transform":

        raise RuntimeError("%s either does not exist or"
                           " isn't a transform." % transformName)

    if not view:
        view = OpenMayaUI.M3dView.active3dView()

    else:
        if not type(view) is OpenMayaUI.M3dView and type(view) is str:
            viewStr = view
            view = OpenMayaUI.M3dView()

            try:
                OpenMayaUI.M3dView.getM3dViewFromModelPanel(
                    viewStr, view)

            except:
                raise RuntimeError(
                    "%s is not a model panel or view." % view)

        else:
            raise RuntimeError("%s is not a view." % view)


def getCamera(view):
    """
    Gets the camera from the current view.

    :param view (OpenMaya.M3dView): View to get camera from.

    Raises:
        None

    Returns:
        (OpenMaya.MFnCamera) Camera function set.
    """
    dagCam = OpenMaya.MDagPath()
    view.getCamera(dagCam)

    fnCamera = OpenMaya.MFnCamera(dagCam)

    return fnCamera


class Nudge(object):
    """
    :class:`Nudge` moves a camera or object based a pixel amount.

        nudgeView = Nudge(transformName="pSphere1",
                          view=OpenMayaUI.M3dView.active3dView())
        nudgeView.moveUp(pixelAmount=1.0)

    Instance this class with a transform and view if required.
    """
    def __init__(self, transformName=None, view=None):

        if not transformName:
            raise RuntimeError("No transformName supplied.")

        if not cmds.objExists(transformName) or \
                not cmds.nodeType(transformName) == "transform":

            raise RuntimeError("%s either does not exist or"
                               " isn't a transform." % transformName)

        self.transformName = transformName

        if not view:
            self.view = OpenMayaUI.M3dView.active3dView()

        else:
            if type(view) is OpenMayaUI.M3dView:
                self.view = view

            elif type(view) is str:
                self.view = OpenMayaUI.M3dView()

                try:
                    OpenMayaUI.M3dView.getM3dViewFromModelPanel(
                        view, self.view)

                except:
                    raise RuntimeError(
                        "%s is not a model panel or view." % view)

            else:
                raise RuntimeError("%s is not a view." % view)

        self.fnCamera = self.getCamera()

    def getCamera(self):
        """
        Gets the camera from the current view.

        Raises:
            None

        Returns:
            (OpenMaya.MFnCamera) Camera function set.
        """
        dagCam = OpenMaya.MDagPath()
        self.view.getCamera(dagCam)

        fnCamera = OpenMaya.MFnCamera(dagCam)

        return fnCamera

    def moveVertical(self, pixelAmount=1.0, moveObject=False, rotate=False):
        """
        Moves object/camera vertical by pixel amount.

        Raises:
            None

        Returns:
            None
        """
        cameraPoint = self.fnCamera.eyePoint(OpenMaya.MSpace.kWorld)
        transformPoint = OpenMaya.MPoint(*cmds.xform(
            self.transformName,
            query=True,
            worldSpace=True,
            translation=True))

        startDirVec = (transformPoint - cameraPoint)
        pointDist = startDirVec.length()

        x, y = self.worldToScreen(cameraPoint=cameraPoint,
                                  transformPoint=transformPoint)

        xyz = self.screenToWorld(point2D=[x, y + pixelAmount],
                                 cameraPoint=cameraPoint,
                                 setDistance=pointDist)

        offset = (xyz - transformPoint) + OpenMaya.MVector(transformPoint)

        cmds.undoInfo(openChunk=True)

        if moveObject:
            cmds.move(offset.x,
                      offset.y,
                      offset.z,
                      self.transformName,
                      relative=True)

        else:
            cmds.move(offset.x,
                      offset.y,
                      offset.z,
                      self.fnCamera.fullPathName(),
                      relative=True)

            if rotate:
                nDirVec = (xyz - cameraPoint)
                angle = -math.degrees(startDirVec.angle(nDirVec))

                cmds.rotate(angle, 0, 0,
                            self.fnCamera.fullPathName(),
                            objectSpace=True,
                            relative=True)

        cmds.undoInfo(closeChunk=True)

    def moveHorizontal(self, pixelAmount=1.0, moveObject=False, rotate=False):
        """
        Moves object/camera horizontal by pixel amount.

        Raises:
            None

        Returns:
            None
        """
        cameraPoint = self.fnCamera.eyePoint(OpenMaya.MSpace.kWorld)
        transformPoint = OpenMaya.MPoint(*cmds.xform(
            self.transformName,
            query=True,
            worldSpace=True,
            translation=True))

        startDirVec = (transformPoint - cameraPoint)
        pointDist = startDirVec.length()

        x, y = self.worldToScreen(cameraPoint=cameraPoint,
                                  transformPoint=transformPoint)

        xyz = self.screenToWorld(point2D=[x + pixelAmount, y],
                                 cameraPoint=cameraPoint,
                                 setDistance=pointDist)

        offset = (xyz - transformPoint) + OpenMaya.MVector(transformPoint)

        cmds.undoInfo(openChunk=True)

        if moveObject:
            cmds.move(offset.x,
                      offset.y,
                      offset.z,
                      self.transformName,
                      relative=True)

        else:
            cmds.move(offset.x,
                      offset.y,
                      offset.z,
                      self.fnCamera.fullPathName(),
                      relative=True)

            if rotate:
                nDirVec = (xyz - cameraPoint)
                angle = -math.degrees(startDirVec.angle(nDirVec))

                cmds.rotate(0, angle, 0,
                            self.fnCamera.fullPathName(),
                            objectSpace=True,
                            relative=True)

        cmds.undoInfo(closeChunk=True)

    def worldToScreen(self,
                      cameraPoint=None,
                      transformPoint=None):
        '''
        Converts a world point into a screen point.

        :param cameraPoint(OpenMaya.MPoint): Position to test.
        :param transformPoint(OpenMaya.MPoint): Position to test.

        Returns
            (list of floats) x and y position of 3d point.

        Raises:
            None
        '''
        # Get camera direction.
        cameraDir = self.fnCamera.viewDirection(OpenMaya.MSpace.kWorld)

        # Grab project and view matrices.
        projectionMatrix = OpenMaya.MMatrix()
        self.view.projectionMatrix(projectionMatrix)

        viewMatrix = OpenMaya.MMatrix()
        self.view.modelViewMatrix(viewMatrix)

        # Grab viewport width/height.
        width = self.view.portWidth()
        height = self.view.portHeight()

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

    def screenToWorld(self,
                      point2D=None,
                      cameraPoint=None,
                      setDistance=1.0):
        '''
        Converts a screen point to world.

        :param point2D(list of floats): x and y values to convert to 3d value.
        :param cameraPoint(OpenMaya.MPoint): Position to test.
        :param setDistance(float): Distance to set returned point from camera.

        Returns:
            (OpenMaya.MPoint) 2d Point converted to 3d point.

        Raises:
            None
        '''
        # Grab project and view matrices.
        projectionMatrix = OpenMaya.MMatrix()
        self.view.projectionMatrix(projectionMatrix)

        viewMatrix = OpenMaya.MMatrix()
        self.view.modelViewMatrix(viewMatrix)

        # Grab viewport width/height.
        width = self.view.portWidth()
        height = self.view.portHeight()

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
    nudgeView = Nudge(transformName="pSphere1")
    nudgeView.moveHorizontal(pixelAmount=10)
    nudgeView.moveVertical(pixelAmount=10)
