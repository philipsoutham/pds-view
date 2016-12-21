// Copyright 2016, by the California Institute of Technology.
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
// $Id: $

package gov.nasa.pds.tracking.email;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.util.Properties;

import javax.mail.Authenticator;
import javax.mail.Message;
import javax.mail.MessagingException;
import javax.mail.PasswordAuthentication;
import javax.mail.Session;
import javax.mail.Transport;
import javax.mail.internet.AddressException;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeMessage;

public class SendEmail
{	
	// Sender's email ID needs to be mentioned
	private String from = "pds_operator@jpl.nasa.gov";

	// Assuming you are sending email from localhost
	private String host = "smtp.jpl.nasa.gov";

	// Recipient's email ID needs to be mentioned
	private String toAddress;
	private ArrayList<String> toAddressList;

	private String port = "587";
	private String user;
	private String pass;
	private int maxMsgNums = 200;

	// Get system properties
	private Properties properties = System.getProperties();

	private Session session; 

	/*
	 * Constructor
	 */
	public SendEmail() {
		init();
	}

	/*
	 * Constructor 
	 */
	public SendEmail(String host, String from) {
		this.host = host;
		this.from = from;
		init();
	}

	/*
	 * Constructor 
	 */
	public SendEmail(String host, String port, String user, String pass) {
		this.host = host;
		this.port = port;
		this.user = user;
		this.pass = pass;
		init();
	}

	public void init() {
		// Setup mail server
		properties.put("mail.smtp.host", host);
		properties.put("mail.smtp.port", port);
		if (user!=null)
			properties.setProperty("mail.user", user);
		if (pass!=null)
			properties.setProperty("mail.password", pass);

		if (user==null && pass==null) {
			// Get the default Session object.
			session = Session.getDefaultInstance(properties);
			//System.out.println("*****no username and password....");
		}
		else {
			properties.put("mail.smtp.auth", "true");
			properties.put("mail.smtp.starttls.enable", "true");
			// creates a new session with an authenticator
			Authenticator auth = new Authenticator() {
				public PasswordAuthentication getPasswordAuthentication() {
					return new PasswordAuthentication(user, pass);
				}
			};

			//System.out.println("*****With username and password....session is with authenticator....");
			session = Session.getInstance(properties, auth);
		}
		//session.setDebug(true);
	}

	public void setFrom(String from) {
		this.from = from;
	}

	public void setHost(String host) {
		this.host = host;
	}

	public void setPort(String port) {
		this.port = port;
	}

	public void setTo(String toAddress) {
		this.toAddress = toAddress;
	}

	public void setTo(ArrayList<String> toAddress) {
		this.toAddressList = toAddress;
	}

	public void setUsername(String userName) {
		this.user = userName;
	}

	public void setPassword(String passwd) {
		this.pass = passwd;
	}
	
	public void setMaxMsgNums(int maxNum) {
		this.maxMsgNums = maxNum;
	}

	public void send(ArrayList<String> listOfEmails, String subject, String msgContent) {
		InternetAddress[] listOfToAddress = new InternetAddress[listOfEmails.size()];

		try {
			for (int i = 0; i < listOfEmails.size(); i++) {
				if (listOfEmails.get(i)!=null) {
					listOfToAddress[i] = new InternetAddress(listOfEmails.get(i));
				}
			}
		} catch (AddressException aex) {
			aex.printStackTrace();
		}

		try{
			// Create a default MimeMessage object.
			MimeMessage message = new MimeMessage(session);

			// Set From: header field of the header.
			message.setFrom(new InternetAddress(from));

			// Set Subject: header field
			message.setSubject(subject);

			// Now set the actual message
			message.setText(msgContent);

			message.setSentDate(new Date());

			// Chunk the email list to smaller size when it's bigger than the maximum msg size on the server
			// and send msg repeatedly 
			if (listOfEmails.size()>maxMsgNums) {
				int numToIterate = (int)Math.ceil(listOfEmails.size()/(float)maxMsgNums);
				//System.out.println("numToIterate = " + numToIterate);
				for (int i=0; i<numToIterate; i++) {
					InternetAddress[] tmpLists;
					if (i<(numToIterate-1))
						tmpLists = new InternetAddress[maxMsgNums];
					else {
						if (maxMsgNums==1)
							tmpLists = new InternetAddress[1];
						else {
							if (listOfEmails.size()%maxMsgNums == 0)
								tmpLists = new InternetAddress[maxMsgNums];
							else 
								tmpLists = new InternetAddress[listOfEmails.size()%maxMsgNums];
						}
					}

					for (int j=0; j<maxMsgNums; j++) {
						if (((i*maxMsgNums)+j)<listOfEmails.size()) {
							//System.out.println("(i*maxMsgNums)+j = " + ((i*maxMsgNums)+j) + "       listOfEmails.size() = " + listOfEmails.size());
							tmpLists[j] = new InternetAddress(listOfEmails.get((i*maxMsgNums)+j)); 
						}
					}		   

					// Set To: header field of the header.
					message.setRecipients(Message.RecipientType.TO, tmpLists);
					// Send message
					Transport.send(message);
					//System.out.println("Sent message successfully to multiple recipients....i = " + i);
				}
			}
			else {
				// Set To: header field of the header.
				message.setRecipients(Message.RecipientType.TO, listOfToAddress);
				// Send message
				Transport.send(message);
				//System.out.println("Sent message successfully to multiple recipients....with listOfToAddress");
			}
		} catch (MessagingException mex) {
			mex.printStackTrace();
		}

	}

	public void send(String toAddress, String subject, String msgContent) {
		try{
			// Check if the toAddress contains more than one recipient and the size is bigger than 
			// the maximum msg size on the server, then, call other method with ArrayList
			if (toAddress.contains(",")) {
				String[] toAddressArray = toAddress.split(",");
				if (toAddressArray.length>maxMsgNums)
					send(new ArrayList<String>(Arrays.asList(toAddressArray)), subject, msgContent);
			}

			// Create a default MimeMessage object.
			MimeMessage message = new MimeMessage(session);   

			// Set From: header field of the header.
			message.setFrom(new InternetAddress(from));

			// Set To: header field of the header.		   
			message.setRecipients(Message.RecipientType.TO, toAddress);

			// Set Subject: header field
			message.setSubject(subject);

			// Now set the actual message content
			message.setText(msgContent);

			message.setSentDate(new Date());

			// Send message
			Transport.send(message);
			//System.out.println("Sent message successfully to recipient with String type....");
		}catch (MessagingException mex) {
			mex.printStackTrace();
		}
	}

	/*
	 * Main 
	 */
	public static void main(String [] args)
	{    	      
		if (args.length<4)
			System.err.println("Usage: java gov.nasa.pds.tracking.email.SendEmail <host> <port> <username> <password>");
		else {
			//System.out.println("args[0] = " + args[0] + "    args[1] = " + args[1] + "    args[2] = " + args[2] +
			//	   "   args[3] = " + args[3]);

			SendEmail sm = new SendEmail(args[0], args[1], args[2], args[3]);

			int maxMsgNums = 2;
			if (args[4]!=null)
				maxMsgNums = Integer.parseInt(args[4]);

			sm.setMaxMsgNums(maxMsgNums);

			ArrayList<String> testEmails = new ArrayList<String>();
			testEmails.add("hhlee445@yahoo.com");
			testEmails.add("Hyun.H.Lee@jpl.nasa.gov");
			testEmails.add("hhlee445@gmail.com");
			testEmails.add("Hyun.H.Lee@jpl.nasa.gov");

			String msg = "Testing a SendEmail class for the tracking service...";
			String subj = "Test email tracking service";

			// test for multiple recipients
			sm.send(testEmails, subj + " as multiple recipients as arrayList", msg);

			// test for one recipients
			sm.send("Hyun.H.Lee@jpl.nasa.gov", subj + " as one TO", msg);	  
			sm.send("Hyun.H.Lee@jpl.nasa.gov,hhlee445@yahoo.com,hhlee445@gmail.com", subj + " as multiple recipients", msg);
		}
	}
}