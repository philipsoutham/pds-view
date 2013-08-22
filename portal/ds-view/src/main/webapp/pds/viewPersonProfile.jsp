<%
   String pdshome = application.getInitParameter("pdshome.url");
   String registryUrl = application.getInitParameter("registry.url");
%>
<html>
<head>
   <title>PDS: Person Information</title>
   <META  NAME="keywords"  CONTENT="Planetary Data System">
   <META  NAME="description" CONTENT="This website serves as a mechanism for displaying the PDS user information.">
   <link href="/ds-view/pds/css/pds_style.css" rel="stylesheet" type="text/css">
   <%@ page language="java" session="true" isThreadSafe="true" info="PDS Search" 
            isErrorPage="false" contentType="text/html; charset=ISO-8859-1" 
            import="gov.nasa.pds.registry.model.ExtrinsicObject, gov.nasa.pds.dsview.registry.Constants, 
                    java.util.*, java.net.*, java.io.*, java.lang.*"
   %>

   <SCRIPT LANGUAGE="JavaScript">
      <%@ include file="/pds/utils.js"%>
   </SCRIPT>
</head>

<body class="menu_data menu_item_data_data_search ">

   <%@ include file="/pds/header.html" %>
   <%@ include file="/pds/main_menu.html" %>

   <div id="submenu">
   <div id="submenu_data">
   <h2 class="nonvisual">Menu: PDS Data</h2>
   <ul>
      <li id="data_data_search"><a href="http://pds.jpl.nasa.gov/tools/data-search/">Data Search</a></li>
      <li><a href="/ds-view/pds/index.jsp">Form Search</a></li>
      <li id="data_how_to_search"><a href="http://pds.jpl.nasa.gov/data/how-to-search.shtml">How to Search</a></li>
      <li id="data_data_set_status"><a href="http://pds.jpl.nasa.gov/tools/dsstatus/">Data Set Status</a></li>
      <li id="data_release_summary"><a href="http://pds.jpl.nasa.gov/tools/subscription_service/SS-Release.shtml">Data Release Summary</a></li>
   </ul>
   </div>
   <div class="clear"></div>
   </div>

<!-- Main content -->
<div id="content">
   <div style="border-top: 1px solid_white;">
   <table align="center" bgColor="#FFFFFF" BORDER="0" CELLPADDING="10" CELLSPACING="0">
   <tr>
      <td>
         <table width="760" border="0" cellspacing="3" cellpadding="2">
            <tr valign="TOP">
               <td valign="TOP" colspan="2" class="pageTitle">
                  <b>Person Information</b><br/>
               </td>
            </tr>

<%
String pdsUserId=request.getParameter("PDS_USER_ID");
if ((pdsUserId == null) || (pdsUserId == "")) {
%>
            <tr valign="TOP">
               <td bgcolor="#F0EFEF" width=200 valign=top>
                  Please specify a valid <b>PDS_USER_ID</b>.
               </td>
            </tr>
<%
}
else {
   gov.nasa.pds.dsview.registry.SearchRegistry searchRegistry = new gov.nasa.pds.dsview.registry.SearchRegistry(registryUrl);
   String personLid = "urn:nasa:pds:context_pds3:personnel:personnel." + pdsUserId.toLowerCase();
   ExtrinsicObject personObj = searchRegistry.getExtrinsic(personLid);
  
   if (personObj==null) { 
   %>
            <tr valign="TOP">
               <td bgcolor="#F0EFEF" width=200 valign=top>
                  Information not found for PDS_USER_ID <b><%=pdsUserId%></b>. Please verify the value.
               </td>
            </tr>
   <%
   } 
   else { 
      //out.println("personObj guid = " + personObj.getGuid());
      for (java.util.Map.Entry<String, String> entry: Constants.personPds3ToRegistry.entrySet()) {
         String key = entry.getKey();
		 String tmpValue = entry.getValue();
         %>
            <TR>
               <td bgcolor="#F0EFEF" width=200 valign=top><%=key%></td> 
               <td bgcolor="#F0EFEF" valign=top>
         <% 
         //String tmpValue = displayedValueNames[i];
         List<String> slotValues = searchRegistry.getSlotValues(personObj, tmpValue);
         if (slotValues!=null) {
            for (int j=0; j<slotValues.size(); j++) {
               out.println(slotValues.get(j).toUpperCase() + "<br>");
                         	   
               if (slotValues.size()>1) 
                  out.println("<br>");
            } // end for
         } // end if (slotValues!=null
         else {
            if (tmpValue.equals("pds_user_id")) 
               out.println(pdsUserId + "<br>");
         }
         %>
               </td>
            </TR>
<%         
      } // for loop
   } // end else personObj!=null
} // if PDS_USER_ID is specified
%>        
         </table>
      </td>
   </tr>
</TABLE>
</div>
</div>

<%@ include file="/pds/footer.html" %>

</BODY>
</HTML>

