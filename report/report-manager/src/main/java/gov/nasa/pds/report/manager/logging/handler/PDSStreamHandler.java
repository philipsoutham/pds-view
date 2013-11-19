// Copyright 2006-2010, by the California Institute of Technology.
// ALL RIGHTS RESERVED. United States Government Sponsorship acknowledged.
// Any commercial use must be negotiated with the Office of Technology Transfer
// at the California Institute of Technology.
//
// This software is subject to U. S. export control laws and regulations
// (22 C.F.R. 120-130 and 15 C.F.R. 730-774). To the extent that the software
// is subject to U.S. export control laws and regulations, the recipient has
// the responsibility to obtain export licenses or other export authority as
// may be required before exporting such information to foreign countries or
// providing access to foreign nationals.
//
// $Id: HarvestStreamHandler.java 7917 2010-10-21 21:03:42Z mcayanan $
package gov.nasa.pds.report.manager.logging.handler;

import gov.nasa.pds.report.manager.logging.filter.ToolsLogFilter;

import java.io.OutputStream;
import java.util.logging.Formatter;
import java.util.logging.Level;
import java.util.logging.StreamHandler;

/**
 * This class sets up a stream handler for the tools logging capability.
 *
 * @author jpadams
 * @author mcayanan
 *
 */
public class PDSStreamHandler extends StreamHandler {

    /**
     * Constructor. Automatically sets the log level to 'ALL'.
     *
     * @param out An output stream.
     * @param formatter Formatter to be used to format the log messages.
     */
    public PDSStreamHandler(OutputStream out, Formatter formatter) {
        this(out, Level.ALL, formatter);
    }

    /**
     * Constructor.
     * @param out An output stream.
     * @param level Sets the log level, specifying which message levels will
     * be logged by this handler.
     * @param formatter Formatter to be used to format the log messages.
     */
    public PDSStreamHandler(OutputStream out, Level level,
            Formatter formatter) {
        super(out, formatter);
        setLevel(level);
        setFilter(new ToolsLogFilter());
    }
}