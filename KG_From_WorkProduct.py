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
	MERGE(welllog:WellLog {name:"Well Log", value:"Well Log"})
	WITH  value, welllog
	UNWIND value.WorkProductComponents as wpc
		FOREACH(iw in wpc.Data.IndividualTypeProperties | 
			MERGE(wellboreid:WellBoreId{name:"WellboreID", value:iw.WellboreID, WellboreID:iw.WellboreID}) 
			MERGE(wellboreid)<-[:Has_Wellbore]-(welllog)
			MERGE(curveheader:Curves{name:"Curves", id:iw.WellboreID})
			MERGE(curveheader)<-[:Has_Curves]-(wellboreid)
			FOREACH(cur in wpc.Data.IndividualTypeProperties.Curves |
				MERGE(curve:Curve{Mnemonic: cur.Mnemonic, TopDepth: cur.TopDepth, BaseDepth:cur.BaseDepth, DepthUnit:cur.DepthUnit, CurveUnit:cur.CurveUnit})
				MERGE(curve)<-[:Has_Curve]-(curveheader)
			FOREACH (td in  wpc.Data.IndividualTypeProperties.TopMeasuredDepth |
				MERGE(tmd:TopMeasuredDepth{name:"TopMeasuredDepth", value:td.Depth, id:iw.WellboreID})
				MERGE(tmd)<-[:Has_TopMeasuredDepth]-(wellboreid)
				MERGE(tmduom:tmdUOM{name: "TopMeasuredUOM",value:td.UnitsOfMeasure, id:iw.WellboreID})
				MERGE(tmduom)<-[:Has_TopMeasuredUOM]-(wellboreid)
			FOREACH (bd in  wpc.Data.IndividualTypeProperties.BottomMeasuredDepth | 
				MERGE(bmd:BottomMeasuredDepth{name: "BottomMeasuredDepth", value:bd.Depth, id:iw.WellboreID})
				MERGE(bmd)<-[:Has_BottomMeasuredDepth]-(wellboreid)
				MERGE(bmduom:bmdUOM{name: "BottomMeasuredUOM",value:bd.UnitsOfMeasure, id:iw.WellboreID})
				MERGE(bmduom)<-[:Has_BottomMeasuredUOM]-(wellboreid)
			FOREACH (ad in wpc.Data.IndividualTypeProperties.AuthorIDs |
				MERGE(author:AuthorId {AuthorId:  ad, id:iw.WellboreID})
				MERGE(author)<-[:Has_Autnors]-(wellboreid)
				MERGE (welldscr:WellDescription{WellDescription:iw.Description,id:iw.WellboreID}) 
				MERGE (welldscr)<-[:Has_WellDescription]-(wellboreid))))))
		WITH value
        MATCH(wellboreid:WellBoreId{name:"WellboreID"})
		WITH value, wellboreid
		UNWIND value.WorkProduct as wpitems
			FOREACH(c in wpitems.ComponentsAssociativeIDs |
				MERGE (caid:ComponentsAssociativeID{name:c, value:c, id:wellboreid.value})
				MERGE (caid)<-[:Has_ComponentAssociative]-(wellboreid) )'''
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
