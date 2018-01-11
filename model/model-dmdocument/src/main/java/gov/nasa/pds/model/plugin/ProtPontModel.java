package gov.nasa.pds.model.plugin; 
import java.util.*;

/**
 * Transforms a token array (parsed Protege .pont file) into logical entities (e.g. classes and attributes).
 *   getProtModel  - get token array from parser and convert into classes and attributes
 */
class ProtPontModel extends InfoModel{
	
	PDSObjDefn objClass;
	AttrDefn attrClass;
	ArrayList <String> tokenArray;
	String attrTitle;
	String className;
	String classNameSpaceIdNC;
	TreeMap <String, String> masterClassDispo = new TreeMap <String, String> ();
	
	public ProtPontModel () {
		objArr = new ArrayList <PDSObjDefn> ();
		objDict = new HashMap<String, PDSObjDefn> ();
		attrDict = new HashMap<String, AttrDefn>();
		className = "";
		classNameSpaceIdNC = "";
		return;
	}
	
	/**
	 *   getProtModel  - get token array from parser and convert into classes and attributes
	 */
	public void getProtModel (String modelId, String fname) throws Throwable {
		ProtFramesParser lparser = new ProtFramesParser();
		if (lparser.parse(fname)) {
			tokenArray = lparser.getTokenArray();
			Iterator<String> tokenIter = tokenArray.iterator();
			getOntology(modelId, tokenIter);
		}
		return;
	}
	
	private void getOntology(String subModelId, Iterator<String> tokenIter) {
		int type = 0;
		int nestlevel = 0;
		
		while (tokenIter.hasNext()) {
			String token = (String) tokenIter.next();
			if (token.compareTo("name_") == 0) {
				token = "name";				
			}				
			if (token.compareTo("(") == 0) {
				nestlevel++;
			} else if (token.compareTo(")") == 0) {
				nestlevel--;
			}
			switch (type) {
			case 0:
				if (token.compareTo("defclass") == 0) {
					type = 1;
				} else if (token.compareTo("is-a") == 0) {
					type = 2;
				} else if (token.compareTo("single-slot") == 0) {
					type = 3;
				} else if (token.compareTo("multislot") == 0) {
					type = 4;
				} else if (token.compareTo("type") == 0) {
					type = 5;
				} else if (token.compareTo("allowed-classes") == 0) {
					type = 6;
				} else if (token.compareTo("value") == 0) {
					type = 7;
				} else if (token.compareTo("cardinality") == 0) {
					type = 8;
				} else if (token.compareTo("comment") == 0) {
					type = 9;
				} else if (token.compareTo("role") == 0) {
					type = 10;
				} else if (token.compareTo("default") == 0) {
					type = 11;
				}
				break;
			case 1: // class name
				className = token;
//				if (className.compareTo("%3ACLIPS_TOP_LEVEL_SLOT_CLASS") == 0) className = DMDocument.TopLevelAttrClassName;
				String luid3 = getNextUId();
//				String lClassRdfIdentifier = DMDocument.rdfPrefix + className + "." + getNextUId();
				String lClassRdfIdentifier = DMDocument.rdfPrefix + className + "." + luid3;
				objClass = new PDSObjDefn(lClassRdfIdentifier);
				objClass.title = className;
				objClass.uid = luid3;
//				objClass.versionId = InfoModel.identifier_version_id;
				objClass.versionId = DMDocument.classVersionIdDefault;
				objClass.docSecType = className;
				objClass.regAuthId = DMDocument.registrationAuthorityIdentifierValue;
				objClass.subModelId = subModelId;

				// get disposition for the class
				PDSObjDefn lClassWDisp = DMDocument.getClassDisposition (objClass, className, true);
				if (lClassWDisp != null) {
					classNameSpaceIdNC = lClassWDisp.nameSpaceIdNC;  // global needed for parser
					objDict.put(lClassWDisp.rdfIdentifier, lClassWDisp);
					objArr.add(lClassWDisp);
//					System.out.println("\ndebug ProtPontModel lClassWDisp.rdfIdentifier:" + lClassWDisp.rdfIdentifier);					
					attrClass = new AttrDefn("TBD");
					String token1 = (String) tokenIter.next();
					if (token1.compareTo("(") != 0) {
						lClassWDisp.description = InfoModel.unEscapeProtegeString(token1);
					}
				} else {
					objClass.identifier = InfoModel.getClassIdentifier("tbd", className);
					if (! DMDocument.LDDToolFlag) {
						System.out.println(">>warning - Class disposition was not found - " + "<Record> <Field>Y</Field> <Field>UpperModel.0001_NASA_PDS_1." + objClass.title + "</Field> <Field>1M</Field> <Field>#nm</Field> <Field>ns</Field> </Record>"); 
					}
				}	
				type = 0;
				break;
			case 2: // subClassOf
				objClass.subClassOfTitle = token;
//				if (token.compareTo(DMDocument.masterUserClassName) != 0) {
//					objClass.subClassOfIdentifier = InfoModel.getClassIdentifier(DMDocument.masterNameSpaceIdNCLC, token);
//				} else {
//					objClass.subClassOfIdentifier = InfoModel.getClassIdentifier(DMDocument.masterUserClassNamespaceIdNC, token);
//				}
				type = 0;
				break;
			case 3: // single-slot
				attrTitle = token;
				String luid1 = getNextUId();
				String lSsRdfIdentifier = DMDocument.rdfPrefix + objClass.title + "." + attrTitle + "." + luid1;			
				attrClass = new AttrDefn(lSsRdfIdentifier);
				attrClass.uid = luid1;
				attrClass.title = attrTitle;
				attrClass.parentClassTitle = className;
				attrClass.classNameSpaceIdNC = classNameSpaceIdNC;
				attrClass.attrNameSpaceIdNC = classNameSpaceIdNC;
				attrClass.attrNameSpaceId = attrClass.attrNameSpaceIdNC + ":";
				attrClass.setAttrIdentifier (classNameSpaceIdNC, className, classNameSpaceIdNC, attrTitle);
				attrClass.set11179Attr(attrClass.identifier);
				attrClass.regAuthId = DMDocument.registrationAuthorityIdentifierValue;
				attrClass.subModelId = subModelId;
				attrClass.cardMin = "0";
				attrClass.cardMinI = 0;
				attrClass.cardMax = "1";
				attrClass.cardMaxI = 1;
				attrClass.classSteward = objClass.steward;
				attrClass.steward = attrClass.classSteward;
				attrClass.isPDS4 = true;
				attrClass = resolveAttrNamespace (attrClass);
				objClass.hasSlot.add(attrClass);
				attrDict.put(attrClass.rdfIdentifier, attrClass);
//				System.out.println("debug ProtPontModel singleSlot attrClass.rdfIdentifier:" + attrClass.rdfIdentifier);
				type = 0;
				break;
			case 4: // multislot
				attrTitle = token;
				String luid2 = getNextUId();
				String lMsRdfIdentifier = DMDocument.rdfPrefix + objClass.title + "." + attrTitle + "." + luid2;
				attrClass = new AttrDefn(lMsRdfIdentifier);
				attrClass.uid = luid2;		
				attrClass.title = attrTitle;
				attrClass.parentClassTitle = className;
				attrClass.classNameSpaceIdNC = classNameSpaceIdNC;
				attrClass.attrNameSpaceIdNC = classNameSpaceIdNC;
				attrClass.attrNameSpaceId = attrClass.attrNameSpaceIdNC + ":";				
				attrClass.setAttrIdentifier (classNameSpaceIdNC, className, classNameSpaceIdNC, attrTitle);
				attrClass.set11179Attr(attrClass.identifier);
				attrClass.regAuthId = DMDocument.registrationAuthorityIdentifierValue;
				attrClass.subModelId = subModelId;
				attrClass.cardMin = "0";
				attrClass.cardMinI = 0;
				attrClass.cardMax = "*";
				attrClass.cardMaxI = 9999999;
				attrClass.classSteward = objClass.steward;
				attrClass.steward = attrClass.classSteward;
				attrClass.isPDS4 = true;
				attrClass = resolveAttrNamespace (attrClass);
				
				objClass.hasSlot.add(attrClass);
				attrDict.put(attrClass.rdfIdentifier, attrClass);
//				System.out.println("debug ProtPontModel multiSlot attrClass.rdfIdentifier:" + attrClass.rdfIdentifier);
				type = 0;
				break;
			case 5: // type:Instance
				if (token.compareTo("INSTANCE") == 0) {
					attrClass.propType = "INSTANCE";
					attrClass.protValType = "CLASS";
					attrClass.isAttribute = false;
					objClass.ownedAssocNSTitle.add(attrClass.nsTitle);
					objClass.ownedAssociation.add(attrClass);
				} else {
					attrClass.propType = "ATTRIBUTE";
					attrClass.protValType = token.toLowerCase();
					attrClass.isAttribute = true;
					attrClass.isOwnedAttribute = true;
					objClass.ownedAttrNSTitle.add(attrClass.nsTitle);
					objClass.ownedAttribute.add(attrClass);
				}
				type = 0;
				break;
			case 6: // allowed-classes
				if (token.compareTo(")") == 0) {
					type = 0;
				} else {
					if (token.indexOf("XSChoice%23") > -1) {
						attrClass.isChoice= true;
						attrClass.groupName = token;
					} else {
						attrClass.valArr.add(token);
						attrClass.isEnumerated = true;
					}
//					attrClass.valArr.add(token);
				}
				break;
			case 7: // values
				if (token.compareTo(")") == 0) {
					type = 0;
				} else {
					attrClass.valArr.add(token);
					attrClass.isEnumerated = true;
				}
				break;
			case 8: // cardinality
//				System.out.println("debug attrTitle:" + attrTitle);
				Integer ival = new Integer(token);
				attrClass.cardMin = token;
				attrClass.cardMinI = ival;
				String token2 = (String) tokenIter.next();
				if (token2.compareTo("?VARIABLE") == 0) {
					attrClass.cardMax = "*";
					attrClass.cardMaxI = 9999999;
				} else {
					ival = new Integer(token2);
					attrClass.cardMax = token2;
					attrClass.cardMaxI = ival;
				}
				type = 0;
				break;
			case 9: // comment
//				attrClass.description = token;
				attrClass.description = InfoModel.unEscapeProtegeString(token);
				type = 0;
				break;
			case 10: // role
				objClass.role = token;
//				objClass.isAbstract = false;
				if (objClass.role.compareTo("abstract") == 0) {
					objClass.isAbstract = true;					
				}
				type = 0;
				break;
			case 11: // default - XSChoice#
				if (token.compareTo(")") == 0) {
					type = 0;
				} else {
					if (token.indexOf("XSChoice#") > -1) {
						attrClass.isChoice= true;
						attrClass.groupName = token;
					} else if (token.indexOf("33") > -1) {
						attrClass.isChoice= true;
						attrClass.groupName = "XSChoice#" + token;
					}
				}
				type = 0;
				break;
			}
		}
	}
	
	/**
	 *   resolveAttrNamespace - temporary method to resolve attribute namespaces
	 *   Plan on using OWL version so that namespaces can be specified in Protege.
	 */
	public AttrDefn resolveAttrNamespace (AttrDefn lAttr) {
		String lNameSpaceIdNC = InfoModel.attrNamespaceResolutionMap.get(lAttr.classNameSpaceIdNC + "." + lAttr.parentClassTitle + "." + lAttr.attrNameSpaceIdNC + "." + lAttr.title);
		if (lNameSpaceIdNC != null) {
			lAttr.attrNameSpaceIdNC = lNameSpaceIdNC;
			lAttr.attrNameSpaceId = lAttr.attrNameSpaceIdNC + ":";
			lAttr.setAttrIdentifier (lAttr.classNameSpaceIdNC, lAttr.parentClassTitle, lAttr.attrNameSpaceIdNC, lAttr.title);
			lAttr.set11179Attr(lAttr.identifier);
		}
		return lAttr;
	}	
}
