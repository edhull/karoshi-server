#!/bin/bash
#Copyright (C) 2007 Paul Sharrad

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
############################
#Language
############################

STYLESHEET=defaultstyle.css
TIMEOUT=300
NOTIMEOUT=127.0.0.1
[ -f /opt/karoshi/web_controls/user_prefs/$REMOTE_USER ] && source /opt/karoshi/web_controls/user_prefs/$REMOTE_USER
TEXTDOMAIN=karoshi-server

#Check if timout should be disabled
if [ `echo $REMOTE_ADDR | grep -c $NOTIMEOUT` = 1 ]
then
TIMEOUT=86400
fi
############################
#Show page
############################
URIENTRY="http://172.30.0.5/mirrors/pclinuxos/apt/"
echo "Content-type: text/html"
echo ""
echo '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><title>'$"Linux Client set repository"'</title><meta http-equiv="REFRESH" content="'$TIMEOUT'; URL=/cgi-bin/admin/logout.cgi"><link rel="stylesheet" href="/css/'$STYLESHEET'?d='`date +%F`'"><script src="/all/stuHover.js" type="text/javascript"></script></head><body><div id="pagecontainer">'
#########################
#Get data input
#########################
TCPIP_ADDR=$REMOTE_ADDR
DATA=`cat | tr -cd 'A-Za-z0-9\._:\+-'`
function show_status {
echo '<SCRIPT language="Javascript">'
echo 'alert("'$MESSAGE'")';
echo '                window.location = "/cgi-bin/admin/linux_client_set_repository.cgi";'
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

#Generate navigation bar
/opt/karoshi/web_controls/generate_navbar_admin

echo '<form action="/cgi-bin/admin/linux_client_set_repository2.cgi" method="post"><div id="actionbox"><div class="sectiontitle">'$"Linux Client set repository"'</div><br>'

if [ -f /var/lib/samba/netlogon/linuxclient/versions.txt ]
then
LINUXVERSION_COUNT=`cat /var/lib/samba/netlogon/linuxclient/versions.txt | wc -l`
else
LINUXVERSION_COUNT=0
fi

#Show current linux client versions
if [ $LINUXVERSION_COUNT -gt 0 ]
then
echo '<table class="standard" style="text-align: left; width: 60%;" border="0"
 cellpadding="2" cellspacing="2"
><tbody><tr><td>'$"URI"'</td><td><input size="40" value="'$URIENTRY'" name="___URI___"></td><td><a class="info" href="javascript:void(0)"><img class="images" alt="" src="/images/help/info.png"><span>'$"Enter the full address of the linux client repository. This is used for installing and updating the Linux clients."'</span></a></td></tr><tr><td>'$"Distribution"'</td><td><input size="40" value="'$"pclinuxos/2007"'" name="___DISTRIBUTION___"></td><td><a class="info" href="javascript:void(0)"><img class="images" alt="" src="/images/help/info.png"><span>'$"Enter in the distribution you are using."'</span></a></td></tr><tr><td>'$"Sections"'</td><td><input size="40" value="'$"main extra nonfree kde gnome"'" name="___SECTIONS___"></td><td><a class="info" href="javascript:void(0)"><img class="images" alt="" src="/images/help/info.png"><span>'$"Enter in the sections that you want to use in the repository."'</span></a></td></tr>'
echo '<tr><td>'$"Linux Version"'</td><td><select name="___LINUXVERSION___">'
COUNTER=1
while [ $COUNTER -le $LINUXVERSION_COUNT ]
do
LINUXVERSION=`sed -n $COUNTER,$COUNTER'p' /var/lib/samba/netlogon/linuxclient/versions.txt`
echo '<option value="'$LINUXVERSION'">'$LINUXVERSION'</option>'
let COUNTER=$COUNTER+1
done
echo '</select></td><td><a class="info" href="javascript:void(0)"><img class="images" alt="" src="/images/help/info.png"><span>'$"Please choose the linux version you want to edit."'</span></a></td></tr></tbody></table>'
else
echo $"You have no linux client configurations."'<br>'
fi

echo "</div>"
echo '<div id="submitbox"><input value="Submit" type="submit"> <input value="Reset" type="reset"></div>'
echo '</form></div></body></html>'
exit
