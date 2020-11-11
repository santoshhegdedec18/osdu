# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 16:54:51 2020

@author: SA20149963
"""

import spacy
from spacy import displacy
from spacy.matcher import Matcher
nlp= spacy.load('en_core_web_sm')

text = '''London is the capital and largest city of England and the United Kingdom. 
Standing on the River Thames in the south-east of England, at the head of its 50-mile (80 km) 
estuary leading to the North Sea, London has been a major settlement for two millennia. 
Londinium was founded by the Romans. The City of London, London's ancient core − an area of just 1.12 
square miles (2.9 km2) and colloquially known as the Square Mile − retains boundaries that follow closely 
its medieval limits.The City of Westminster is also an Inner London borough holding city status. 
Greater London is governed by the Mayor of London and the London Assembly.London is located in the southeast 
of England.Westminster is located in London.London is the biggest city in Britain. London has a population 
of 7,172,036.'''

json_text = '''{'ResourceTypeID': 'srn:type:master-data/Wellbore:', 'Manifest': 
    {'ResourceID': 'srn:master-data/Wellbore:1000:', 'ResourceTypeID': 'srn:type:master-data/Wellbore:', 
    'ResourceSecurityClassification': 'srn:reference-data/ResourceSecurityClassification:RESTRICTED:', 
    'Data': {'IndividualTypeProperties': {'FacilityTypeID': 'srn:reference-data/FacilityType:WELLBORE:', 
    'FacilityOperator': [{'FacilityOperatorOrganisationID': 'srn:master-data/Organisation:ROVD:'}], 
    'DataSourceOrganisationID': 'srn:master-data/Organisation:TNO:', 'SpatialLocation': 
        [{'Coordinates': [{'x': 5.98136045, 'y': 51.43503877}], 'VerticalCRSID': 
            'srn:reference-data/VerticalCRS:NAP:', 'HorizontalCRSID': 'srn:reference-data/HorizontalCRS:WGS84:', 
            'HeightAboveGroundLevelUOMID': 'srn:reference-data/UnitOfMeasure:M:'},
            {'Coordinates': [{'x': 707310.0, 'y': 5702632.0}], 'HorizontalCRSID': 
                'srn:reference-data/HorizontalCRS:UTM31_ED50:'}], 'FacilityName': 'ACA-11', 
            'FacilityNameAlias': [{'AliasName': 'ACA-11', 'AliasNameTypeID': 
                'srn:reference-data/AliasNameType:Name:'}, {'AliasName': '1000', 'AliasNameTypeID': 
                    'srn:reference-data/AliasNameType:UWBI:'}], 'FacilityState': 
                    [{'FacilityStateTypeID': 'srn:reference-data/FacilityStateType:Abandoned:'}], 
                    'FacilityEvent': [{'FacilityEventTypeID': 'srn:reference-data/FacilityEventType:SPUD:', 
                    'EffectiveDateTime': '1909-04-05T00:00:00'}, {'FacilityEventTypeID': 'srn:reference-data/FacilityEventType:DRILLING FINISH:', 'EffectiveDateTime': '1910-01-19T00:00:00'}], 'WellID': 'srn:master-data/Well:1000:', 'SequenceNumber': 1, 'VerticalMeasurements': [{'VerticalMeasurementID': 'Rotary Table', 'VerticalMeasurementTypeID': 'srn:reference-data/VerticalMeasurementType:Rotary Table:', 'VerticalMeasurement': 29.3, 
                    'VerticalMeasurementPathID': 'srn:reference-data/VerticalMeasurementPath:Elevation:', 'VerticalMeasurementUnitOfMeasureID': 'srn:reference-data/UnitOfMeasure:M:', 'VerticalCRSID': 'srn:reference-data/VerticalCRS:NAP:'}, {'VerticalMeasurementID': 'TWO', 'VerticalMeasurementTypeID': 'srn:reference-data/VerticalMeasurementType:Rotary Table:', 'VerticalMeasurement': 1171.7, 'VerticalMeasurementPathID':
                        'srn:reference-data/VerticalMeasurementPath:Measured Depth:', 'VerticalMeasurementUnitOfMeasureID': 'srn:reference-data/UnitOfMeasure:M:'}, {'VerticalMeasurementID': 'THREE', 'VerticalMeasurementTypeID': 'srn:reference-data/VerticalMeasurementType:Rotary Table:', 'VerticalMeasurement': 1171.7, 'VerticalMeasurementPathID': 'srn:reference-data/VerticalMeasurementPath:True Vertical Depth:',
                        'VerticalMeasurementUnitOfMeasureID': 'srn:reference-data/UnitOfMeasure:M:'}], 'DrillingReason': [{'DrillingReasonTypeID': 'srn:reference-data/DrillingReasonType:EXP-C:'}], 'TrajectoryTypeID': 'srn:reference-data/WellboreTrajectoryType:Vertical:', 'PrimaryMaterialID': 'srn:reference-data/MaterialType:Coal:', 'DefaultVerticalMeasurementID': 'Rotary Table', 'ProjectedBottomHoleLocation': 
                            {'Coordinates': [{'x': 707310.0, 'y': 5702632.0}], 'HorizontalCRSID': 'srn:reference-data/HorizontalCRS:UTM31_ED50:'}}}}}
'''
doc = nlp(json_text)

for token in doc:
    print (token.text, token.pos_, token.dep_)
'''
for token in doc:
  print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
            token.shape_, token.is_alpha, token.is_stop)
'''