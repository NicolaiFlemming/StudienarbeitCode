# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__

def SteppedJoint():
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.Line(point1=(0.0, 0.0), point2=(150.0, 0.0))
    s.HorizontalConstraint(entity=g[2], addUndoState=False)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=176.801, 
        farPlane=200.322, width=180.062, height=95.3803, cameraPosition=(
        -4.87703, -0.368693, 188.562), cameraTarget=(-4.87703, -0.368693, 0))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=114.588, 
        farPlane=199.134, cameraPosition=(69.9493, 1.30257, 173.072), 
        cameraUpVector=(0.0433486, 0.998657, -0.028385))
    session.viewports['Viewport: 1'].view.setValues(cameraPosition=(142.896, 
        0.820338, 141.539), cameraTarget=(68.0701, -0.850925, -31.5334))
    session.viewports['Viewport: 1'].view.setValues(session.views['Front'])
    s.Line(point1=(150.0, 0.0), point2=(150.0, 0.5))
    s.VerticalConstraint(entity=g[3], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[2], entity2=g[3], addUndoState=False)
    s.Line(point1=(150.0, 0.5), point2=(140.0, 0.5))
    s.HorizontalConstraint(entity=g[4], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[3], entity2=g[4], addUndoState=False)
    s.Line(point1=(140.0, 0.5), point2=(140.0, 1.0))
    s.VerticalConstraint(entity=g[5], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[4], entity2=g[5], addUndoState=False)
    s.Line(point1=(140.0, 1.0), point2=(130.0, 1.0))
    s.HorizontalConstraint(entity=g[6], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[5], entity2=g[6], addUndoState=False)
    s.Line(point1=(130.0, 1.0), point2=(130.0, 1.5))
    s.VerticalConstraint(entity=g[7], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[6], entity2=g[7], addUndoState=False)
    s.Line(point1=(130.0, 1.5), point2=(120.0, 1.5))
    s.HorizontalConstraint(entity=g[8], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[7], entity2=g[8], addUndoState=False)
    s.Line(point1=(120.0, 1.5), point2=(120.0, 2.0))
    s.VerticalConstraint(entity=g[9], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[8], entity2=g[9], addUndoState=False)
    s.Line(point1=(120.0, 2.0), point2=(0.0, 2.0))
    s.HorizontalConstraint(entity=g[10], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[9], entity2=g[10], addUndoState=False)
    s.Line(point1=(0.0, 2.0), point2=(0.0, 0.0))
    s.VerticalConstraint(entity=g[11], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[10], entity2=g[11], addUndoState=False)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=288.358, 
        farPlane=311.642, width=178.248, height=94.4193, cameraPosition=(
        72.9293, -0.839473, 300), cameraTarget=(72.9293, -0.839473, 0))
    p = mdb.models['Model-1'].Part(name='Fuegepartner1', dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    p.BaseSolidExtrude(sketch=s, depth=25.0)
    s.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models['Model-1'].sketches['__profile__']
    session.viewports['Viewport: 1'].view.setValues(nearPlane=241.517, 
        farPlane=407.539, width=105.555, height=55.9134, cameraPosition=(
        -241.468, 63.1598, 48.7283), cameraUpVector=(0.411884, 0.685714, 
        -0.600123), cameraTarget=(81.4911, -3.18839, 10.1973))
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    p.DatumPointByCoordinate(coords=(0.0, 0.0, 0.25))
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    p.DatumPointByCoordinate(coords=(0.0, 0.0, 0.5))
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    p.DatumPointByCoordinate(coords=(0.0, 0.0, 0.75))
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    del p.features['Datum pt-1']
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    del p.features['Datum pt-2']
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    del p.features['Datum pt-3']
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    p.DatumPointByCoordinate(coords=(0.0, 0.25, 0.0))
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    p.DatumPointByCoordinate(coords=(0.0, 0.5, 0.0))
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    p.DatumPointByCoordinate(coords=(0.0, 0.75, 0.0))
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    p.DatumPointByCoordinate(coords=(0.0, 1.0, 0.0))
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    p.DatumPointByCoordinate(coords=(0.0, 1.25, 0.0))
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    p.DatumPointByCoordinate(coords=(0.0, 1.5, 0.0))
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    p.DatumPointByCoordinate(coords=(0.0, 1.75, 0.0))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=248.202, 
        farPlane=400.854, width=23.0958, height=12.234, viewOffsetX=-17.9987, 
        viewOffsetY=1.06255)
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    e, v1, d1 = p.edges, p.vertices, p.datums
    p.PartitionCellByPlanePointNormal(point=d1[5], normal=e[29], cells=pickedCells)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=248.728, 
        farPlane=400.328, width=15.9669, height=8.45779, viewOffsetX=-19.548, 
        viewOffsetY=1.18418)
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#2 ]', ), )
    e1, v2, d2 = p.edges, p.vertices, p.datums
    p.PartitionCellByPlanePointNormal(point=d2[6], normal=e1[4], cells=pickedCells)
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#4 ]', ), )
    e, v1, d1 = p.edges, p.vertices, p.datums
    p.PartitionCellByPlanePointNormal(point=d1[7], normal=e[6], cells=pickedCells)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=248.986, 
        farPlane=400.07, width=12.4791, height=6.61025, viewOffsetX=-20.2352, 
        viewOffsetY=1.33115)
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#8 ]', ), )
    e1, v2, d2 = p.edges, p.vertices, p.datums
    p.PartitionCellByPlanePointNormal(point=d2[8], normal=e1[7], cells=pickedCells)
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#10 ]', ), )
    e, v1, d1 = p.edges, p.vertices, p.datums
    p.PartitionCellByPlanePointNormal(point=d1[9], normal=e[6], cells=pickedCells)
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#20 ]', ), )
    e1, v2, d2 = p.edges, p.vertices, p.datums
    p.PartitionCellByPlanePointNormal(point=d2[10], normal=e1[7], 
        cells=pickedCells)
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#40 ]', ), )
    e, v1, d1 = p.edges, p.vertices, p.datums
    p.PartitionCellByPlanePointNormal(point=d1[11], normal=e[6], cells=pickedCells)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=247.846, 
        farPlane=401.21, width=31.5533, height=16.714, viewOffsetX=-16.4029, 
        viewOffsetY=3.42909)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=244.282, 
        farPlane=396.098, width=31.0996, height=16.4737, cameraPosition=(
        -223.339, 64.7439, 109.763), cameraUpVector=(0.300383, 0.699696, 
        -0.648225), cameraTarget=(85.0281, -3.91223, 7.85578), 
        viewOffsetX=-16.1671, viewOffsetY=3.37978)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=242.067, 
        farPlane=398.313, width=67.389, height=35.6964, viewOffsetX=-18.0665, 
        viewOffsetY=5.40875)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=241.796, 
        farPlane=398.583, width=67.3136, height=35.6565, viewOffsetX=-6.28142, 
        viewOffsetY=1.2255)
    session.viewports['Viewport: 1'].view.setValues(viewOffsetX=-5.8135, 
        viewOffsetY=0.022468)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=281.446, 
        farPlane=342.325, width=78.3518, height=41.5035, cameraPosition=(
        15.2899, 150.06, 279.882), cameraUpVector=(-0.482221, 0.457255, 
        -0.747249), cameraTarget=(79.6444, -6.61996, -5.59837), 
        viewOffsetX=-6.7668, viewOffsetY=0.0261523)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=279.168, 
        farPlane=344.603, width=102.071, height=54.0676, viewOffsetX=-4.92716, 
        viewOffsetY=1.57542)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=237.898, 
        farPlane=392.794, width=86.9814, height=46.0747, cameraPosition=(
        -193.152, 52.9313, 170.138), cameraUpVector=(0.330057, 0.855374, 
        -0.399246), cameraTarget=(90.2768, -3.33129, 6.76268), 
        viewOffsetX=-4.19876, viewOffsetY=1.34252)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=241.682, 
        farPlane=389.009, width=44.739, height=23.6986, viewOffsetX=-17.0386, 
        viewOffsetY=-2.02896)
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#40 ]', ), )
    p.Set(cells=cells, name='Set-1')
    mdb.models['Model-1'].parts['Fuegepartner1'].sets.changeKey(fromName='Set-1', 
        toName='Ply1')
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#20 ]', ), )
    p.Set(cells=cells, name='Ply2')
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#10 ]', ), )
    p.Set(cells=cells, name='Ply3')
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#8 ]', ), )
    p.Set(cells=cells, name='Ply4')
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#4 ]', ), )
    p.Set(cells=cells, name='Ply5')
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#2 ]', ), )
    p.Set(cells=cells, name='Ply6')
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    p.Set(cells=cells, name='Ply7')
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#80 ]', ), )
    p.Set(cells=cells, name='Ply8')
    session.viewports['Viewport: 1'].view.setValues(nearPlane=238.469, 
        farPlane=392.222, width=88.3156, height=46.7814, viewOffsetX=-5.89687, 
        viewOffsetY=2.58134)
    s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=200.0)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=STANDALONE)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=179.38, 
        farPlane=197.744, cameraPosition=(57.3475, 3.54264, 188.562), 
        cameraTarget=(57.3475, 3.54264, 0))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=171.515, 
        farPlane=205.609, width=261.009, height=138.258, cameraPosition=(
        69.8312, 12.2749, 188.562), cameraTarget=(69.8312, 12.2749, 0))
    s1.Line(point1=(150.0, 0.0), point2=(150.0, 2.0))
    s1.VerticalConstraint(entity=g[2], addUndoState=False)
    s1.Line(point1=(150.0, 2.0), point2=(0.0, 2.0))
    s1.HorizontalConstraint(entity=g[3], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[2], entity2=g[3], addUndoState=False)
    s1.Line(point1=(0.0, 2.0), point2=(0.0, 1.5))
    s1.VerticalConstraint(entity=g[4], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[3], entity2=g[4], addUndoState=False)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=181.393, 
        farPlane=195.731, width=109.76, height=58.1409, cameraPosition=(
        28.9457, 5.96522, 188.562), cameraTarget=(28.9457, 5.96522, 0))
    s1.Line(point1=(0.0, 1.5), point2=(10.0, 1.5))
    s1.HorizontalConstraint(entity=g[5], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[4], entity2=g[5], addUndoState=False)
    s1.Line(point1=(10.0, 1.5), point2=(10.0, 1.0))
    s1.VerticalConstraint(entity=g[6], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[5], entity2=g[6], addUndoState=False)
    s1.Line(point1=(10.0, 1.0), point2=(20.0, 1.0))
    s1.HorizontalConstraint(entity=g[7], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[6], entity2=g[7], addUndoState=False)
    s1.Line(point1=(20.0, 1.0), point2=(20.0, 0.5))
    s1.VerticalConstraint(entity=g[8], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[7], entity2=g[8], addUndoState=False)
    s1.Line(point1=(20.0, 0.5), point2=(30.0, 0.5))
    s1.HorizontalConstraint(entity=g[9], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[8], entity2=g[9], addUndoState=False)
    s1.Line(point1=(30.0, 0.5), point2=(30.0, 0.0))
    s1.VerticalConstraint(entity=g[10], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[9], entity2=g[10], addUndoState=False)
    s1.Line(point1=(30.0, 0.0), point2=(150.0, 0.0))
    s1.HorizontalConstraint(entity=g[11], addUndoState=False)
    s1.PerpendicularConstraint(entity1=g[10], entity2=g[11], addUndoState=False)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=171.375, 
        farPlane=205.749, width=263.149, height=139.392, cameraPosition=(
        9.46613, 15.5413, 188.562), cameraTarget=(9.46613, 15.5413, 0))
    session.viewports['Viewport: 1'].view.setValues(cameraPosition=(78.0626, 
        16.0638, 188.562), cameraTarget=(78.0626, 16.0638, 0))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=175.143, 
        farPlane=201.981, width=181.539, height=96.1623, cameraPosition=(
        67.0812, 10.1688, 188.562), cameraTarget=(67.0812, 10.1688, 0))
    p = mdb.models['Model-1'].Part(name='Fuegepartner2', dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts['Fuegepartner2']
    p.BaseSolidExtrude(sketch=s1, depth=25.0)
    s1.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts['Fuegepartner2']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models['Model-1'].sketches['__profile__']
    p = mdb.models['Model-1'].parts['Fuegepartner2']
    p.DatumPointByCoordinate(coords=(150.0, 0.25, 0.0))
    p = mdb.models['Model-1'].parts['Fuegepartner2']
    p.DatumPointByCoordinate(coords=(150.0, 0.5, 0.0))
    p = mdb.models['Model-1'].parts['Fuegepartner2']
    p.DatumPointByCoordinate(coords=(150.0, 0.75, 0.0))
    p = mdb.models['Model-1'].parts['Fuegepartner2']
    p.DatumPointByCoordinate(coords=(150.0, 1.0, 0.0))
    p = mdb.models['Model-1'].parts['Fuegepartner2']
    p.DatumPointByCoordinate(coords=(150.0, 1.25, 0.0))
    p = mdb.models['Model-1'].parts['Fuegepartner2']
    p.DatumPointByCoordinate(coords=(150.0, 1.5, 0.0))
    p = mdb.models['Model-1'].parts['Fuegepartner2']
    p.DatumPointByCoordinate(coords=(150.0, 1.75, 0.0))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=254.937, 
        farPlane=418.384, width=111.421, height=59.0203, cameraPosition=(
        397.416, 88.459, 54.7151), cameraUpVector=(-0.52832, 0.778485, 
        -0.338878), cameraTarget=(81.4911, -3.18842, 10.1973))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=262.615, 
        farPlane=410.707, width=9.65979, height=5.11686, viewOffsetX=20.4118, 
        viewOffsetY=-7.74982)
    p = mdb.models['Model-1'].parts['Fuegepartner2']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    e1, v2, d2 = p.edges, p.vertices, p.datums
    p.PartitionCellByPlanePointNormal(point=d2[2], normal=e1[27], 
        cells=pickedCells)
    p = mdb.models['Model-1'].parts['Fuegepartner2']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#2 ]', ), )
    e, v1, d1 = p.edges, p.vertices, p.datums
    p.PartitionCellByPlanePointNormal(point=d1[3], normal=e[36], cells=pickedCells)
    p = mdb.models['Model-1'].parts['Fuegepartner2']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    e1, v2, d2 = p.edges, p.vertices, p.datums
    p.PartitionCellByPlanePointNormal(point=d2[4], normal=e1[4], cells=pickedCells)
    p = mdb.models['Model-1'].parts['Fuegepartner2']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    e, v1, d1 = p.edges, p.vertices, p.datums
    p.PartitionCellByPlanePointNormal(point=d1[5], normal=e[21], cells=pickedCells)
    p = mdb.models['Model-1'].parts['Fuegepartner2']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#2 ]', ), )
    e1, v2, d2 = p.edges, p.vertices, p.datums
    p.PartitionCellByPlanePointNormal(point=d2[6], normal=e1[9], cells=pickedCells)
    p = mdb.models['Model-1'].parts['Fuegepartner2']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    e, v1, d1 = p.edges, p.vertices, p.datums
    p.PartitionCellByPlanePointNormal(point=d1[7], normal=e[22], cells=pickedCells)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=262.967, 
        farPlane=410.355, width=4.89729, height=2.59413, viewOffsetX=21.377, 
        viewOffsetY=-7.62547)
    p = mdb.models['Model-1'].parts['Fuegepartner2']
    c = p.cells
    pickedCells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    e1, v2, d2 = p.edges, p.vertices, p.datums
    p.PartitionCellByPlanePointNormal(point=d2[8], normal=e1[10], 
        cells=pickedCells)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=260.685, 
        farPlane=412.637, width=40.4498, height=21.4266, viewOffsetX=27.9504, 
        viewOffsetY=-4.10373)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=260.52, 
        farPlane=412.802, width=40.4242, height=21.413, viewOffsetX=8.84463, 
        viewOffsetY=-5.40557)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=256.71, 
        farPlane=416.611, width=101.181, height=53.5963, viewOffsetX=13.1859, 
        viewOffsetY=-3.40257)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=256.31, 
        farPlane=417.012, width=101.023, height=53.5127, viewOffsetX=10.1055, 
        viewOffsetY=-0.638874)
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    session.viewports['Viewport: 1'].view.setValues(session.views['Iso'])
    p = mdb.models['Model-1'].parts['Fuegepartner2']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    session.viewports['Viewport: 1'].view.setValues(session.views['Iso'])
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
        engineeringFeatures=ON)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
        referenceRepresentation=OFF)
    mdb.models['Model-1'].Material(name='SIGAPREG C U230-0/NF-E320/39%')
    mdb.models['Model-1'].materials['SIGAPREG C U230-0/NF-E320/39%'].Elastic(
        type=ENGINEERING_CONSTANTS, table=((124311.0, 8767.0, 8767.0, 0.35, 
        0.35, 0.5, 4272.0, 4272.0, 2922.0), ))
    mdb.models['Model-1'].materials['SIGAPREG C U230-0/NF-E320/39%'].Density(
        table=((1.55e-09, ), ))
    mdb.models['Model-1'].materials['SIGAPREG C U230-0/NF-E320/39%'].HashinDamageInitiation(
        alpha=1.0, table=((1800.0, 1200.0, 36.0, 149.0, 64.0, 42.0), ))
    mdb.models['Model-1'].materials['SIGAPREG C U230-0/NF-E320/39%'].hashinDamageInitiation.DamageEvolution(
        type=ENERGY, table=((92.0, 80.0, 0.21, 0.8), ))
    layupOrientation = None
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    region1 = p.sets['Ply1']
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    region2 = p.sets['Ply2']
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    region3 = p.sets['Ply3']
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    region4 = p.sets['Ply4']
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    region5 = p.sets['Ply5']
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    region6 = p.sets['Ply6']
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    region7 = p.sets['Ply7']
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    region8 = p.sets['Ply8']
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    s = p.faces
    side1Faces = s.getSequenceFromMask(mask=('[#0 #1 ]', ), )
    normalAxisRegion = p.Surface(side1Faces=side1Faces, name='Surf-1')
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    e = p.edges
    edges = e.getSequenceFromMask(mask=('[#400000 ]', ), )
    primaryAxisRegion = p.Set(edges=edges, name='Set-9')
    compositeLayup = mdb.models['Model-1'].parts['Fuegepartner1'].CompositeLayup(
        name='CompositeLayup-Fuegepartner1', description='', 
        elementType=CONTINUUM_SHELL, symmetric=False)
    compositeLayup.Section(preIntegrate=OFF, integrationRule=SIMPSON, 
        poissonDefinition=DEFAULT, thicknessModulus=None, temperature=GRADIENT, 
        useDensity=OFF)
    compositeLayup.suppress()
    compositeLayup.CompositePly(suppressed=False, plyName='Ply-1', region=region1, 
        material='SIGAPREG C U230-0/NF-E320/39%', 
        thicknessType=SPECIFY_THICKNESS, thickness=1.0, 
        orientationType=SPECIFY_ORIENT, orientationValue=-45.0, 
        additionalRotationType=ROTATION_NONE, additionalRotationField='', 
        axis=AXIS_3, angle=0.0, numIntPoints=3)
    compositeLayup.CompositePly(suppressed=False, plyName='Ply-2', region=region2, 
        material='SIGAPREG C U230-0/NF-E320/39%', 
        thicknessType=SPECIFY_THICKNESS, thickness=1.0, 
        orientationType=SPECIFY_ORIENT, orientationValue=0.0, 
        additionalRotationType=ROTATION_NONE, additionalRotationField='', 
        axis=AXIS_3, angle=0.0, numIntPoints=3)
    compositeLayup.CompositePly(suppressed=False, plyName='Ply-3', region=region3, 
        material='SIGAPREG C U230-0/NF-E320/39%', 
        thicknessType=SPECIFY_THICKNESS, thickness=1.0, 
        orientationType=SPECIFY_ORIENT, orientationValue=45.0, 
        additionalRotationType=ROTATION_NONE, additionalRotationField='', 
        axis=AXIS_3, angle=0.0, numIntPoints=3)
    compositeLayup.CompositePly(suppressed=False, plyName='Ply-4', region=region4, 
        material='SIGAPREG C U230-0/NF-E320/39%', 
        thicknessType=SPECIFY_THICKNESS, thickness=1.0, 
        orientationType=SPECIFY_ORIENT, orientationValue=90.0, 
        additionalRotationType=ROTATION_NONE, additionalRotationField='', 
        axis=AXIS_3, angle=0.0, numIntPoints=3)
    compositeLayup.CompositePly(suppressed=False, plyName='Ply-5', region=region5, 
        material='SIGAPREG C U230-0/NF-E320/39%', 
        thicknessType=SPECIFY_THICKNESS, thickness=1.0, 
        orientationType=SPECIFY_ORIENT, orientationValue=90.0, 
        additionalRotationType=ROTATION_NONE, additionalRotationField='', 
        axis=AXIS_3, angle=0.0, numIntPoints=3)
    compositeLayup.CompositePly(suppressed=False, plyName='Ply-6', region=region6, 
        material='SIGAPREG C U230-0/NF-E320/39%', 
        thicknessType=SPECIFY_THICKNESS, thickness=1.0, 
        orientationType=SPECIFY_ORIENT, orientationValue=45.0, 
        additionalRotationType=ROTATION_NONE, additionalRotationField='', 
        axis=AXIS_3, angle=0.0, numIntPoints=3)
    compositeLayup.CompositePly(suppressed=False, plyName='Ply-7', region=region7, 
        material='SIGAPREG C U230-0/NF-E320/39%', 
        thicknessType=SPECIFY_THICKNESS, thickness=1.0, 
        orientationType=SPECIFY_ORIENT, orientationValue=0.0, 
        additionalRotationType=ROTATION_NONE, additionalRotationField='', 
        axis=AXIS_3, angle=0.0, numIntPoints=3)
    compositeLayup.CompositePly(suppressed=False, plyName='Ply-8', region=region8, 
        material='SIGAPREG C U230-0/NF-E320/39%', 
        thicknessType=SPECIFY_THICKNESS, thickness=1.0, 
        orientationType=SPECIFY_ORIENT, orientationValue=-45.0, 
        additionalRotationType=ROTATION_NONE, additionalRotationField='', 
        axis=AXIS_3, angle=0.0, numIntPoints=3)
    compositeLayup.resume()
    compositeLayup.ReferenceOrientation(orientationType=DISCRETE, localCsys=None, 
        additionalRotationType=ROTATION_NONE, angle=0.0, 
        additionalRotationField='', axis=AXIS_3, stackDirection=STACK_3, 
        normalAxisDefinition=SURFACE, normalAxisRegion=normalAxisRegion, 
        normalAxisDirection=AXIS_3, flipNormalDirection=False, 
        primaryAxisDefinition=EDGE, primaryAxisRegion=primaryAxisRegion, 
        primaryAxisDirection=AXIS_1, flipPrimaryDirection=False)
    p1 = mdb.models['Model-1'].parts['Fuegepartner2']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=277.907, 
        farPlane=385.989, width=39.878, height=21.1236, viewOffsetX=24.2715, 
        viewOffsetY=-20.2152)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=278.08, 
        farPlane=385.816, width=39.9028, height=21.1368, viewOffsetX=36.9866, 
        viewOffsetY=-28.8648)
    p = mdb.models['Model-1'].parts['Fuegepartner2']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#40 ]', ), )
    p.Set(cells=cells, name='Ply1')
    p = mdb.models['Model-1'].parts['Fuegepartner2']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#80 ]', ), )
    p.Set(cells=cells, name='Ply2')
    p = mdb.models['Model-1'].parts['Fuegepartner2']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#20 ]', ), )
    p.Set(cells=cells, name='Ply3')
    p = mdb.models['Model-1'].parts['Fuegepartner2']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#8 ]', ), )
    p.Set(cells=cells, name='Ply4')
    p = mdb.models['Model-1'].parts['Fuegepartner2']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#10 ]', ), )
    p.Set(cells=cells, name='Ply5')
    p = mdb.models['Model-1'].parts['Fuegepartner2']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#4 ]', ), )
    p.Set(cells=cells, name='Ply6')
    p = mdb.models['Model-1'].parts['Fuegepartner2']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
    p.Set(cells=cells, name='Ply7')
    p = mdb.models['Model-1'].parts['Fuegepartner2']
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#2 ]', ), )
    p.Set(cells=cells, name='Ply8')
    session.viewports['Viewport: 1'].view.setValues(nearPlane=274.673, 
        farPlane=389.223, width=94.4944, height=50.0543, viewOffsetX=49.1757, 
        viewOffsetY=-37.8635)
    layupOrientation = None
    p = mdb.models['Model-1'].parts['Fuegepartner2']
    region1 = p.sets['Ply1']
    p = mdb.models['Model-1'].parts['Fuegepartner2']
    region2 = p.sets['Ply2']
    p = mdb.models['Model-1'].parts['Fuegepartner2']
    region3 = p.sets['Ply3']
    p = mdb.models['Model-1'].parts['Fuegepartner2']
    region4 = p.sets['Ply4']
    p = mdb.models['Model-1'].parts['Fuegepartner2']
    region5 = p.sets['Ply5']
    p = mdb.models['Model-1'].parts['Fuegepartner2']
    region6 = p.sets['Ply6']
    p = mdb.models['Model-1'].parts['Fuegepartner2']
    region7 = p.sets['Ply7']
    p = mdb.models['Model-1'].parts['Fuegepartner2']
    region8 = p.sets['Ply8']
    p = mdb.models['Model-1'].parts['Fuegepartner2']
    s = p.faces
    side1Faces = s.getSequenceFromMask(mask=('[#0 #80 ]', ), )
    normalAxisRegion = p.Surface(side1Faces=side1Faces, name='Surf-1')
    p = mdb.models['Model-1'].parts['Fuegepartner2']
    e = p.edges
    edges = e.getSequenceFromMask(mask=('[#4000 ]', ), )
    primaryAxisRegion = p.Set(edges=edges, name='Set-9')
    compositeLayup = mdb.models['Model-1'].parts['Fuegepartner2'].CompositeLayup(
        name='CompositeLayup-Fuegepartner2', description='', 
        elementType=CONTINUUM_SHELL, symmetric=False)
    compositeLayup.Section(preIntegrate=OFF, integrationRule=SIMPSON, 
        poissonDefinition=DEFAULT, thicknessModulus=None, temperature=GRADIENT, 
        useDensity=OFF)
    compositeLayup.suppress()
    compositeLayup.CompositePly(suppressed=False, plyName='Ply-1', region=region1, 
        material='SIGAPREG C U230-0/NF-E320/39%', 
        thicknessType=SPECIFY_THICKNESS, thickness=1.0, 
        orientationType=SPECIFY_ORIENT, orientationValue=-45.0, 
        additionalRotationType=ROTATION_NONE, additionalRotationField='', 
        axis=AXIS_3, angle=0.0, numIntPoints=3)
    compositeLayup.CompositePly(suppressed=False, plyName='Ply-2', region=region2, 
        material='SIGAPREG C U230-0/NF-E320/39%', 
        thicknessType=SPECIFY_THICKNESS, thickness=1.0, 
        orientationType=SPECIFY_ORIENT, orientationValue=0.0, 
        additionalRotationType=ROTATION_NONE, additionalRotationField='', 
        axis=AXIS_3, angle=0.0, numIntPoints=3)
    compositeLayup.CompositePly(suppressed=False, plyName='Ply-3', region=region3, 
        material='SIGAPREG C U230-0/NF-E320/39%', 
        thicknessType=SPECIFY_THICKNESS, thickness=1.0, 
        orientationType=SPECIFY_ORIENT, orientationValue=45.0, 
        additionalRotationType=ROTATION_NONE, additionalRotationField='', 
        axis=AXIS_3, angle=0.0, numIntPoints=3)
    compositeLayup.CompositePly(suppressed=False, plyName='Ply-4', region=region4, 
        material='SIGAPREG C U230-0/NF-E320/39%', 
        thicknessType=SPECIFY_THICKNESS, thickness=1.0, 
        orientationType=SPECIFY_ORIENT, orientationValue=90.0, 
        additionalRotationType=ROTATION_NONE, additionalRotationField='', 
        axis=AXIS_3, angle=0.0, numIntPoints=3)
    compositeLayup.CompositePly(suppressed=False, plyName='Ply-5', region=region5, 
        material='SIGAPREG C U230-0/NF-E320/39%', 
        thicknessType=SPECIFY_THICKNESS, thickness=1.0, 
        orientationType=SPECIFY_ORIENT, orientationValue=90.0, 
        additionalRotationType=ROTATION_NONE, additionalRotationField='', 
        axis=AXIS_3, angle=0.0, numIntPoints=3)
    compositeLayup.CompositePly(suppressed=False, plyName='Ply-6', region=region6, 
        material='SIGAPREG C U230-0/NF-E320/39%', 
        thicknessType=SPECIFY_THICKNESS, thickness=1.0, 
        orientationType=SPECIFY_ORIENT, orientationValue=45.0, 
        additionalRotationType=ROTATION_NONE, additionalRotationField='', 
        axis=AXIS_3, angle=0.0, numIntPoints=3)
    compositeLayup.CompositePly(suppressed=False, plyName='Ply-7', region=region7, 
        material='SIGAPREG C U230-0/NF-E320/39%', 
        thicknessType=SPECIFY_THICKNESS, thickness=1.0, 
        orientationType=SPECIFY_ORIENT, orientationValue=0.0, 
        additionalRotationType=ROTATION_NONE, additionalRotationField='', 
        axis=AXIS_3, angle=0.0, numIntPoints=3)
    compositeLayup.CompositePly(suppressed=False, plyName='Ply-8', region=region8, 
        material='SIGAPREG C U230-0/NF-E320/39%', 
        thicknessType=SPECIFY_THICKNESS, thickness=1.0, 
        orientationType=SPECIFY_ORIENT, orientationValue=-45.0, 
        additionalRotationType=ROTATION_NONE, additionalRotationField='', 
        axis=AXIS_3, angle=0.0, numIntPoints=3)
    compositeLayup.resume()
    compositeLayup.ReferenceOrientation(orientationType=DISCRETE, localCsys=None, 
        additionalRotationType=ROTATION_NONE, angle=0.0, 
        additionalRotationField='', axis=AXIS_3, stackDirection=STACK_3, 
        normalAxisDefinition=SURFACE, normalAxisRegion=normalAxisRegion, 
        normalAxisDirection=AXIS_3, flipNormalDirection=False, 
        primaryAxisDefinition=EDGE, primaryAxisRegion=primaryAxisRegion, 
        primaryAxisDirection=AXIS_1, flipPrimaryDirection=False)
    session.viewports['Viewport: 1'].view.setValues(session.views['Iso'])
    a = mdb.models['Model-1'].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(
        optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
    session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF, 
        engineeringFeatures=OFF)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
        referenceRepresentation=ON)
    p = mdb.models['Model-1'].parts['Fuegepartner2']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    a = mdb.models['Model-1'].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    a = mdb.models['Model-1'].rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = mdb.models['Model-1'].parts['Fuegepartner1']
    a.Instance(name='Fuegepartner1-1', part=p, dependent=ON)
    a = mdb.models['Model-1'].rootAssembly
    p = mdb.models['Model-1'].parts['Fuegepartner2']
    a.Instance(name='Fuegepartner2-1', part=p, dependent=ON)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=198.07, 
        farPlane=396.544, width=183.385, height=97.1402, viewOffsetX=-25.4457, 
        viewOffsetY=18.2152)
    a = mdb.models['Model-1'].rootAssembly
    a.translate(instanceList=('Fuegepartner2-1', ), vector=(120.0, 0.0, 0.0))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=198.78, 
        farPlane=395.834, width=184.042, height=97.4883, viewOffsetX=42.1766, 
        viewOffsetY=-25.0274)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=211.491, 
        farPlane=381.357, width=195.81, height=103.722, cameraPosition=(
        231.927, 61.7388, 289.137), cameraUpVector=(-0.414157, 0.843912, 
        -0.341007), cameraTarget=(81.8232, 2.0122, -0.847321), 
        viewOffsetX=44.8736, viewOffsetY=-26.6278)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=207.132, 
        farPlane=385.715, width=261.308, height=138.417, viewOffsetX=80.2091, 
        viewOffsetY=-38.0473)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=206.211, 
        farPlane=386.637, width=260.145, height=137.801, viewOffsetX=12.0388, 
        viewOffsetY=-11.0153)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=212.6, 
        farPlane=380.247, width=178.239, height=94.4144, viewOffsetX=-20.5119, 
        viewOffsetY=11.1526)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=211.935, 
        farPlane=380.913, width=177.681, height=94.1189, viewOffsetX=100.594, 
        viewOffsetY=-25.048)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=211.933, 
        farPlane=380.915, width=177.679, height=94.1179, viewOffsetX=55.4233, 
        viewOffsetY=-22.0487)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=213.884, 
        farPlane=378.964, width=158.721, height=84.0755, viewOffsetX=142.048, 
        viewOffsetY=-41.3024)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=213.283, 
        farPlane=379.565, width=158.274, height=83.8391, viewOffsetX=66.2836, 
        viewOffsetY=-24.2141)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=204.514, 
        farPlane=388.333, width=300.985, height=159.434, viewOffsetX=80.8435, 
        viewOffsetY=-12.4864)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=203.483, 
        farPlane=389.365, width=299.467, height=158.63, viewOffsetX=66.1613, 
        viewOffsetY=-8.70674)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=205.781, 
        farPlane=387.067, width=251.542, height=133.243, viewOffsetX=57.024, 
        viewOffsetY=-8.91968)
    session.viewports['Viewport: 1'].view.setValues(session.views['Iso'])
    session.viewports['Viewport: 1'].view.setValues(width=217.037, height=114.966, 
        viewOffsetX=1.45481, viewOffsetY=0.597995)
    a = mdb.models['Model-1'].rootAssembly
    a.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=50.0)
    a = mdb.models['Model-1'].rootAssembly
    a.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=250.0)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=488.079, 
        farPlane=694.631, width=256.103, height=135.66, viewOffsetX=-7.38533, 
        viewOffsetY=8.45899)
    a = mdb.models['Model-1'].rootAssembly
    del a.features['Datum plane-2']
    a = mdb.models['Model-1'].rootAssembly
    a.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=220.0)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=489.59, 
        farPlane=693.12, width=232.622, height=123.222, viewOffsetX=3.49571, 
        viewOffsetY=6.44179)
    a1 = mdb.models['Model-1'].rootAssembly
    a1.makeIndependent(instances=(a1.instances['Fuegepartner1-1'], ))
    a1 = mdb.models['Model-1'].rootAssembly
    a1.makeIndependent(instances=(a1.instances['Fuegepartner2-1'], ))
    p = mdb.models['Model-1'].parts['Fuegepartner2']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    a = mdb.models['Model-1'].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    a = mdb.models['Model-1'].rootAssembly
    c1 = a.instances['Fuegepartner1-1'].cells
    cells1 = c1.getSequenceFromMask(mask=('[#ff ]', ), )
    a.Set(cells=cells1, name='Fuegerpartner1-All')
    mdb.models['Model-1'].rootAssembly.sets.changeKey(
        fromName='Fuegerpartner1-All', toName='Fuegepartner1-All')
    a = mdb.models['Model-1'].rootAssembly
    c1 = a.instances['Fuegepartner2-1'].cells
    cells1 = c1.getSequenceFromMask(mask=('[#ff ]', ), )
    a.Set(cells=cells1, name='Fuegepartner2-All')
    a = mdb.models['Model-1'].rootAssembly
    c1 = a.instances['Fuegepartner1-1'].cells
    pickedCells = c1.getSequenceFromMask(mask=('[#ff ]', ), )
    d11 = a.datums
    a.PartitionCellByDatumPlane(datumPlane=d11[6], cells=pickedCells)
    a = mdb.models['Model-1'].rootAssembly
    c1 = a.instances['Fuegepartner2-1'].cells
    pickedCells = c1.getSequenceFromMask(mask=('[#ff ]', ), )
    d31 = a.datums
    a.PartitionCellByDatumPlane(datumPlane=d31[8], cells=pickedCells)
    session.viewports['Viewport: 1'].assemblyDisplay.hideInstances(instances=(
        'Fuegepartner2-1', ))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=527.627, 
        farPlane=683.951, width=82.3091, height=43.5997, viewOffsetX=-12.6505, 
        viewOffsetY=8.2529)
    a = mdb.models['Model-1'].rootAssembly
    s1 = a.instances['Fuegepartner1-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#0:2 #a8 ]', ), )
    a.Surface(side1Faces=side1Faces1, name='Fuegepartner1-Klebeflaeche')
    session.viewports['Viewport: 1'].view.setValues(nearPlane=524.234, 
        farPlane=687.344, width=144.566, height=76.5774, viewOffsetX=-0.271557, 
        viewOffsetY=9.71156)
    session.viewports['Viewport: 1'].assemblyDisplay.showInstances(instances=(
        'Fuegepartner2-1', ))
    session.viewports['Viewport: 1'].assemblyDisplay.hideInstances(instances=(
        'Fuegepartner1-1', ))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=515.284, 
        farPlane=658.197, width=142.098, height=75.2701, cameraPosition=(
        374.246, -398.329, 370.206), cameraUpVector=(-0.302708, 0.806065, 
        0.508554), cameraTarget=(144.207, -3.41461, -5.06108), 
        viewOffsetX=-0.266921, viewOffsetY=9.54577)
    a = mdb.models['Model-1'].rootAssembly
    s1 = a.instances['Fuegepartner2-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#0:2 #54 ]', ), )
    a.Surface(side1Faces=side1Faces1, name='Fuegepartner2-Klebeflaeche')
    session.viewports['Viewport: 1'].assemblyDisplay.showInstances(instances=(
        'Fuegepartner1-1', ))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=514.27, 
        farPlane=659.212, width=160.501, height=85.0183, viewOffsetX=1.86532, 
        viewOffsetY=10.8663)
    session.viewports['Viewport: 1'].view.setValues(session.views['Iso'])
    session.viewports['Viewport: 1'].view.setValues(nearPlane=432.992, 
        farPlane=728.543, width=178.909, height=94.7693, cameraPosition=(
        -425.145, -92.6284, 134.317), cameraUpVector=(0.0794602, 0.659644, 
        -0.747366))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=538.662, 
        farPlane=609.355, width=222.571, height=117.897, cameraPosition=(
        88.9508, 315.704, 490.369), cameraUpVector=(-0.0798149, 0.586863, 
        -0.805743), cameraTarget=(136.659, -13.7255, 0.784691))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=426.879, 
        farPlane=724.177, width=176.383, height=93.4314, cameraPosition=(
        693.519, -115.277, 88.6519), cameraUpVector=(-0.136543, 0.988432, 
        -0.0660213), cameraTarget=(117.684, -0.19878, 13.393))
    a = mdb.models['Model-1'].rootAssembly
    f1 = a.instances['Fuegepartner1-1'].faces
    faces1 = f1.getSequenceFromMask(mask=('[#0:2 #202 ]', ), )
    f2 = a.instances['Fuegepartner2-1'].faces
    faces2 = f2.getSequenceFromMask(mask=('[#10000200 ]', ), )
    a.Set(faces=faces1+faces2, name='Klemmflaechen')
    session.viewports['Viewport: 1'].view.setValues(session.views['Iso'])
    session.viewports['Viewport: 1'].view.setValues(nearPlane=440.19, 
        farPlane=715.645, width=181.883, height=96.3448, cameraPosition=(
        -371.389, 185.529, 221.099), cameraUpVector=(0.228818, 0.511748, 
        -0.828104))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=450.493, 
        farPlane=705.342, width=54.0005, height=28.6044, viewOffsetX=-40.6961, 
        viewOffsetY=3.08877)
    a = mdb.models['Model-1'].rootAssembly
    s1 = a.instances['Fuegepartner1-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#0 #28140a0 #401 ]', ), )
    a.Surface(side1Faces=side1Faces1, name='Ankerseite')
    session.viewports['Viewport: 1'].view.setValues(nearPlane=445.575, 
        farPlane=710.26, width=136.225, height=72.1596, viewOffsetX=-31.4694, 
        viewOffsetY=12.1605)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=513.657, 
        farPlane=575.392, width=157.04, height=83.1853, cameraPosition=(92.485, 
        473.974, 282.877), cameraUpVector=(-0.789146, -0.078564, -0.60916), 
        cameraTarget=(148.438, -11.7663, -50.9175), viewOffsetX=-36.2778, 
        viewOffsetY=14.0186)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=373.196, 
        farPlane=664.822, width=114.097, height=60.4381, cameraPosition=(
        653.737, 8.2025, 68.0092), cameraUpVector=(-0.392003, 0.885133, 
        0.250747), cameraTarget=(74.4647, 9.22967, -54.204), 
        viewOffsetX=-26.3576, viewOffsetY=10.1852)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=377.455, 
        farPlane=658.164, width=115.399, height=61.1278, cameraPosition=(
        642.25, 28.3052, 126.188), cameraUpVector=(-0.451508, 0.869823, 
        0.198866), cameraTarget=(81.0298, 6.66908, -61.0484), 
        viewOffsetX=-26.6584, viewOffsetY=10.3014)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=381.23, 
        farPlane=654.389, width=64.4914, height=34.1616, viewOffsetX=-24.6117, 
        viewOffsetY=5.17707)
    a = mdb.models['Model-1'].rootAssembly
    s1 = a.instances['Fuegepartner2-1'].faces
    side1Faces1 = s1.getSequenceFromMask(mask=('[#0 #2822090 #201 ]', ), )
    a.Surface(side1Faces=side1Faces1, name='Zugseite')
    session.viewports['Viewport: 1'].view.setValues(nearPlane=377.657, 
        farPlane=657.962, width=119.099, height=63.0874, viewOffsetX=-20.7733, 
        viewOffsetY=10.0796)
    session.viewports['Viewport: 1'].view.setValues(session.views['Iso'])
    a = mdb.models['Model-1'].rootAssembly
    c1 = a.instances['Fuegepartner1-1'].cells
    cells1 = c1.getSequenceFromMask(mask=('[#ffff ]', ), )
    c2 = a.instances['Fuegepartner2-1'].cells
    cells2 = c2.getSequenceFromMask(mask=('[#fffc ]', ), )
    a.Set(cells=cells1+cells2, name='AllCells')
    a = mdb.models['Model-1'].rootAssembly
    a.ReferencePoint(point=(270.0, 1.0, 12.5))
    a = mdb.models['Model-1'].rootAssembly
    a.ReferencePoint(point=(0.0, 1.0, 12.5))
    mdb.models['Model-1'].rootAssembly.features.changeKey(fromName='RP-1', 
        toName='ZugMesspunkt')
    mdb.models['Model-1'].rootAssembly.features.changeKey(fromName='RP-2', 
        toName='Ankerpunkt')
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(interactions=ON, 
        constraints=ON, connectors=ON, engineeringFeatures=ON)
    a = mdb.models['Model-1'].rootAssembly
    r1 = a.referencePoints
    refPoints1=(r1[19], )
    a.Set(referencePoints=refPoints1, name='ZugMesspunkt')
    a = mdb.models['Model-1'].rootAssembly
    r1 = a.referencePoints
    refPoints1=(r1[20], )
    a.Set(referencePoints=refPoints1, name='Ankerpunkt')
    a = mdb.models['Model-1'].rootAssembly
    region1=a.sets['ZugMesspunkt']
    a = mdb.models['Model-1'].rootAssembly
    region2=a.surfaces['Zugseite']
    mdb.models['Model-1'].Coupling(name='Constraint-1', controlPoint=region1, 
        surface=region2, influenceRadius=WHOLE_SURFACE, couplingType=KINEMATIC, 
        alpha=0.0, localCsys=None, u1=ON, u2=ON, u3=ON, ur1=ON, ur2=ON, ur3=ON)
    a = mdb.models['Model-1'].rootAssembly
    region1=a.sets['Ankerpunkt']
    a = mdb.models['Model-1'].rootAssembly
    region2=a.surfaces['Ankerseite']
    mdb.models['Model-1'].Coupling(name='Constraint-2', controlPoint=region1, 
        surface=region2, influenceRadius=WHOLE_SURFACE, couplingType=KINEMATIC, 
        alpha=0.0, localCsys=None, u1=ON, u2=ON, u3=ON, ur1=ON, ur2=ON, ur3=ON)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(interactions=OFF, 
        constraints=OFF, connectors=OFF, engineeringFeatures=OFF, 
        adaptiveMeshConstraints=ON)
    mdb.models['Model-1'].TempDisplacementDynamicsStep(name='Step-1', 
        previous='Initial', massScaling=((SEMI_AUTOMATIC, MODEL, AT_BEGINNING, 
        0.0, 1e-05, BELOW_MIN, 0, 0, 0.0, 0.0, 0, None), ), 
        improvedDtMethod=ON)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(interactions=ON, 
        constraints=ON, connectors=ON, engineeringFeatures=ON, 
        adaptiveMeshConstraints=OFF)
    mdb.models['Model-1'].ContactProperty('General')
    mdb.models['Model-1'].interactionProperties['General'].TangentialBehavior(
        formulation=PENALTY, directionality=ISOTROPIC, slipRateDependency=OFF, 
        pressureDependency=OFF, temperatureDependency=OFF, dependencies=0, 
        table=((0.3, ), ), shearStressLimit=None, maximumElasticSlip=FRACTION, 
        fraction=0.005, elasticSlipStiffness=None)
    mdb.models['Model-1'].interactionProperties['General'].NormalBehavior(
        pressureOverclosure=HARD, allowSeparation=ON, 
        constraintEnforcementMethod=DEFAULT)
    mdb.models['Model-1'].ContactProperty('Cohesive')
    mdb.models['Model-1'].interactionProperties['Cohesive'].NormalBehavior(
        pressureOverclosure=HARD, allowSeparation=ON, 
        constraintEnforcementMethod=DEFAULT)
    mdb.models['Model-1'].interactionProperties['Cohesive'].CohesiveBehavior(
        defaultPenalties=OFF, table=((6596.0, 2390.0, 2390.0), ))
    mdb.models['Model-1'].interactionProperties['Cohesive'].Damage(
        criterion=QUAD_TRACTION, initTable=((30.112, 36.0, 36.0), ), 
        useEvolution=ON, evolutionType=ENERGY, useMixedMode=ON, 
        mixedModeType=BK, exponent=1.0, evolTable=((0.9055, 2.3213, 2.3213), ))
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Initial')
    mdb.models['Model-1'].ContactExp(name='Int-1', createStepName='Initial')
    mdb.models['Model-1'].interactions['Int-1'].includedPairs.setValuesInStep(
        stepName='Initial', useAllstar=ON)
    r21=mdb.models['Model-1'].rootAssembly.surfaces['Fuegepartner1-Klebeflaeche']
    r22=mdb.models['Model-1'].rootAssembly.surfaces['Fuegepartner2-Klebeflaeche']
    mdb.models['Model-1'].interactions['Int-1'].contactPropertyAssignments.appendInStep(
        stepName='Initial', assignments=((GLOBAL, SELF, 'General'), (r21, r22, 
        'Cohesive')))
    mdb.models['Model-1'].interactions['Int-1'].wearSurfacePropertyAssignments.appendInStep(
        stepName='Initial', assignments=((GLOBAL, ''), ))
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
    mdb.models['Model-1'].SmoothStepAmplitude(name='SmoothStep', timeSpan=STEP, 
        data=((0.0, 0.0), (2.0, 1.0)))
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
        predefinedFields=ON, interactions=OFF, constraints=OFF, 
        engineeringFeatures=OFF)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Initial')
    a = mdb.models['Model-1'].rootAssembly
    region = a.sets['Klemmflaechen']
    mdb.models['Model-1'].DisplacementBC(name='Location', createStepName='Initial', 
        region=region, u1=UNSET, u2=SET, u3=SET, ur1=UNSET, ur2=UNSET, 
        ur3=UNSET, amplitude=UNSET, distributionType=UNIFORM, fieldName='', 
        localCsys=None)
    a = mdb.models['Model-1'].rootAssembly
    region = a.sets['Ankerpunkt']
    mdb.models['Model-1'].PinnedBC(name='Pinned', createStepName='Initial', 
        region=region, localCsys=None)
    a = mdb.models['Model-1'].rootAssembly
    region = a.sets['ZugMesspunkt']
    mdb.models['Model-1'].DisplacementBC(name='Zug', createStepName='Initial', 
        region=region, u1=UNSET, u2=SET, u3=SET, ur1=UNSET, ur2=UNSET, 
        ur3=UNSET, amplitude=UNSET, distributionType=UNIFORM, fieldName='', 
        localCsys=None)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
    mdb.models['Model-1'].boundaryConditions['Zug'].setValuesInStep(
        stepName='Step-1', u1=6.0, amplitude='SmoothStep')
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON, loads=OFF, 
        bcs=OFF, predefinedFields=OFF, connectors=OFF)
    session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
        meshTechnique=ON)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=487.543, 
        farPlane=696.507, width=273.944, height=145.399, viewOffsetX=27.4174, 
        viewOffsetY=2.9711)
    a = mdb.models['Model-1'].rootAssembly
    c1 = a.instances['Fuegepartner1-1'].cells
    cells1 = c1.getSequenceFromMask(mask=('[#ffff ]', ), )
    c2 = a.instances['Fuegepartner2-1'].cells
    cells2 = c2.getSequenceFromMask(mask=('[#ffff ]', ), )
    pickedCells = cells1+cells2
    f1 = a.instances['Fuegepartner1-1'].faces
    a.assignStackDirection(referenceRegion=f1[65], cells=pickedCells)
    elemType1 = mesh.ElemType(elemCode=SC8R, elemLibrary=EXPLICIT, 
        secondOrderAccuracy=OFF, hourglassControl=DEFAULT, elemDeletion=ON)
    elemType2 = mesh.ElemType(elemCode=SC6R, elemLibrary=EXPLICIT)
    elemType3 = mesh.ElemType(elemCode=UNKNOWN_TET, elemLibrary=EXPLICIT)
    a = mdb.models['Model-1'].rootAssembly
    c1 = a.instances['Fuegepartner1-1'].cells
    cells1 = c1.getSequenceFromMask(mask=('[#ffff ]', ), )
    c2 = a.instances['Fuegepartner2-1'].cells
    cells2 = c2.getSequenceFromMask(mask=('[#fffc ]', ), )
    pickedRegions =((cells1+cells2), )
    a.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
        elemType3))
    a = mdb.models['Model-1'].rootAssembly
    partInstances =(a.instances['Fuegepartner1-1'], a.instances['Fuegepartner2-1'], 
        )
    a.seedPartInstance(regions=partInstances, size=0.4, deviationFactor=0.1, 
        minSizeFactor=0.1)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=488.171, 
        farPlane=695.879, width=264.386, height=140.326, viewOffsetX=24.917, 
        viewOffsetY=6.88884)
    a = mdb.models['Model-1'].rootAssembly
    partInstances =(a.instances['Fuegepartner1-1'], a.instances['Fuegepartner2-1'], 
        )
    a.generateMesh(regions=partInstances)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=486.956, 
        farPlane=697.093, width=282.862, height=150.132, viewOffsetX=44.5439, 
        viewOffsetY=9.07139)
    session.viewports['Viewport: 1'].view.setValues(session.views['Iso'])
    session.viewports['Viewport: 1'].setValues(displayedObject=None)
    session.mdbData.summary()
    a = mdb.models['Model-1'].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF)
    session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
        meshTechnique=OFF)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
        predefinedFields=ON, connectors=ON)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON, loads=OFF, 
        bcs=OFF, predefinedFields=OFF, connectors=OFF)
    session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
        meshTechnique=ON)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF, 
        optimizationTasks=ON, geometricRestrictions=ON, stopConditions=ON)
    session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
        meshTechnique=OFF)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(
        adaptiveMeshConstraints=ON, optimizationTasks=OFF, 
        geometricRestrictions=OFF, stopConditions=OFF)
    mdb.models['Model-1'].OperatorFilter(name='MinValue', operation=MIN, 
        limit=-0.1, halt=ON)
    session.viewports['Viewport: 1'].view.setValues(width=218.825, height=115.913, 
        viewOffsetX=-0.104306, viewOffsetY=1.71099)
    mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=(
        'DAMAGEC', 'DAMAGEFC', 'DAMAGEFT', 'DAMAGEMC', 'DAMAGEMT', 'DAMAGESHR', 
        'DAMAGET', 'DMICRT', 'LE', 'S', 'SDEG'), numIntervals=50, layupNames=(
        'Fuegepartner1-1.CompositeLayup-Fuegepartner1', ), 
        layupLocationMethod=SPECIFIED, outputAtPlyTop=False, 
        outputAtPlyMid=True, outputAtPlyBottom=False, rebar=EXCLUDE)
    mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=(
        'S', 'LE', 'DAMAGEC', 'DAMAGET', 'DAMAGEFT', 'DAMAGEFC', 'DAMAGEMT', 
        'DAMAGEMC', 'DAMAGESHR', 'SDEG', 'DMICRT', 'STATUS'), 
        layupLocationMethod=SPECIFIED, outputAtPlyTop=False, 
        outputAtPlyMid=True, outputAtPlyBottom=False)
    mdb.models['Model-1'].FieldOutputRequest(name='F-Output-2', 
        createStepName='Step-1', variables=('DAMAGEC', 'DAMAGEFC', 'DAMAGEFT', 
        'DAMAGEMT', 'DAMAGESHR', 'DAMAGET', 'DMICRT', 'LE', 'S', 'SDEG', 
        'STATUS'))
    mdb.models['Model-1'].fieldOutputRequests['F-Output-2'].setValues(variables=(
        'DAMAGEC', 'DAMAGEFC', 'DAMAGEFT', 'DAMAGEMT', 'DAMAGESHR', 'DAMAGET', 
        'DMICRT', 'LE', 'S', 'SDEG', 'STATUS'), numIntervals=50, layupNames=(
        'Fuegepartner2-1.CompositeLayup-Fuegepartner2', ), 
        layupLocationMethod=SPECIFIED, outputAtPlyTop=False, 
        outputAtPlyMid=True, outputAtPlyBottom=False, rebar=EXCLUDE)
    mdb.models['Model-1'].FieldOutputRequest(name='F-Output-3', 
        createStepName='Step-1', variables=('CSDMG', 'STATUS'), 
        numIntervals=50)
    mdb.models['Model-1'].historyOutputRequests['H-Output-1'].setValues(variables=(
        'ALLIE', 'ALLKE'), numIntervals=100)
    regionDef=mdb.models['Model-1'].rootAssembly.sets['ZugMesspunkt']
    mdb.models['Model-1'].HistoryOutputRequest(name='ZugMesspunkt', 
        createStepName='Step-1', variables=('RF1', 'U1'), region=regionDef, 
        sectionPoints=DEFAULT, rebar=EXCLUDE)
    regionDef=mdb.models['Model-1'].rootAssembly.sets['ZugMesspunkt']
    mdb.models['Model-1'].HistoryOutputRequest(name='H-Output-Criteria', 
        createStepName='Step-1', variables=('RF1', ), region=regionDef, 
        filter='MinValue', sectionPoints=DEFAULT, rebar=EXCLUDE)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(
        adaptiveMeshConstraints=OFF)
    mdb.Job(name='Job-1', model='Model-1', description='', type=ANALYSIS, 
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
        memoryUnits=PERCENTAGE, explicitPrecision=SINGLE, 
        nodalOutputPrecision=SINGLE, echoPrint=OFF, modelPrint=OFF, 
        contactPrint=OFF, historyPrint=OFF, userSubroutine='', scratch='', 
        resultsFormat=ODB, numDomains=28, activateLoadBalancing=False, 
        numThreadsPerMpiProcess=1, numCpus=28)
    mdb.Job(name='Job-1', model='Model-1', description='', type=ANALYSIS, 
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
        memoryUnits=PERCENTAGE, explicitPrecision=SINGLE, 
        nodalOutputPrecision=SINGLE, echoPrint=OFF, modelPrint=OFF, 
        contactPrint=OFF, historyPrint=OFF, userSubroutine='', scratch='', 
        resultsFormat=ODB, numDomains=12, activateLoadBalancing=False, 
        numThreadsPerMpiProcess=1, numCpus=12)
    mdb.saveAs(
        pathName='C:/Users/nicol/Documents/Abaqus/SteppedJoint/SteppedJoint')


