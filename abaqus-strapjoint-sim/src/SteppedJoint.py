from abaqus import *
from abaqusConstants import *
from caeModules import *
import __main__
import sys


#Overlap = 30 #mm
#orient = [-45.0, 0.0, 45.0, 90.0, 90.0, 45.0, 0.0, -45.0]
#Film_thickness = 0.1 #mm
#Cores = 10 #number of cores for the job

class AdhesiveMaterial:
    def __init__(self, name, Ek, Gk, damage_initiation, damage_evolution):
        self.name = name
        self.Ek = Ek
        self.Gk = Gk
        self.damage_initiation = damage_initiation
        self.damage_evolution = damage_evolution

    def cohesive_penalties(self, thickness):
        Kn = self.Ek / thickness
        Ks = self.Gk / thickness
        Kt = Ks
        return (Kn, Ks, Kt)

DP490 = AdhesiveMaterial(
    name = "DP490",
    Ek=659.6,
    Gk=239.0,
    damage_initiation=(30.112, 36.0, 36.0),
    damage_evolution=(0.9055, 2.3213, 2.3213),
)

AF163 = AdhesiveMaterial(
    name = "AF163",
    Ek=1110.0,
    Gk=413.69,
    damage_initiation=(48.26, 47.92, 47.92),
    damage_evolution=(3.8, 9.8, 9.8),
)


def SteppedJoint(stepratio, adhesive, film_thickness, cores, L=150.0, B=25.0, th=2.0, pl=8, num_steps=4, orientation_values= [-45.0, 0.0, 45.0, 90.0, 90.0, 45.0, 0.0, -45.0]):

    stepratio_str = f"{stepratio}"
    # Format film thickness
    if film_thickness < 1:
        film_thickness_str = f"{int(film_thickness * 1000)}mu"  # e.g., 0.12 -> 120mu
    else:
        film_thickness_str = str(film_thickness).replace(".", "p")  # e.g., 1.5 -> 1p5
    
    if adhesive is None:
        adhesive_name = "None"
    elif hasattr(adhesive, 'name'):
        adhesive_name = adhesive.name
    else:
        # fallback to class name
        adhesive_name = adhesive.__class__.__name__
    
    adhesive_name = adhesive_name.replace(" ", "_").replace(".", "_").replace(",", "_")
    part_name = f"SEP{stepratio_str}_{film_thickness_str}_{adhesive_name}"

    #Paramters
    pl_th = th / pl  #thickness of each ply
    HStep = th / (num_steps)  #height of each step
    LStep = stepratio * HStep #length of each step
    Overlap = LStep * (num_steps - 1)  #total overlap length
    
    #create new empty model database
    Mdb()

    mymodel = mdb.models['Model-1']

    myview = session.viewports[session.currentViewportName]

    #sketch 1st part
    s = mymodel.ConstrainedSketch(name='SketchFuegepartner1', 
        sheetSize=200.0)

    # Bottom edge
    s.Line(point1=(0.0, 0.0), point2=(L, 0.0))
    
    # Draw stepped profile from right to left
    x = L
    y = 0.0
    for i in range(num_steps):
        y += HStep  # Vertical line up
        s.Line(point1=(x, y - HStep), point2=(x, y))
        x -= LStep  # Horizontal line left
        s.Line(point1=(x + LStep, y), point2=(x, y))
    
    # Top edge back to origin
    s.Line(point1=(x, y), point2=(0.0, th))
    
    # Close the sketch
    s.Line(point1=(0.0, th), point2=(0.0, 0.0))
    
    #create part and extrude
    p = mymodel.Part(name='Fuegepartner1', dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    
    p.BaseSolidExtrude(sketch=s, depth=B)
    del mymodel.sketches['SketchFuegepartner1']

    #create datum points for partitioning 1st part
    dps = []
    for i in range(1, pl):   
        y = pl_th * i
        dp = p.DatumPointByCoordinate(coords=(0.0, y, 0.0))
        dps.append(dp)

    #partition the 1st part
    for i in range(1, pl):
        e, d = p.edges.findAt(((0.0, th/2, 0.0),))[0], p.datums[dps[i-1].id]
        p.PartitionCellByPlanePointNormal(point=d, normal=e, cells=p.cells)

        #Create sets for each ply
    for i in range(1, pl+1):
        ply_name = 'Ply' + str(i)
        y = pl_th * (i - (2*pl_th))
        cells = p.cells.findAt(((L/2, y, B/2),))
        p.Set(cells=cells, name= ply_name)

    #sketch 2nd part
    s1 = mymodel.ConstrainedSketch(name='SketchFuegepartner2', 
        sheetSize=200.0)

    # Start at right edge
    s1.Line(point1=(L, 0.0), point2=(L, th))
    
    # Top edge
    s1.Line(point1=(L, th), point2=(0.0, th))
    
    # Draw stepped profile from left to right (descending)
    x = 0.0
    y = th
    for i in range(num_steps):
        y -= HStep  # Vertical line down
        s1.Line(point1=(x, y + HStep), point2=(x, y))
        x += LStep  # Horizontal line right
        s1.Line(point1=(x - LStep, y), point2=(x, y))
    
    # Close the sketch back to right edge
    s1.Line(point1=(x, 0.0), point2=(L, 0.0))

    p = mymodel.Part(name='Fuegepartner2', dimensionality=THREE_D, 
        type=DEFORMABLE_BODY)
    
    p.BaseSolidExtrude(sketch=s1, depth=B)
    del mymodel.sketches['SketchFuegepartner2']

    #create datum points for partitioning 2nd part
    dps = []
    for i in range(1, pl):   
        y = pl_th * i
        dp = p.DatumPointByCoordinate(coords=(L, y, 0.0))
        dps.append(dp)

        #partition the 2nd part
    for i in range(1, pl):
        e, d = p.edges.findAt(((L, th/2, 0.0),))[0], p.datums[dps[i-1].id]
        p.PartitionCellByPlanePointNormal(point=d, normal=e, cells=p.cells)

        #Create sets for each ply
    for i in range(1, pl+1):
        ply_name = 'Ply' + str(i)
        y = pl_th * (i - (2*pl_th))
        cells = p.cells.findAt(((L/2, y, B/2),))
        p.Set(cells=cells, name= ply_name)

    #Create material
    mymodel.Material(name='SIGAPREG C U230-0/NF-E320/39%')
    mymodel.materials['SIGAPREG C U230-0/NF-E320/39%'].Elastic(
        type=ENGINEERING_CONSTANTS, table=((124311.0, 8767.0, 8767.0, 0.35, 
        0.35, 0.5, 4272.0, 4272.0, 2922.0), ))
    mymodel.materials['SIGAPREG C U230-0/NF-E320/39%'].Density(
        table=((1.55e-09, ), ))
    mymodel.materials['SIGAPREG C U230-0/NF-E320/39%'].HashinDamageInitiation(
        table=((1800.0, 1200.0, 36.0, 149.0, 64.0, 42.0), ),
        alpha=1.0)
    mymodel.materials['SIGAPREG C U230-0/NF-E320/39%'].hashinDamageInitiation.DamageEvolution(
        type=ENERGY, table=((92.0, 80.0, 0.21, 0.8), ))
    
    #Create composite layups
    ##Layup part 1
    p = mymodel.parts['Fuegepartner1']
    side1Faces = p.faces.findAt(((L/2, th, B/2),))
    normalAxisRegion = p.Surface(side1Faces=side1Faces, name='REF-SURF')

    edges = p.edges.findAt(((L/2,0.0,0.0),))
    primaryAxisRegion = p.Set(edges=edges, name='REF-EDGE')

    compositeLayup = mymodel.parts['Fuegepartner1'].CompositeLayup(
        name='CompositeLayup-Fuegepartner1', description='', elementType=CONTINUUM_SHELL, 
        symmetric=False)
    compositeLayup.Section(preIntegrate=OFF, integrationRule=SIMPSON, 
        poissonDefinition=DEFAULT, thicknessModulus=None, temperature=GRADIENT, 
        useDensity=OFF)
    
    compositeLayup.suppress()

    for i in range (1, pl+1):
        pl_name = 'Ply-' + str(i)
        region = mymodel.parts['Fuegepartner1'].sets['Ply' + str(i)]
        orientation_value = orientation_values[i-1] if i <= len(orientation_values) else 0.0
        compositeLayup.CompositePly(
            suppressed=False,
            plyName=pl_name,
            region=region,
            material='SIGAPREG C U230-0/NF-E320/39%',
            thicknessType=SPECIFY_THICKNESS,
            thickness=1.0,
            orientationType=SPECIFY_ORIENT,
            orientationValue=orientation_value,
            additionalRotationType=ROTATION_NONE,
            additionalRotationField='',
            axis=AXIS_3,
            angle=0.0,
            numIntPoints=3
        )
    
    compositeLayup.resume()
    compositeLayup.ReferenceOrientation(orientationType=DISCRETE, localCsys=None, 
        additionalRotationType=ROTATION_NONE, angle=0.0, 
        additionalRotationField='', axis=AXIS_3, stackDirection=STACK_3, 
        normalAxisDefinition=SURFACE, normalAxisRegion=normalAxisRegion, 
        normalAxisDirection=AXIS_3, flipNormalDirection=False, 
        primaryAxisDefinition=EDGE, primaryAxisRegion=primaryAxisRegion, 
        primaryAxisDirection=AXIS_1, flipPrimaryDirection=False)


    ##Layup part 2
    p = mymodel.parts['Fuegepartner2']
    side1Faces = p.faces.findAt(((L/2, th, B/2),))
    normalAxisRegion = p.Surface(side1Faces=side1Faces, name='REF-SURF')

    edges = p.edges.findAt(((L/2,th,0.0),))
    primaryAxisRegion = p.Set(edges=edges, name='REF-EDGE')

    compositeLayup = mymodel.parts['Fuegepartner2'].CompositeLayup(
        name='CompositeLayup-Fuegepartner2', description='', elementType=CONTINUUM_SHELL, 
        symmetric=False)
    compositeLayup.Section(preIntegrate=OFF, integrationRule=SIMPSON, 
        poissonDefinition=DEFAULT, thicknessModulus=None, temperature=GRADIENT, 
        useDensity=OFF)
    
    compositeLayup.suppress()

    for i in range (1, pl+1):
        pl_name = 'Ply-' + str(i)
        region = mymodel.parts['Fuegepartner2'].sets['Ply' + str(i)]
        orientation_value = orientation_values[i-1] if i <= len(orientation_values) else 0.0
        compositeLayup.CompositePly(
            suppressed=False,
            plyName=pl_name,
            region=region,
            material='SIGAPREG C U230-0/NF-E320/39%',
            thicknessType=SPECIFY_THICKNESS,
            thickness=1.0,
            orientationType=SPECIFY_ORIENT,
            orientationValue=orientation_value,
            additionalRotationType=ROTATION_NONE,
            additionalRotationField='',
            axis=AXIS_3,
            angle=0.0,
            numIntPoints=3
        )
    
    compositeLayup.resume()
    compositeLayup.ReferenceOrientation(orientationType=DISCRETE, localCsys=None, 
        additionalRotationType=ROTATION_NONE, angle=0.0, 
        additionalRotationField='', axis=AXIS_3, stackDirection=STACK_3, 
        normalAxisDefinition=SURFACE, normalAxisRegion=normalAxisRegion, 
        normalAxisDirection=AXIS_3, flipNormalDirection=False, 
        primaryAxisDefinition=EDGE, primaryAxisRegion=primaryAxisRegion, 
        primaryAxisDirection=AXIS_1, flipPrimaryDirection=True)

    #Assembly
    a = mymodel.rootAssembly

    a.DatumCsysByDefault(CARTESIAN)
   
    p = mymodel.parts['Fuegepartner1']
    a.Instance(name='Fuegepartner1-1', part=p, dependent=OFF)
    p = mymodel.parts['Fuegepartner2']
    a.Instance(name='Fuegepartner2-1', part=p, dependent=OFF)

    a.translate(instanceList=('Fuegepartner2-1', ), vector=(L - Overlap, 0.0, 0.0))

    #create datum planes and partitions
    dplane1 = a.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=50.0) 
    dplane2 = a.DatumPlaneByPrincipalPlane(principalPlane=YZPLANE, offset=(2*L - Overlap - 50.0))

    a.PartitionCellByDatumPlane(datumPlane=a.datums[dplane1.id], cells=a.instances['Fuegepartner1-1'].cells)
    a.PartitionCellByDatumPlane(datumPlane=a.datums[dplane2.id], cells=a.instances['Fuegepartner2-1'].cells)

    #create surfaces, sets and reference points
    f1 = a.instances['Fuegepartner1-1'].faces
    f1_faces = []
    for i in range(1, num_steps):
        f1_face = f1.findAt(((L - i*LStep + LStep/2, i*HStep, B/2),))
        f1_faces.append(f1_face)
    a.Surface(side1Faces=tuple(f1_faces), name='Fuegepartner1-Klebeflaeche')

    f1 = a.instances['Fuegepartner2-1'].faces
    f1_faces = []
    for i in range(1, num_steps):
        f1_face = f1.findAt(((L - Overlap + i*LStep - LStep/2, th - i*HStep, B/2),))
        f1_faces.append(f1_face)
    a.Surface(side1Faces=tuple(f1_faces), name='Fuegepartner2-Klebeflaeche')

    f1 = a.instances['Fuegepartner1-1'].faces
    f1_1 = f1.findAt(((25, th, B/2),))
    f1_2 = f1.findAt(((25, 0.0, B/2),))
    f2 = a.instances['Fuegepartner2-1'].faces
    f2_1 = f2.findAt(((2*L - Overlap - 25, th, B/2),))
    f2_2 = f2.findAt(((2*L - Overlap - 25, 0.0, B/2),))
    faces1 = [f1_1, f1_2, f2_1, f2_2]
    a.Set(faces=faces1, name='Klemmflaechen')

    f1 = a.instances['Fuegepartner1-1'].faces
    faces1 = f1.getByBoundingBox(
    xMin=0, xMax=0,
    yMin=0, yMax=th,
    zMin=0, zMax=B
    )
    a.Surface(side1Faces=faces1, name='Ankerseite')

    f1 = a.instances['Fuegepartner2-1'].faces
    faces1 = f1.getByBoundingBox(
    xMin=2*L - Overlap, xMax=2*L - Overlap,
    yMin=0, yMax=th,
    zMin=0, zMax=B
    )
    a.Surface(side1Faces=faces1, name='Zugseite')

    c1 = a.instances['Fuegepartner1-1'].cells
    c2 = a.instances['Fuegepartner2-1'].cells
    a.Set(cells=c1+c2, name='AllCells')

    zugMesspunkt = a.ReferencePoint(point=(2*L - Overlap, th/2, B/2))
    ankerpunkt = a.ReferencePoint(point=(0.0, th/2, B/2))

    a.Set(referencePoints=(a.referencePoints[zugMesspunkt.id],), name='ZugMesspunkt')
    a.Set(referencePoints=(a.referencePoints[ankerpunkt.id],), name='Ankerpunkt')

    #create couplings
    region1=a.sets['ZugMesspunkt']
    region2=a.surfaces['Zugseite']
    mymodel.Coupling(name='Constraint-1', controlPoint=region1, 
        surface=region2, influenceRadius=WHOLE_SURFACE, couplingType=KINEMATIC, 
        alpha=0.0, localCsys=None, u1=ON, u2=ON, u3=ON, ur1=ON, ur2=ON, ur3=ON)
    
    region1=a.sets['Ankerpunkt']
    region2=a.surfaces['Ankerseite']
    mymodel.Coupling(name='Constraint-2', controlPoint=region1, 
        surface=region2, influenceRadius=WHOLE_SURFACE, couplingType=KINEMATIC, 
        alpha=0.0, localCsys=None, u1=ON, u2=ON, u3=ON, ur1=ON, ur2=ON, ur3=ON)
       
    #create step
    mymodel.ExplicitDynamicsStep(name='Step-1', previous='Initial', 
        massScaling=((SEMI_AUTOMATIC, MODEL, AT_BEGINNING, 0.0, 1e-05, 
        BELOW_MIN, 0, 0, 0.0, 0.0, 0, None), ), improvedDtMethod=ON)
    
    #create interaction properties
    mymodel.ContactProperty('General')
    mymodel.interactionProperties['General'].TangentialBehavior(
        formulation=PENALTY, directionality=ISOTROPIC, slipRateDependency=OFF, 
        pressureDependency=OFF, temperatureDependency=OFF, dependencies=0, 
        table=((0.3, ), ), shearStressLimit=None, maximumElasticSlip=FRACTION, 
        fraction=0.005, elasticSlipStiffness=None)
    mymodel.interactionProperties['General'].NormalBehavior(
        pressureOverclosure=HARD, allowSeparation=ON, 
        constraintEnforcementMethod=DEFAULT)
    mymodel.ContactProperty('Cohesive')
    mymodel.interactionProperties['Cohesive'].NormalBehavior(
        pressureOverclosure=HARD, allowSeparation=ON, 
        constraintEnforcementMethod=DEFAULT)
    mymodel.interactionProperties['Cohesive'].CohesiveBehavior(
        defaultPenalties=OFF, table=(adhesive.cohesive_penalties(film_thickness), ))
    mymodel.interactionProperties['Cohesive'].Damage(
        criterion=QUAD_TRACTION, initTable=(adhesive.damage_initiation, ), 
        useEvolution=ON, evolutionType=ENERGY, useMixedMode=ON, 
        mixedModeType=BK, exponent=1.0, evolTable=(adhesive.damage_evolution, ))
    
    #create interactions
    mymodel.ContactExp(name='Int-1', createStepName='Initial')
    mymodel.interactions['Int-1'].includedPairs.setValuesInStep(
        stepName='Initial', useAllstar=ON)
    
    r21=mymodel.rootAssembly.surfaces['Fuegepartner1-Klebeflaeche']
    r22=mymodel.rootAssembly.surfaces['Fuegepartner2-Klebeflaeche']

    mymodel.interactions['Int-1'].contactPropertyAssignments.appendInStep(
        stepName='Initial', assignments=((GLOBAL, SELF, 'General'), (r21, r22, 
        'Cohesive')))
    
    mymodel.interactions['Int-1'].wearSurfacePropertyAssignments.appendInStep(
        stepName='Initial', assignments=((GLOBAL, ''), ))
    
    #create smooth step amplitude
    mymodel.SmoothStepAmplitude(name='SmoothStep', timeSpan=STEP, 
        data=((0.0, 0.0), (2.0, 1.0)))
    

     #boundary conditions
    region = a.sets['Klemmflaechen']
    mymodel.DisplacementBC(name='Location', createStepName='Initial', 
        region=region, u1=UNSET, u2=SET, u3=SET, ur1=UNSET, ur2=UNSET, ur3=UNSET, 
        amplitude=UNSET, distributionType=UNIFORM, fieldName='', 
        localCsys=None)
    
    region = a.sets['Ankerpunkt']
    mymodel.PinnedBC(name='Pinned', createStepName='Initial', 
        region=region, localCsys=None)

    region = a.sets['ZugMesspunkt']
    mymodel.DisplacementBC(name='Zug', createStepName='Initial', 
        region=region, u1=UNSET, u2=SET, u3=SET, ur1=UNSET, ur2=UNSET, ur3=UNSET, 
        amplitude=UNSET, distributionType=UNIFORM, fieldName='', 
        localCsys=None)
    
    mymodel.boundaryConditions['Zug'].setValuesInStep(
        stepName='Step-1', u1=6.0, amplitude='SmoothStep')
    
    #mesh

    f1 = a.instances['Fuegepartner2-1'].faces
    faces1 = f1.findAt(((L + L/2, th, B/2),))
    a.assignStackDirection(referenceRegion=faces1[0], cells=a.sets['AllCells'].cells)

    elemType1 = mesh.ElemType(elemCode=SC8R, elemLibrary=EXPLICIT, 
        secondOrderAccuracy=OFF, hourglassControl=DEFAULT, elemDeletion=ON)
    a.setElementType(regions=a.sets["AllCells"], elemTypes=(elemType1,))

    partInstances =(a.instances['Fuegepartner1-1'], a.instances['Fuegepartner2-1'], 
        )
    a.seedPartInstance(regions=partInstances, size=0.4, deviationFactor=0.1, 
        minSizeFactor=0.1)

    a.generateMesh(regions=partInstances)

    #create outputs and filter
    mymodel.OperatorFilter(name='MinValue', operation=MIN, 
        limit=-0.1, halt=ON)
    

    mymodel.fieldOutputRequests['F-Output-1'].setValues(variables=(
        'DAMAGEC', 'DAMAGEFC', 'DAMAGEFT', 'DAMAGEMC', 'DAMAGEMT', 'DAMAGESHR', 'DAMAGET', 'DMICRT', 'LE', 'S', 'SDEG', 'STATUS'),
        numIntervals=50, layupNames=('Fuegepartner1-1.CompositeLayup-Fuegepartner1', ),
        layupLocationMethod=SPECIFIED, outputAtPlyTop=False, 
        outputAtPlyMid=True, outputAtPlyBottom=False, rebar=EXCLUDE)
    
    mymodel.FieldOutputRequest(name='F-Output-2', 
        createStepName='Step-1', variables=('DAMAGEC', 'DAMAGEFC', 'DAMAGEFT', 'DAMAGEMC', 'DAMAGEMT', 'DAMAGESHR', 'DAMAGET', 'DMICRT', 'LE', 'S', 'SDEG', 'STATUS'),
        numIntervals=50, layupNames=('Fuegepartner2-1.CompositeLayup-Fuegepartner2', ), layupLocationMethod=SPECIFIED,
        outputAtPlyTop=False, outputAtPlyMid=True, outputAtPlyBottom=False, 
        rebar=EXCLUDE)
    
    mymodel.FieldOutputRequest(name='F-Output-3', 
        createStepName='Step-1', variables=('CSDMG', 'STATUS'), 
        numIntervals=50)
    

    mymodel.historyOutputRequests['H-Output-1'].setValues(variables=(
        'ALLIE', 'ALLKE'), numIntervals=100)
    
    regionDef=mymodel.rootAssembly.sets['ZugMesspunkt']
    mymodel.HistoryOutputRequest(name='H-Output-2', 
        createStepName='Step-1', variables=('RF1', 'U1'), numIntervals=200, 
        region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE)
    
    regionDef=mymodel.rootAssembly.sets['ZugMesspunkt']
    mymodel.HistoryOutputRequest(name='H-Output-Criteria', 
        createStepName='Step-1', variables=('RF1', ), numIntervals=200, 
        region=regionDef, filter='MinValue', sectionPoints=DEFAULT, 
        rebar=EXCLUDE)
    

    #create job
    mdb.Job(name=part_name, model='Model-1', description='', type=ANALYSIS, 
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
        memoryUnits=PERCENTAGE, explicitPrecision=SINGLE, 
        nodalOutputPrecision=SINGLE, echoPrint=OFF, modelPrint=OFF, 
        contactPrint=OFF, historyPrint=OFF, userSubroutine='', scratch='', 
        resultsFormat=ODB, numDomains=cores, activateLoadBalancing=False, 
        numThreadsPerMpiProcess=1, numCpus=cores)
    
    #job = mdb.jobs[part_name]
    #job.submit()
    #job.waitForCompletion()

    #mdb.saveAs(pathName=f"{part_name}.cae")

SteppedJoint(stepratio=20, adhesive=DP490, film_thickness=0.1, cores=12, L=150.0, B=25.0, th=2.0, pl=8, num_steps=4, orientation_values= [-45.0, 0.0, 45.0, 90.0, 90.0, 45.0, 0.0, -45.0])
