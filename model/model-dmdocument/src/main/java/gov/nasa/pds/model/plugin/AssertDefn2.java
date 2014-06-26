package gov.nasa.pds.model.plugin;
import java.util.ArrayList;

public class AssertDefn2 {
	String identifier;
	String attrTitle;
	String assertType;
	String assertMsg;
	String assertStmt;
	String specMesg;			// a cleaned up assertMsg for the DD and Specification
	ArrayList <String> testValArr;

	public AssertDefn2 (String id) {
		identifier = id; 		
		attrTitle = id;
		assertType = "RAW";								// RAW, EVERY, IF
		assertMsg = "TBD_assertMsg";
		assertStmt = "TBD_assertMsg";
		specMesg = "TBD_specMessage";
		testValArr = new ArrayList <String>();
	} 
}