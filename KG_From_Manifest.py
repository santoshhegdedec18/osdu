# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 22:17:02 2020

@author: SA20149963
"""
#Program to create Knowledge Graph from the OSDU Manifest files

from neo4j import GraphDatabase
import os
directory ="D:/OSDU/Manifest_files"
uri = "neo4j://40.117.46.5:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "admin"))

def import_manifest(tx, filename):
    #Import JSON string from the file
    print(filename)
    query='''CALL apoc.load.json("'''+filename+'''")
    YIELD value 
	MERGE(welllog:WellLog {name:"Well Log", value:"Well Log"})
	WITH  value, welllog
	UNWIND value as val
	FOREACH(mf in val.Manifest | 
		MERGE(wellboreid:WellBoreId{name:"WellboreID", value:mf.ResourceID, WellboreID:mf.ResourceID})
		MERGE(wellboreid)<-[:Has_Wellbore]-(welllog)
		MERGE(restype:ResourceType{name:"ResourceTypeID", value:mf.ResourceTypeID, id:mf.ResourceID})
		MERGE(restype)<-[:Has_ResourceType]-(wellboreid)
		MERGE(resseccls:ResourceSecurityClassification{name:"ResourceSecurityClassification",value:mf.ResourceSecurityClassification, id:mf.ResourceID})
		MERGE(resseccls)<-[:Has_SecurityClassification]-(wellboreid)
	FOREACH(dit in val.Manifest.Data.IndividualTypeProperties |
		MERGE(facilitytype:FacilityTypeID{name:"FacilityTypeID",value:dit.FacilityTypeID,id: mf.ResourceID})
		MERGE(facilitytype)<-[:Has_FacilityType]-(wellboreid)
		MERGE(facilityname:FacilityName{name:"FacilityName",value:dit.FacilityName, id:mf.ResourceID})
		MERGE(facilityname)<-[:Has_FacilityName]-(wellboreid)
		MERGE(wellid:WellID{name:"WellID", value:dit.WellID,id:mf.ResourceID})
		MERGE(wellid)<-[:Has_WellID]-(wellboreid)
		MERGE(datasourceorg:DataSourceOrganisationID{name:"DataSourceOrganisationID", value:dit.DataSourceOrganisationID, id:mf.ResourceID})
		MERGE(datasourceorg)<-[:Has_DataSourceOrganization]-(wellboreid)
		MERGE(seqnum:SequenceNumber{name:"SequenceNumber", value:dit.SequenceNumber, id:mf.ResourceID})
		MERGE(seqnum)<-[:Has_SequenceNumber]-(wellboreid)
		MERGE(trajectorytype:TrajectoryTypeID{name:"TrajectoryTypeID", value:dit.TrajectoryTypeID, id:mf.ResourceID})
		MERGE(trajectorytype)<-[:Has_TrajectoryType]-(wellboreid)
		MERGE(primarymaterial:PrimaryMaterialID{name:"PrimaryMaterialID", value:dit.PrimaryMaterialID, id:mf.ResourceID})
		MERGE(primarymaterial)<-[:Has_PrimaryMaterial]-(wellboreid)
		MERGE(defvertmeasurement:DefaultVerticalMeasurementID{name:"DefaultVerticalMeasurementID", value:dit.DefaultVerticalMeasurementID, id:mf.ResourceID})
		MERGE(defvertmeasurement)<-[:Has_DefaultVerticalMeasurement]-(wellboreid)
		MERGE(projbottomholelocation:ProjectedBottomHoleLocation{name:"ProjectedBottomHoleLocation", id:mf.ResourceID})
		MERGE(projbottomholelocation)<-[:Has_ProjectedBottomHoleLocation]-(wellboreid)
		MERGE(horizontalcrs:HorizontalCRSID{name:"HorizontalCRSID", value:dit.ProjectedBottomHoleLocation.HorizontalCRSID, id:mf.ResourceID})
		MERGE(horizontalcrs)<-[:Has_HorizontalCRS_Type]-(projbottomholelocation)
	FOREACH(pbhl in dit.ProjectedBottomHoleLocation.Coordinates |
		MERGE(horizontalcordonates:HorozontalCoordinates{x:COALESCE(pbhl.x,""), y:COALESCE(pbhl.y,"")})
		MERGE(horizontalcordonates)<-[:Has_Horozontal_Coordinates]-(projbottomholelocation)
		MERGE(drillingreason:DrillingReason{name:"DrillingReason", id:mf.ResourceID})
		MERGE(drillingreason)<-[:Has_DrillingReason]-(wellboreid)
	FOREACH (dr in dit.DrillingReason |
		MERGE(drillingreasontype:DrillingReasonTypeID{name:"DrillingReasonTypeID", value:dr.DrillingReasonTypeID,id:mf.ResourceID})
		MERGE(drillingreasontype)<-[:Has_DrillingReasonType]-(drillingreason)
		MERGE(verticalmeasurements:VerticalMeasurement{name:"VerticalMeasurement",id:mf.ResourceID})
		MERGE(verticalmeasurements)<-[:Has_VerticalMeasurements]-(wellboreid)
	FOREACH (vm in dit.VerticalMeasurements |
		MERGE(verticalmeasurement:VerticalMeasurements{VerticalMeasurementID:COALESCE(vm.VerticalMeasurementID,""), VerticalMeasurementTypeID:COALESCE(vm.VerticalMeasurementTypeID,""), VerticalMeasurement:COALESCE(vm.VerticalMeasurement,""), VerticalMeasurementPathID:COALESCE(vm.VerticalMeasurementPathID,""), VerticalMeasurementUnitOfMeasureID:COALESCE(vm.VerticalMeasurementUnitOfMeasureID,""),VerticalCRSID: COALESCE(vm.VerticalCRSID,"")})
		MERGE(verticalmeasurement)<-[:Has_VerticalMeasurement]-(verticalmeasurements)
	FOREACH(fe in dit.FacilityEvent | 
		MERGE(facilityevents:FacilityEvents{name:"FacilityEvent", id:mf.ResourceID})
		MERGE(facilityevents)<-[:Has_FacilityEvents]-(wellboreid)
		MERGE(facilityevent:FacilityEvent{FacilityEventTypeID:COALESCE(fe.FacilityEventTypeID,""), EffectiveDateTime:COALESCE(fe.EffectiveDateTime,"")})
		MERGE(facilityevent)<-[:Has_FacilityEvent]-(facilityevents)
	FOREACH(fe in dit.FacilityState | 
		MERGE(facilitystates:Facilitystates{name:"FacilityState", id:mf.ResourceID})
		MERGE(facilitystates)<-[:Has_FacilityStates]-(wellboreid)
		MERGE(facilitystate:FacilityState{FacilityStateTypeID:COALESCE(fe.FacilityStateTypeID,""), id:mf.ResourceID})
		MERGE(facilitystate)<-[:Has_FacilityState]-(facilitystates)
	FOREACH(fna in dit.FacilityNameAlias |
		MERGE(namealiases:FacilityNameAliases{name:"FacilityNameAlias", id:mf.ResourceID})
		MERGE(namealiases)<-[:Has_FacilityNameAliases]-(wellboreid)
		MERGE(namealias:FacilityNameAlias{AliasName:COALESCE(fna.AliasName,""), AliasNameTypeID:COALESCE(fna.AliasNameTypeID,"")})
		MERGE(namealias)<-[:Has_NameAlias]-(namealiases)
		MERGE(spaciallocation:SpatialLocation{name:"SpatialLocation", id:mf.ResourceID})
		MERGE(spaciallocation)<-[:Has_SpacialLocations]-(wellboreid)
	FOREACH(sl in dit.SpatialLocation |
		MERGE(cordinates:Coordinates{name:"Coordinates", x:COALESCE(sl.Coordinates[0].x,""),y:COALESCE(sl.Coordinates[0].y,""), HorizontalCRSID:COALESCE(sl.HorizontalCRSID,""),VerticalCRSID:COALESCE(sl.VerticalCRSID,""),HorizontalCRSID:COALESCE(sl.HorizontalCRSID,""),HeightAboveGroundLevelUOMID:COALESCE(sl.HeightAboveGroundLevelUOMID,""), id:mf.ResourceID})
		MERGE(spaciallocation)<-[:Has_Coordinate]-(cordinates)
		MERGE(facilityoperators:FacilityOperator{name:"FacilityOperator", id:mf.ResourceID})
		MERGE(facilityoperators)<-[:Has_FacilityOperators]-(wellboreid)
	FOREACH(fo in dit.FacilityOperator |
		MERGE(fcilityoperator:FacilityOperatorOrganisationID{FacilityOperatorOrganisationID:COALESCE(fo.FacilityOperatorOrganisationID,""), id:mf.ResourceID})
		MERGE(fcilityoperator)<-[:Has_FacilityOperator]-(facilityoperators)
	))))))))))'''
    result = tx.run(query)
    print("Importing JSON...........\n")
    for record in result:
       print(record)
    print("\n Completed Importing JSON...........\n")

#import Ontology using neosemantics plugin / import ontology OWL file
with driver.session() as session:
    for filename in os.listdir(directory):
        if filename.endswith(".json"): 
            session.write_transaction(import_manifest,"manifestfiles/"+filename)
            continue
        else:
            continue    
   
driver.close() 
