#!/bin/bash
#Copyright (C) 2007  Paul Sharrad

#This file is part of Karoshi Server.
#
#Karoshi Server is free software: you can redistribute it and/or modify
#it under the terms of the GNU Affero General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#Karoshi Server is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU Affero General Public License for more details.
#
#You should have received a copy of the GNU Affero General Public License
#along with Karoshi Server.  If not, see <http://www.gnu.org/licenses/>.

#
#The Karoshi Team can be contacted at: 
#mpsharrad@karoshi.org.uk
#jsharrad@karoshi.org.uk

#
#Website: http://www.karoshi.org.uk
########################
#Required input variables
########################
#  _FIRSTNAME_
#  _SURNAME_
# _USERNAMESTYLE_
#  _PASSWORD1_  Password used for new user
#  _PASSWORD2_  Checked against PASSWORD1 for typos.
#  _GROUP_      This is the primary group for the new user eg yr2000, staff, officestaff.
##########################
#Language
##########################

STYLESHEET=defaultstyle.css
[ -f /opt/karoshi/web_controls/user_prefs/$REMOTE_USER ] && source /opt/karoshi/web_controls/user_prefs/$REMOTE_USER
TEXTDOMAIN=karoshi-server

##########################
#Show page
##########################
echo "Content-type: text/html"
echo ""
echo '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><title>'$"View auto reset passwords"'</title><link rel="stylesheet" href="/css/'$STYLESHEET'?d='`date +%F`'"></head><script src="/all/stuHover.js" type="text/javascript"></script><body><div id="pagecontainer">'
#Generate navigation bar
/opt/karoshi/web_controls/generate_navbar_admin
echo '</div><div id="actionbox">'
#########################
#Get data input
#########################
TCPIP_ADDR=$REMOTE_ADDR
DATA=`cat | tr -cd 'A-Za-z0-9\._:\-'`
#########################
#Assign data to variables
#########################
END_POINT=3
#Assign ACCOUNTTYPE
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
if [ `echo $DATAHEADER'check'` = ACCOUNTTYPEcheck ]
then
let COUNTER=$COUNTER+1
ACCOUNTTYPE=`echo $DATA | cut -s -d'_' -f$COUNTER`
break
fi
let COUNTER=$COUNTER+1
done

function show_status {
echo '<SCRIPT language="Javascript">'
echo 'alert("'$MESSAGE'")';
echo '                window.location = "/cgi-bin/admin/view_auto_reset_passwords_fm.cgi";'
echo '</script>'
echo "</div></body></html>"
exit
}
#########################
#Check https access
#########################
if [ https_$HTTPS != https_on ]
then
export MESSAGE=$"You must access this page via https."
show_status
fi
#########################
#Check user accessing this script
#########################
if [ ! -f /opt/karoshi/web_controls/web_access_admin ] || [ $REMOTE_USER'null' = null ]
then
MESSAGE=$"You must be a Karoshi Management User to complete this action."
show_status
fi

if [ `grep -c ^$REMOTE_USER: /opt/karoshi/web_controls/web_access_admin` != 1 ]
then
MESSAGE=$"You must be a Karoshi Management User to complete this action."
show_status
fi
#########################
#Check data
#########################
#Check to see that ACCOUNTTYPE is not blank
if [ $ACCOUNTTYPE'null' = null ]
then
MESSAGE=$"The account choice cannot be blank."
show_status
fi

#Check that usernamestyle is the correct value
if [ $ACCOUNTTYPE != guests ] && [ $ACCOUNTTYPE != tech ]
then
MESSAGE=$"There are no guest passwords available to view."
show_status
fi

MD5SUM=`md5sum /var/www/cgi-bin_karoshi/admin/view_auto_reset_passwords.cgi | cut -d' ' -f1`
#View auto reset passwords
echo "$REMOTE_USER:$REMOTE_ADDR:$MD5SUM:$ACCOUNTTYPE:" | sudo -H /opt/karoshi/web_controls/exec/view_auto_reset_passwords
EXEC_STATUS=`echo $?`
if [ $EXEC_STATUS = 101 ]
then
MESSAGE=`echo $"There was a problem with this action." $"Please check the karoshi web administration logs for more details."`
show_status
fi
if [ $EXEC_STATUS = 102 ]
then
MESSAGE=$"There are no guest passwords available to view."
show_status
fi
if [ $EXEC_STATUS = 103 ]
then
MESSAGE=$"There are no tech passwords available to view."
show_status
fi
echo '</div></form></div></body></html>'
exit

