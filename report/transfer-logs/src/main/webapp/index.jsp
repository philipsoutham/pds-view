<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
    pageEncoding="ISO-8859-1"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">

<link rel="stylesheet" href="css/jquery-ui-1.8.6.custom.css"></link>
<link rel="stylesheet" href="css/main.css"></link>
<title>Log Transfer</title>

<!-- %
boolean dbError = false;
String realPath = application.getRealPath("/WEB-INF/classes");
DBUtil util = new DBUtil(realPath);
ArrayList<Profile> pList = new ArrayList<Profile>();
try {
	pList = util.findAllProfiles();
	//util.closeConn();
} catch (Exception e) {
	dbError = true;
	//pList = null;
	//out.print("<body>ERROR: Notify System Administrator: "+e.getMessage()+"</body>");
}
%-->

<script type="text/javascript" src="http://code.jquery.com/jquery.js"></script>
<script type="text/javascript" src="js/jquery-ui-1.8.6.custom.min.js"></script>
<script type="text/javascript" src="js/jquery.tmpl.js"></script>
<script type="text/javascript" src="js/jquery.tmplPlus.js"></script>

<script id="logDetailsTemplate" type="text/x-jquery-tmpl">
	<div id="log-set-${'${'}count}" class="log-set">
		<div class="form-section ui-corner-top">
			{{if !newSet}}
				<span class="remove-icon hover-focus"><span class="ui-icon ui-icon-close"></span></span>
			{{/if}}
			<div class="form-row">
				<div class="log-header">Log Set ${'${'}count}</div>
			</div>
			<div class="form-row">
				<div class="label">Log Set Title:</div>
				<input id="label-${'${'}count}" name="label-${'${'}count}" type="text" class="set-info" value="${'${'}label}"/>
				<span class="tooltip-link hover-light" title="The title for this specific set of logs." ><span class="ui-icon ui-icon-info"></span></span>
			</div>
			<div class="form-row">
				<div class="label">Hostname:</div>
				<input id="hostname-${'${'}count}" name="hostname-${'${'}count}" type="text" class="set-info" value="${'${'}hostname}"/>
				<span class="tooltip-link hover-light" title="The hostname for the host machine where the logs reside. i.e. jpl.nasa.gov" ><span class="ui-icon ui-icon-info"></span></span>
			</div>
			<div class="form-row">
				<div class="label">Username:</div>
				<input id="username-${'${'}count}" name="username-${'${'}count}" type="text" class="set-info" value="${'${'}username}"/>
				<span class="tooltip-link hover-light" title="The username for the user with proper privileges to copy the logs from the host machine." ><span class="ui-icon ui-icon-info"></span></span>
			</div>
			<div class="form-row">
				<div class="label">Password:</div>
				<input id="password-${'${'}count}" name="password-${'${'}count}" type="password" class="set-info" value="${'${'}password}" />
				<span class="tooltip-link hover-light" title="The password for the user entered above." ><span class="ui-icon ui-icon-info"></span></span>
			</div>
			<div class="form-row">
				<div class="label">Pathname:</div>
				<input id="pathname-${'${'}count}" name="pathname-${'${'}count}" type="text" class="set-info" value="${'${'}pathname}" />
				<span class="tooltip-link hover-light" title="The ABSOLUTE path where the logs reside on the host machine. Wildcards are preferred. i.e. /home/logs/access_log.*" ><span class="ui-icon ui-icon-info"></span></span>
			</div>
			<input id="log-set-id-${'${'}count}" class="set-id" name="log-set-id-${'${'}count}" type="hidden" value="${'${'}logSetId}" />
			<input id="active-flag-${'${'}count}" class="flag" name="active-flag-${'${'}count}" type="hidden" value="y" />
		</div>
	</div>
</script>

<script id="connectionsTemplate" type="text/x-jquery-tmpl">
	<div class="log-set-header">Log Set: ${'${'}label}</div>
	<div class="form-row"><div class="label">Hostname:</div>${'${'}hostname}</div>
	<div class="form-row"><div class="label">Path:</div>${'${'}pathname}</div>
	
	<div class="form-row"><div class="label">Connect:</div>{{html connect}}</div>
	<div class="form-row"><div class="label">SFTP:</div>{{html sftp}}</div>
	
	<div class="form-row"><div class="label">Files found:</div>
		<div class="file-list">
			{{html filelist}}
		</div>
	</div>
</script>

<script type="text/javascript">
var details= {};

$(function() {
	
	resetForm();

	$('#create-new-log').click(function() {
		details.count++;
		createLogSet(details, true);
	});

	$('.hover-light').live('mouseenter mouseleave', function() { 
		$(this).toggleClass('ui-state-highlight').toggleClass('highlight-text');
	});

	$('.hover-focus').live('mouseenter mouseleave', function() { 
		$(this).toggleClass('ui-state-focus').toggleClass('highlight-text');
	});

	/*
	May want to eventually catch updates here for to minimize server-side functionality
	$('#profile-section').change(function() {
		var val = $('#profile-updated').val();
		var val
	}*/
	
	$('#profile').change(function() {
		getProfileInfo();
	});
	
	$('#node').change(function() {
		setProfileName();
	});

	$('#identifier').change(function() {
		setProfileName();
	});

	// TODO - Remove a Log Set - Currently only hides the log set
	$('.remove-icon').live('click',function() {
		var logSet = $(this).parent().parent();
		logSet.toggle();
		logSet.find('.flag').val('n');
		$('#removed-log-set').val(logSet.find('.set-id').val());
		$.getJSON('update', $('.update-fields').serialize(), function(data) {
			alert("Log Set Inactive");
		});
		$('#removed-log-set').val(0);
		//$('#log-set-count').val($('#log-set-count').val()/1-1);
	});
		
	$('#submit-btn').click(function() {
		var html="", fail, connect, sftp, modalButtons = {}, label1, label2, saveButtons = {};
		
		$.post('setup', $('#transfer-form').serialize(), function(data) {
			var testSetup = {count: 0};
			var filelist = '';
			$('#setup-modal').html('');
			$.each(data.logs, function (i, log) {
				connect = "OK";
				sftp = "OK";
				fail = 0;
				filelist = '';
				testSetup.count++;

				if (log.connect == 0) {
					connect = "<div class=\"ui-state-error\">FAILED -  "+log.error+"</div>";
					fail = 1;
				} else if (log.sftp == 0) {
					sftp = "<div class=\"ui-state-error\">FAILED -  "+log.error+"</div>";
					fail = 1;
				}

				testSetup.connect = connect;
				testSetup.sftp = sftp;
				testSetup.fail = fail;
				testSetup.hostname = log.hostname;
				testSetup.pathname = log.pathname;
				testSetup.label = log.label;

				modalButtons = {};
				if (fail == 0) {
					if (log.files.length == 0) {
						filelist = "0 Files Found<br />Verify this is expected";
					} else {
						$.each(log.files, function (i, filename) {
							if (i < 9) {
								filelist += filename+"<br />";
							} else {
								if (i == 9) {
									filelist += "<span class=\"hidden-files\" style=\"display: inline;\"><a href=\"javascript:toggleHiddenFiles()\">More Files...</a></span>";
								}
								filelist += "<span class=\"hidden-files\">"+filename+"<br /></span>";
							}
						});
					}

					testSetup.filelist = filelist;

					// Set modal buttons according to whether or not error is thrown
					modalButtons['Submit'] = function() { 				
						$.post('save',$('#transfer-form').serialize(), function (data) {
							saveButtons = {};
							$('#setup-modal').dialog('close');
							if (data.error == "") {
								var saveHtml = "<p>Please Note: Logs will now be migrated. " +
								 	"Depending on the file size, they may not be immediately available " +
								 	"by the Report Service.</p>";
								 	
								//saveButtons['Continue'] = function() { window.location.replace("http://pdsops.jpl.nasa.gov/report-service/"); };
								saveButtons['Continue'] = function() { window.location.replace("http://127.0.0.1:8080/cgi-bin/sawmill.cgi"); };
								saveButtons['Close'] = function() {
									resetForm(); 
									$(this).dialog("close");
								}; 	
							} else {
								var saveHtml = "<p class=\"ui-state-error\">Error: "+data.error+"</p>";
								saveButtons['Close'] = function() { $(this).dialog("close"); };
							}
						 	$('#save-modal').html(saveHtml);
							$('#save-modal').dialog({
								modal: true,
								title: "Save Complete",
								width: "500px",
								buttons: saveButtons
							});
						}, 'json');
					};
					modalButtons['Cancel'] = function() { $(this).dialog("close"); };
				} else {
					modalButtons['Close'] = function() { $(this).dialog("close"); };
				}			
				$('#setup-modal').append($('#connectionsTemplate').tmpl(testSetup));
			});
			
			//$('#setup-modal').html(html);
			$('#setup-modal').dialog({
				modal: true,
				title: 'Profile: '+$('#name').val(),
				width: '500px',
				maxHeight: '500px',
				buttons: modalButtons
			});
		}, "json");
	});
});

function resetForm() {
	$('#transfer-form')[0].reset();
	$('#log-set-container').html('');
	resetLogSetCnt();
	createLogSet(details, true);
	resetProfiles();

	$('.set-info').attr('readonly','').removeClass('ui-state-disabled');
}

function resetLogSetCnt() {
	$('#log-set-count').val(0);
	$('#new-log-set').val(0);
}

function createLogSet(details, isNew) {
	$('#log-set-count').val($('#log-set-count').val()/1+1);
	
	if (isNew) {
		$('#new-log-set').val($('#new-log-set').val()/1+1);
		//details = { count: $('#log-set-count').val(), label: '', hostname: 'pdsdev.jpl.nasa.gov', username: 'jpadams', password: 'Ph1ll1es8008', pathname: '/home/jpadams/logs/access_log.2011-01-01.txt.gz', logSetId: 0 };
		details = { count: $('#log-set-count').val(), label: 'log set '+$('#log-set-count').val(), hostname: '', username: '', password: '', pathname: '', logSetId: 0, newSet: 1};
		$('#logDetailsTemplate').tmpl(details).appendTo('#log-set-container', details);
	} else {
		details.newSet = 0;
		$('#logDetailsTemplate').tmpl(details).appendTo('#log-set-container', details);
		$('.log-set input').attr('readonly','readonly').addClass('ui-state-disabled'); // Remove input styling from input boxes
		//$('.log-set').prepend('<span class="remove-icon"><span class="ui-icon ui-icon-close"></span></span>');
	}
	// Set the highlight for hover over icons
	//setHover();	
}

function resetProfiles() {
	var select = $('#profile');
	$('option', select).remove();
	var options = select.attr('options');
	options[0] = new Option('Create new...', 'new');
	select.val('new');
	$.getJSON('update', $('.update-fields').serialize(), function(data) {
		if (data.error == "") {
			if (data.empty == 0) {
				$.each(data.profiles, function (i, prof) {
					options[options.length] = new Option(prof.name, prof.id);
				});
			}
		} else {
			$('#error-section').html(data.error);
			$('#error-section').toggle();
		}
	});
}

function getProfileInfo() {
	if ($('#profile').val() == 'new') {
		resetForm();
	} else {
		resetLogSetCnt();
		
		$.getJSON('update', $('.update-fields').serialize(), function(data) {
			var html="";

			if (data.error == "") {
				$('#profile-id').val(data.profileId);
				$('#node').val(data.node);
				$('#identifier').val(data.identifier);
				$('#name').val(data.name);
				$('#method').val(data.method);

				$('#log-set-container').html('');
				$.each(data.logSets, function (i, logset) {
					details = { count: i+1, label: logset.label, hostname: logset.hostname, username: logset.username, password: logset.password, pathname: logset.pathname, logSetId: logset.logSetId };
					createLogSet(details, false); // Add new log set section for each log set queried from DB
				});
			} else {
				$('#error-section').html(data.error);
				$('#error-section').toggle();
			}
		});

		$('.set-info').attr('readonly','readonly').addClass('ui-state-disabled');
	}
}

function setProfileName() {
	$('#name').val($('#node').val()+"-"+$('#identifier').val());
}

function toggleHiddenFiles() {
	$('.hidden-files').toggle();
}
</script>

</head>
<body>
	<div class="top-bar">
		<h1>Log Transfer</h1>
		<p class="transfer-text">Software that gains access to all node web/ftp logs to be utilized by the Report Service.</p>
	</div>
	<form id="transfer-form" action="setup" method="post">
		<div id="main-content">
			<h2 class="title">Profile Information</h2>
			<p class="transfer-text">Please enter/modify information to describe the Report Service profile.</p>
			<div id="error-section" class="ui-state-error" style="display:none;"></div>
			<div id="profile-section" class="form-section ui-corner-all">
				<input id="profile-id" name="profile-id" type="hidden" value="0" />
				<div class="form-row">
					<div class="label">Profile:</div>
					<select id="profile" name="profile" class="update-fields"></select>
					<span class="tooltip-link hover-light" title="Select a Sawmill profile that already exists, or create a new one." ><span class="ui-icon ui-icon-info"></span></span>
				</div>
				<div class="form-row loaded-profile">
					<div class="label">Node:</div>
					<select id="node" name="node" class="set-info">
						<option value="">Select a Node</option>
						<option value="atm">ATM</option>
						<option value="cdn">CDN</option>
						<option value="eng">ENG</option>
						<option value="geo">GEO</option>
						<option value="gre">GRE</option>
						<option value="hrd">HRD</option>
						<option value="img">IMG</option>
						<option value="jpl">JPL</option>
						<option value="ldn">LDN</option>
						<option value="lol">LOL</option>
						<option value="lro">LRO</option>
						<option value="nai">NAI</option>
						<option value="ppi">PPI</option>
						<option value="psi">PSI</option>
						<option value="rng">RNG</option>
						<option value="rsf">RSF</option>
						<option value="sbn">SBN</option>
						<option value="swr">SWR</option>
						<option value="tes">TES</option>
						<option value="the">THE</option>
						<option value="uoi">UOI</option>
					</select>
					<span class="tooltip-link hover-light" title="Select a node where these logs will come from." ><span class="ui-icon ui-icon-info"></span></span>
				</div>
				<div class="form-row">
					<div class="label">Profile Identifier:</div>
					<input id="identifier" name="identifier" type="text" class="set-info" />
					<span class="tooltip-link hover-light" title="Enter a descriptive, unique identifier that will be used to create the Profile Name.  i.e. web-logs" ><span class="ui-icon ui-icon-info"></span></span>
				</div>
				<div class="form-row">
					<div class="label">Profile Name:</div>
					<input id="name" name="name" class="ui-state-disabled" type="text" readonly="readonly" />
					<span class="tooltip-link hover-light" title="The unique name of the Profile that will be present in Sawmill. Created using following naming scheme: &lt;NODE&gt;-&lt;IDENTIFIER&gt;" ><span class="ui-icon ui-icon-info"></span></span>
				</div>
				<div class="form-row">
					<div class="label">Transfer Method:</div>
					<select id="method" name="method" class="set-info">
						<option value="pull">Weekly download</option>
						<!-- option value="push">Upload</option>
						<option value="email">Submit by email</option-->
					</select>
					<span class="tooltip-link hover-light" title="Select a method you would like to use to submit your logs to the Report Service." ><span class="ui-icon ui-icon-info"></span></span>
				</div>
			</div>
			<h2 class="title">Log Details</h2>
			<p class="transfer-text">Please enter/modify the information necessary to retrieve the log files.</p>
			<div id="log-details-section">
				<div id="log-set-container"></div>
				<div class="add-log-section form-section ui-corner-bottom hover-light">
					<div class="form-row" id="create-new-log">
						<p><span class="add-log ui-icon ui-icon-plusthick"></span>Add Another Log Set</p>
					</div>
				</div>	
			</div>
			<div class="button-section">
				<div class="form-row button-row">
					<input id="submit-btn" type="button" value="Submit" />
				</div>
			</div>
		</div>
		<input id="log-set-count" name="log-set-count" type="hidden" value="0" />
		<input id="new-log-set" name="new-log-set" type="hidden" value="0" />
		<input id="removed-log-set" class="update-fields" name="removed-log-set" type="hidden" value="0" />
	</form>
	<div id="setup-modal" class="modal-section"></div>
	<div id="save-modal" class="modal-section"></div>
</body>
</html>