# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 10:07:24 2020

@author: SA20149963
"""

from neo4j import GraphDatabase
import os
directory ="D:\OSDU\Log Metadata"
uri = "neo4j://40.117.46.5:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "admin"))




def import_LASMetadata(tx, filename):
    #Import JSON string from the file
    print(filename)
    query='''CALL apoc.load.json("'''+filename+'''")
    YIELD value
	MERGE(welllogs:WellLogs {Name:"WellLogs", Value:"Well Logs"})
	WITH  value, welllogs
	UNWIND value.WorkProductComponents as wpc
		FOREACH(iw in wpc.Data.IndividualTypeProperties | 
			MERGE(logid:BoreId{Name:"Well Log", Value:iw.WellboreID}) 
			MERGE (wellboreid:Wellbore{Wellbore:iw.WellboreID}) 
			MERGE (wellboreid)-[dw:CHILD_OF]->(logid)
			MERGE(logid)-[:CHILD_OF]->(welllogs)
			MERGE(curveheader:Curves{Name:"Curves", Id:iw.WellboreID})
			MERGE(curveheader)-[:CHILD_OF]->(logid)
			FOREACH(cur in wpc.Data.IndividualTypeProperties.Curves |
				MERGE(curve:Curve{Mnemonic: cur.Mnemonic, TopDepth: cur.TopDepth, BaseDepth:cur.BaseDepth, DepthUnit:cur.DepthUnit, CurveUnit:cur.CurveUnit})
				MERGE(curve)-[:CHILD_OF]->(curveheader))
			FOREACH (td in  wpc.Data.IndividualTypeProperties.TopMeasuredDepth |
				MERGE(tmd:TopMeasuredDepth{Name:"Top_Measured_Depth", Value:td.Depth, Id:iw.WellboreID})
				MERGE(tmd)-[:CHILD_OF]->(logid)
				MERGE(tmduom:tmdUOM{Name: "Top_Measured_UOM",Value:td.UnitsOfMeasure, id:iw.WellboreID})
				MERGE(tmduom)-[:CHILD_OF]->(logid))
			FOREACH (bd in  wpc.Data.IndividualTypeProperties.BottomMeasuredDepth | 
				MERGE(bmd:BottomMeasuredDepth{Name: "Bottom_Measured_Depth", Value:bd.Depth, id:iw.WellboreID})
				MERGE(bmd)-[:CHILD_OF]->(logid)
				MERGE(bmduom:bmdUOM{Name: "Bottom_Measured_UOM",Value:bd.UnitsOfMeasure, id:iw.WellboreID})
				MERGE(bmduom)-[:CHILD_OF]->(logid))
			FOREACH (ad in wpc.Data.IndividualTypeProperties.AuthorIDs |
				MERGE(author:AuthorId {AuthorId:  ad, id:iw.WellboreID})
				MERGE(author)-[:CHILD_OF]->(logid))
				
				MERGE (wellname:WellName{Name:iw.Name,Id:iw.WellboreID}) 
				MERGE (wellname)-[:CHILD_OF]->(logid) 
				MERGE (welldscr:WellDescription{Description:iw.Description,Id:iw.WellboreID}) 
				MERGE (welldscr)-[:CHILD_OF]->(logid))
		WITH value
		MATCH(logid:BoreId)
		WITH value, logid
		UNWIND value.WorkProduct as wpitems
			MERGE(resourcetypeid:ResourceTypeID {name:"ResourceTypeID", val:wpitems.ResourceTypeID, Id:logid.Value})
			MERGE (resourcetypeid)-[r:CHILD_OF]->(logid)
			MERGE(rsc:ResourceSecurityClassification {name:"ResourceSecurityClassification", val:wpitems.ResourceSecurityClassification,Id:logid.Value})
			MERGE (rsc)-[rs:CHILD_OF]->(logid)
			FOREACH(c in wpitems.ComponentsAssociativeIDs |
				MERGE (caid:ComponentsAssociativeID{Name:c, Value:c,Id:logid.Value})
				MERGE (caid)-[:CHILD_OF]->(logid) )'''
    result = tx.run(query)
    print("Importing JSON...........\n")
    for record in result:
       print(record)
    print("\n Completed Importing JSON...........\n")

#import Ontology using neosemantics plugin / import ontology OWL file
with driver.session() as session:
    for filename in os.listdir(directory):
        if filename.endswith(".json"): 
            session.write_transaction(import_LASMetadata,"jsonmetadata/"+filename)
            continue
        else:
            continue    
   
driver.close() 
