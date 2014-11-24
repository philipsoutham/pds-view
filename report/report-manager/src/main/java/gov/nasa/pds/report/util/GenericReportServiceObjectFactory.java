//	Copyright 2014, by the California Institute of Technology.
//	ALL RIGHTS RESERVED. United States Government Sponsorship acknowledged.
//	Any commercial use must be negotiated with the Office of Technology 
//	Transfer at the California Institute of Technology.
//	
//	This software is subject to U. S. export control laws and regulations 
//	(22 C.F.R. 120-130 and 15 C.F.R. 730-774). To the extent that the software 
//	is subject to U.S. export control laws and regulations, the recipient has 
//	the responsibility to obtain export licenses or other export authority as 
//	may be required before exporting such information to foreign countries or 
//	providing access to foreign nationals.
//	
//	$Id$
//
package gov.nasa.pds.report.util;

import gov.nasa.pds.report.processing.Processor;

import java.util.logging.Logger;

public class GenericReportServiceObjectFactory{
	
	private static Logger log = Logger.getLogger(
			GenericReportServiceObjectFactory.class.getName());
	
	private GenericReportServiceObjectFactory() throws InstantiationException{
		throw new InstantiationException("Don't instantiate me, bro!");
	}
	
	public static Processor getProcessor(String qualifiedClassName){
		
		Processor p = null;
		
		try {
			p = (Processor)Class.forName(qualifiedClassName).newInstance();
		} catch (Exception e) {
			log.warning("An error occurred while creating an instance of " +
					"Processor " + qualifiedClassName + ": " + e.getMessage());
		}
		
		return p;
		
	}
	
}