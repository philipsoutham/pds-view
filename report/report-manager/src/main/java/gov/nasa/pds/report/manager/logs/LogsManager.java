//	Copyright 2013, by the California Institute of Technology.
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
//	$Id: RSUpdateLauncher.java 11670 2013-06-20 17:14:33Z jpadams $
//

package gov.nasa.pds.report.manager.logs;

import gov.nasa.pds.report.manager.logging.ToolsLevel;
import gov.nasa.pds.report.manager.logging.ToolsLogRecord;
import gov.nasa.pds.report.manager.logs.pushpull.PushPull;
import gov.nasa.pds.report.manager.logs.pushpull.PushPullImpl;
import gov.nasa.pds.report.manager.util.Utility;

import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.logging.Logger;

import org.apache.commons.io.FileUtils;

/**
 * Manages the logs being pulled, the destinations, and all things
 * related to the physical logs files
 * 
 * @author jpadams
 * @version $Revision$
 *
 */
public class LogsManager {
	
    /* our log stream */
    private static final Logger LOG = Logger.getLogger(LogsManager.class
            .getName());
	
	protected int port;
	protected File propertiesFilePath;
	protected File sitesFilePath;
	
	public LogsManager() {
		this(PushPull.DEFAULT_PORT, null, null);
	}
	
	public LogsManager(int port, File propertiesFilePath, File sitesFilePath) {
		this.port = port;
		this.propertiesFilePath = propertiesFilePath;
		this.sitesFilePath = sitesFilePath;
	}
	
	/**
	 * Pull the Log files using the PushPullImpl class
	 * 
	 * @throws LogsManagerException
	 */
	public void pullLogFiles() throws LogsManagerException {
		LOG.log(new ToolsLogRecord(ToolsLevel.INFO, "Pulling Log Files: " + this.port + " - " + this.propertiesFilePath.getAbsolutePath() + " - " + this.sitesFilePath.getAbsolutePath()));
		PushPullImpl pullObject;
		try {
			createStagingAreas(this.sitesFilePath);
			
			pullObject = new PushPullImpl(this.port, this.propertiesFilePath, this.sitesFilePath);
			pullObject.pull();
		} catch (Exception e) {
			throw new LogsManagerException(e.getMessage());
		}
	}
	
	/**
	 * Creates the staging areas designated in the RemoteSpecs.xml
	 * @param sitesFilePath
	 * @throws LogsManagerException
	 */
	public void createStagingAreas(File sitesFilePath) throws LogsManagerException {
		
		// Check if all staging areas already exists
		// If yes, exit
		// If no, create directory
		List<String> dirList = null;
		try {
			dirList = Utility.getValuesFromXML(sitesFilePath, PushPull.STAGING_TAG_NAME, PushPull.STAGING_ATTRIBUTE_NAME);
			
			for (String dir : dirList) {
				LOG.log(new ToolsLogRecord(ToolsLevel.INFO, "Creating directory: " + dir));
				FileUtils.forceMkdir(new File(dir));
			}
			
		} catch (IOException e) {
			throw new LogsManagerException("Error creating staging area. Verify permissions and paths found in " + sitesFilePath);
		} catch (Exception e) {
			throw new LogsManagerException("Error reading " + sitesFilePath.getAbsolutePath());
		}
	}

	/**
	 * @return the port
	 */
	public int getPort() {
		return port;
	}

	/**
	 * @param port the port to set
	 */
	public void setPort(int port) {
		this.port = port;
	}

	/**
	 * @return the propertiesFilePath
	 */
	public File getPropertiesFilePath() {
		return this.propertiesFilePath;
	}

	/**
	 * @param propertiesFilePath the propertiesFilePath to set
	 */
	public void setPropertiesFilePath(File propertiesFile) {
		this.propertiesFilePath = propertiesFile;
	}

	/**
	 * @return the sitesFilePath
	 */
	public File getSitesFilePath() {
		return this.sitesFilePath;
	}

	/**
	 * @param sitesFilePath the sitesFilePath to set
	 */
	public void setSitesFilePath(File sitesFile) {
		this.sitesFilePath = sitesFile;
	}
	
}